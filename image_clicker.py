import time
import pyautogui
import logging
from typing import Tuple, Optional
import random



class ImageClicker:
    """
    图像识别与点击操作工具类（支持Retina屏幕适配）
    功能：识别屏幕上的目标图像并执行点击/双击操作
    """
    
    def __init__(self, 
                 confidence: float = 0.9,
                 double_click_delay: float = 0.1,
                 move_duration: float = 0.3):
        """
        初始化配置
        :param confidence: 图像匹配置信度阈值 (0-1)
        :param double_click_delay: 双击间隔时间（秒）
        :param move_duration: 鼠标移动动画时间（秒）
        """
        self.confidence = confidence
        self.double_click_delay = double_click_delay
        self.move_duration = move_duration
        self._is_retina = self._detect_retina()
        
        # 日志配置
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s: %(message)s'
        )

    def _detect_retina(self) -> bool:
        """检测是否为Retina屏幕（高DPI屏幕）"""
        try:
            return pyautogui.screenshot().size[0] > pyautogui.size().width
        except Exception:
            return False

    def _adjust_coords(self, location: tuple) -> Tuple[int, int, int, int]:
        """
        Retina屏幕坐标修正
        :param location: (x, y, width, height) 元组
        :return: 修正后的坐标元组
        """
        if self._is_retina:
            return (location[0]//2, location[1]//2, location[2]//2, location[3]//2)
        return location

    def _get_target_center(self, location: tuple) -> Tuple[int, int]:
        """
        计算目标区域的中心坐标
        :param location: (x, y, width, height) 元组
        :return: (center_x, center_y) 中心坐标
        """
        x, y, w, h = location
        return (x + w // 2, y + h // 2)

    def locate_image(self, image_path: str) -> Optional[Tuple[int, int, int, int]]:
        """
        定位图像在屏幕上的位置
        :param image_path: 目标图像文件路径
        :return: 位置元组 (x, y, width, height) 或 None
        """
        try:
            location = pyautogui.locateOnScreen(
                image_path,
                confidence=self.confidence,
                grayscale=True
            )
            if location:
                return self._adjust_coords(location)
            logging.warning(f"⚠️ 未找到目标图像: {image_path}")
            return None
        except Exception as e:
            # logging.error(f"❌ 图像定位异常: {str(e)}")
            return None

    def click_on_image(self, image_path: str) -> bool:
        """
        在目标图像位置执行单击操作
        :param image_path: 目标图像文件路径
        :return: 是否成功执行
        """
        location = self.locate_image(image_path)
        if not location:
            return False
            
        try:
            x, y = self._get_target_center(location)
            pyautogui.moveTo(x, y, duration=self.move_duration)
            time.sleep(0.3)
            pyautogui.click()
            self.getMoveMouse()
            # logging.info(f"🖱️ 单击位置: ({x}, {y}) - 目标: {image_path}")
            return True
        except Exception as e:
            logging.error(f"❌ 单击操作异常: {str(e)}")
            return False

    def double_click_on_image(self, image_path: str) -> bool:
        """
        在目标图像位置执行双击操作
        :param image_path: 目标图像文件路径
        :return: 是否成功执行
        """
        location = self.locate_image(image_path)
        if not location:
            return False
            
        try:
            x, y = self._get_target_center(location)
            pyautogui.moveTo(x, y, duration=self.move_duration)
            time.sleep(0.3)
            pyautogui.click()
            pyautogui.PAUSE = self.double_click_delay
            pyautogui.click()
            # logging.info(f"🖱️🖱️ 双击位置: ({x}, {y}) - 目标: {image_path}")
            return True
        except Exception as e:
            logging.error(f"❌ 双击操作异常: {str(e)}")
            return False
    
    
    # 获取随机数，作为点击之后（x,y）的一个随机坐标，每次都要随机生成不能写死，看起来比较自然
    def getMoveMouse(self):
        x = random.uniform(50, 100)
        y = random.uniform(50, 100)
        # d = random.uniform(0.1, 0.3)
        pyautogui.moveTo(x, y)

