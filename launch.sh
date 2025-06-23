#!/bin/bash

# =============================================
# 自动激活虚拟环境并执行 Python 主脚本
# 适用场景：项目根目录下存在 .conda 虚拟环境
# =============================================

# 获取脚本所在的绝对路径（即项目根目录）
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "项目根目录: $PROJECT_ROOT"

# 定义虚拟环境路径
VENV_PYTHON="$PROJECT_ROOT/.conda/bin/python"
MAIN_SCRIPT="$PROJECT_ROOT/main.py"

# 检查虚拟环境是否存在
if [[ ! -f "$VENV_PYTHON" ]]; then
    echo "[错误] 未找到虚拟环境中的 Python 解释器: $VENV_PYTHON"
    exit 1
fi

# 检查主脚本是否存在
if [[ ! -f "$MAIN_SCRIPT" ]]; then
    echo "[错误] 未找到主脚本: $MAIN_SCRIPT"
    exit 1
fi

# 执行命令（核心逻辑）
echo "启动虚拟环境中的 Python 并执行脚本..."
"$VENV_PYTHON" "$MAIN_SCRIPT"

# 检查执行结果
if [[ $? -eq 0 ]]; then
    echo "脚本执行成功!"
else
    echo "[警告] 脚本执行可能出错，请检查输出"
fi