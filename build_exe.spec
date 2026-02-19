# PyInstaller 打包配置：生成单文件 exe，无控制台窗口
# 用法: pyinstaller build_exe.spec  或直接运行 build_exe.bat

# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['kantu.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['pygame', 'PIL', 'PIL._tkinter_finder'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='kantu',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,   # 无黑窗口，双击直接全屏看图
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
