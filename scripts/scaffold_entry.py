#!/usr/bin/env python3
"""Create a new weekly discussion or project entry with a minimal index.md."""

from __future__ import annotations

import argparse
import datetime as dt
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a new weekly discussion or project directory."
    )
    subparsers = parser.add_subparsers(dest="entry_type", required=True)

    weekly_parser = subparsers.add_parser(
        "weekly", help="Create a weekly discussion directory."
    )
    weekly_parser.add_argument("name", help="Date in YYYY-MM-DD format.")
    weekly_parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite index.md if it already exists.",
    )
    weekly_parser.add_argument(
        "--skip-toc",
        action="store_true",
        help="Do not run scripts/update_toc.py after scaffolding.",
    )

    project_parser = subparsers.add_parser(
        "project", help="Create a project directory."
    )
    project_parser.add_argument("name", help="Project directory name.")
    project_parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite index.md if it already exists.",
    )
    project_parser.add_argument(
        "--skip-toc",
        action="store_true",
        help="Do not run scripts/update_toc.py after scaffolding.",
    )
    return parser.parse_args()


def validate_weekly_name(name: str) -> str:
    try:
        dt.datetime.strptime(name, "%Y-%m-%d")
    except ValueError as exc:
        raise SystemExit(f"Invalid weekly date '{name}'. Expected YYYY-MM-DD.") from exc
    return name


def validate_project_name(name: str) -> str:
    candidate = Path(name)
    if candidate.name != name or name in {".", ".."}:
        raise SystemExit(
            f"Invalid project name '{name}'. Use a single directory name without '/'."
        )
    return name


def build_target(entry_type: str, name: str) -> Path:
    if entry_type == "weekly":
        return REPO_ROOT / "weekly_discussion" / validate_weekly_name(name)
    if entry_type == "project":
        return REPO_ROOT / "projects" / validate_project_name(name)
    raise SystemExit(f"Unsupported entry type: {entry_type}")


def render_index(entry_type: str, name: str) -> str:
    if entry_type == "weekly":
        title = f"Weekly Discussion {name}"
        intro = "本目录用于记录当期组会讨论与相关 notebook。"
    else:
        title = name
        intro = "本目录用于沉淀该项目的 notebook、结论与补充材料。"

    return f"""# {title}

{intro}

## Contents

- 在当前目录添加 notebook、图片或补充说明
- 如需更详细说明，可直接扩展本页
"""


def write_index(target_dir: Path, content: str, force: bool) -> None:
    index_path = target_dir / "index.md"
    existed_before = index_path.exists()
    if existed_before and not force:
        print(f"index exists, kept as-is: {index_path.relative_to(REPO_ROOT)}")
        return

    index_path.write_text(content, encoding="utf-8")
    action = "overwrote" if existed_before else "created"
    print(f"{action} index: {index_path.relative_to(REPO_ROOT)}")


def maybe_update_toc(skip_toc: bool) -> None:
    if skip_toc:
        return

    update_script = REPO_ROOT / "scripts" / "update_toc.py"
    if not update_script.exists():
        print("update_toc.py not found, skipped TOC update.")
        return

    result = subprocess.run(
        [sys.executable, str(update_script)],
        cwd=REPO_ROOT,
        check=False,
    )
    if result.returncode != 0:
        raise SystemExit(f"update_toc.py failed with exit code {result.returncode}")


def main() -> int:
    args = parse_args()
    target_dir = build_target(args.entry_type, args.name)
    target_dir.mkdir(parents=True, exist_ok=True)
    print(f"ready: {target_dir.relative_to(REPO_ROOT)}")

    content = render_index(args.entry_type, args.name)
    write_index(target_dir, content, args.force)
    maybe_update_toc(args.skip_toc)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
