# -*- coding: utf-8 -*-
"""目录选择界面：事件循环、绘制、按键/鼠标处理；使用 dir_loader 异步加载，加载中显示动画。"""

import os

import pygame
import config
from constants import (
    COLOR_BG,
    COLOR_FAVORITE,
    COLOR_HAS_IMAGE,
    COLOR_ROW_BORDER,
    COLOR_ROW_SEL,
    COLOR_TEXT,
    COLOR_TEXT_SEL,
    COLOR_TITLE,
    LINE_HEIGHT,
    PADDING,
    SCAN_B,
    SCAN_F,
)
import i18n
from dir_loader import DirLoader


def _key_physical(event, key_constant, scancode):
    """判断是否为指定物理键，避免中文输入法下 event.key 被 IME 占用。"""
    if event.key == key_constant:
        return True
    return getattr(event, "scancode", None) == scancode


def run_dir_selector(screen, base_dir, favorites):
    """空格=进入目录 回车=进入播放 退格=上一级 F=收藏 B=收藏夹；返回 (selected_path) 或 None。"""
    w, h = screen.get_size()
    font = pygame.font.SysFont("microsoftyahei,simhei,arial", 28)
    title_font = pygame.font.SysFont("microsoftyahei,simhei,arial", 22)
    current_root = base_dir
    favorites_mode = False
    sel = 0
    choices = None
    clock = pygame.time.Clock()
    last_click_row = -1
    last_click_time = 0
    loader = DirLoader()
    loader.start_load(base_dir, current_root, favorites_mode, favorites)

    while True:
        title = (
            i18n.t("dir.title_favorites", "收藏夹 — 回车 播放  空格 进入目录  退格 退出收藏夹  ESC 退出")
            if favorites_mode
            else i18n.t("dir.title", "空格 进入目录  回车 进入播放  退格 上一级  F 收藏  B 收藏夹  ESC 退出")
        )
        title_surf = title_font.render(title, True, COLOR_TITLE)
        title_rect = title_surf.get_rect(midtop=(w // 2, PADDING))
        y0 = title_rect.bottom + PADDING * 2
        # 1. 事件处理（立即响应，不等待 IO）
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None
                if event.key == pygame.K_BACKSPACE:
                    if favorites_mode:
                        favorites_mode = False
                        current_root = base_dir
                        loader.start_load(base_dir, current_root, favorites_mode, favorites)
                    elif current_root != base_dir:
                        current_root = os.path.dirname(current_root)
                        loader.start_load(base_dir, current_root, favorites_mode, favorites)
                    break
                if event.key == pygame.K_SPACE:
                    if choices and sel < len(choices):
                        path = choices[sel][1]
                        if favorites_mode:
                            if path:
                                current_root = path
                                favorites_mode = False
                            loader.start_load(base_dir, current_root, favorites_mode, favorites)
                        else:
                            current_root = path
                            loader.start_load(base_dir, current_root, favorites_mode, favorites)
                    break
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    if choices and sel < len(choices):
                        path = choices[sel][1]
                        if path:
                            return path
                    break
                if _key_physical(event, pygame.K_b, SCAN_B) and not favorites_mode:
                    favorites_mode = True
                    loader.start_load(base_dir, current_root, favorites_mode, favorites)
                    break
                if _key_physical(event, pygame.K_f, SCAN_F) and not favorites_mode and choices:
                    if sel < len(choices):
                        path = choices[sel][1]
                        if path:
                            path = os.path.normpath(path)
                            if path in favorites:
                                favorites.discard(path)
                            else:
                                favorites.add(path)
                            config.save_favorites(favorites)
                    break
                if event.key == pygame.K_UP:
                    sel = max(0, sel - 1)
                elif event.key == pygame.K_DOWN:
                    sel = min(len(choices) - 1, sel + 1) if choices else 0
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and choices:
                row_rects = _row_rects(w, y0, choices)
                for i, rect in enumerate(row_rects):
                    if rect.collidepoint(event.pos):
                        if i == last_click_row and (pygame.time.get_ticks() - last_click_time) < 400:
                            last_click_row = -1
                            path = choices[i][1]
                            if favorites_mode and path:
                                current_root = path
                                favorites_mode = False
                            else:
                                current_root = path
                            loader.start_load(base_dir, current_root, favorites_mode, favorites)
                        else:
                            sel = i
                            last_click_row = i
                            last_click_time = pygame.time.get_ticks()
                        break

        # 2. 轮询加载结果
        busy, new_choices, load_error = loader.get_state()
        if not busy and new_choices is not None:
            if not favorites_mode and len(new_choices) == 0:
                loader.consume_result()
                return None
            choices = new_choices
            loader.consume_result()
            sel = min(max(0, sel), len(choices) - 1)

        # 3. 绘制（使用本帧已算好的 title_surf / title_rect / y0）
        screen.fill(COLOR_BG)
        screen.blit(title_surf, title_rect)

        if busy or choices is None:
            _draw_loading(screen, w, h, y0)
        else:
            row_rects = _row_rects(w, y0, choices)
            for i, (label, path, has_images) in enumerate(choices):
                rect = pygame.Rect(PADDING, y0 + i * LINE_HEIGHT, w - PADDING * 2, LINE_HEIGHT)
                if i == sel:
                    pygame.draw.rect(screen, COLOR_ROW_SEL, rect)
                    pygame.draw.rect(screen, COLOR_ROW_BORDER, rect, 2)
                color = COLOR_TEXT_SEL if i == sel else COLOR_TEXT
                display_label = "  " + i18n.translate_label(label)
                path_norm = os.path.normpath(path) if path else ""
                if path and has_images:
                    display_label += "  " + i18n.t("dir.has_images", "[有图]")
                if path_norm and path_norm in favorites:
                    display_label += "  ★"
                if path and has_images and i != sel:
                    color = COLOR_HAS_IMAGE
                if path_norm and path_norm in favorites and i != sel:
                    color = COLOR_FAVORITE
                text = font.render(display_label, True, color)
                tr = text.get_rect(midleft=(rect.left + 8, rect.centery))
                screen.blit(text, tr)

        pygame.display.flip()
        clock.tick(60)


def _row_rects(w, y0, choices):
    """计算每行矩形，用于点击检测；y0 与绘制时一致。"""
    return [pygame.Rect(PADDING, y0 + i * LINE_HEIGHT, w - PADDING * 2, LINE_HEIGHT) for i in range(len(choices))]


def _draw_loading(screen, w, h, y0):
    """在列表区域绘制加载动画（旋转弧 + 文字）。"""
    import math
    center_x = w // 2
    center_y = y0 + 80
    r = 24
    t = pygame.time.get_ticks() % 1000 / 1000.0
    start_rad = t * 2 * math.pi
    end_rad = start_rad + 1.5 * math.pi
    rect = pygame.Rect(center_x - r, center_y - r, r * 2, r * 2)
    try:
        pygame.draw.arc(screen, (120, 160, 200), rect, start_rad, end_rad, 4)
    except Exception:
        pass
    load_font = pygame.font.SysFont("microsoftyahei,simhei,arial", 22)
    load_surf = load_font.render(i18n.t("dir.loading", "加载中..."), True, (180, 180, 180))
    load_rect = load_surf.get_rect(center=(center_x, center_y + r + 20))
    screen.blit(load_surf, load_rect)
