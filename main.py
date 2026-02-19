# -*- coding: utf-8 -*-
"""
看图应用入口：读配置/弹窗选目录、延迟导入 pygame/PIL、启动主循环（目录 ↔ 看图）。
"""

import os
import sys

import config
import folder_dialog
import i18n


def _err(msg):
    title = i18n.t("app.title", "看图")
    if sys.platform == "win32" and getattr(sys, "frozen", False):
        import ctypes
        ctypes.windll.user32.MessageBoxW(0, msg, title, 0)
    else:
        print(msg)


def main(base_dir):
    """base_dir 由入口处在选择目录对话框中确定，此处不再弹窗。"""
    if not os.path.isdir(base_dir):
        _err(i18n.t("app.dir_not_found", "目录不存在: ") + base_dir)
        return
    favorites = config.load_favorites()
    import pygame
    import ui_dir_selector
    import ui_viewer
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)
    pygame.display.set_caption(i18n.t("app.title", "看图"))
    pygame.mouse.set_visible(True)
    from PIL import Image as _Image, ImageEnhance as _ImageEnhance
    while True:
        path = ui_dir_selector.run_dir_selector(screen, base_dir, favorites)
        if path is None:
            break
        result = ui_viewer.run_manga_viewer(screen, path, _Image, _ImageEnhance, err_callback=_err)
        if result == 'quit':
            break
    pygame.quit()


def run():
    """解析配置/命令行与选目录，写入配置后启动主循环。供 __main__ 或 kantu.py 调用。"""
    i18n.load()
    app_dir = config.app_dir()
    saved_dir = config.load_default_dir()
    if saved_dir:
        base_dir = saved_dir
    else:
        if len(sys.argv) > 1 and os.path.isdir(sys.argv[1]):
            initial_dir = os.path.abspath(sys.argv[1])
        else:
            initial_dir = app_dir
        picked = folder_dialog.ask_folder(initial_dir, err_callback=_err)
        if not picked or not picked.strip():
            _err(i18n.t("app.must_choose_dir", "必须选择目标目录才能进入程序。"))
            sys.exit(1)
        base_dir = os.path.normpath(os.path.abspath(picked))
        if not os.path.isdir(base_dir):
            _err(i18n.t("app.dir_not_found", "目录不存在: ") + base_dir)
            sys.exit(1)
    config.save_default_dir(base_dir)
    main(base_dir)


if __name__ == '__main__':
    run()
