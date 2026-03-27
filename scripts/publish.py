#!/usr/bin/env python3
"""One-command publish pipeline for this repository."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
import shutil
import socket

import nbformat
from bs4 import BeautifulSoup

from update_toc import update_toc


REPO_ROOT = Path(__file__).resolve().parent.parent
NPM_CACHE_DIR = REPO_ROOT / ".npm-cache"
COPY_EXCLUDES = {
    ".git",
    "_build",
    ".npm-cache",
    "__pycache__",
    ".publish-workdir",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Publish this Jupyter Book site.")
    parser.add_argument(
        "--show-code",
        action="store_true",
        help="Show notebook code cells in published pages. Default is hidden.",
    )
    return parser.parse_args()


def run(command: list[str], *, cwd: Path, env: dict[str, str]) -> None:
    print("+", " ".join(command), flush=True)
    subprocess.run(command, cwd=cwd, env=env, check=True)


def build_env() -> dict[str, str]:
    env = os.environ.copy()
    NPM_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    env["NPM_CONFIG_CACHE"] = str(NPM_CACHE_DIR)
    return env


def theme_dir(root: Path) -> Path:
    return root / "_build" / "templates" / "site" / "myst" / "book-theme"


def bootstrap_theme(root: Path, env: dict[str, str]) -> None:
    if theme_dir(root).joinpath("package.json").exists():
        return
    run(["jupyter", "book", "build"], cwd=root, env=env)


def install_theme_dependencies(root: Path, env: dict[str, str]) -> None:
    theme = theme_dir(root)
    express_dir = theme / "node_modules" / "express"
    if express_dir.exists():
        return
    if not theme.joinpath("package.json").exists():
        raise RuntimeError(f"Theme directory missing package.json: {theme}")
    run(["npm", "ci", "--ignore-scripts"], cwd=theme, env=env)


def build_html(root: Path, env: dict[str, str]) -> None:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
    run(["jupyter", "book", "build", "--html", "--port", str(port)], cwd=root, env=env)
    index_html = root / "_build" / "html" / "index.html"
    if not index_html.exists():
        raise RuntimeError(f"Build finished but missing HTML output: {index_html}")


def copy_repo_tree(source: Path, dest: Path) -> None:
    for path in source.iterdir():
        if path.name in COPY_EXCLUDES:
            continue
        target = dest / path.name
        if path.is_dir():
            shutil.copytree(
                path,
                target,
                ignore=shutil.ignore_patterns(*COPY_EXCLUDES),
            )
        else:
            shutil.copy2(path, target)


def seed_theme_cache(dest_root: Path) -> None:
    source_templates = REPO_ROOT / "_build" / "templates"
    if source_templates.exists():
        shutil.copytree(
            source_templates,
            dest_root / "_build" / "templates",
            dirs_exist_ok=True,
        )


def hide_code_inputs(root: Path) -> int:
    changed = 0
    for notebook in root.rglob("*.ipynb"):
        if any(part in COPY_EXCLUDES for part in notebook.parts):
            continue
        nb = nbformat.read(notebook, as_version=4)
        notebook_changed = False
        for cell in nb.cells:
            if cell.cell_type != "code":
                continue
            tags = list(cell.metadata.get("tags", []))
            if "remove-input" not in tags:
                tags.append("remove-input")
                cell.metadata["tags"] = tags
                notebook_changed = True
        if notebook_changed:
            nbformat.write(nb, notebook)
            changed += 1
    return changed


def sync_html_back(build_root: Path) -> None:
    source_html = build_root / "_build" / "html"
    target_html = REPO_ROOT / "_build" / "html"
    if target_html.exists():
        shutil.rmtree(target_html)
    target_html.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source_html, target_html)


def strip_hidden_code_from_json(node: object) -> object | None:
    if isinstance(node, list):
        items = []
        for child in node:
            next_child = strip_hidden_code_from_json(child)
            if next_child is not None:
                items.append(next_child)
        return items

    if not isinstance(node, dict):
        return node

    if node.get("type") == "code" and node.get("visibility") == "remove":
        return None

    next_node = dict(node)
    if "children" in next_node:
        next_node["children"] = strip_hidden_code_from_json(next_node["children"])
    if (
        next_node.get("type") == "block"
        and next_node.get("kind") == "notebook-code"
        and not next_node.get("children")
    ):
        return None
    return next_node


def strip_hidden_code_from_payload(node: object) -> object:
    if isinstance(node, list):
        return [strip_hidden_code_from_payload(child) for child in node]

    if not isinstance(node, dict):
        return node

    next_node = {}
    for key, value in node.items():
        if key == "mdast":
            next_node[key] = strip_hidden_code_from_json(value)
        else:
            next_node[key] = strip_hidden_code_from_payload(value)
    return next_node


def strip_hidden_code_from_remix_context(html_text: str) -> str:
    marker = "window.__remixContext = "
    start = html_text.find(marker)
    if start == -1:
        return html_text

    json_start = start + len(marker)
    json_end = html_text.find(";</script>", json_start)
    if json_end == -1:
        return html_text

    payload = json.loads(html_text[json_start:json_end])
    payload = strip_hidden_code_from_payload(payload)
    payload_text = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    return html_text[:json_start] + payload_text + html_text[json_end:]


def strip_hidden_code_from_notebook_pages(build_root: Path) -> None:
    html_root = build_root / "_build" / "html"
    for json_path in html_root.glob("*.json"):
        data = json.loads(json_path.read_text(encoding="utf-8"))
        if data.get("kind") != "Notebook":
            continue

        data["mdast"] = strip_hidden_code_from_json(data.get("mdast"))
        json_path.write_text(
            json.dumps(data, ensure_ascii=False, separators=(",", ":")),
            encoding="utf-8",
        )

        slug = data.get("slug")
        if not slug:
            continue
        html_path = html_root / slug / "index.html"
        if not html_path.exists():
            continue

        html_text = html_path.read_text(encoding="utf-8")
        soup = BeautifulSoup(html_text, "html.parser")
        for block in soup.select("div.myst-code"):
            block.decompose()
        cleaned_html = strip_hidden_code_from_remix_context(str(soup))
        html_path.write_text(cleaned_html, encoding="utf-8")


def main() -> int:
    args = parse_args()
    print("[1/4] Scanning content and updating navigation", flush=True)
    result = update_toc()
    print(
        f"found {len(result['weekly_entries'])} weekly entries and "
        f"{len(result['project_entries'])} project entries",
        flush=True,
    )

    env = build_env()
    with tempfile.TemporaryDirectory(prefix="reportpublish-build-", dir="/tmp") as tmpdir:
        build_root = Path(tmpdir)
        copy_repo_tree(REPO_ROOT, build_root)
        seed_theme_cache(build_root)

        if args.show_code:
            print("[2/4] Preparing build copy with notebook code visible", flush=True)
        else:
            print("[2/4] Preparing build copy with notebook code hidden", flush=True)
            changed = hide_code_inputs(build_root)
            print(f"tagged notebooks for hidden code: {changed}", flush=True)

        print("[3/4] Bootstrapping Jupyter Book template if needed", flush=True)
        bootstrap_theme(build_root, env)

        print("[4/4] Building static HTML", flush=True)
        install_theme_dependencies(build_root, env)
        build_html(build_root, env)
        if not args.show_code:
            strip_hidden_code_from_notebook_pages(build_root)
        sync_html_back(build_root)

    print(f"published: {REPO_ROOT / '_build' / 'html'}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
