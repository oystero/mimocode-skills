---
name: html-deck-to-pptx
description: 把 HTML 演示文稿/课件的版式与视觉系统一比一复刻成 .pptx。Use when the user says「按该 html 风格输出 pptx」「把网页课件做成 PPT」「HTML 转 PPTX」「复刻这个 HTML 幻灯片」「outputs 里的 html 生成同款 pptx」，or provides a self-contained presentation HTML (fixed 1920×1080 stage, slide sections, CSS design tokens) and wants a matching PowerPoint deck. Also for DESIGN.md-style HTML slide specs → PPTX. Do NOT use for converting arbitrary websites to slides, or for building a deck from a prompt with no source HTML.
---

# HTML Deck → PPTX

把固定舞台 HTML 课件（CSS tokens + slide sections）复刻为风格一致的 `.pptx`。核心是：**先提取设计系统，再按组件映射逐页生成，最后用真实渲染做视觉 QA**。

## 重要约束

1. **必须先读 HTML 的 CSS 与全部 slide DOM**，禁止凭印象配色/排版。
2. **CJK 字体必须写 `a:latin` + `a:ea` + `a:cs` 三槽**，否则中文掉字或替换字体。
3. **图片一律本地文件**；`add_picture` 不接受 HTTP URL。源 HTML 无位图时不要硬造配图。
4. **导出 QA 优先用 PowerPoint COM**（Windows 已装 Office 时）；捆绑 LibreOffice 在部分环境会 `0xC000007B` 崩溃。
5. 生成后必须跑：结构诊断 + 关键短语完整性 + 渲染图 chrome 抽查。

## 工作流

### Step 1 — 解析 HTML 设计系统

从 `<style>` 与 `:root` 提取 tokens，写入工作区 `DESIGN.md`（内部用，不必交付）：

| 项 | 抓什么 |
|----|--------|
| 舞台尺寸 | 通常 `width:1920px;height:1080px` |
| 色板 | `--slide-bg / --ink / --ox / --gold / --rule` 等 hex |
| 字体 | serif / sans 的 Google Fonts 或 font-family |
| 版心 | `padding`（如 `82px 112px 76px`）、左侧色条宽 |
| 组件 | `.sequence / .choice-list / .case-quote / .rule-frame / .pill / .number / .list` |
| 页眉页脚 | `.eyebrow / .chapter / .page-mark` |
| 备注 | 每个 `<section>` 的 `data-notes`、`data-title` |

用脚本或正则枚举所有 `<section class="slide">`，得到页数与标题清单。

### Step 2 — 单位换算（1920×1080 → 16:9 PPT）

PowerPoint 16:9 = **13.333 × 7.5 in**（= 12192000 × 6858000 EMU）。

```
inches = html_px × 13.333 / 1920
pt     = html_px × 0.5          # 1920px 宽 ≡ 960pt 幻灯片宽
```

直接用这两个公式写坐标/字号，可与 HTML 几乎像素级对齐。

### Step 3 — CJK 字体（必做）

```python
from pptx.oxml.ns import qn

def set_cjk_font(run, font_name):
    run.font.name = font_name          # a:latin
    rPr = run._r.get_or_add_rPr()
    successors = {
        "a:ea": ("a:cs", "a:sym", "a:hlinkClick", "a:hlinkMouseOver", "a:rtl", "a:extLst"),
        "a:cs": ("a:sym", "a:hlinkClick", "a:hlinkMouseOver", "a:rtl", "a:extLst"),
    }
    for tag in ("a:ea", "a:cs"):
        el = rPr.find(qn(tag))
        if el is None:
            el = rPr.makeelement(qn(tag), {})
            rPr.insert_element_before(el, *successors[tag])
        el.set("typeface", font_name)
```

Windows 本机渲染/QA 时优先用 HTML 里声明的字体名（如 `Noto Serif SC` / `Noto Sans SC`）；跨平台交付可退回 `Microsoft YaHei`。

### Step 4 — 组件映射

| HTML 组件 | PPTX 画法 |
|-----------|-----------|
| `.slide` 背景 | `slide.background` 填 `--slide-bg` |
| `::after` 左侧色条 | 通高 `rect(0,0,barW,1080)` 填 `--ox` |
| `.slide::before` 竖线纹理 | 每 96px 一条 1px 淡色线（先算 blend，不要用不透明强调色） |
| `.eyebrow` | 短金线 + 字距加大的 sans 小字 |
| `.slide-title` | serif 大标题，`line_spacing≈1.28` |
| `.chapter` | 右上角；演示态多为 `当前页 / 总页数` |
| `.page-mark` | 左下金线 + 固定文案 |
| `.sequence` | 顶/底 1px rule + N 列，列间竖 rule；step 小字 + 标题 + 正文 |
| `.case-quote` | 左侧 4px `--gold` 竖条 + serif 引文 |
| `.choice-list` | 字母列 + 文案 + 结果列 + 行底 rule |
| `.number` | serif 超大字，色在 ox / gold / sage 间轮换 |
| `.rule-frame` | 顶 2–4px gold + 底 1px rule，内文 lead/body |
| `.pill` | 1px 暖色描边矩形 + ox 小字 |
| `.list` | 金色 serif 序号 `01` + 正文 |
| `.answer-box` | 左 ox 竖条 + 极浅暖底 + 正文（静态 PPT 默认显示答案） |
| 封面 `.seal-ring` | **注意 CSS 是 `right:205px`** → `left = 1920-205-width`，勿写成 left:205 |
| `data-notes` | `slide.notes_slide.notes_text_frame.text` |

互动揭示（`answers-on` / `data-quiz`）在 PPT 里改为**静态展开**，并在备注写讲解提示。

### Step 5 — 生成

用 `python-pptx`（`MIMO_PYTHON`）写构建脚本，一页一个函数块，色板/字体集中成 token。  
用户要「完全一致」时：**页序、文案、备注与 HTML 1:1**，不要自行增删章节。

### Step 6 — QA（缺一不可）

1. **诊断**：用 pptx-official 技能的 diagnose 脚本，或 Presentation() 往返打开。
2. **残渣**：`dump_text` 后搜 `{{` / TODO / lorem / click to add。
3. **关键短语**：从 HTML 抽 20–40 个锚点词，确认均出现在 PPT 文本中。
4. **渲染**：
   - 优先 PowerPoint COM 导出 PNG（见 `scripts/export_slides.ps1`）。
   - LibreOffice 可用则 `render_slides.py`；若退出码 `-1073741701`（0xC000007B）直接改走 COM。
5. **chrome 抽查**（程序化即可）：内容页应有左色条、eyebrow 色、标题 ink、page-mark 金线、右上 chapter。
6. 有条件再做人工/视觉子代理对照 HTML 截图。

## 示例

**输入**：`outputs/课件.html`（1920 舞台、21 个 section、Noto Serif/Sans SC、ox/gold 米白）  
**输出**：同名 `.pptx`，21 页，色板/字阶/组件一致，备注来自 `data-notes`。

## Troubleshooting

| 问题 | 处理 |
|------|------|
| 中文变成豆腐块 | 补 `a:ea`/`a:cs`；确认字体名本机存在 |
| 封面印章压标题 | 用 CSS 的 `right` 换算绝对 `left`，勿照抄 `right` 当 `left` |
| 通页竖条纹刺眼 | 网格线用与背景 blend 后的极淡色，勿用强调色 1px |
| LibreOffice 转 PDF 崩溃 | 改 PowerPoint COM 导出 |
| 标题折行 | 56px 级标题在 1500px 栏约 26 个汉字/行；超了缩短文案或加宽 |
| 章节号对不上 | 先对齐 HTML 静态值还是演示脚本运行值（JS 常改成页码） |

## 配套文件

- `references/mapping.md` — 完整 token/组件对照与换算表
- `scripts/extract_html_tokens.py` — 从 HTML 抽 tokens 与 slide 清单
- `scripts/export_slides.ps1` — PowerPoint COM 导出 1920×1080 PNG

