# -*- coding: utf-8 -*-
"""应用目录、配置文件与收藏文件的路径及读写。"""

import os
import sys


def app_dir():
    """程序/脚本所在目录，用于存放配置与收藏文件。"""
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def config_file():
    """配置文件路径：保存默认目录等。"""
    return os.path.join(app_dir(), "kantu_config.txt")


def favorites_file():
    """收藏文件路径：与 exe/脚本同目录。"""
    return os.path.join(app_dir(), "kantu_favorites.txt")


def load_default_dir():
    """从配置文件读取默认目录；无文件或为空或目录不存在则返回 None。"""
    path = config_file()
    if not os.path.isfile(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            line = (f.readline() or "").strip()
        if not line:
            return None
        p = os.path.normpath(line)
        return p if os.path.isdir(p) else None
    except Exception:
        return None


def load_language():
    """从配置文件读取语言代码（第二行）；缺失则返回 zh。具体是否支持由 i18n 判定。"""
    path = config_file()
    if not os.path.isfile(path):
        return "zh"
    try:
        with open(path, "r", encoding="utf-8") as f:
            f.readline()
            line = (f.readline() or "").strip()
        return line or "zh"
    except Exception:
        return "zh"


def save_default_dir(dir_path, lang=None):
    """将默认目录写入配置文件；可选同时写入语言（第二行）。"""
    path = config_file()
    try:
        lang = lang if lang is not None else load_language()
        with open(path, "w", encoding="utf-8") as f:
            f.write(os.path.normpath(dir_path) + "\n")
            f.write(lang + "\n")
    except Exception:
        pass


def save_language(lang):
    """仅更新配置文件中的语言行，保留第一行路径不变。"""
    path = config_file()
    if not lang or not lang.strip():
        return
    lang = lang.strip()
    try:
        lines = []
        if os.path.isfile(path):
            with open(path, "r", encoding="utf-8") as f:
                lines = [f.readline(), f.readline()]
        if not lines:
            lines = ["\n", "\n"]
        lines[0] = (lines[0] or "").rstrip("\n") + "\n"
        lines[1] = lang + "\n"
        with open(path, "w", encoding="utf-8") as f:
            f.write(lines[0])
            f.write(lines[1])
    except Exception:
        pass


def load_favorites():
    """从文件加载收藏目录集合；路径统一规范化为 normpath。"""
    path = favorites_file()
    if not os.path.isfile(path):
        return set()
    try:
        with open(path, "r", encoding="utf-8") as f:
            return set(os.path.normpath(line.strip()) for line in f if line.strip())
    except Exception:
        return set()


def save_favorites(favorites):
    """将收藏目录列表写入文件（路径已规范化）。"""
    path = favorites_file()
    try:
        with open(path, "w", encoding="utf-8") as f:
            for p in sorted(favorites):
                f.write(os.path.normpath(p) + "\n")
    except Exception:
        pass
