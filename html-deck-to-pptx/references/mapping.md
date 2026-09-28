# HTML → PPTX 映射参考

## 尺寸与换算

| HTML (1920×1080 stage) | PPT 16:9 |
|------------------------|----------|
| 1 px | `13.333/1920` in ≈ 0.006944 in |
| 1 px 字号 | 0.5 pt |
| 112px 版心左右 | 0.778 in |
| 82px 版心上 | 0.569 in |
| 16px 左侧色条 | 0.111 in |
| 96px 网格间距 | 0.667 in |

```
prs.slide_width  = Emu(12192000)
prs.slide_height = Emu(6858000)
inches = px * 13.333 / 1920
pt     = px * 0.5
```

## 字阶示例（1920 舞台 px → pt）

| 角色 | px | pt | 字体 |
|------|----|----|------|
| Cover title | 94 | 47 | Serif |
| Slide title | 56 | 28 | Serif |
| Lead | 34 | 17 | Serif |
| Case quote | 38 | 19 | Serif |
| Body | 29 | 14.5 | Sans |
| Small | 23 | 11.5 | Sans |
| Eyebrow | 18 | 9 | Sans bold |
| Chapter | 24 | 12 | Serif |
| Number | 76–112 | 38–56 | Serif |

行高：title 1.28，lead/case-quote 1.65，body 1.72，list 1.58。

## 色板 token 解析规则

1. 读 `:root { --name: #hex }`。
2. `rgba(r,g,b,a)` 落到 PPT 时与背景 blend：
   `blend = a*fg + (1-a)*bg`，再取整 hex。  
   例：`rgba(120,47,52,.035)` over `#F5F2EB` ≈ `#F2EFE8`（网格线）。
3. 圆环/印章描边用低饱和暖色，不要纯 ox。

## 组件几何

### sequence（N 列）
- 顶线 y，底线 y+min_h+pad，高 1px `--rule`
- 列宽 `w/N`，列间竖线 1px
- step（gold, 字距）→ 标题（ox bold）→ 正文（muted/sage）

### choice-list
- 行高约 67px，行距约 17px
- 三栏：字母 60px | 文案 | 结果 80px（右对齐）
- 行底 1px 半透明 rule

### rule-frame
- 顶 `--gold` 4px（CSS 常为 2px）
- 底 `--rule` 1px
- 内边距约 26–38px，内文 lead 或 body

### case-quote
- 左 `--gold` 4px
- 文案 `padding-left: 38px`
- 来源 `small-copy` 在下方

### pill
- 描边 `rgba(ox,.26)` blend ≈ `#C9A9A4`
- padding 约 10×19，字号 19px，字距 0.08em

### seal-ring（封面）
- `position:absolute; right:205px; top:265px; w=h=365`
- **left = 1920 - 205 - 365 = 1350**
- 双层 inset 18/38 圆环 + 中心大字

## 页眉页脚

```
eyebrow:  金线 44px + 18px ox bold，letter-spacing ~0.2em
title:    56px serif，margin-top ~27px
chapter:  右上 24px，#9A958B
page-mark: 左下 金线 38px + 17px「…」
```

静态 HTML 的 `.chapter` 可能是章节号；演示 JS 常改成 `pad(当前页) / total`。交付 PPT 时选一种并在 DESIGN.md 写明。

## QA 颜色采样

内容页应稳定出现：

| 颜色 | hex | 检查位置 |
|------|-----|----------|
| 左条 | `#782F34` | x=0–16 |
| 背景 | `#F5F2EB` | 大面积 |
| 标题 ink | `#252B29` | 标题区 |
| 金线 | `#B08A55` | eyebrow / page-mark |
| chapter | `#9A958B` | 右上 |

## 完整性锚点

从 HTML 可见文本抽专有名词、数字、口诀（如「停、查、问」「6500」），在 PPT 全文检索必须命中。
