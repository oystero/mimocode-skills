# mimocode-skills

MiMo Desktop / MiMoCode agent skills monorepo.

## Skills

| Skill | Directory | What it does |
| --- | --- | --- |
| **frontend-slides** | [`frontend-slides/`](frontend-slides/) | Zero-dependency, animation-rich HTML presentations (fixed 1920×1080 stage), presenter chrome, PPTX extract / PDF export / deploy |
| **html-deck-to-pptx** | [`html-deck-to-pptx/`](html-deck-to-pptx/) | Replicate an HTML deck’s layout & visual system as a matching `.pptx` |

Typical pipeline: build the deck with `frontend-slides`, then convert that HTML to PowerPoint with `html-deck-to-pptx`.

## Install

Copy each skill folder into a skills root, keeping the directory name as the skill ID:

```text
# project-level
<project>/.mimocode/skills/frontend-slides/
<project>/.mimocode/skills/html-deck-to-pptx/

# or user-level
~/.config/mimocode/skills/frontend-slides/
~/.config/mimocode/skills/html-deck-to-pptx/
```

`~/.agents/skills/` is also scanned as a read-only compatibility surface on MiMo Desktop.

Each skill folder is self-contained (`SKILL.md` + scripts/references). Install them as sibling folders — do not nest one skill inside another.

## Attribution

`frontend-slides/bold-template-pack` indexes templates from [zarazhangrui/beautiful-html-templates](https://github.com/zarazhangrui/beautiful-html-templates). See that skill’s README for details.

## License

Skill instructions and scripts are provided as-is for use with MiMo Desktop / MiMoCode. Referenced template designs remain under their original repository’s license.
