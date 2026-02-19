# Kantu — User Manual

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
