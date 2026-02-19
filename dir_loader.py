# -*- coding: utf-8 -*-
"""异步目录加载：在后台线程执行 get_dir_choices / 收藏列表，结果通过带锁状态交给主线程。"""

import threading

from fs_utils import get_dir_choices, get_favorites_choices


class DirLoader:
    """后台加载目录列表，主线程轮询 busy 与 choices。"""

    def __init__(self):
        self._lock = threading.Lock()
        self._busy = False
        self._choices = None
        self._error = None
        self._worker = None

    def start_load(self, base_dir, current_root, favorites_mode, favorites):
        """提交加载任务：favorites_mode 为 True 时加载收藏列表，否则加载目录列表。"""
        with self._lock:
            self._busy = True
            self._choices = None
            self._error = None
        def run():
            try:
                if favorites_mode:
                    choices = get_favorites_choices(favorites)
                    if not choices:
                        choices = [("[暂无收藏]", "", False)]
                else:
                    choices = get_dir_choices(base_dir, current_root)
            except Exception as e:
                choices = None
                err = str(e)
            else:
                err = None
            with self._lock:
                self._choices = choices
                self._error = err
                self._busy = False

        self._worker = threading.Thread(target=run, daemon=True)
        self._worker.start()

    def get_state(self):
        """返回 (busy, choices, error)。主线程每帧调用。"""
        with self._lock:
            return self._busy, self._choices, self._error

    def consume_result(self):
        """主线程取走当前结果后调用，清空 choices/error 以便下次加载。"""
        with self._lock:
            self._choices = None
            self._error = None
