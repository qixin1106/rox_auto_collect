# ROX (仙境传说新启航) macOS 园艺自动化脚本

## 简介
本项目是一个为 MMORPG《仙境传说：新启航》(ROX) 编写的自动化脚本，旨在帮助玩家在 macOS 平台上自动完成每日的"园艺"采集任务。

游戏中的园艺任务需要大量重复的手动点击操作，非常耗时且枯燥。本脚本通过模拟键鼠操作和图像识别技术，实现了自动化采集流程，从而解放您的双手。

⚠️ **免责声明：** 使用任何形式的自动化脚本或第三方工具都可能违反游戏的用户协议（Terms of Service）。使用本项目所带来的任何风险（包括但不限于账号封禁等）均由使用者自行承担。请谨慎使用。

## 主要功能
- 自动进行园艺采集
- 通过 OCR 技术识别游戏中的验证码并自动完成验证
- 循环执行，直到完成任务或手动停止

## 系统与环境要求
本脚本在以下环境中开发和测试通过：
- 操作系统: macOS 15.5
- 硬件: MacBook Pro (Apple Silicon M3 Pro 芯片)
- Python 环境: 3.10 (强烈建议使用 Conda 进行环境管理)

## 安装指南
请严格按照以下步骤进行安装，以确保脚本能够正常运行。

### 1. 克隆项目
首先，将本项目克隆到您的本地电脑。

```bash
git clone https://github.com/qixin1106/rox_auto_collect
cd rox_auto_collect
```

### 2. 创建并激活 Conda 环境
使用 Conda 创建一个独立的 Python 3.10 虚拟环境，以避免与其他项目产生依赖冲突。
请自行查阅如何安装`miniconda`

```bash
# 创建一个名为 rox_auto 的 python3.10 环境
conda create -n rox_auto python=3.10

# 激活该环境
conda activate rox_auto
```

### 3. 安装依赖库
本项目依赖 pyautogui 进行屏幕控制，PaddlePaddle 和 paddleocr 进行图像识别。

​**​重要提示：**​​ 由于 macOS 不支持 NVIDIA 的 CUDA，我们必须安装 CPU 版本的 PaddlePaddle。

```bash
# 方式1
# ----- 手动安装方式 -------
# 1. 安装 PaddlePaddle (CPU 版本)
# 使用官方推荐的国内源进行安装，速度更快
python -m pip install paddlepaddle==3.0.0 -i https://www.paddlepaddle.org.cn/packages/stable/cpu/

# 2. 安装 paddleocr
pip install paddleocr

# 3. 安装 pyautogui
pip install pyautogui
```

```bash
# 方式2
# ----- 配置安装方式 ------
pip install -r requirements.txt
```

> **以上两种任选一个即可**

关于国内镜像： 如果您在安装 paddleocr 或 pyautogui 时遇到下载速度过慢的问题，可以指定使用国内的 pip 镜像源，例如清华大学源：

## 使用方法

### 1. 授予权限 (至关重要！)

本脚本需要通过截取屏幕图像来识别游戏界面和验证码。因此，您必须为您的终端程序（或您使用的代码编辑器，如 VS Code）授予 "屏幕录制" 权限。

前往 ​**​系统设置** > **隐私与安全性** > **屏幕录制**​​
将您用于运行此脚本的应用程序（例如 终端、iTerm2 或 Visual Studio Code）添加到允许列表中

如果您不授予此权限，脚本将在尝试截图时失败并报错。

此外，还需要授权 ​**​系统设置** > **隐私与安全性** > **辅助功能**

### 2. 运行脚本
完成所有设置后，确保游戏窗口是打开且处于激活状态，然后直接运行 main.py 文件。

```bash
python main.py
```

脚本启动后会自动开始执行园艺任务。您可以随时通过 Control + C 来中止脚本。

## 注意事项

* ​屏幕分辨率：​​ 本脚本中的坐标可能基于特定分辨率编写。如果您的屏幕分辨率不同，或者游戏UI有变动，您可能需要自行调整代码中的坐标点。

* ​​游戏窗口：​​ 运行时请保持游戏窗口在前台，不要被其他窗口遮挡。
​
* ​保持更新：​​ 游戏更新可能会导致UI元素变化，从而使脚本失效。届时需要手动更新代码以适配新版游戏。



## 本项目使用了以下开源组件：

* [PyAutoGUI](https://github.com/asweigart/pyautogui)

* [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)