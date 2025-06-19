from pyautogui import sleep
from image_clicker import ImageClicker

# 测试一下，验证置信度到多少可以准确的点击这个对应的数字
clicker = ImageClicker(confidence=0.98)

for i in range(0, 10):
    clicker.click_on_image(f"assets/{i}.png")
    sleep(0.1)
    