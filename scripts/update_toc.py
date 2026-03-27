#!/usr/bin/env python3
"""Scan content directories, create minimal generated pages, and rewrite myst.yml."""

from __future__ import annotations

import re
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parent.parent
SITE_CONFIG_PATH = REPO_ROOT / "site_config.yml"
AUTO_MARKER = "<!-- AUTO-GENERATED: scripts/update_toc.py -->"
CONTENT_SUFFIXES = {".md", ".ipynb"}
DEFAULT_PROJECT_ID = "8f251e0d-3ef1-446f-b54b-5921849eaec0"
DEFAULT_TITLE = "Quant Research Notebook Library"


def relative(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def is_generated(path: Path) -> bool:
    return AUTO_MARKER in "\n".join(read_text(path).splitlines()[:10])


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def write_generated(path: Path, content: str) -> bool:
    ensure_parent(path)
    current = read_text(path)
    if current == content:
        return False
    path.write_text(content, encoding="utf-8")
    return True


def ensure_generated_or_missing(path: Path, content: str) -> bool:
    if path.exists() and not is_generated(path):
        return False
    return write_generated(path, content)


def load_site_title() -> str:
    if not SITE_CONFIG_PATH.exists():
        return DEFAULT_TITLE
    data = yaml.safe_load(read_text(SITE_CONFIG_PATH)) or {}
    title = data.get("title")
    if isinstance(title, str) and title.strip():
        return title.strip()
    return DEFAULT_TITLE


def parse_existing_project_meta(site_title: str) -> tuple[str, str]:
    project_id = DEFAULT_PROJECT_ID
    title = site_title
    myst_path = REPO_ROOT / "myst.yml"
    if not myst_path.exists():
        return project_id, title

    text = read_text(myst_path)
    id_match = re.search(r"^\s*id:\s*(.+?)\s*$", text, re.MULTILINE)
    title_match = re.search(r"^\s*title:\s*(.+?)\s*$", text, re.MULTILINE)
    if id_match:
        project_id = id_match.group(1).strip().strip("'\"")
    if title_match and site_title == DEFAULT_TITLE:
        title = title_match.group(1).strip().strip("'\"")
    return project_id, title


def content_files(entry_dir: Path) -> list[Path]:
    files = []
    for path in sorted(entry_dir.iterdir(), key=lambda p: p.name.lower()):
        if not path.is_file():
            continue
        if path.name.startswith(".") or path.name == "index.md":
            continue
        if path.suffix not in CONTENT_SUFFIXES:
            continue
        files.append(path)
    return files


def has_publishable_content(entry_dir: Path) -> bool:
    for path in entry_dir.iterdir():
        if not path.is_file():
            continue
        if path.name.startswith("."):
            continue
        if path.suffix in CONTENT_SUFFIXES:
            return True
    return False


def weekly_entries() -> list[Path]:
    root = REPO_ROOT / "weekly_discussion"
    if not root.exists():
        return []
    pattern = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    entries = [
        path
        for path in root.iterdir()
        if path.is_dir() and pattern.fullmatch(path.name) and has_publishable_content(path)
    ]
    return sorted(entries, key=lambda p: p.name, reverse=True)


def project_entries() -> list[Path]:
    root = REPO_ROOT / "projects"
    if not root.exists():
        return []
    entries = [
        path
        for path in root.iterdir()
        if path.is_dir() and not path.name.startswith(".") and has_publishable_content(path)
    ]
    return sorted(entries, key=lambda p: p.name.lower())


def render_generated_root_index(site_title: str) -> str:
    return f"""---
title: {site_title}
---
{AUTO_MARKER}

这个站点用于沉淀 weekly discussion 与项目研究 notebook。

- [Weekly Discussion](weekly_discussion/overview.md)
- [Projects](projects/overview.md)
"""


def render_generated_overview(section: str, entries: list[Path]) -> str:
    if section == "weekly_discussion":
        title = "Weekly Discussion"
        intro = "这里汇总每次组会讨论与临时研究记录。"
    else:
        title = "Projects"
        intro = "这里汇总长期维护的项目目录。"

    lines = ["---", f"title: {title}", "---", AUTO_MARKER, "", intro, ""]
    if entries:
        lines.append("当前已发现：")
        lines.append("")
        for entry in entries:
            lines.append(f"- [{entry.name}]({entry.name}/index.md)")
    else:
        lines.append("当前还没有可发布的内容目录。")
    lines.append("")
    return "\n".join(lines)


def entry_title(section: str, entry_name: str) -> str:
    if section == "weekly_discussion":
        return f"Weekly Discussion {entry_name}"
    return entry_name


def entry_intro(section: str) -> str:
    if section == "weekly_discussion":
        return "本页为当期讨论入口，自动列出目录中的 notebook 与 markdown。"
    return "本页为项目入口，自动列出目录中的 notebook 与 markdown。"


def render_generated_entry_index(section: str, entry_dir: Path) -> str:
    files = content_files(entry_dir)
    lines = [
        "---",
        f"title: {entry_title(section, entry_dir.name)}",
        "---",
        AUTO_MARKER,
        "",
        entry_intro(section),
        "",
    ]
    if files:
        lines.append("## Contents")
        lines.append("")
        for file_path in files:
            lines.append(f"- [{file_path.name}]({file_path.name})")
    else:
        lines.append("当前目录还没有 notebook 或 markdown 内容。")
    lines.append("")
    return "\n".join(lines)


def ensure_support_pages(site_title: str, weekly: list[Path], projects: list[Path]) -> list[str]:
    touched: list[str] = []
    if ensure_generated_or_missing(REPO_ROOT / "index.md", render_generated_root_index(site_title)):
        touched.append("index.md")

    weekly_overview = REPO_ROOT / "weekly_discussion" / "overview.md"
    if ensure_generated_or_missing(
        weekly_overview, render_generated_overview("weekly_discussion", weekly)
    ):
        touched.append(relative(weekly_overview))

    projects_overview = REPO_ROOT / "projects" / "overview.md"
    if ensure_generated_or_missing(
        projects_overview, render_generated_overview("projects", projects)
    ):
        touched.append(relative(projects_overview))
    return touched


def ensure_entry_indexes(section: str, entries: list[Path]) -> list[str]:
    touched: list[str] = []
    for entry_dir in entries:
        index_path = entry_dir / "index.md"
        content = render_generated_entry_index(section, entry_dir)
        if ensure_generated_or_missing(index_path, content):
            touched.append(relative(index_path))
    return touched


def toc_items_for_entries(entries: list[Path]) -> list[dict]:
    items: list[dict] = []
    for entry_dir in entries:
        item: dict[str, object] = {"file": relative(entry_dir / "index.md")}
        children = [{"file": relative(path)} for path in content_files(entry_dir)]
        if children:
            item["children"] = children
        items.append(item)
    return items


def render_toc_items(items: list[dict], indent: int = 4) -> list[str]:
    lines: list[str] = []
    pad = " " * indent
    child_pad = " " * (indent + 2)
    for item in items:
        lines.append(f"{pad}- file: {item['file']}")
        children = item.get("children", [])
        if children:
            lines.append(f"{child_pad}children:")
            lines.extend(render_toc_items(children, indent + 4))
    return lines


def render_myst(project_id: str, title: str, weekly: list[Path], projects: list[Path]) -> str:
    toc = [
        {"file": "index.md"},
        {
            "file": "weekly_discussion/overview.md",
            "children": toc_items_for_entries(weekly),
        },
        {
            "file": "projects/overview.md",
            "children": toc_items_for_entries(projects),
        },
    ]
    lines = [
        "# AUTO-GENERATED: scripts/update_toc.py",
        "# Edit content files, not this navigation file.",
        "version: 1",
        "project:",
        f"  id: {project_id}",
        f"  title: {title}",
        "  toc:",
    ]
    lines.extend(render_toc_items(toc))
    lines.extend(["site:", "  template: book-theme", ""])
    return "\n".join(lines)


def update_toc() -> dict[str, list[str]]:
    weekly = weekly_entries()
    projects = project_entries()
    site_title = load_site_title()

    touched_pages = ensure_support_pages(site_title, weekly, projects)
    touched_pages.extend(ensure_entry_indexes("weekly_discussion", weekly))
    touched_pages.extend(ensure_entry_indexes("projects", projects))

    project_id, title = parse_existing_project_meta(site_title)
    myst_content = render_myst(project_id, title, weekly, projects)
    myst_changed = write_generated(REPO_ROOT / "myst.yml", myst_content)

    return {
        "weekly_entries": [relative(path) for path in weekly],
        "project_entries": [relative(path) for path in projects],
        "touched_pages": touched_pages,
        "myst_changed": ["myst.yml"] if myst_changed else [],
    }


def main() -> int:
    result = update_toc()
    print(f"weekly entries: {len(result['weekly_entries'])}")
    print(f"project entries: {len(result['project_entries'])}")
    for path in result["touched_pages"] + result["myst_changed"]:
        print(f"updated: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
