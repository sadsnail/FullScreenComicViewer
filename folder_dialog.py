# -*- coding: utf-8 -*-
"""选择目标文件夹对话框（tk），支持本地与网络映射路径。"""

import os
import sys


def ask_folder(default_dir, err_callback=None):
    """选择目标文件夹，支持本地与网络映射路径（如 Z:\\ 或 \\\\server\\share）。
    可浏览选择，也可直接输入/粘贴路径。
    err_callback(msg) 在无法显示对话框时被调用；若为 None 则静默忽略。"""
    try:
        import i18n
        import tkinter as tk
        from tkinter import filedialog, ttk
        root = tk.Tk()
        root.title(i18n.t("dialog.folder_title", "选择漫画根目录"))
        root.attributes("-topmost", True)
        root.resizable(True, False)
        var = tk.StringVar(value=default_dir or "")
        f = ttk.Frame(root, padding=12)
        f.pack(fill=tk.X)
        ttk.Label(f, text=i18n.t("dialog.folder_prompt", "目标文件夹（支持网络映射盘，如 Z:\\ 或 \\\\服务器\\共享名）：")).pack(anchor=tk.W)
        entry = ttk.Entry(f, textvariable=var, width=60)
        entry.pack(fill=tk.X, pady=(4, 8))
        bf = ttk.Frame(f)
        bf.pack(fill=tk.X)
        browse_title = i18n.t("dialog.browse_title", "浏览文件夹")

        def browse():
            start = var.get().strip() or default_dir
            if start and os.path.isdir(start):
                d = filedialog.askdirectory(title=browse_title, initialdir=start)
            else:
                d = filedialog.askdirectory(title=browse_title)
            if d:
                var.set(d)

        def ok_click():
            root.result = var.get().strip() or None
            root.destroy()

        ttk.Button(bf, text=i18n.t("dialog.browse", "浏览..."), command=browse).pack(side=tk.LEFT, padx=(0, 6))
        ttk.Button(bf, text=i18n.t("dialog.ok", "确定"), command=ok_click).pack(side=tk.LEFT, padx=(0, 6))
        ttk.Button(bf, text=i18n.t("dialog.cancel", "取消"), command=root.destroy).pack(side=tk.LEFT)
        root.result = None
        root.protocol("WM_DELETE_WINDOW", root.destroy)
        entry.focus_set()
        root.bind("<Return>", lambda e: ok_click())
        root.update_idletasks()
        root.update()
        root.lift()
        root.focus_force()
        if sys.platform == "win32":
            try:
                root.after(50, lambda: root.attributes("-topmost", True))
            except Exception:
                pass
        root.mainloop()
        return getattr(root, "result", None)
    except Exception as e:
        if err_callback:
            import i18n
            err_callback(i18n.t("dialog.folder_error", "无法显示文件夹选择对话框（%s），将使用默认目录。") % (e,))
        return None
