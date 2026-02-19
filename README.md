# 看图（Kantu）— 中文功能说明与使用文档

本文档描述当前「看图」应用的功能、操作方式与使用要求，可作为产品需求与用户说明使用。

---

## 1. 应用概述

- **用途**：漫画/图片全屏查看器。先选择根目录，再在目录树中浏览子文件夹，选择某个目录后进入全屏看图；支持在「目录选择」与「看图播放」之间来回切换。
- **技术**：Python + Pygame + Pillow；可打包为独立 exe 运行。
- **支持格式**：`.jpg`、`.jpeg`、`.png`、`.gif`、`.bmp`、`.webp`。

---

## 2. 启动与根目录选择

- **配置文件**：程序在自身所在目录使用 **`kantu_config.txt`** 保存上次使用的默认目录（第一行为路径）。下次启动时若该文件存在且其中路径有效，则**直接使用该目录进入**，不再弹窗。
- **无配置或配置为空/无效时**：弹出「选择漫画根目录」对话框，**必须**选择或输入目录并点「确定」才能进入；取消或关闭窗口会提示并退出程序。
  - 可直接在输入框中输入或粘贴路径（支持本地与网络映射路径，如 `Z:\`、`\\服务器\共享名`）。
  - 可点击「浏览...」用系统文件夹选择器选择目录。
  - 选择并进入后，该路径会写入配置文件，下次启动将直接使用。
- **命令行**：若启动时带一个参数且为有效目录（如 `kantu.exe D:\漫画`），仅在「需要弹窗」时作为对话框的**初始值**；有有效配置文件时不会弹窗。

---

## 3. 目录模式（文件夹列表）

进入程序后首先显示「目录选择」界面：以当前根目录为基准，列出可进入的目录与当前目录下的子文件夹。

### 3.1 列表内容

- **[上一级]**：返回父目录（当不在根目录时显示）。
- **[当前目录]**：当前目录本身（可直接回车进入播放）。
- 子文件夹：按名称排序；有图片的目录会显示 `[有图]`，已收藏的会显示 `★`。

### 3.2 按键与操作

| 按键 | 功能 |
|------|------|
| **空格** | 进入当前选中项对应的目录（进入子目录或把当前目录设为选中路径） |
| **回车** | 以当前选中目录「进入播放」，进入全屏看图 |
| **退格** | 返回上一级目录（若已在根目录则无效） |
| **F** | 收藏/取消收藏当前选中目录（写入收藏夹） |
| **B** | 进入「收藏夹」模式（仅显示收藏的文件夹列表） |
| **↑ / ↓** | 上下移动选中行 |
| **ESC** | 退出程序 |
| **鼠标** | 单击选中某行；双击某行等同「空格」进入该目录 |

### 3.3 收藏夹模式（按 B 进入）

- 按 **B** 后，列表切换为**仅显示所有已收藏的文件夹**（来自 `kantu_favorites.txt`，不存在的目录会自动过滤）。
- 在收藏夹列表中：
  - **回车**：以当前选中项**进入播放**。
  - **空格**：进入该目录（并退出收藏夹模式，回到普通目录列表）。
  - **退格**：**退出收藏夹模式**，回到进入收藏夹前的目录列表。
  - 上下键、鼠标选择与普通目录模式相同。
- 若暂无收藏，会显示「[暂无收藏]」，此时只能退格退出收藏夹或 ESC 退出程序。

### 3.4 收藏数据

- 收藏的目录保存在与程序/脚本同目录下的 **`kantu_favorites.txt`** 中，每行一个绝对路径。
- 收藏在目录模式与收藏夹模式中通用；在目录列表中可用 **F** 随时对当前选中项收藏/取消收藏。

---

## 4. 播放模式（全屏看图）

从目录模式选中某目录后按回车（或从收藏夹按回车）进入该目录的「播放」界面，全屏显示图片。

### 4.1 显示方式

- **单页模式**：一屏一图，居中显示，按比例缩放适应屏幕。
- **双页模式**：左右两页，以屏幕中线为界并排显示（漫画跨页效果）。
- **上/下方向键**：切换单页/双页；切换后会有短暂操作提示显示。

### 4.2 翻页与操作

| 按键/操作 | 功能 |
|-----------|------|
| **→ / 左键点击** | 下一页（单页+1，双页+2） |
| **← / 右键点击** | 上一页（单页-1，双页-2） |
| **H** | 开关 HDR 增强（亮度/对比度），便于高亮屏观看 |
| **Backspace** | 返回目录模式（不退出程序） |
| **ESC** | 退出程序 |

### 4.3 界面提示

- 右下角显示当前页码（如 `1 / 10` 或 `1-2 / 10`）。
- 翻页或切换单/双页后，左下角会短暂显示操作提示（约 2 秒后淡出）。

---

## 5. 运行与依赖

- **依赖**：`pygame`、`Pillow`（见 `requirements-kantu.txt`）。
- **运行**：  
  - 源码：`python kantu.py` 或 `python kantu.py "D:\某目录"`（路径为可选初始目录）。  
  - 打包后：双击 exe 或命令行 `kantu.exe [初始目录]`。
- **配置文件**：与 exe/脚本同目录的 `kantu_config.txt`（第一行默认目录，第二行可选语言代码）；**收藏文件**：`kantu_favorites.txt`，程序自动读写。
- **语言**：在 `kantu_config.txt` 第二行填写 `zh`（简体中文，默认）或 `en`（英文）可切换界面语言。英文说明见 `Kantu-User-Manual-EN.md`。

---

## 6. 功能汇总表

| 模块 | 功能要点 |
|------|----------|
| 启动 | 始终弹出根目录选择框；支持本地与网络路径；命令行参数仅作初始值 |
| 目录模式 | 子目录列表、上一级/当前目录/子文件夹、有图/收藏标记 |
| 目录操作 | 空格进入、回车播放、退格上一级、F 收藏、B 收藏夹、ESC 退出 |
| 收藏夹模式 | B 进入；仅显示收藏目录；回车播放、空格进入目录、退格退出收藏夹 |
| 播放模式 | 单页/双页、左右翻页、HDR、Backspace 回目录、ESC 退出 |
| 数据 | 默认目录 `kantu_config.txt`；收藏 `kantu_favorites.txt` |

---

*文档与当前代码行为一致，如有界面或按键变更请同步更新本文档。*

# Kantu — User Manual EN

This document describes the **Kantu** image/comic viewer: features, controls, and setup. For the Chinese version see《看图-功能与使用说明》.

---

## 1. Overview

- **Purpose**: Full-screen image/comic viewer. Choose a root folder, then browse subfolders and open a folder to view images full screen. You can switch between **folder list** and **viewer** at any time.
- **Tech**: Python + Pygame + Pillow; can be packaged as a standalone exe.
- **Formats**: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.webp`.

---

## 2. Startup and root folder

- **Config file**: The app stores the last-used root path in **`kantu_config.txt`** (first line) in the same directory as the exe/script. If this file exists and the path is valid, the app **starts directly** with that folder (no dialog).
- **No config or invalid path**: A “Choose comic root folder” dialog appears. You **must** choose or type a folder and click OK to continue; cancel closes the app.
  - You can type or paste a path (local or network, e.g. `Z:\`, `\\server\share`).
  - Or click “Browse...” to pick a folder.
  - After you confirm, the path is saved; the next start will use it without asking.
- **Command line**: You can pass a folder as the first argument (e.g. `kantu.exe D:\Comics`). It is used only as the **initial path** when the dialog is shown; it does not override an existing valid config.

### Language

- **Language** is read from the **second line** of `kantu_config.txt`.
- Set the second line to **`en`** for English, **`zh`** for Chinese (default if missing).
- Example `kantu_config.txt`:
  ```
  D:\Comics
  en
  ```

---

## 3. Folder list (directory mode)

After startup you see the **folder list**: the current root and its subfolders.

### 3.1 List contents

- **[Parent]**: Go to the parent folder (only when not at root).
- **[Current folder]**: The current folder itself (Enter = open in viewer).
- Subfolders: Sorted by name. Folders that contain images show **[Has images]**; favorites show **★**.

### 3.2 Keys and actions

| Key | Action |
|-----|--------|
| **Space** | Open the selected item (go into that folder) |
| **Enter** | Start viewing (full-screen) the selected folder |
| **Backspace** | Go up one level (no effect at root) |
| **F** | Add/remove current folder from favorites |
| **B** | Switch to **Favorites** list only |
| **↑ / ↓** | Move selection |
| **ESC** | Quit app |
| **Mouse** | Click to select; double-click = same as Space (open folder) |

### 3.3 Favorites (press B)

- **B** shows only **favorites** (from `kantu_favorites.txt`; missing folders are skipped).
- In favorites:
  - **Enter**: Start viewing the selected folder.
  - **Space**: Open that folder (and leave favorites list).
  - **Backspace**: Leave favorites, back to normal folder list.
- If there are no favorites, “[No favorites]” is shown; use Backspace or ESC.

### 3.4 Favorites data

- Favorites are stored in **`kantu_favorites.txt`** (one path per line), next to the exe/script.
- You can add/remove favorites with **F** in the folder list anytime.

---

## 4. Viewer (full-screen)

Press **Enter** on a folder to open the **viewer**: full-screen image display.

### 4.1 Display modes

- **Single page**: One image per screen, centered and scaled.
- **Dual page**: Two images side by side (split at center).
- **↑ / ↓**: Switch between single and dual page.

### 4.2 Controls

| Key / action | Effect |
|--------------|--------|
| **→ / Left click** | Next page (single +1, dual +2) |
| **← / Right click** | Previous page (single -1, dual -2) |
| **H** | Toggle HDR (brightness/contrast) |
| **Backspace** | Back to folder list (app keeps running) |
| **ESC** | Quit app |

### 4.3 On-screen info

- Bottom-right: page number (e.g. `1 / 10` or `1-2 / 10`).
- Bottom-left: Short hint after page/mode change (fades after a few seconds).

---

## 5. Run and dependencies

- **Dependencies**: `pygame`, `Pillow` (see `requirements-kantu.txt`).
- **Run**:
  - Source: `python kantu.py` or `python main.py`, optionally `python kantu.py "D:\Folder"`.
  - Packaged: run the exe, or `kantu.exe [folder]` from command line.
- **Config**: `kantu_config.txt` (path + language); **Favorites**: `kantu_favorites.txt`.

---

## 6. Quick reference

| Area | Summary |
|------|---------|
| Startup | Root folder dialog if no valid config; supports local and network paths |
| Folder list | Parent / current / subfolders; [Has images] and ★ for favorites |
| Keys | Space open, Enter view, Backspace up, F favorite, B favorites list, ESC quit |
| Favorites | B to open; Enter view, Space open folder, Backspace exit |
| Viewer | Single/dual page, ←→ page, H HDR, Backspace back, ESC quit |
| Data | Path and language in `kantu_config.txt`; favorites in `kantu_favorites.txt` |

---

*This manual matches the current app behavior. If the UI or keys change, the doc will be updated accordingly.*

