# -*- coding: utf-8 -*-
"""Generate evo_i18n_table.inc from zh-CN.tsv.

用法:
    python gen_table.py zh-CN.tsv projects/evoplayer/core/src/i18n/evo_i18n_table.inc
"""
import sys, os

def esc(s: str) -> str:
    out = []
    for ch in s:
        if ch == '\\':
            out.append('\\\\')
        elif ch == '"':
            out.append('\\"')
        elif ch == '\t':
            out.append('\\t')
        elif ch == '\n':
            out.append('\\n')
        else:
            out.append(ch)
    return ''.join(out)

def main() -> int:
    tsv = sys.argv[1] if len(sys.argv) > 1 else 'zh-CN.tsv'
    inc = sys.argv[2] if len(sys.argv) > 2 else os.path.join(
        'projects', 'evoplayer', 'core', 'src', 'i18n', 'evo_i18n_table.inc')
    rows, seen, skipped = [], set(), 0
    with open(tsv, encoding='utf-8-sig') as f:
        for lineno, line in enumerate(f, 1):
            line = line.rstrip('\n').rstrip('\r')
            if not line or line.startswith('#'):
                continue
            if '\t' not in line:
                print(f'  skip line {lineno}: no tab')
                skipped += 1
                continue
            en, zh = line.split('\t', 1)
            if not en or not zh:
                skipped += 1
                continue
            if en in seen:
                continue
            seen.add(en)
            rows.append((en, zh))
            continue
    with open(inc, 'w', encoding='utf-8', newline='\n') as f:
        f.write('/* 由 tools/gen_table.py 从 zh-CN.tsv 生成，请勿手改。 */\n')
        for en, zh in rows:
            f.write('    {"%s", "%s"},\n' % (esc(en), esc(zh)))
    print(f'entries: {len(rows)}  skipped: {skipped}  ->  {inc}')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
