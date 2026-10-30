# EVO Player（简体中文版）

**面向已越狱 PlayStation 5 的原生媒体播放器。**

可从 U 盘、内部存储、网络共享（FTP）、直播电视（IPTV / M3U）以及媒体服务器（Emby、Jellyfin、Stremio）播放视频。视频由主机自带的硬件解码器解码，最高 4K、10 位 HDR 与 Dolby Vision；界面通过裸机 `sceAgc` 直接在 GPU 上绘制；一切围绕 DualSense 手柄和大屏幕从零设计。

> 本文是 [EVO-PLAYER-PS5](https://github.com/sainsaji/EVO-PLAYER-PS5) 官方英文 README 的简体中文翻译，并附带中文界面补丁。原项目使用 **GPL-3.0-or-later** 许可。

**[下载最新版本](https://github.com/sainsaji/EVO-PLAYER-PS5/releases/latest)** · **[从 ProsperoStore 安装](https://github.com/blackbearreloaded/ProsperoStore)** · **[加入 Discord](https://discord.gg/MyNnCWNU5)**

---

## v0.13.0 更新内容

- **应用内更新器：** 侧边卡片提示新版本，下载并校验后一次重命名完成安装，然后关闭 EVO。
- **章节：** L1 / R1 在章节间跳转，进度条显示章节刻度，R3 打开章节选择器。OSD 会显示视频结束时间与剩余时间。
- **音量增强、音频延迟与网络缓冲：** 新增设置项，另有播放诊断面板，显示 HDR、音频输出与丢帧情况。
- **每个影视源都有内容架：** Jellyfin、Emby、Stremio、Nuvio、Plex 共用一套主页布局，带详情区（简介、评分、演员）以及 Xtream 电视指南。
- **更好的选择器与键盘：** 流与音轨选择器带胶囊标签和详情卡；原生风格虚拟键盘；PGS 图形字幕；每个设置项都有预览卡。
- **修复：** 硬件 VP9 Profile 2、无静音的 AAC、低帧率视频播放速度、手柄拖动进度总能提交。
- **滚动更新日志：** 右摇杆可滚动应用内的长篇更新说明。

完整说明：[CHANGELOG.md](https://github.com/sainsaji/EVO-PLAYER-PS5/blob/main/CHANGELOG.md)。

### v0.12.5 亮点

- **原生 Plex 集成：** 通过 `plex.tv/link` 的 PIN 码关联、局域网服务器自动发现、原生媒体库/剧集浏览、直连流播放、时间线已看状态回传。
- **多 U 盘与 M.2 硬盘：** 识别 `/mnt/usb0`–`/mnt/usb7` 与 `/mnt/ext0`–`/mnt/ext1`；接入多个硬盘时显示硬盘选择器，并支持跨盘搜索。
- **键盘光标导航：** L1、R1 移动 UTF-8 安全的光标，可原地编辑而不清空整行。
- **主页直接播放影视源内容：** 可从主页继续播放影视源内容，背景图与海报封面异步解码。
- **本地 Nuvio 应用：** Nuvio 网页应用直接打包进安装包（`local:nuvio`），离线可用，不依赖外部站点。
- **泰语字幕与 CJK 回退：** 内嵌 Noto Sans Thai 字体用于字幕渲染，并支持从 `/data/evoplayer/fonts/` 运行时加载 CJK 字体。

完整说明：[CHANGELOG.md](https://github.com/sainsaji/EVO-PLAYER-PS5/blob/main/CHANGELOG.md)。

### v0.12.0 亮点

- **音频直通：** 设置 → 音频 → `AUDIO PASSTHROUGH` 将 Dolby Digital、Dolby Digital Plus（含 Atmos）、DTS 与 AAC 原封不动经 HDMI 送出，由回音壁或功放解码。Dolby TrueHD 作为实验选项提供。
- **用手机输入文字：** 同一网络下可用手机浏览器发送服务器地址、播放列表 URL 与插件链接。键盘上会显示要打开的网址，无需安装任何应用。
- **Stremio 插件：** 由 “Addons” 更名，每个已保存插件都有 `Remove` 行，地址可省略 `http://`。
- **匹配视频帧率（实验性）：** 向显示设备请求视频自身帧率，12.70 固件上播放电影时可回退到 119.88 Hz。

### v0.11.0 亮点

- **直播电视与 IPTV：** 插入含 M3U 播放列表的 U 盘或输入 URL。完整频道指南与 XMLTV EPG（NOW / NEXT）、2×4 频道台标网格、L1/R1 快速翻页、Xtream Codes 账户。
- **媒体服务器（Emby、Jellyfin、Stremio）：** EVO 原生界面提供媒体库、海报墙、季、集与继续观看；支持 Jellyfin Quick Connect 与多版本流选择。
- **实时 AI 超分：** 4K 以下媒体实时超分，可用 AMD FSR 1 空间锐化（`Sharp`）或 Anime4K 卷积神经网络（`AI` — Standard、Large，PS5 Pro 可用 Maximum）。
- **Dolby Vision Profile 5 与 AV1：** 在 GPU 上依据 RPU 重塑色彩，色调映射更准确；AV1 硬件/软件解码最高 4K 10 位。
- **环绕声工作室与 DualSense 自动校准：** 可交互 2.5D 声场与声球导航、独立 5.1 / 7.1 线性 PCM 输出，并用 DualSense 手柄麦克风做房间声学校准。
- **内置文件管理器与完整 FTP 支持：** 在任意文件或文件夹上按 Options 可复制、移动、重命名（屏幕虚拟键盘）或删除，实时显示传输速度（MB/s）与剩余时间。支持**自动识别 PS5 内部 FTP 服务**（`127.0.0.1:2121`）、高速回环文件代理，并可从侧边栏直接挂载远程 FTP/NAS 共享。
- **字幕与自动同步：** 语音声学自动同步、双字幕轨并行（主字幕在底部、副字幕在顶部）、用手柄触控板滑动即时调整时间轴。
- **120 Hz 输出与运动平滑：** HDMI 2.1 120 Hz 输出让 24 fps 电影获得无抖动的 5:5 pulldown，另有实验性 24 → 60 fps GPU 运动平滑。

---

## 安装

EVO Player 是**游戏类应用模块**（`PPSA99039`），以单个 `.ffpfsc` 镜像安装，从 **Games** 行启动，和其他游戏一样。

### 前提条件

- 已越狱的 PS5，固件**低于 13.60**；开发与测试基于 12.70。
- 主机上安装 **ShadowMountPlus**，用于挂载和管理应用镜像。
- 主机上有 FTP 服务（常见越狱载荷会在 `2121` 端口提供）。
- *（U 盘播放）* 一块 **exFAT** 或 **FAT32** 格式的 U 盘，插在 `/mnt/usb0`。

### 最简单：从 ProsperoStore 安装

**[ProsperoStore](https://github.com/blackbearreloaded/ProsperoStore)** 是 [homebrew.page](https://homebrew.page) 目录的原生 PS5 应用商店，可在主机上直接安装并更新 EVO Player，无需电脑、无需 FTP。在商店里找到 EVO Player，安装，然后从 **Games** 行启动。

### 手动安装步骤

1. 从最新 **[GitHub Release](https://github.com/sainsaji/EVO-PLAYER-PS5/releases/latest)** 下载 **`PPSA99039.ffpfsc`**。
2. 通过 FTP 复制到主机的 `/data/homebrew/`。
3. ShadowMountPlus 会在文件变化时挂载并自动启动；否则从 **Games** 行启动 **EVO Player**。

> [!IMPORTANT]
> **安装新版本前请先关闭 EVO。** 应用槽会常驻，若在运行中的实例下面替换镜像——或在已有实例上再叠一次启动——可能导致主机崩溃。请用 **QUIT EVO**（侧边导航栏或 **设置 → 系统与诊断**）释放解码器和 GPU，然后从切换器关闭。

---

## 功能

### 硬件视频解码、HDR 与 Dolby Vision

视频由主机自带的 `sceVideodec2` 硬件解码器解码——**H.264、HEVC 与 VP9，最高 4K**——启动时为每种编解码器各建一个常驻解码器。超出硬件限制的片源会自动回退到 FFmpeg。

- **10 位 HDR（HDR10 / PQ 与 HLG）：** 由硬件解码器处理。**设置 → 视频与显示 → HDR OUTPUT** 决定呈现方式：**Auto** 跟随显示设备，**Off** 用 BT.2390 曲线做 SDR 色调映射（BT.2020 → BT.709）。
- **Dolby Vision Profile 5：** 依据 RPU 数据在 GPU 上重塑正确的 IPT 色彩，消除洋红/绿色偏色。
- **AV1 支持：** 通过优化的 libdav1d 解码 AV1，最高 4K 10 位。

#### 视频编码

| 编码 | 解码器 | 上限 | 已验证 |
|---|---|---|---|
| **HEVC / H.265 Main（8 位）** | 硬件（`sceVideodec2`） | 4K 60fps 实时 | 是 |
| **HEVC Main 10（HDR10 与 HLG）** | 硬件（`sceVideodec2`） | 4K 60fps 实时 | 是 |
| **Dolby Vision Profile 5** | 硬件 + GPU 色调映射 | 4K 60fps 实时 | 是 |
| **H.264 / AVC High** | 硬件（`sceVideodec2`） | 4K 30fps / 1080p 60fps | 是 |
| **VP9 Profile 0 与 Profile 2** | 硬件（`sceVideodec2`） | 4K（Profile 0）/ 1080p（Profile 2） | 是 |
| **AV1（10 位）** | 软件（libdav1d） | 4K 实时 | 是 |
| **MPEG-2、MPEG-4 Part 2、VC-1** | 软件 | 1080p | 是 |

#### 音频编码与环绕输出

多声道片源解码为独立的 **线性 PCM 5.1 与 7.1** 经 HDMI 输出，或干净地下混为立体声，供耳机和电视扬声器使用。

| 编码 | 解码器 | 声道 | 已验证 |
|---|---|---|---|
| **线性 PCM** | 硬件 / 直通 | 2.0、5.1、7.1 独立声道 | 是 |
| **Dolby TrueHD** | 软件解码 | 5.1、7.1 | 是 |
| **Dolby Digital（AC-3）与 E-AC-3** | 软件解码 | 5.1、7.1（Atmos bed） | 是 |
| **DTS-HD Master Audio 与 DTS 核心** | 软件解码 | 5.1、7.1 | 是 |
| **DTS:X（bed）** | 软件解码 | 7.1.4 | 是 |
| **FLAC 与 ALAC** | 软件解码 | 最高 192 kHz / 24 位（5.1、7.1） | 是 |
| **AAC / AAC-LATM / MP3 / Opus** | 软件解码 | 立体声与多声道 | 是 |

---

### 实时 AI 超分

4K 以下的内容都可以用主机计算着色器实时超分：

- **Sharp（AMD FSR 1）：** 边缘自适应方向性空间重建滤镜，开销极低（约 1.2 ms/帧），适合广播电视、体育与实拍电影。
- **AI（Anime4K 神经网络）：** 在 GPU 上实时运行的深度卷积神经网络（CNN）推理，重建锐利线条与细腻纹理。
  - **Standard：** 均衡的神经网络处理，开销最小。
  - **Large：** 多轮精修，适合动画和干净的数字内容。
  - **Maximum：** 极致的多级网络推理（为 PS5 Pro 优化）。

在 **设置 → 视频与显示 → 超分辨率** 中选择引擎。播放时 OSD 会显示实时标记确认。

---

### 直播电视与 IPTV

直播 IPTV 播放完整集成在 EVO 原生界面中：

- **自动发现 M3U：** 把 `iptv.m3u` 放到 U 盘，EVO 会自动找到；也可指定远程 URL。
- **XMLTV 频道指南：** 电子节目指南（EPG）显示当前（`NOW`）与即将播出（`NEXT`）的节目表，并带频道台标。
- **导航：** 2×4 台标网格，L1 / R1 快速翻页，实时搜索。
- **Xtream Codes API：** 原生支持直播、点播（VOD）与剧集分类账户。
- **直播切换台：** 播放中按 **R2** 可即时更换视频流、画质版本或音轨。

---

### 媒体服务器：Emby、Jellyfin 与 Stremio

无需离开原生界面即可连接媒体服务器：

- **原生媒体库：** 海报墙、继续观看、电视剧、季与集进度跟踪；已看状态与播放位置会回传服务器。
- **Jellyfin Quick Connect：** 用 6 位码即时登录，不必用手柄输入密码。
- **局域网发现：** 自动找到本地网络中的 Emby 与 Jellyfin 服务器。
- **多版本选择器：** 若电影或剧集有多个版本（如 4K HDR Remux、1080p SDR、Web-DL），EVO 让你选择播放哪一个。
- **内嵌网页视图：** 在导航栏旁快速打开 Emby、Jellyfin 与 Nuvio 网页。

---

### 环绕声工作室与 DualSense 自动校准

2.5D 可视化声场（**设置 → 音频 → 环绕声测试**），用于配置并测试多声道扬声器布局：

- **可交互声场：** 可用摇杆、触控板或方向键自由漫游的 3D 声球。
- **实时 VU 表与测试音：** 各声道独立发声：`FL`、`FC`、`FR`、`LFE`、`SL`、`SR`、`BL`、`BR`。
- **DualSense 麦克风自动校准：** 把手柄放在主要聆听位置，EVO 依次发出扫频声。手柄麦克风阵列采集房间脉冲响应，据此计算：
  - 精确的扬声器距离补偿（厘米 / 毫秒）。
  - 亚毫秒级的相位到达对齐。
  - 各声道增益响度平衡。
- **干净的立体声下混：** 在 **设置 → 音频 → 输出声道** 下把 5.1 与 7.1 内容相位准确地折叠为 2.0 立体声。

---

### 文件操作与 FTP 网络存储

在 PS5 上直接管理存储，原生文件操作与 FTP 集成：

- **文件管理器：** 在任意文件或文件夹上按 **OPTIONS**，可复制、剪切、粘贴、重命名（屏幕虚拟键盘）、删除或新建文件夹。
- **异步传输：** 文件操作在独立后台线程执行，实时显示传输速度（MB/s）、已复制字节与剩余时间。
- **即时筛选胶囊：** 在首行按 **上**，无需重新扫描硬盘即可按视频、音频、图片筛选当前文件夹。
- **自动识别 PS5 内部 FTP：** EVO Player 自动检测并连接主机上常驻的越狱 FTP 载荷（回环 `127.0.0.1:2121`），在浏览器侧边栏预置为 **PS5 Local FTP**，无需输入 IP 或凭据即可浏览和管理整个主机文件系统（`/`）。
- **高速回环代理：** 大于 64 MB 的内部文件传输会自动经回环 FTP 守护进程转发，绕过单进程写入限速，跑满硬盘速度（约 80+ MB/s）。
- **远程 FTP / NAS 挂载：** 在侧边栏添加家庭网络中的远程 FTP 服务器，可直接播放媒体，或在电脑/NAS 与主机间传文件，不必离开沙发。

---

### 字幕与音频自动同步

- **实验性音频自动同步：** 实时分析对白音频，计算声学时间偏移并自动同步字幕轨。
- **双字幕并行：** 同时显示两种语言——主字幕在屏幕底部，副字幕在顶部。
- **触控板实时微调：** 播放中在 DualSense 触控板上横向滑动或左右点击（或按 **L2**），以 ±50 ms 步进微调时间轴，无需暂停。
- **广泛格式支持：** 带完整样式与定位的 ASS / SSA、SRT、SubRip 与 WebVTT。

---

### 120 Hz 输出与运动平滑

- **120 Hz 高帧率（HDMI 2.1）：** 为 24.000 / 23.976 fps 电影提供干净的 5:5 pulldown，消除 3:2 pulldown 抖动。选项：关闭、自动、仅播放时，位于 **设置 → 视频与显示**。
- **实验性运动平滑：** 在 GPU 上实时合成 24 → 60 fps 插帧，位于 **设置 → 实验性**。

---

### GPU 渲染界面（`sceAgc`）

整个用户界面通过裸机 `sceAgc` 以面板原生分辨率在 GPU 上渲染：

- 锁定 60 fps 导航，帧时间极低。
- 仅状态变化时重绘，空闲 GPU 负载接近零。
- 内置五套配色主题（Midnight、Carbon、Ember、Aurora），并支持 U 盘自定义主题（`/mnt/usb0/evo_themes`）。

---

## 按键速查

| 按键 | 菜单与文件浏览器 | 播放中 | 屏幕键盘 |
|---|---|---|---|
| **CROSS ✕** | 选择 / 打开 | 播放 / 暂停 | 输入字符 |
| **CIRCLE ○** | 返回 | 停止播放（有确认） | 取消 |
| **TRIANGLE △** | 切换收藏 / 网页视图 | 循环切换画面比例（适应 / 填充 / 拉伸） | 空格 |
| **SQUARE □** | 文件详情 / 影视源设置 | 媒体信息（编码、分辨率、解码器） | 退格 |
| **OPTIONS** | 文件操作（复制、移动、重命名、删除） | 播放设置菜单 | 完成 |
| **方向键 / 左摇杆** | 移动焦点，长按滚动 | 拖动进度条（长按高速） | 在按键间移动（首行向上：清除 X） |
| **左** | 打开导航栏 | — | — |
| **上** | 即时文件夹筛选胶囊 | 切换 OSD 叠加层 | — |
| **下** | — | 打开字幕轨选择器 | — |
| **L1 / R1** | 上翻页 / 下翻页 | 章节跳转 / ±60 秒跳转 | 光标左移 / 右移 |
| **L2 / R2** | 按字母跳转（A–Z） | **L2：** 字幕同步 ±50ms<br>**R2：** 直播画质与音轨选择 | **L2：** Shift（再按：Caps Lock）<br>**R2：** 完成 |
| **触控板滑动** | — | 实时字幕同步偏移微调 | — |
| **L3 / R3** | 截图保存到 `/mnt/usb0` | 截图 | — |

---

## 从源码构建

在固定版本的 Docker 工具链内构建：

```bash
git clone --recursive https://github.com/sainsaji/EVO-PLAYER-PS5
cd EVO-PLAYER-PS5
echo "PS5_HOST=192.168.0.10" > .env      # 你的主机 IP

docker compose build
```

打包并部署应用模块：

```bash
docker compose run --rm ps5-dev bash -lc '
  ./scripts/package-app.sh --ffpfsc
  ./scripts/deploy-app.sh --ffpfsc'
```

*注意：`deploy-app.sh` 更新前需要先关闭 EVO。若应用槽已清空，可加 `--force`。*

无需硬件，在电脑上渲染界面预览：

```bash
./tools/uiview.sh --all                  # 输出到 output/uiview/
./tools/uiplay.sh                        # 所有屏幕的缩略图拼版
```

运行测试：

```bash
docker compose run --rm ps5-dev ./tests/run_tests.sh
```

---

## 文档

| 文档 | 用途 |
|---|---|
| [docs/README.md](https://github.com/sainsaji/EVO-PLAYER-PS5/blob/main/docs/README.md) | 以下所有文档的索引 |
| [docs/build/building.md](https://github.com/sainsaji/EVO-PLAYER-PS5/blob/main/docs/build/building.md) | 构建环境、SDK、FFmpeg、着色器 |
| [docs/build/packaging.md](https://github.com/sainsaji/EVO-PLAYER-PS5/blob/main/docs/build/packaging.md) | 打包应用模块并部署 |
| [docs/console/hardware-cycle.md](https://github.com/sainsaji/EVO-PLAYER-PS5/blob/main/docs/console/hardware-cycle.md) | 在主机上安全运行构建 |
| [docs/architecture/architecture.md](https://github.com/sainsaji/EVO-PLAYER-PS5/blob/main/docs/architecture/architecture.md) | 核心架构与模块边界 |
| [docs/hardware/codec-support.md](https://github.com/sainsaji/EVO-PLAYER-PS5/blob/main/docs/hardware/codec-support.md) | 编码、封装与硬件解码矩阵 |
| [docs/hardware/video-decode.md](https://github.com/sainsaji/EVO-PLAYER-PS5/blob/main/docs/hardware/video-decode.md) | 通过 `sceVideodec2` 硬件解码 |
| [docs/hardware/agc-runtime.md](https://github.com/sainsaji/EVO-PLAYER-PS5/blob/main/docs/hardware/agc-runtime.md) | 裸机 `sceAgc` GPU 渲染 |
| [docs/ui/hui-kit.md](https://github.com/sainsaji/EVO-PLAYER-PS5/blob/main/docs/ui/hui-kit.md) | 界面：EVO 基于 ps5-homebrew-ui 的屏幕 |
| [docs/ui/settings.md](https://github.com/sainsaji/EVO-PLAYER-PS5/blob/main/docs/ui/settings.md) | 每一项设置 |
| [docs/providers/architecture.md](https://github.com/sainsaji/EVO-PLAYER-PS5/blob/main/docs/providers/architecture.md) | 网络影视源与运行时 UI 包 |
| [docs/ui/theming.md](https://github.com/sainsaji/EVO-PLAYER-PS5/blob/main/docs/ui/theming.md) | 主题令牌与 `.theme` 格式 |
| [CHANGELOG.md](https://github.com/sainsaji/EVO-PLAYER-PS5/blob/main/CHANGELOG.md) | 完整版本历史 |

---

## 社区

问题、Bug 报告、功能请求与早期测试版：加入 **[EVO Player Discord](https://discord.gg/MyNnCWNU5)**。0.11.0 的许多功能最初都来自那里的请求。

---

## 致谢与许可

由 KINGDKAK 的 [ProsperoPlayer](https://github.com/KINGDKAK/ProsperoPlayer) 派生，采用 **GPL-3.0-or-later** 许可（见 [COPYRIGHT.md](https://github.com/sainsaji/EVO-PLAYER-PS5/blob/main/COPYRIGHT.md)）。

如果 EVO 对你的项目有帮助，欢迎在致谢中提及：这是请求，不是许可条件。

- [ps5-payload-dev](https://github.com/ps5-payload-dev)（John Törnblom）——SDK 与工具链
- [KINGDKAK](https://github.com/KINGDKAK)——ProsperoPlayer
- [zecoxao/sce_symbols](https://github.com/zecoxao/sce_symbols)——NID 符号数据库
- [BlackBearReloaded](https://github.com/blackbearreloaded)——[ps5-homebrew-ui](https://github.com/blackbearreloaded/ps5-homebrew-ui)，EVO 界面所基于的 UI 套件
- [mihawk-99](https://github.com/mihawk-99)——[PS5_VulkanTemplate](https://github.com/mihawk-99/PS5_VulkanTemplate)，EVO 应用模块使用了它的 [1 GiB 弹性内存改动](https://github.com/mihawk-99/PS5_VulkanTemplate/commit/04aa411deb9d9d12b40cc2afb479a328394da4ca)
- PS5 开发者 **Philow**、**sword** 与 **0xManuel**——感谢他们的帮助与研究

*EVO Player 是独立自制软件，与 Sony Interactive Entertainment 无关联、未获其认可或赞助。所有 PlayStation 商标归其各自所有者。*
