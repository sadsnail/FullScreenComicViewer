# -*- coding: utf-8 -*-
"""单张图片加载与缩放、LRU 缓存。依赖由调用方注入（pygame screen、PIL Image/ImageEnhance）。"""

from constants import IMAGE_CACHE_MAX


def load_and_scale(path, max_w, max_h, screen, Image, ImageEnhance, hdr_on=False):
    """加载图片并缩放到适应 max_w x max_h，可选 HDR 增强。返回 pygame.Surface。"""
    with Image.open(path) as im:
        im = im.convert('RGB')
        w, h = im.size
        if w <= max_w and h <= max_h:
            rw, rh = w, h
        else:
            scale = min(max_w / w, max_h / h)
            rw, rh = int(w * scale), int(h * scale)
        im = im.resize((rw, rh), Image.Resampling.LANCZOS)
        if hdr_on:
            im = ImageEnhance.Brightness(im).enhance(1.25)
            im = ImageEnhance.Contrast(im).enhance(1.1)
        data = im.tobytes()
    import pygame
    return pygame.image.frombytes(data, (rw, rh), 'RGB').convert(screen)


class ImageLoader:
    """带 LRU 缓存的图片加载器，供全屏看图使用。"""

    def __init__(self, screen, Image, ImageEnhance, cache_max=IMAGE_CACHE_MAX):
        self.screen = screen
        self.Image = Image
        self.ImageEnhance = ImageEnhance
        self.cache_max = cache_max
        self.cache = {}

    def get_surface(self, index, image_list, hdr_on):
        """获取第 index 张图的 Surface，未命中则加载并缓存。"""
        if index < 0 or index >= len(image_list):
            return None
        path = image_list[index]
        key = (path, hdr_on)
        if key not in self.cache:
            while len(self.cache) >= self.cache_max:
                keys = list(self.cache.keys())
                keys.sort(key=lambda k: abs(image_list.index(k[0]) - index))
                del self.cache[keys[-1]]
            try:
                w, h = self.screen.get_size()
                self.cache[key] = load_and_scale(
                    path, w, h, self.screen,
                    self.Image, self.ImageEnhance, hdr_on=hdr_on
                )
            except Exception as e:
                print('加载失败:', path, e)
                return None
        return self.cache[key]

    def clear_cache(self):
        self.cache.clear()
