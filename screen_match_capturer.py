import pyautogui
import os
import logging
from typing import Tuple

class ScreenRegionCapturer:
    """根据参考图像在屏幕中查找匹配区域并截图保存"""

    def __init__(self, output_path: str = "ocr_input/last_code.png", confidence: float = 0.85):
        self.output_path = output_path
        self.confidence = confidence
        self._is_retina = self._detect_retina()

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

    def _detect_retina(self) -> bool:
        """判断是否为 Retina 屏幕（缩放屏幕）"""
        try:
            return pyautogui.screenshot().size[0] > pyautogui.size().width
        except:
            return False

    def _adjust_for_retina(self, region: Tuple[int, int, int, int]) -> Tuple[int, int, int, int]:
        """Retina 屏幕下将区域坐标缩放一半"""
        return tuple(x // 2 for x in region) if self._is_retina else region

    def capture_match(self, template_image: str) -> bool:
        """
        在屏幕中查找 template_image 所匹配区域，并截图保存到固定路径
        :param template_image: 参考图像路径
        :return: 成功与否
        """
        try:
            match = pyautogui.locateOnScreen(template_image, confidence=self.confidence, grayscale=True)
            if not match:
                logging.warning("未找到匹配区域")
                return False

            region = self._adjust_for_retina(match)
            # 这一步是为了将截图弹窗中的位置缩小到仅题目的部分
            region = (region[0] + 96, region[1] + 90, 217, 31)
            img = pyautogui.screenshot(region=region)
            img.save(self.output_path)

            logging.info(f"截图成功，保存至: {self.output_path}")
            return True

        except Exception as e:
            # logging.error(f"截图失败: {e}")
            return False


# ===== 使用示例 =====
if __name__ == "__main__":
    capturer = ScreenRegionCapturer(confidence=0.9, output_path='ocr_input/last_code2.png')
    capturer.capture_match("assets/code.png")
    
    