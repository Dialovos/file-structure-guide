"""Offline behavioral checks for imported projects without existing test runners."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
DOMAINS = ["principles", "code", "notes", "files"]
SECTIONS = [
    "TL;DR",
    "Principles & why",
    "When to use",
    "When NOT to use",
    "Tree diagram",
    "Naming rules",
    "Worked example",
    "Anti-patterns",
    "Scaling & failure modes",
    "Variants",
    "Adoption checklist",
    "Real-world projects using this",
    "Migration & references",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def check_guide() -> None:
    root = ROOT
    domains = DOMAINS
    guides = [guide for domain in domains for guide in (root / domain).glob("*/GUIDE.md")]
    catalog = (root / "INDEX.md").read_text(encoding="utf-8")
    declared = re.search(r"catalog of all (\d+) guidelines", catalog)
    require(declared is not None, "Index must declare its guideline count")
    require(len(guides) == int(declared.group(1)), "Guideline count differs from the index")
    for guide in guides:
        name = guide.parent.name
        require((guide.parent / "tree.md").is_file(), f"Missing tree.md for {name}")
        require((guide.parent / "template").is_dir(), f"Missing template for {name}")
        body = re.sub(r"```.*?```", "", guide.read_text(encoding="utf-8"), flags=re.S)
        headings = re.findall(r"^## (.+?)\s*$", body, re.M)
        require(headings[: len(SECTIONS)] == SECTIONS, f"{name}/GUIDE.md sections differ from the standard order")
        require(f"({guide.parent.parent.name}/{name}/" in catalog, f"INDEX.md does not list {name}")
    readme = (root / "README.md").read_text(encoding="utf-8")
    total = re.search(r"\*\*(\d+) in-depth guidelines\*\*", readme)
    require(total is not None and int(total.group(1)) == len(guides), "README total differs from the guide count")
    for domain in domains:
        actual = len(list((root / domain).glob("*/GUIDE.md")))
        stated = re.search(rf"\[{domain}/\]\({domain}/\)\*\* — (\d+)", readme)
        require(stated is not None, f"README must state the {domain} count")
        require(int(stated.group(1)) == actual, f"README {domain} count differs from the folder")
    pages = [root / name for name in ("README.md", "INDEX.md", "CHOOSE.md")]
    pages += [root / domain / "README.md" for domain in domains]
    checked = 0
    for page in pages:
        for target in re.findall(r"\[[^\]\n]+\]\(([^)\s]+)\)", page.read_text(encoding="utf-8")):
            url = urlsplit(target)
            if url.scheme or url.netloc or not url.path:
                continue
            path = page.parent / unquote(url.path)
            require(path.exists(), f"Broken navigation link in {page.relative_to(root)}: {target}")
            checked += 1
    print(f"File guide: {len(guides)} guideline structures and {checked} navigation links passed.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", choices=["file-structure-guide"])
    parser.parse_args()
    check_guide()


if __name__ == "__main__":
    main()
