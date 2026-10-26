#!/usr/bin/env python3
"""Check that every relative link and image in docs/ points to an existing file.

Usage:  python3 tools/check_links.py [ROOT]

ROOT defaults to the repository root (the parent of this script's folder).
Exit code is 1 if any broken link is found.
"""
import os
import posixpath
import re
import sys
import urllib.parse

LINK_RE = re.compile(r"\]\((<[^>]+>|[^)\s]+)")


def main() -> int:
    root = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else
                           os.path.join(os.path.dirname(__file__), ".."))
    broken = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d != ".git"]
        for name in filenames:
            if not name.endswith(".md"):
                continue
            page = os.path.join(dirpath, name)
            with open(page, encoding="utf-8", errors="ignore") as fh:
                text = fh.read()
            for match in LINK_RE.finditer(text):
                target = match.group(1).strip("<>").split("#", 1)[0]
                if not target or target.startswith(("http://", "https://", "mailto:")):
                    continue
                target = urllib.parse.unquote(target)
                if target.startswith("/"):
                    resolved = os.path.join(root, target.lstrip("/"))
                else:
                    resolved = os.path.normpath(os.path.join(dirpath, target))
                if not os.path.exists(resolved):
                    rel = os.path.relpath(page, root)
                    print(f"BROKEN  {rel}  ->  {match.group(1)}")
                    broken += 1
    print(f"{broken} broken link(s)")
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
