#!/usr/bin/env python3
"""Wrap an Artifact-style HTML page (title, style, body, no document skeleton) into a standalone page.

Usage: make-standalone.py INPUT.html OUTPUT.html [--description TEXT]
Standard library only. A file that already starts with <!doctype is copied unchanged.
"""
import html
import re
import sys


def main() -> int:
    args = sys.argv[1:]
    description = ""
    if "--description" in args:
        i = args.index("--description")
        description = args[i + 1]
        del args[i : i + 2]
    if len(args) != 2:
        print(__doc__)
        return 2
    src = open(args[0], encoding="utf-8").read()
    if src.lstrip().lower().startswith("<!doctype"):
        open(args[1], "w", encoding="utf-8").write(src)
        return 0
    src = re.sub(r'<meta name="claude:[^>]*>\n?', "", src)
    end = src.rfind("</style>")
    if end == -1 or "<title>" not in src:
        print("expected a <title> and a <style> block at the top of the page", file=sys.stderr)
        return 1
    end += len("</style>")
    head, body = src[:end], src[end:]
    meta = ""
    if description:
        meta = '<meta name="description" content="%s">\n' % html.escape(description, quote=True)
    out = (
        '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        + meta
        + head
        + "\n<style>body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>\n"
        "</head>\n<body>"
        + body
        + "\n</body>\n</html>\n"
    )
    open(args[1], "w", encoding="utf-8").write(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
