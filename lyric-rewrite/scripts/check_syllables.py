#!/usr/bin/env python3
"""逐句核对改编歌词与原词的字数是否对齐（可唱性自检）。

用法：
    python3 check_syllables.py --original original.txt --new new.txt

两个文件每行一句，顺序一一对应。脚本逐行统计汉字数（忽略标点、空格、
括号内的结构标注如 [副歌]），并高亮字数不一致的行。

汉字才计入字数；歌词里夹的英文单词不计入（请人工按音节折算判断）。
"""
import argparse
import re
import sys

# 匹配中日韩统一表意文字（基本区），即“算一个字”的汉字
HAN_RE = re.compile(r"[一-鿿]")
# 结构标注行，如 [主歌] [副歌] [Bridge]，或 《歌名》开头，跳过不计
SECTION_RE = re.compile(r"^\s*[\[（(【].*[\]）)】]\s*$")


def count_han(line: str) -> int:
    return len(HAN_RE.findall(line))


def load_lines(path: str):
    """读入非空、非结构标注的歌词行，保留原文用于显示。"""
    out = []
    with open(path, encoding="utf-8") as f:
        for raw in f:
            line = raw.rstrip("\n")
            if not line.strip():
                continue
            if SECTION_RE.match(line):
                continue
            out.append(line)
    return out


def main():
    ap = argparse.ArgumentParser(description="核对改编歌词与原词的逐句字数对齐")
    ap.add_argument("--original", required=True, help="原词文件，每行一句")
    ap.add_argument("--new", required=True, help="改编词文件，每行一句")
    args = ap.parse_args()

    orig = load_lines(args.original)
    new = load_lines(args.new)

    n = max(len(orig), len(new))
    mismatches = 0
    print(f"{'行':>3}  {'原词':>3} {'改编':>3}  说明")
    print("-" * 60)
    for i in range(n):
        o = orig[i] if i < len(orig) else None
        m = new[i] if i < len(new) else None
        oc = count_han(o) if o is not None else "-"
        mc = count_han(m) if m is not None else "-"
        ok = (o is not None and m is not None and oc == mc)
        flag = "✓" if ok else "✗ 不齐"
        if not ok:
            mismatches += 1
        otext = o if o is not None else "（原词无对应句）"
        mtext = m if m is not None else "（改编无对应句）"
        print(f"{i + 1:>3}  {str(oc):>3} {str(mc):>3}  {flag}")
        if not ok:
            print(f"        原: {otext}")
            print(f"        改: {mtext}")

    print("-" * 60)
    if len(orig) != len(new):
        print(f"⚠ 句数不一致：原词 {len(orig)} 句，改编 {len(new)} 句。")
    if mismatches == 0 and len(orig) == len(new):
        print("✅ 全部对齐，可唱性 OK。")
    else:
        print(f"❌ 有 {mismatches} 处字数不齐，请修改到一致。")
        sys.exit(1)


if __name__ == "__main__":
    main()
