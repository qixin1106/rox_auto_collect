import time
from image_clicker import ImageClicker
from paddleocr_math_util import MathExpressionOCR
from screen_match_capturer import ScreenRegionCapturer


def main():
    # 初始化工具对象
    print("🔨 初始化工具对象...")
    clicker = ImageClicker(confidence=0.95)
    ocr_tool = MathExpressionOCR()
    capturer = ScreenRegionCapturer(confidence=0.9)
    print("✅ 初始化完成")

    # 缓存开始按钮的坐标（首次检测后保存，后续复用）
    start_button_pos = None  # 格式: (x, y) 或 None
    textfield_pos = None     # 验证码输入框坐标 (x, y)
    digit_positions = {}     # 数字键盘坐标缓存：{数字字符串: (x, y)}

    while True:
        # 首次检测并缓存开始按钮坐标
        if start_button_pos is None:
            start_button_pos = clicker.only_find_image_center("assets/start_click.png")
            if not start_button_pos:
                # time.sleep(1)  # 等待1秒后重试
                continue
            else:        
                print(f"📌 已缓存采集按钮坐标 {start_button_pos[0], start_button_pos[1]}")

        try:
            x, y = start_button_pos
            clicker.move_to_center_and_click(x, y, is_double_click=True)
            # 这里控制从缓存读取按钮坐标后的点击间隔，避免频繁点击
            time.sleep(1)
        except Exception as e:
            print(f"❌ 点击开始按钮失败: {str(e)}")
            start_button_pos = None
            continue
        
        # print("🔍 开始【园艺】...")

        # 检测是否出现验证码弹窗（必须在这方法中检测，内部会剪裁所需的验证码并保存）
        if capturer.capture_match("assets/code.png"):
            print("🛡 检测到验证码弹窗，开始验证流程...")

            # 识别表达式并计算
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
                else:
                    print(f"📌 已缓存输入框坐标 {textfield_pos[0], textfield_pos[1]}")
                
            # 点击输入框
            x, y = textfield_pos
            clicker.move_to_center_and_click(x, y)
            # time.sleep(0.5)  # 等待输入框激活

                
            # 点击输入框之后，一次性缓存所有数字键盘坐标（0~9）
            if not digit_positions:  # 仅在缓存为空时检测
                for num in range(10):  # 循环检测0~9
                    num_str = str(num)
                    pos = clicker.only_find_image_center(f"assets/{num_str}.png")
                    if pos:
                        digit_positions[num_str] = pos
                        print(f"📌 缓存数字 {num_str} 坐标: {pos}")
                    else:
                        print(f"⚠️ 未找到数字 {num_str}，后续可能失败")
                        continue


            # 输入结果数字（逐位点击）
            for digit in result:
                x, y = digit_positions[digit]
                clicker.move_to_center_and_click(x, y)

            # 我发现可以直接双击完成，第一下是取消输入框，第二下正好可以点确定，能快一点
            clicker.double_click_on_image("assets/finish.png")



if __name__ == "__main__":
    main()