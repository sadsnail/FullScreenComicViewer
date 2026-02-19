# -*- coding: utf-8 -*-
"""纯文件系统工具：自然排序、目录下是否有图、查找图片列表、目录选项生成。无 pygame 依赖。"""

import os
import re

from constants import IMAGE_EXT


def natural_sort_key(s):
    parts = re.split(r'(\d+)', os.path.basename(s).lower())
    return [int(x) if x.isdigit() else x for x in parts if x]


def dir_has_any_image(directory):
    """发现一张图片即返回 True，不继续扫描。"""
    try:
        for name in os.listdir(directory):
            if not os.path.isfile(os.path.join(directory, name)):
                continue
            if os.path.splitext(name)[1].lower() in IMAGE_EXT:
                return True
    except OSError:
        pass
    return False


def find_images(directory):
    """返回目录下图片文件路径列表，按自然序排序。"""
    files = []
    for name in os.listdir(directory):
        path = os.path.join(directory, name)
        if not os.path.isfile(path):
            continue
        ext = os.path.splitext(name)[1].lower()
        if ext in IMAGE_EXT:
            files.append(path)
    return sorted(files, key=natural_sort_key)


def get_dir_choices(base_dir, current_root):
    """返回 [(显示名, 绝对路径, 是否含图片), ...]。有图检测遇一张即停。"""
    choices = []
    if current_root != base_dir:
        parent = os.path.dirname(current_root)
        choices.append(("[上一级]", parent, dir_has_any_image(parent)))
    choices.append(("[当前目录]", current_root, dir_has_any_image(current_root)))
    try:
        for name in sorted(os.listdir(current_root), key=lambda x: x.lower()):
            path = os.path.join(current_root, name)
            if os.path.isdir(path):
                choices.append((name, path, dir_has_any_image(path)))
    except OSError:
        pass
    return choices


def get_favorites_choices(favorites):
    """根据收藏集合生成 [(显示名, 绝对路径, 是否含图), ...]，仅保留仍存在的目录，按显示名排序。"""
    choices = []
    for path in favorites:
        if not path or not os.path.isdir(path):
            continue
        name = os.path.basename(path) or path
        choices.append((name, path, dir_has_any_image(path)))
    choices.sort(key=lambda x: x[0].lower())
    return choices
