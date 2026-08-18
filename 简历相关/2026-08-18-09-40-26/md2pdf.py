#!/usr/bin/env python3
"""Markdown -> styled HTML -> A4 PDF via Chrome headless."""
import sys
import markdown
from pathlib import Path

src = Path("/Users/xiongwei8/WorkBuddy AI/2026-08-18-09-40-26/简历_v8.md")
html_out = Path("/Users/xiongwei8/WorkBuddy AI/2026-08-18-09-40-26/简历_v8.html")
md_text = src.read_text(encoding="utf-8")

html_body = markdown.markdown(
    md_text,
    extensions=["extra", "sane_lists"],
)

html_doc = f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>熊伟 - Agent 开发工程师简历</title>
<style>
  @page {{
    size: A4;
    margin: 12mm 14mm 12mm 14mm;
  }}
  html, body {{
    margin: 0;
    padding: 0;
    color: #111;
    font-family: -apple-system, BlinkMacSystemFont, "PingFang SC",
      "Hiragino Sans GB", "Microsoft YaHei", "Helvetica Neue", Helvetica,
      Arial, sans-serif;
    font-size: 10.2pt;
    line-height: 1.4;
  }}
  body {{ padding: 0; }}
  h1 {{
    font-size: 17pt;
    margin: 0 0 2mm 0;
    font-weight: 700;
    letter-spacing: 0.5px;
  }}
  h2 {{
    font-size: 11.5pt;
    margin: 3.2mm 0 1.5mm 0;
    border-bottom: 0.6pt solid #999;
    padding-bottom: 0.6mm;
    font-weight: 600;
  }}
  h3 {{
    font-size: 11pt;
    margin: 2mm 0 1mm 0;
    font-weight: 600;
  }}
  p {{
    margin: 0 0 1.2mm 0;
  }}
  ul, ol {{
    margin: 0 0 1.4mm 0;
    padding-left: 5mm;
  }}
  li {{
    margin: 0.3mm 0;
  }}
  hr {{
    border: none;
    border-top: 0.4pt solid #ccc;
    margin: 1.6mm 0;
  }}
  strong {{ font-weight: 600; }}
  em {{ font-style: normal; }}
  .small-note {{
    color: #666;
    font-size: 9pt;
  }}
</style>
</head>
<body>
{html_body}
</body>
</html>
"""

html_out.write_text(html_doc, encoding="utf-8")
print(f"HTML written to: {html_out}")
