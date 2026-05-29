#!/usr/bin/env python3
"""把 database/errors_master.csv 转成 Anki 可导入的 TSV。

用法:  python scripts/make_anki.py
生成:  exercises/anki/anki_import.tsv
导入:  Anki -> File -> Import，分隔符选 Tab，字段映射 Front/Back/Tags。
只用标准库。
"""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "database" / "errors_master.csv"
OUT = ROOT / "exercises" / "anki" / "anki_import.tsv"


def build_card(row):
    # 正面：让自己改错（用我说错的原句当题面）
    front = f"改对这句：<br>{row['my_sentence']}"
    # 背面：正确说法 + 解析 + 例句
    examples = row["correct_examples"].replace(" | ", "<br>• ")
    back_parts = [f"✅ {row['correction']}"]
    if row["explanation"]:
        back_parts.append(f"<br><br>📖 {row['explanation']}")
    if examples:
        back_parts.append(f"<br><br>例：<br>• {examples}")
    back = "".join(back_parts)
    tags = f"{row['category']} {row['tag']}".strip()
    return front, back, tags


def clean(s):
    # TSV 里换行/制表符会破坏格式
    return s.replace("\t", " ").replace("\n", "<br>")


def main():
    if not SRC.exists():
        print("找不到 master 表，先运行：python scripts/build_master.py")
        return
    OUT.parent.mkdir(parents=True, exist_ok=True)
    n = 0
    with SRC.open(encoding="utf-8-sig", newline="") as fh, \
         OUT.open("w", encoding="utf-8", newline="") as out:
        reader = csv.DictReader(fh)
        for row in reader:
            front, back, tags = build_card(row)
            out.write(f"{clean(front)}\t{clean(back)}\t{clean(tags)}\n")
            n += 1
    print(f"✅ 生成 {n} 张卡片 → {OUT.relative_to(ROOT)}")
    print("   导入 Anki 时：分隔符=Tab，3 列分别映射 正面/背面/标签。")


if __name__ == "__main__":
    main()
