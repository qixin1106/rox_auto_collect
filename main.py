import time
from image_clicker import ImageClicker
from paddleocr_math_util import MathExpressionOCR
from screen_match_capturer import ScreenRegionCapturer
from keyboard_interrupt_handler import KeyboardInterruptHandler


VER_STRING = "v1.1.0"

def main():
    print("\n\n\n\n\n")
    print(f"版本号：{VER_STRING}")
    print("本脚本用于学习自动化工具开发，仅供学习交流使用")
    # 初始化工具对象
    print("🔨 初始化工具对象...")
    # 监听键盘退出信号
    exit_handler = KeyboardInterruptHandler()
    exit_handler.start()
    # 点击找图工具
    clicker = ImageClicker(confidence=0.95)
    # OCR识别工具，验证码识别器
    ocr_tool = MathExpressionOCR()
    # 截图工具（截屏验证码）
    capturer = ScreenRegionCapturer(confidence=0.9)
    print("✅ 初始化完成")
    print("🔧 开始运行...按【ESC】终止脚本运行")

    # 缓存坐标
    start_button_pos = None
    textfield_pos = None
    digit_positions = {}
    finish_button_pos = None

    # 主循环：添加退出判断（仅修改此处，将while True改为监听退出信号）
    while not exit_handler.should_exit():
        # 首次检测并缓存开始按钮坐标
        if start_button_pos is None:
            start_button_pos = clicker.only_find_image_center("assets/start_click.png")
            if not start_button_pos:
                continue
            print(f"📌 已缓存采集按钮坐标 {start_button_pos[0], start_button_pos[1]}")

        try:
            x, y = start_button_pos
            clicker.move_to_center_and_click(x, y, is_double_click=True)
        except Exception as e:
            print(f"❌ 点击开始按钮失败: {str(e)}")
            start_button_pos = None
            continue

        # 检测验证码弹窗
        if capturer.capture_match("assets/code.png"):
            print("🛡 检测到验证码弹窗，开始验证流程...")

            result = ocr_tool.process_image("ocr_input/last_code.png")
            if not result:
                print("❌ 表达式识别失败，跳过本轮...")
                continue

            # 检测输入框位置
            if textfield_pos is None:
                textfield_pos = clicker.only_find_image_center("assets/textfield.png")
                if not textfield_pos:
                    print("❌ 未找到输入框")
                    continue
                print(f"📌 已缓存输入框坐标 {textfield_pos[0], textfield_pos[1]}")
            
            # 点击输入框
            x, y = textfield_pos
            clicker.move_to_center_and_click(x, y)

            # 缓存数字键盘坐标
            if not digit_positions:
                for num in range(10):
                    num_str = str(num)
                    pos = clicker.only_find_image_center(f"assets/{num_str}.png")
                    if pos:
                        digit_positions[num_str] = pos
                        print(f"📌 缓存数字 {num_str} 坐标: {pos}")
                    else:
                        print(f"⚠️ 未找到数字 {num_str}")

            # 输入结果数字（添加退出检查，避免退出不及时）
            for digit in result:
                if exit_handler.should_exit():  # 中途按下ESC则中断
                    break
                x, y = digit_positions[digit]
                clicker.move_to_center_and_click(x, y)

            if exit_handler.should_exit():
                break  # 退出验证码流程

            # 双击完成按钮
            clicker.double_click_on_image("assets/finish.png")
                    # 首次检测并缓存开始按钮坐标
            if finish_button_pos is None:
                finish_button_pos = clicker.only_find_image_center("assets/finish.png")
                if not finish_button_pos:
                    continue
                print(f"📌 已缓存采集完成坐标 {finish_button_pos[0], finish_button_pos[1]}")
            x, y = finish_button_pos
            clicker.move_to_center_and_click(x, y, is_double_click=True)


    # 程序退出时停止监听
    exit_handler.stop()
    print("✅ 程序已安全终止")


if __name__ == "__main__":
    main()
    