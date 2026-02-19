@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"

echo ========================================
echo   打包 看图 kantu.exe
echo ========================================
echo.

REM 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python，请先安装 Python 并加入 PATH。
    pause
    exit /b 1
)

REM 安装依赖
echo [1/3] 安装运行依赖 pygame Pillow ...
pip install pygame Pillow -q
echo [2/3] 安装打包工具 PyInstaller ...
pip install pyinstaller -q

REM 打包
echo [3/3] 正在打包为单文件 exe（无黑窗口）...
pyinstaller --noconfirm build_exe.spec
if errorlevel 1 (
    echo.
    echo [错误] 打包失败。
    pause
    exit /b 1
)

echo.
echo ========================================
echo   完成：exe 已生成
echo ========================================
echo   路径: dist\kantu.exe
echo   用法: 将 kantu.exe 复制到漫画目录，双击运行即可。
echo ========================================
echo.
explorer dist
pause
