# dabai-skills

大白的 Claude Code 技能包集合。

## 安装

```bash
npx skills add idabaicai/dabai-skills
```

安装指定技能：

```bash
npx skills add idabaicai/dabai-skills/finance-news-brief
```

## 技能列表

### finance-news-brief — 全球财经简报

自动生成每日全球财经新闻简报，涵盖宏观经济、美股、港股、A股四大板块，输出 Markdown 和专业排版 PDF 两种格式。

**触发关键词**：财经简报、财经新闻、市场资讯、今日行情、市场简报

#### 使用方式

在 Claude Code 中直接用自然语言触发：

```
帮我生成今日财经简报
今天市场有什么大事？
```

Claude 会自动执行完整工作流：

1. 通过 WebSearch 抓取各板块最新资讯
2. 整理汇总为结构化 Markdown 文件
3. 调用 `generate_pdf.py` 生成带封面的 PDF

#### 手动生成 PDF

```bash
python finance-news-brief/scripts/generate_pdf.py \
  --input /path/to/finance_brief_YYYYMMDD.md \
  --output /path/to/finance_brief_YYYYMMDD.pdf
```

**依赖**：Python 3.6+，Chrome 或 Chromium 浏览器

#### 输出格式

```
finance_brief_20260312.md   # Markdown 正文
finance_brief_20260312.pdf  # 带封面的 PDF（深蓝色封面 + 金色装饰）
```

简报结构：执行摘要 → 宏观 & 央行动态 → 美股 → 港股 → A股 → 风险提示

## 项目结构

```
dabai-skills/
├── finance-news-brief/
│   ├── SKILL.md              # 完整工作流文档
│   ├── evals/
│   │   └── evals.json        # 测试用例（3 个场景）
│   └── scripts/
│       ├── generate_pdf.py   # Markdown → PDF 转换脚本
│       └── template.html     # PDF 样式模板
└── history/                  # 历史生成的简报
```
