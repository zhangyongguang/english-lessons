#!/usr/bin/env python3
"""把 data/errors/*.json 合并成 database/errors_master.csv。

用法:  python scripts/build_master.py
只用标准库，无需联网或安装依赖。
"""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ERRORS_DIR = ROOT / "data" / "errors"
OUT = ROOT / "database" / "errors_master.csv"

COLUMNS = [
    "id", "date", "category", "tag", "my_sentence", "correction",
    "explanation", "correct_examples", "context",
    "status", "times_seen_again", "last_reviewed", "source_ref",
]


def flatten(rec):
    review = rec.get("review") or {}
    examples = rec.get("correct_examples") or []
    if isinstance(examples, list):
        examples = " | ".join(examples)
    return {
        "id": rec.get("id", ""),
        "date": rec.get("date", ""),
        "category": rec.get("category", ""),
        "tag": rec.get("tag", ""),
        "my_sentence": rec.get("my_sentence", ""),
        "correction": rec.get("correction", ""),
        "explanation": rec.get("explanation", ""),
        "correct_examples": examples,
        "context": rec.get("context", ""),
        "status": review.get("status", ""),
        "times_seen_again": review.get("times_seen_again", 0),
        "last_reviewed": review.get("last_reviewed") or "",
        "source_ref": rec.get("source_ref", ""),
    }


def main():
    rows = []
    files = sorted(p for p in ERRORS_DIR.glob("*.json")
                   if not p.name.endswith(".example.json"))
    if not files:
        print("没找到真实数据文件（*.example.json 会被跳过）。")
        print("先把当天提取好的 JSON 存到 data/errors/YYYY-MM-DD.json")
        return
    for f in files:
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            print(f"⚠️  跳过 {f.name}：JSON 解析失败 ({e})")
            continue
        if isinstance(data, dict):  # 容错：单条也接受
            data = [data]
        for rec in data:
            rows.append(flatten(rec))

    rows.sort(key=lambda r: (r["date"], r["id"]))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(rows)
    print(f"✅ 写入 {len(rows)} 条错误 → {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
