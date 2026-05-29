#!/usr/bin/env python3
"""按 ISO 周列出已提取的错误，并标出哪一周还没生成每周报告。

用法:  python scripts/list_weeks.py
被 /weekly 用来决定该汇总哪一周（逻辑和 list_raw.py 一致：
有数据但 analysis/weekly/<周>.md 不存在 = 待汇总）。
"""
import csv
from collections import defaultdict
from datetime import date
from _common import ROOT

MASTER = ROOT / "database" / "errors_master.csv"
WEEKLY = ROOT / "analysis" / "weekly"


def iso_week(d: str) -> str:
    y, w, _ = date.fromisoformat(d).isocalendar()
    return f"{y}-W{w:02d}"


def main():
    if not MASTER.exists():
        print("还没有总表，先运行：python scripts/build_master.py")
        return

    weeks = defaultdict(lambda: {"count": 0, "dates": set()})
    with MASTER.open(encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh):
            d = (row.get("date") or "").strip()
            if not d:
                continue
            try:
                wk = iso_week(d)
            except ValueError:
                continue
            weeks[wk]["count"] += 1
            weeks[wk]["dates"].add(d)

    if not weeks:
        print("总表里还没有错误数据。先用 /extract 提取几天。")
        return

    pending = []
    for wk in sorted(weeks):
        done = (WEEKLY / f"{wk}.md").exists()
        mark = "✅ 已汇总" if done else "⬜ 待汇总"
        if not done:
            pending.append(wk)
        info = weeks[wk]
        span = f"{min(info['dates'])} ~ {max(info['dates'])}"
        print(f"{wk}  {mark}  （{info['count']} 条错误，{len(info['dates'])} 天：{span}）")

    print()
    if pending:
        print(f"待汇总的周：{', '.join(pending)}")
        print(f"最近一个待汇总：{pending[-1]}")
    else:
        print("全部已汇总 🎉")


if __name__ == "__main__":
    main()
