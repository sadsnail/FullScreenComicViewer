# -*- coding: utf-8 -*-
"""全屏看图：单页/双页、翻页、HDR、提示条；图片由 image_loader 提供。"""

import pygame

import i18n
from constants import HINT_DURATION_MS, HINT_FADE_MS, SCAN_H
from fs_utils import find_images
from image_loader import ImageLoader


def _key_physical(event, key_constant, scancode):
    if event.key == key_constant:
        return True
    return getattr(event, "scancode", None) == scancode


def run_manga_viewer(screen, directory, Image, ImageEnhance, err_callback=None):
    """全屏看图：左右翻页，Backspace 返回目录，ESC 退出程序。
    返回 'back' 表示返回目录，'quit' 表示退出。
    err_callback(msg) 用于显示错误（如该目录下未找到图片）。"""
    from constants import IMAGE_EXT
    image_list = find_images(directory)
    if not image_list:
        if err_callback:
            err_callback(i18n.t("viewer.no_images", "该目录下未找到图片。\n支持: ") + ", ".join(sorted(IMAGE_EXT)))
        return 'back'
    w, h = screen.get_size()
    loader = ImageLoader(screen, Image, ImageEnhance)
    hdr_on = False
    idx = 0
    display_mode = 1  # 1=单页  2=双页
    clock = pygame.time.Clock()
    hint_show_until = pygame.time.get_ticks() + HINT_DURATION_MS + HINT_FADE_MS
    margin = 20
    try:
        font = pygame.font.SysFont("microsoftyahei,simhei,arial", 22)
    except Exception:
        font = pygame.font.Font(None, 36)

    while True:
        now = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'quit'
                if event.key == pygame.K_BACKSPACE:
                    return 'back'
                if _key_physical(event, pygame.K_h, SCAN_H):
                    hdr_on = not hdr_on
                    loader.clear_cache()
                    continue
                if event.key == pygame.K_UP:
                    display_mode = 1
                    hint_show_until = now + HINT_DURATION_MS + HINT_FADE_MS
                    continue
                if event.key == pygame.K_DOWN:
                    display_mode = 2
                    hint_show_until = now + HINT_DURATION_MS + HINT_FADE_MS
                    continue
                if event.key == pygame.K_LEFT:
                    idx = max(0, idx - (2 if display_mode == 2 else 1))
                    hint_show_until = now + HINT_DURATION_MS + HINT_FADE_MS
                elif event.key == pygame.K_RIGHT:
                    idx = min(len(image_list) - 1, idx + (2 if display_mode == 2 else 1))
                    hint_show_until = now + HINT_DURATION_MS + HINT_FADE_MS
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    idx = min(len(image_list) - 1, idx + (2 if display_mode == 2 else 1))
                    hint_show_until = now + HINT_DURATION_MS + HINT_FADE_MS
                elif event.button == 3:
                    idx = max(0, idx - (2 if display_mode == 2 else 1))
                    hint_show_until = now + HINT_DURATION_MS + HINT_FADE_MS

        screen.fill((0, 0, 0))
        if display_mode == 1:
            surf = loader.get_surface(idx, image_list, hdr_on)
            if surf is None:
                idx = min(idx + 1, len(image_list) - 1)
                if idx < 0:
                    return 'back'
                continue
            r = surf.get_rect(center=(w // 2, h // 2))
            screen.blit(surf, r)
            page_text = "%d / %d" % (idx + 1, len(image_list))
            loader.get_surface(idx - 1, image_list, hdr_on)
            loader.get_surface(idx + 1, image_list, hdr_on)
        else:
            half_w = w // 2
            left_surf = loader.get_surface(idx, image_list, hdr_on)
            if left_surf is None:
                idx = min(idx + 1, len(image_list) - 1)
                continue
            lw, lh = left_surf.get_size()
            scale_l = min(half_w / lw, h / lh)
            nw_l, nh_l = int(lw * scale_l), int(lh * scale_l)
            left_scaled = pygame.transform.smoothscale(left_surf, (nw_l, nh_l))
            r_left = left_scaled.get_rect(right=half_w, centery=h // 2)
            screen.blit(left_scaled, r_left)
            right_surf = loader.get_surface(idx + 1, image_list, hdr_on) if idx + 1 < len(image_list) else None
            if right_surf is not None:
                rw, rh = right_surf.get_size()
                scale_r = min(half_w / rw, h / rh)
                nw_r, nh_r = int(rw * scale_r), int(rh * scale_r)
                right_scaled = pygame.transform.smoothscale(right_surf, (nw_r, nh_r))
                r_right = right_scaled.get_rect(left=half_w, centery=h // 2)
                screen.blit(right_scaled, r_right)
            page_text = "%d-%d / %d" % (idx + 1, min(idx + 2, len(image_list)), len(image_list))
            loader.get_surface(idx - 2, image_list, hdr_on)
            loader.get_surface(idx + 2, image_list, hdr_on)

        text_surf = font.render(page_text, True, (255, 255, 255))
        tw, th = text_surf.get_size()
        box = pygame.Rect(w - tw - margin * 2, h - th - margin * 2, tw + margin, th + margin)
        s = pygame.Surface((box.w, box.h))
        s.set_alpha(200)
        s.fill((0, 0, 0))
        screen.blit(s, (box.x, box.y))
        screen.blit(text_surf, (w - tw - margin, h - th - margin))
        if now < hint_show_until:
            try:
                hint_font = pygame.font.SysFont("microsoftyahei,simhei,arial", 16)
            except Exception:
                hint_font = pygame.font.Font(None, 24)
            hint_text = i18n.t("viewer.hint", "左键下 右键上  ←→翻页  上单页 下双页  H HDR  Backspace 返回  ESC 退出")
            hint_surf = hint_font.render(hint_text, True, (255, 255, 255))
            hw, hh = hint_surf.get_size()
            left_ms = hint_show_until - now
            if left_ms > HINT_FADE_MS:
                alpha = 200
            else:
                alpha = max(0, int(200 * left_ms / HINT_FADE_MS))
            hint_box = pygame.Rect(margin, h - hh - margin * 2, hw + margin, hh + margin)
            sh = pygame.Surface((hint_box.w, hint_box.h))
            sh.set_alpha(alpha)
            sh.fill((0, 0, 0))
            screen.blit(sh, (hint_box.x, hint_box.y))
            hint_surf.set_alpha(alpha)
            screen.blit(hint_surf, (margin * 2, h - hh - margin))
        pygame.display.flip()
        clock.tick(60)
