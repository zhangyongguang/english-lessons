#!/usr/bin/env python3
"""为新的一天创建占位文件。

用法:
    python scripts/new_day.py            # 用今天的日期
    python scripts/new_day.py 2026-05-30 # 指定日期
"""
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    d = sys.argv[1] if len(sys.argv) > 1 else date.today().isoformat()
    raw = ROOT / "data" / "raw" / f"{d}.txt"
    errors = ROOT / "data" / "errors" / f"{d}.json"

    if not raw.exists():
        raw.write_text("", encoding="utf-8")
        print(f"📄 已建空文件 {raw.relative_to(ROOT)} —— 把腾讯会议转写粘贴进去")
    if not errors.exists():
        errors.write_text("[]\n", encoding="utf-8")
        print(f"📄 已建空文件 {errors.relative_to(ROOT)} —— 提取后存这里")

    print("\n下一步：")
    print(f"  1. 转写存入 data/raw/{d}.txt")
    print("  2. 把它 + prompts/extract_errors.md 发给 Claude")
    print(f"  3. 得到的 JSON 存入 data/errors/{d}.json")
    print("  4. 运行 python scripts/build_master.py 更新总表")


if __name__ == "__main__":
    main()
