import argparse
import base64
import json
import mimetypes
import re
from pathlib import Path


SCRIPT_SRC_PATTERN = re.compile(
    r'<script\s+([^>]*?)src=["\']([^"\']+)["\']([^>]*)></script>',
    re.IGNORECASE,
)


BOOTSTRAP_TEMPLATE = """
<script>
(function () {
    const files = __ALLURE_FILES__;
    const originalFetch = window.fetch.bind(window);
    const reportDirectory = decodeURIComponent(window.location.pathname)
        .replace(/\\/[^/]*$/, "");

    function normalizePath(value) {
        const url = new URL(value, window.location.href);
        let path = decodeURIComponent(url.pathname);
        if (path.startsWith(reportDirectory + "/")) {
            path = path.slice(reportDirectory.length + 1);
        }
        return path.replace(/^\\/+/, "");
    }

    function decodeFile(file) {
        const binary = window.atob(file.content);
        const bytes = new Uint8Array(binary.length);
        for (let index = 0; index < binary.length; index += 1) {
            bytes[index] = binary.charCodeAt(index);
        }
        return new Blob([bytes], { type: file.mime });
    }

    window.fetch = async function (input, init) {
        const path = normalizePath(typeof input === "string" ? input : input.url);
        if (files[path]) {
            const file = files[path];
            return new Response(decodeFile(file), {
                status: 200,
                headers: { "Content-Type": file.mime },
            });
        }
        return originalFetch(input, init);
    };
}());
</script>
"""


def mime_type(path):
    return mimetypes.guess_type(path.name)[0] or "application/octet-stream"


def build_file_map(source_dir):
    file_map = {}
    for path in source_dir.rglob("*"):
        if not path.is_file() or path.name == "index.html":
            continue
        relative_path = path.relative_to(source_dir).as_posix()
        encoded = base64.b64encode(path.read_bytes()).decode("ascii")
        file_map[relative_path] = {
            "mime": mime_type(path),
            "content": encoded,
        }
    return file_map


def inline_local_scripts(html, source_dir):
    def replace_script(match):
        prefix, source, suffix = match.groups()
        if source.startswith(("http://", "https://", "//")):
            return ""

        script_path = source_dir / source
        if not script_path.is_file():
            return match.group(0)

        script = script_path.read_text(encoding="utf-8").replace("</script", "<\\/script")
        return f"<script{prefix}{suffix}>{script}</script>"

    return SCRIPT_SRC_PATTERN.sub(replace_script, html)


def build_single_file(source_dir, output_file):
    index_path = source_dir / "index.html"
    if not index_path.is_file():
        raise FileNotFoundError(f"Allure index not found: {index_path}")

    file_map = build_file_map(source_dir)
    html = index_path.read_text(encoding="utf-8")
    html = inline_local_scripts(html, source_dir)
    bootstrap = BOOTSTRAP_TEMPLATE.replace(
        "__ALLURE_FILES__", json.dumps(file_map, separators=(",", ":"))
    )
    first_script = html.find("<script")
    if first_script == -1:
        raise RuntimeError("Allure index does not contain an application script")

    html = html[:first_script] + bootstrap + html[first_script:]
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(html, encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a standalone Allure HTML report")
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    arguments = parser.parse_args()
    build_single_file(arguments.source, arguments.output)
    print(f"Standalone report generated: {arguments.output}")
