#!/usr/bin/env python3
"""列出 data/raw/ 里的转写，按日期分组，并标出哪天还没提取错误。

用法:  python scripts/list_raw.py
被 /extract 工作流用来决定该处理哪一天。
"""
from collections import defaultdict
from _common import ROOT, parse_date

RAW = ROOT / "data" / "raw"
ERRORS = ROOT / "data" / "errors"


def main():
    groups = defaultdict(list)
    for f in sorted(RAW.glob("*.txt")):
        d = parse_date(f.name) or "未知日期"
        groups[d].append(f.name)

    if not groups:
        print("data/raw/ 里没有转写文件。把腾讯会议下载的 .txt 放进去即可。")
        return

    pending = []
    for d in sorted(groups):
        done = (ERRORS / f"{d}.json").exists()
        mark = "✅ 已提取" if done else "⬜ 待提取"
        if not done:
            pending.append(d)
        print(f"{d}  {mark}  （{len(groups[d])} 个转写）")
        for n in groups[d]:
            print(f"      - {n}")

    print()
    if pending:
        print(f"待提取的日期：{', '.join(pending)}")
        print(f"最近一个待提取：{pending[-1]}")
    else:
        print("全部已提取 🎉")


if __name__ == "__main__":
    main()
