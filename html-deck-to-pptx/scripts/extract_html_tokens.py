#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extract design tokens and slide manifest from a presentation HTML."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


def parse_css_vars(css: str) -> dict[str, str]:
    root = re.search(r":root\s*\{([^}]+)\}", css)
    if not root:
        return {}
    vars_: dict[str, str] = {}
    for m in re.finditer(r"(--[\w-]+)\s*:\s*([^;]+);", root.group(1)):
        vars_[m.group(1)] = m.group(2).strip()
    return vars_


def parse_slides(html: str) -> list[dict]:
    slides = []
    for i, m in enumerate(
        re.finditer(r"<section\b([^>]*)>(.*?)</section>", html, re.S | re.I), 1
    ):
        attrs, body = m.group(1), m.group(2)
        def attr(name: str) -> str:
            am = re.search(rf'data-{name}="([^"]*)"', attrs)
            return am.group(1) if am else ""
        classes = re.search(r'class="([^"]*)"', attrs)
        text = re.sub(r"<script[\s\S]*?</script>", " ", body)
        text = re.sub(r"<style[\s\S]*?</style>", " ", text)
        text = re.sub(r"<[^>]+>", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        slides.append(
            {
                "index": i,
                "title": attr("title"),
                "notes": attr("notes"),
                "classes": classes.group(1) if classes else "",
                "text": text[:500],
            }
        )
    return slides


def parse_typography(css: str) -> list[str]:
    fonts = re.findall(r"font-family:\s*([^;]+);", css)
    sizes = sorted({s for s in re.findall(r"font-size:\s*(\d+)px", css)}, key=int, reverse=True)
    return [f.strip() for f in fonts[:8]], [int(s) for s in sizes[:20]]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("html", type=Path)
    ap.add_argument("--json", type=Path, help="Write full manifest JSON")
    args = ap.parse_args()

    html = args.html.read_text(encoding="utf-8", errors="replace")
    style = "\n".join(re.findall(r"<style[^>]*>([\s\S]*?)</style>", html, re.I))
    tokens = parse_css_vars(style)
    slides = parse_slides(html)
    font_families, font_sizes = parse_typography(style)

    print(f"File: {args.html}")
    print(f"Slides: {len(slides)}")
    print("\nCSS tokens:")
    for k, v in tokens.items():
        print(f"  {k}: {v}")
    print(f"\nFont families (sample): {font_families}")
    print(f"Font sizes px (sample): {font_sizes}")
    print("\nManifest:")
    for s in slides:
        print(f"  {s['index']:02d}. {s['title'] or '(no data-title)'}")

    if args.json:
        args.json.write_text(
            json.dumps(
                {
                    "tokens": tokens,
                    "slides": slides,
                    "font_families": font_families,
                    "font_sizes_px": font_sizes,
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
        print(f"\nWrote {args.json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
