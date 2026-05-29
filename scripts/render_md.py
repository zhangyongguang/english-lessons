#!/usr/bin/env python3
"""把某天的 data/errors/DATE.json 渲染成一个简洁的两列表格 Markdown。

只输出「错误」和「正确」两列，其余字段（解释、例句、上下文等）不展示。
用法:  python scripts/render_md.py 2026-05-28
生成:  data/errors/2026-05-28.md
"""
import json
import sys
from _common import ROOT


def cell(text):
    """让一段文本能安全放进 Markdown 表格单元格：转义竖线、压平换行。"""
    return str(text).replace("|", "\\|").replace("\n", " ").strip()


def main():
    if len(sys.argv) < 2:
        print("用法: python scripts/render_md.py YYYY-MM-DD")
        return
    date = sys.argv[1]
    src = ROOT / "data" / "errors" / f"{date}.json"
    if not src.exists():
        print(f"找不到 {src.relative_to(ROOT)}")
        return

    data = json.loads(src.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        data = [data]

    lines = [
        f"# Mistakes · {date}",
        "",
        "| Mistake | Correct |",
        "|---|---|",
    ]
    for e in data:
        lines.append(f"| {cell(e.get('my_sentence', ''))} | {cell(e.get('correction', ''))} |")
    lines.append("")

    out = ROOT / "data" / "errors" / f"{date}.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"✅ 生成报告 → {out.relative_to(ROOT)}（{len(data)} 条）")


if __name__ == "__main__":
    main()
