# EVO Player 简体中文补丁

给 [EVO-PLAYER-PS5](https://github.com/sainsaji/EVO-PLAYER-PS5)（PS5 越狱主机原生媒体播放器）做的简体中文化补丁：**一个 `i18n-zh/` 文件夹，拷进源码树、加一行 include，重新编译就是中文界面。**

> 官方的 `PPSA99039.ffpfsc` 是编译好的只读镜像，文本常量已经固化在二进制里，**没法对安装包打补丁**。中文界面必须带着本补丁重新编译一次——本仓库提供的就是这次编译所需的全部材料。

## 文件夹模式集成

### 一条命令（推荐）

```bash
git clone https://github.com/sainsaji/EVO-PLAYER-PS5
cd EVO-PLAYER-PS5
python <这个仓库>/tools/install.py --root . --apply
./scripts/package-app.sh --ffpfsc
```

`install.py` 会做三件事：拷 `i18n-zh/` 到源码根目录、在 `projects/evoplayer/Makefile` 里插入 `include i18n-zh/i18n-zh.mk`、把界面英文字面量包成 `evo_tr("…")`。不加 `--apply` 时全部只预演，不落盘。

### 手动三步（等价）

1. **拷文件夹**：把整个 `i18n-zh/` 放到 EVO 源码根目录，和 `projects/` 同级。

   ```
   EVO-PLAYER-PS5/
   ├── projects/evoplayer/Makefile
   └── i18n-zh/            <- 拷到这里
       ├── i18n-zh.mk
       ├── include/evo_i18n.h
       ├── src/evo_i18n.c
       ├── src/evo_i18n_table.inc
       └── lang/zh-CN.tsv
   ```

2. **加一行 include**：编辑 `projects/evoplayer/Makefile`，在 `C_SRCS := $(PP_SRCS) $(UI_SRCS) $(MEDIA_SRCS) $(ADDON_SRCS)` 这行**之后**、`C_OBJS := $(C_SRCS:.c=.o)` **之前**插入：

   ```make
   include i18n-zh/i18n-zh.mk
   ```

   位置不能错：`i18n-zh.mk` 会把 `i18n-zh/src/evo_i18n.c` 追加进 `C_SRCS` 并加 `-Ii18n-zh/include`，而 `C_OBJS` 是由 `C_SRCS` 推导出来的——插晚了 `evo_i18n.o` 不会进链接，报未定义符号 `evo_tr`。

3. **包裹界面文案并打包**：

   ```bash
   python <这个仓库>/tools/apply_zh_patch.py --root . \
          --tsv i18n-zh/lang/zh-CN.tsv --apply
   ./scripts/package-app.sh --ffpfsc
   ```

   产物 `PPSA99039.ffpfsc` 装到主机 `/data/homebrew/`，先退出正在运行的 EVO，再从 **Games** 行启动。

> 不要直接 `make`。EVO 的 Makefile 只产出 ELF，`.ffpfsc` 要由仓库根目录的 `scripts/package-app.sh --ffpfsc` 生成。

## 目录

| 路径 | 内容 |
| --- | --- |
| `i18n-zh/` | **要拷进源码树的文件夹**：翻译层源码 + Makefile 片段 + 词表 |
| `i18n-zh/include/evo_i18n.h` | 翻译入口（`evo_tr` / `evo_i18n_load` / `evo_i18n_enabled`） |
| `i18n-zh/src/evo_i18n.c` | 实现：FNV-1a 哈希索引 + 线性探测，纯 C11，内置表 + 运行时覆盖 |
| `i18n-zh/src/evo_i18n_table.inc` | 由 TSV 生成的 1171 条内置词表 |
| `i18n-zh/lang/zh-CN.tsv` | **1171 条**界面文案，`英文<TAB>中文`，`#` 开头为注释 |
| `i18n-zh/i18n-zh.mk` | Makefile 片段（`C_SRCS`、`CFLAGS`、`CXXFLAGS`） |
| `tools/install.py` | 一条命令完成拷文件夹 + 改 Makefile + 包裹 |
| `tools/apply_zh_patch.py` | 把界面字面量包成 `evo_tr("…")`，默认 dry-run |
| `tools/gen_table.py` | TSV → `evo_i18n_table.inc` |
| `patches/zh_patch.diff` | 在 v0.13.0 的 34 文件源码镜像上生成的统一 diff（575 处 / 24 文件） |
| `patches/zh_patch_report.txt` | 每个文件的包裹数量 |
| `patches/miss_report.txt` | 命中词表但没自动包裹的位置（`文件:行号: 文案`），供人工复核 |
| `docs/集成说明.md` | 编译侧的完整说明：接入、再生成词表、运行时覆盖、回滚、自检清单 |
| `docs/中文使用手册.md` | 装好中文版之后怎么看：安装、导航、按键速查、六大设置分组、CJK 字体、FAQ |
| `docs/术语表.md` | 统一译法：按键名、界面、播放、影视源、设置分组标题、保留原文的品牌词、占位符规则 |
| `docs/README.zh-CN.md` | 上游 README 的完整中译（v0.13.0 更新说明、安装、编码支持、按键表、构建） |

## 效果与验证

- **词表**：1327 条原始候选 → 剔除 156 条噪声（类名、JSON 键、HTTP 头、日志、语言代码）→ **1171 条**真实界面文案。4 批并行翻译后校验：英文列逐字符一致、占位符集合一致、合并去重 0 冲突。
- **包裹**：`575 处 / 24 个文件`。逐文件复查：注释内误包 0、引号失衡 0、词表未命中 0、比较/日志误包 0。`"POST"`、`"DELETE"`、`"TimeUpdate"`、`"Transcode"` 这类协议值全部未被包裹。
- **翻译层**：内置表 + `/data/evoplayer/lang/zh-CN.tsv` 运行时覆盖；查不到就原样返回英文，不会出现空白或崩溃。
- **集成自测**：在干净源码镜像上跑 `tools/install.py --apply`，得 575 处、Makefile 插入位置正确、`evo_i18n.o` 进 `C_SRCS`。

## 覆盖范围

- **已覆盖**：导航栏、主页、文件浏览器、播放 OSD、各选择器、设置六大分组、影视源（Emby / Jellyfin / Plex / Stremio / Nuvio / IPTV）、关于与诊断、对话框与提示。
- **部分覆盖**：`addons/` 协议层中少量用户可见提示保持英文（该目录里 API 枚举值太多，自动包裹不安全）。
- **未覆盖**：`ui_rml/`（61 MB 内嵌 RmlUi 旧界面资源包）。只有把 `/mnt/usb0/evo_no_hui` 放上去切回旧界面时才可见。

补齐手段：按 `miss_report.txt` 手工包 `evo_tr()`；或者不改代码，直接把补充译文写进主机 `/data/evoplayer/lang/zh-CN.tsv`，改完重启 EVO 即生效。

## 中文字体

界面与字幕显示中文需要 CJK 字形：把中文字体（建议 Noto Sans SC，OFL 许可）放到主机 `/data/evoplayer/fonts/` 后重启。EVO 自带的 `noto-fallback.huifont` 会与它一起做字形回退，缺字体时会显示方块。

## 许可与致谢

- 补丁与文档按 **GPL-3.0-or-later** 发布，与上游保持一致；上游基于 ProsperoPlayer。
- 上游作者：[sainsaji/EVO-PLAYER-PS5](https://github.com/sainsaji/EVO-PLAYER-PS5)。
- 本仓库只新增翻译层与包裹改动，不修改第三方子模块，不内置任何上游二进制。
