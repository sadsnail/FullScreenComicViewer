# -*- coding: utf-8 -*-
"""可配置多语言：从 lang/<code>.json 加载文案，通过 config 读取当前语言。"""

import json
import os

import config

# 支持的语言代码（新增语言时在此登记并添加对应 lang/xx.json）
SUPPORTED = ("zh", "en")
_DEFAULT = "zh"
_strings = {}
_lang = None


def _lang_dir():
    """语言文件所在目录：与 exe/脚本同目录下的 lang 文件夹。"""
    return os.path.join(config.app_dir(), "lang")


def current():
    """当前语言代码。"""
    global _lang
    if _lang is None:
        _lang = config.load_language()
        if _lang not in SUPPORTED:
            _lang = _DEFAULT
    return _lang


def load(lang_code=None):
    """加载指定语言的文案；若未传则使用 config 中的语言。返回是否成功。"""
    global _strings, _lang
    if lang_code is None:
        lang_code = config.load_language()
    if lang_code not in SUPPORTED:
        lang_code = _DEFAULT
    _lang = lang_code
    path = os.path.join(_lang_dir(), lang_code + ".json")
    try:
        if os.path.isfile(path):
            with open(path, "r", encoding="utf-8") as f:
                _strings = json.load(f)
            return True
    except Exception:
        pass
    _strings = {}
    return False


def t(key, fallback=None):
    """获取当前语言下 key 对应的文案；无则返回 fallback 或 key。"""
    if not _strings and _lang is not None:
        load(_lang)
    s = _strings.get(key)
    if s is not None:
        return s
    return fallback if fallback is not None else key


def translate_label(label):
    """将列表项显示名中的固定文案（如 [上一级]）转为当前语言。"""
    if label == "[上一级]":
        return t("dir.parent", "[上一级]")
    if label == "[当前目录]":
        return t("dir.current", "[当前目录]")
    if label == "[暂无收藏]":
        return t("dir.no_favorites", "[暂无收藏]")
    return label
