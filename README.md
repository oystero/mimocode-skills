# frontend-slides

MiMo Desktop / MiMoCode agent skill for creating zero-dependency, animation-rich HTML presentations (1920×1080 fixed stage), with optional PPTX extraction, PDF export, and simple static deploy.

## Install

Copy this folder into one of:

- `<project>/.agents/skills/frontend-slides/`
- `<project>/.mimocode/skills/frontend-slides/`
- or your user-level skills directory

Then invoke via the skill system (`/frontend-slides` or natural language such as “做一份 HTML 演示文稿”).

## What’s included

| Path | Purpose |
| --- | --- |
| `SKILL.md` | Main skill instructions (stage rules, presenter chrome, content rules) |
| `STYLE_PRESETS.md` | Visual style presets |
| `animation-patterns.md` | Motion / reveal patterns |
| `html-template.md` | HTML deck template guidance |
| `viewport-base.css` | Fixed-stage scaling CSS |
| `scripts/extract-pptx.py` | Extract content from PowerPoint |
| `scripts/export-pdf.sh` | Export slides to PDF |
| `scripts/deploy.sh` | Deploy a deck folder / HTML file |
| `bold-template-pack/selection-index.json` | Compact index of bold HTML templates |

## Template pack attribution

`bold-template-pack` indexes templates from:

**[zarazhangrui/beautiful-html-templates](https://github.com/zarazhangrui/beautiful-html-templates)**

Those designs remain the work of their original authors. This skill only stores a selection index (`selection-index.json`) for choosing styles; full `templates/*/` design files are not redistributed in this repository by default.

## Usage notes

- Every deck uses a fixed **1920×1080** stage scaled to the viewport (do not reflow slides for mobile).
- Classroom / live teaching decks should include the presenter chrome described in `SKILL.md` (notes, overview, timer, auto-dim toolbar).
- Prefer local double-click HTML for classroom presentation; use deploy scripts / GitHub Pages for share URLs.

## License

Skill instructions and scripts in this repository are provided as-is for use with MiMo Desktop / MiMoCode. Template designs referenced via `selection-index.json` remain under their original repository’s license.
