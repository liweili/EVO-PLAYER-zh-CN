# -*- coding: utf-8 -*-
"""直接改发布版 eboot.bin：把明文字符串等长替换成中文，不需要重新编译。

    python tools/patch_eboot.py --eboot <目录或 eboot.bin> --tsv i18n-zh/lang/zh-CN.tsv
    python tools/patch_eboot.py --eboot ... --apply     # 真正写入（先自动备份）

原理：EBoot 里的界面文案是明文字符串（NUL 结尾）。脚本把文件里每段“可打印
ASCII 连续字节”切出来，只有整段文本与词表某条英文完全相等时才替换，所以
"AUTO" 不会误伤到 "AUTOMATIC" 里。替换后剩余字节用空格补满，字节长度与原来
完全一致，不移动任何数据、不改任何偏移。

限制：
  * 中文 UTF-8 比英文长的条目（短片词）放不下，保留英文；
  * 需要主机上有 CJK 字形，否则显示方块。
"""
import argparse
import os
import re
import shutil
import sys

sys.stdout.reconfigure(encoding='utf-8')

RUN = re.compile(rb'[\x20-\x7e]{2,}')
SPEC = re.compile(r'%(?:\d+\$)?[-+ #0]*\d*(?:\.\d+)?[diouxXeEfgGcs%]')


def load_table(path):
    table = {}
    with open(path, encoding='utf-8-sig') as f:
        for line in f:
            line = line.rstrip('\n').rstrip('\r')
            if not line or line.startswith('#') or '\t' not in line:
                continue
            en, zh = line.split('\t', 1)
            if en and zh and zh != en:
                table[en] = zh
    return table


def resolve(path):
    if os.path.isdir(path):
        return os.path.join(path, 'eboot.bin')
    return path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--eboot', required=True, help='发布版目录，或直接给 eboot.bin')
    ap.add_argument('--tsv', required=True, help='zh-CN.tsv')
    ap.add_argument('--apply', action='store_true', help='真正写入（默认只预演）')
    ap.add_argument('--report', default='eboot_patch_report.txt')
    args = ap.parse_args()

    path = resolve(args.eboot)
    if not os.path.isfile(path):
        raise SystemExit('找不到 eboot.bin：' + path)
    table = load_table(args.tsv)

    with open(path, 'rb') as f:
        data = f.read()

    hits, not_fit, seen, bad_fmt = [], set(), set(), set()
    for m in RUN.finditer(data):
        text = m.group().decode('ascii')
        if text not in table:
            continue
        zh = table[text]
        zh_b = zh.encode()
        if len(zh_b) > len(text):
            not_fit.add(text)
            continue
        if '%' in text and sorted(SPEC.findall(text)) != sorted(SPEC.findall(zh)):
            bad_fmt.add(text)     # 占位符对不上，替换会打崩 printf
            continue
        seen.add(text)
        hits.append((m.start(), text, zh_b))

    missing = sorted(k for k in table if k not in seen and k not in not_fit and k not in bad_fmt)

    print('文件    :', path, '(%.1f MB)' % (len(data) / 1048576))
    print('词表    :', len(table), '条')
    print('命中替换:', len(hits), '处 /', len(seen), '条')
    print('放不下  :', len(not_fit), '条（中文比英文长，保留英文）')
    print('占位符不符:', len(bad_fmt), '条（保留英文）')
    print('未出现  :', len(missing), '条（可能不存在于这个版本）')

    if not args.apply:
        with open(args.report, 'w', encoding='utf-8', newline='\n') as f:
            f.write('# eboot.bin 中文替换（dry-run）\n')
            f.write('替换 %d 处，涉及 %d 条英文\n\n' % (len(hits), len(seen)))
            f.write('[放不下，保留英文] %d 条\n' % len(not_fit))
            for k in sorted(not_fit, key=lambda s: -len(s)):
                f.write('  %-40s %s\n' % (k, table[k]))
            f.write('\n[未在文件中出现] %d 条\n' % len(missing))
            for k in missing:
                f.write('  %s\n' % k)
        print('report  :', args.report)
        print('dry-run 完成，确认后加 --apply。')
        return

    bak = path + '.bak'
    if not os.path.exists(bak):
        shutil.copy2(path, bak)
        print('备份    :', bak)
    else:
        print('备份    :', bak, '已存在，未覆盖')

    ba = bytearray(data)
    for off, text, zh_b in hits:
        ba[off:off + len(text)] = zh_b + b' ' * (len(text) - len(zh_b))

    with open(path, 'wb') as f:
        f.write(ba)

    with open(args.report, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# eboot.bin 中文替换（已写入）\n')
        f.write('替换 %d 处，涉及 %d 条英文\n\n' % (len(hits), len(seen)))
        f.write('[放不下，保留英文] %d 条\n' % len(not_fit))
        for k in sorted(not_fit, key=lambda s: -len(s)):
            f.write('  %-40s %s\n' % (k, table[k]))
        f.write('\n[未在文件中出现] %d 条\n' % len(missing))
        for k in missing:
            f.write('  %s\n' % k)
    print('已写入  :', path)
    print('report  :', args.report)
    print('还原命令: copy /y "%s" "%s"' % (bak, path))


if __name__ == '__main__':
    main()
