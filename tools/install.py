# -*- coding: utf-8 -*-
"""把 i18n-zh/ 文件夹装进 EVO Player 源码树。

    python tools/install.py --root D:\\path\\EVO-PLAYER-PS5            # 只预演
    python tools/install.py --root D:\\path\\EVO-PLAYER-PS5 --apply    # 真装

三步：
  1. 拷 i18n-zh/ 到 <root>/i18n-zh/
  2. 在 projects/evoplayer/Makefile 的 `C_SRCS :=` 之后插入
     `include i18n-zh/i18n-zh.mk`
  3. 调 apply_zh_patch.py 把界面字面量包成 evo_tr("...")

不加 --apply 时一切都只打印，不落盘。
"""
import argparse
import os
import re
import shutil
import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SRC_FOLDER = os.path.join(REPO, 'i18n-zh')
MARKER = 'include i18n-zh/i18n-zh.mk'


def find_makefile(root):
    p = os.path.join(root, 'projects', 'evoplayer', 'Makefile')
    return p if os.path.isfile(p) else None


def makefile_plan(mf):
    """返回 (新内容, 动作说明)；无法自动处理时抛 SystemExit。"""
    with open(mf, encoding='utf-8', errors='replace', newline='') as f:
        text = f.read()
    if MARKER in text:
        return text, '已包含 include，跳过'
    lines = text.splitlines(keepends=True)
    for i, line in enumerate(lines):
        if re.match(r'^\s*C_SRCS\s*:=', line):
            lines.insert(i + 1, MARKER + '\n')
            return ''.join(lines), '在第 %d 行（C_SRCS :=）之后插入 include' % (i + 1)
    raise SystemExit(
        '没找到 `C_SRCS :=` 行，请手动把下面这行加到 projects/evoplayer/Makefile\n'
        '（位置要在 C_OBJS := $(C_SRCS:.c=.o) 之前）：\n\n    ' + MARKER)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', required=True, help='EVO-PLAYER-PS5 仓库根目录')
    ap.add_argument('--apply', action='store_true', help='真正写入（默认只预演）')
    ap.add_argument('--force', action='store_true', help='覆盖已存在的 i18n-zh/')
    args = ap.parse_args()

    root = os.path.abspath(args.root)
    mf = find_makefile(root)
    if not mf:
        raise SystemExit('这不是 EVO Player 仓库根目录（找不到 projects/evoplayer/Makefile）：' + root)
    if not os.path.isdir(SRC_FOLDER):
        raise SystemExit('补丁源目录缺了：' + SRC_FOLDER)

    dst = os.path.join(root, 'i18n-zh')
    if os.path.exists(dst) and not args.force:
        copy_note = 'i18n-zh/ 已存在，跳过复制（要覆盖加 --force）'
    else:
        copy_note = '复制 i18n-zh/ 到 ' + dst
        if args.apply:
            shutil.copytree(SRC_FOLDER, dst, dirs_exist_ok=True)

    new_text, mf_note = makefile_plan(mf)
    if args.apply and new_text:
        with open(mf, 'w', encoding='utf-8', newline='') as f:
            f.write(new_text)

    print('根目录 :', root)
    print('1. 拷贝 :', copy_note)
    print('2. 编译 :', mf_note, '(' + mf + ')')

    tsv = os.path.join(dst, 'lang', 'zh-CN.tsv')
    if not args.apply:
        tsv = os.path.join(SRC_FOLDER, 'lang', 'zh-CN.tsv')   # 预演时源目录还没拷过去
    cmd = [sys.executable, os.path.join(HERE, 'apply_zh_patch.py'),
           '--root', root, '--tsv', tsv,
           '--report', os.path.join(dst, 'zh_patch_report.txt'),
           '--diff', os.path.join(dst, 'zh_patch.diff')]
    if args.apply:
        cmd.append('--apply')
    print('3. 包裹 :', ' '.join(cmd))
    if not args.apply:
        print('\n预演完成，什么都没写。确认无误后加 --apply。')
        return
    subprocess.run(cmd, check=True)
    print('\n装好了。接下来：')
    print('    cd', root, '&& ./scripts/package-app.sh --ffpfsc')
    print('（不要直接 make，打包脚本才会生成 .ffpfsc）')


if __name__ == '__main__':
    main()
