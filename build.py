#!/usr/bin/env python3
"""Inline every local asset into one standalone HTML file.

The site needs no build step to run or to deploy - index.html works as it is.
This script exists only to produce a single file you can email, drop into a
learning-management system, or open straight from disk with no web server.

    python3 build.py            ->  dist/compilearn.html

The only remaining external reference is the Google Fonts stylesheet. Pass
--no-fonts to strip it and fall back to the system font stack.
"""

import argparse
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "dist" / "compilearn.html"

CSS_LINK = re.compile(r'[ \t]*<link rel="stylesheet" href="([^"]+)">[ \t]*\n')
JS_TAG = re.compile(r'[ \t]*<script src="([^"]+)"></script>[ \t]*\n')
ICON_LINK = re.compile(r'[ \t]*<link rel="icon"[^>]*>[ \t]*\n')
FONT_LINKS = re.compile(r'[ \t]*<link[^>]*fonts\.(googleapis|gstatic)\.com[^>]*>[ \t]*\n')


def read(rel: str) -> str:
    path = ROOT / rel
    if not path.exists():
        sys.exit(f"missing asset: {rel}")
    return path.read_text(encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--no-fonts", action="store_true",
                    help="drop the Google Fonts link and use system fonts")
    args = ap.parse_args()

    html = read("index.html")

    html = CSS_LINK.sub(
        lambda m: "<style>\n" + read(m.group(1)) + "</style>\n", html)

    scripts = []
    html = JS_TAG.sub(lambda m: scripts.append(read(m.group(1))) or "", html)
    if not scripts:
        sys.exit("no <script src=...> tags found in index.html")
    html = html.replace("</body>", "<script>\n" + "\n".join(scripts) + "\n</script>\n</body>", 1)

    html = ICON_LINK.sub("", html)
    if args.no_fonts:
        html = FONT_LINKS.sub("", html)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}  ({len(html) / 1024:.0f} KB, "
          f"{len(scripts)} scripts inlined)")


if __name__ == "__main__":
    main()
