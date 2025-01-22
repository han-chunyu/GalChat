@echo off
REM 安装 SWIFT 的批处理脚本
REM 替代方法: pip install ms-swift -U

set CONDA_ENV_NAME=llmft

REM 检查 Conda 是否可用
where conda >nul 2>&1
if errorlevel 1 (
    echo Conda 未安装或未添加到环境变量中。
    echo 请先安装 Anaconda 或 Miniconda。
    pause
    exit /b
)

REM 激活 Conda 环境
call conda activate %CONDA_ENV_NAME%
if errorlevel 1 (
    echo Conda 环境 "%CONDA_ENV_NAME%" 不存在。
    echo 请先创建 Conda 环境：conda create -n %CONDA_ENV_NAME% python=3.10
    pause
    exit /b
)

REM 检查 Python 版本
python --version
if errorlevel 1 (
    echo Python 未安装或未添加到环境变量中。
    echo 请确保 Conda 环境 "%CONDA_ENV_NAME%" 中安装了 Python 3.10 或更高版本。
    pause
    exit /b
)

REM 检查 PyTorch 版本
python -c "import torch; print(torch.__version__)"
if errorlevel 1 (
    echo PyTorch 未安装。
    echo 正在安装 PyTorch...
    pip install torch>=2.0
)

REM 安装 ms-swift
echo 正在安装 ms-swift...
pip install ms-swift -U

if errorlevel 1 (
    echo 安装 ms-swift 失败。
    pause
    exit /b
)

echo ms-swift 安装成功！
pause