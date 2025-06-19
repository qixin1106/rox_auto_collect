import time
import random
from image_clicker import ImageClicker
from paddleocr_math_util import MathExpressionOCR
from screen_match_capturer import ScreenRegionCapturer

def random_sleep():
    duration = random.uniform(0.1, 0.3)
    time.sleep(duration)

def main():
    # 初始化工具对象
    print("🔨 初始化工具对象...")
    clicker = ImageClicker(confidence=0.98)
    ocr_tool = MathExpressionOCR()
    capturer = ScreenRegionCapturer(confidence=0.9)
    print("✅ 初始化完成")

    while True:
        # 尝试点击开始按钮,这里首次是双击，万一窗口没有焦点，首次可以进入焦点
        found = clicker.double_click_on_image("assets/start_click.png")
        if not found:
            # print("未找到开始按钮，重试中...")
            time.sleep(1)
            continue
        
        print("🔍 开始【园艺】...")

        # 检测是否出现验证码弹窗
        if capturer.capture_match("assets/code.png"):
            print("🛡 检测到验证码弹窗，开始验证流程...")

            # 识别表达式并计算
            result = ocr_tool.process_image("ocr_input/last_code.png")
            if not result:
                print("❌ 表达式识别失败，跳过本轮...")
                continue

            # 点击输入框
            if not clicker.click_on_image("assets/textfield.png"):
                print("❌ 未找到输入框")
                continue

            # 输入结果数字（逐位点击）
            for digit in result:
                img_path = f"assets/{digit}.png"
                if not clicker.click_on_image(img_path):
                    print(f"❌ 未找到数字键：{digit}")
                    continue
                # 稍作停顿,这里必须稍微长一点，因点击时有个特效会影响识别
                # 并且还需要点击完后鼠标移开，不然如遇到11这样的数字会鼠标遮挡数字按键，影响识别
                time.sleep(1)

            # 点击完成按钮
            clicker.click_on_image("assets/done.png")
            random_sleep()

            # 点击验证完成按钮
            clicker.click_on_image("assets/finish.png")
            random_sleep()



if __name__ == "__main__":
    main()