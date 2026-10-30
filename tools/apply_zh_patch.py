# -*- coding: utf-8 -*-
"""把 EVO Player 源码里的界面英文字面量包成 evo_tr("...")。

默认 dry-run：只扫描并输出报告与 diff，不改文件。加 --apply 才真正写入。

    python apply_zh_patch.py --root D:\\path\\EVO-PLAYER-PS5 --tsv zh-CN.tsv
    python apply_zh_patch.py --root ... --tsv zh-CN.tsv --apply

只处理 EVO 自己的代码（projects/evoplayer），跳过第三方子模块与 RmlUi 旧界面
（ui_rml/、third_party/、main.c.legacy）。只有出现在词表里、且处在“画文本 /
赋标题”位置的字面量才会被包裹，所以日志、比较、JSON 键不会被误改。
"""
import argparse
import difflib
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

SKIP_DIRS = {'ui_rml', 'third_party', 'assets', 'build', 'output', '.git', 'tests',
             'addons',    # addons/ 里大量字符串是 API 枚举值，自动包裹不安全
             'i18n-zh'}   # 补丁自己的目录，不许改
SKIP_FILES = {'main.c.legacy', 'evo_i18n.c', 'evo_i18n.h'}

POS = re.compile(
    r'\b(?:ui::(?:text|paragraph|heading|label|body|button|field|chip|row)|'
    r'paint\.(?:heading|label|body|button|field|chip|row|value|detail|title)|'
    r'evo_tr|makeSection|valueDef|toggleDef|actionDef|optionDef|sectionDef|'
    r'text|paragraph|heading|label|body|button|field|chip|row|toast|notice|'
    r'prompt|badge|value|detail|title|subtitle|hint|option|choice|message)\s*\('
    r'|\?\s*$|:\s*$'
)

FMT_POS = re.compile(r'\b(?:std::)?(?:snprintf|sprintf)\s*\([^()]*,\s*$')

ASSIGN = re.compile(
    r'\.(?:title|subtitle|detail|label|name|badge|benefit|message|hint|text|'
    r'opt_label\[[^\]]*\]|empty_title_|empty_hint_|server_name)\s*=\s*'
    r'|\b(?:msg|message|text|title|subtitle|detail|label|hint|badge|name|'
    r'server_name|display_name|str|buf|out|tmp)\s*=\s*'
)

NEG = re.compile(
    r'(?:==|!=|strcmp|strncmp|strcasecmp|strstr|\.find\(|\.count\(|::find\(|'
    r'case\s|#include|#define|#if|static_assert|\bfprintf\b|\bprintf\b|'
    r'evo_log|EVO_LOG|LOG\(|assert|map<|unordered_map|'
    r'cJSON_|GetObjectItem|GetArrayItem|AddStringToObject|AddNumberToObject|'
    r'AddBoolToObject|AddArrayToObject|AddItemToObject|jstr\(|jnum\(|jbool\()'
)

LITERAL = re.compile(r'"((?:[^"\\]|\\.)*)"')
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


def candidate_files(root):
    for base, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in files:
            if name in SKIP_FILES:
                continue
            if os.path.splitext(name)[1] in ('.c', '.cpp', '.h', '.hpp', '.cc'):
                yield os.path.join(base, name)


def add_include(text):
    if 'evo_i18n.h' in text:
        return text
    lines = text.splitlines(keepends=True)
    last = -1
    for i, line in enumerate(lines[:150]):
        if line.lstrip().startswith('#include'):
            last = i
    inc = '#include "evo_i18n.h"\n'
    if last >= 0:
        lines.insert(last + 1, inc)
    else:
        lines.insert(0, inc + '\n')
    return ''.join(lines)


def stmt_bounds(text, pos):
    """当前语句的起止位置（跨行，以 ; { } 为界）。"""
    cut = max(text.rfind(';', 0, pos), text.rfind('{', 0, pos), text.rfind('}', 0, pos))
    ends = [i for i in (text.find(';', pos), text.find('{', pos), text.find('}', pos)) if i >= 0]
    end = min(ends) if ends else len(text)
    return cut + 1, end


def patch_text(text, table, stats):
    out, pos = [], 0
    for m in LITERAL.finditer(text):
        raw = m.group(1)
        if '\\' in raw or raw not in table:
            continue
        if '%' in raw and sorted(SPEC.findall(raw)) != sorted(SPEC.findall(table[raw])):
            stats['negative'] += 1   # 格式串占位符对不上，不能替换
            continue
        beg, end = stmt_bounds(text, m.start())
        if '\\t' in text[beg:end]:        # 同一语句里还有 tab 拼装的 pills 串，拆开翻会不一致
            stats['no_context'] += 1
            continue
        ctx = text[beg:m.start()][-400:]
        if (POS.search(ctx) is None and ASSIGN.search(ctx) is None
                and FMT_POS.search(ctx) is None):
            stats['no_context'] += 1
            continue
        if NEG.search(ctx):
            stats['negative'] += 1
            continue
        if ctx.rstrip().endswith('evo_tr('):
            continue
        out.append(text[pos:m.start()])
        out.append('evo_tr("%s")' % raw)
        pos = m.end()
        stats['wrapped'] += 1
    out.append(text[pos:])
    return ''.join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', required=True, help='EVO-PLAYER-PS5 仓库根目录')
    ap.add_argument('--tsv', required=True, help='zh-CN.tsv')
    ap.add_argument('--apply', action='store_true', help='真正写入（默认只报告）')
    ap.add_argument('--report', default='zh_patch_report.txt')
    ap.add_argument('--diff', default='zh_patch.diff')
    ap.add_argument('--miss', default=None,
                    help='把“词表命中但没被包裹”的位置写到这个文件（人工复核用）')
    args = ap.parse_args()

    table = load_table(args.tsv)
    root = os.path.abspath(args.root)
    totals = {'wrapped': 0, 'no_context': 0, 'negative': 0}
    per_file, diffs, misses = [], [], []

    for path in candidate_files(root):
        with open(path, encoding='utf-8', errors='replace') as f:
            orig = f.read()
        stats = {'wrapped': 0, 'no_context': 0, 'negative': 0}
        new = patch_text(orig, table, stats)
        new = add_include(new)
        rel = os.path.relpath(path, root)
        if args.miss:
            for lineno, line in enumerate(new.splitlines(), 1):
                for lit in LITERAL.finditer(line):
                    raw = lit.group(1)
                    if '\\' in raw or raw not in table:
                        continue
                    if line[:lit.start()].rstrip().endswith('evo_tr('):
                        continue
                    misses.append('%s:%d: %s' % (rel, lineno, raw))
        if stats['wrapped'] == 0:
            for k in totals:
                totals[k] += stats[k]
            continue
        per_file.append((rel, stats['wrapped']))
        d = difflib.unified_diff(orig.splitlines(), new.splitlines(),
                                 fromfile=rel, tofile=rel, lineterm='', n=1)
        diffs.extend(list(d))
        for k in totals:
            totals[k] += stats[k]
        if args.apply:
            with open(path, 'w', encoding='utf-8', newline='\n') as f:
                f.write(new)

    with open(args.report, 'w', encoding='utf-8') as f:
        f.write('EVO Player 中文化补丁报告（%s）\n' % ('已写入' if args.apply else 'dry-run，未写入'))
        f.write('仓库: %s\n词表: %s（%d 条）\n' % (root, args.tsv, len(table)))
        f.write('\n包裹 %d 处，涉及 %d 个文件；因上下文不符跳过 %d 处，因比较/日志跳过 %d 处。\n'
                % (totals['wrapped'], len(per_file), totals['no_context'], totals['negative']))
        f.write('\n每文件包裹数：\n')
        for rel, n in sorted(per_file, key=lambda x: -x[1]):
            f.write('  %5d  %s\n' % (n, rel))

    with open(args.diff, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(diffs) + '\n')

    if args.miss:
        with open(args.miss, 'w', encoding='utf-8', newline='\n') as f:
            f.write('# 词表里有、但没被自动包裹的字符串（需人工判断是界面文案还是逻辑值）\n')
            f.write('# 共 %d 条\n' % len(misses))
            f.write('\n'.join(misses) + '\n')
        print('miss  :', args.miss)

    print('wrapped %d in %d files (no-context %d, negative %d)'
          % (totals['wrapped'], len(per_file), totals['no_context'], totals['negative']))
    print('report:', args.report)
    print('diff  :', args.diff)
    if not args.apply:
        print('dry-run 完成；确认报告与 diff 后加 --apply 写入。')


if __name__ == '__main__':
    main()
