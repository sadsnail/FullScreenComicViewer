# -*- coding: utf-8 -*-
"""看图应用常量：图片扩展名、SDL 物理键、UI 尺寸与颜色等。"""

IMAGE_EXT = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}

# SDL2 物理键 scancode（与输入法无关），用于中文 IME 下快捷键仍生效
SCAN_F = 9   # SDL_SCANCODE_F
SCAN_B = 5   # SDL_SCANCODE_B
SCAN_H = 11  # SDL_SCANCODE_H

# 目录选择界面
LINE_HEIGHT = 44
PADDING = 24
COLOR_BG = (30, 30, 36)
COLOR_TITLE = (180, 180, 180)
COLOR_ROW_SEL = (70, 70, 90)
COLOR_ROW_BORDER = (120, 120, 140)
COLOR_TEXT_SEL = (240, 240, 240)
COLOR_TEXT = (200, 200, 200)
COLOR_HAS_IMAGE = (180, 230, 180)
COLOR_FAVORITE = (220, 210, 150)

# 看图界面
HINT_DURATION_MS = 2000
HINT_FADE_MS = 500
IMAGE_CACHE_MAX = 3
