from threading import Thread
import time
from pynput.keyboard import Listener, Key


class KeyboardInterruptHandler:
    """
    ESC键监听退出工具类
    功能：在后台监听ESC键，按下时触发退出信号，供主程序判断是否终止
    """

    def __init__(self):
        self._exit_flag = False  # 退出标志（False：运行中；True：需退出）
        self._listener_thread = None  # 监听线程

    def _on_key_press(self, key):
        """键盘按键回调：按下ESC键时设置退出标志"""
        if key == Key.esc:
            self._exit_flag = True
            print("\n⚠️ 检测到ESC键，准备退出程序...")
            return False  # 停止监听

    def start(self):
        """启动后台监听线程"""
        if self._listener_thread is None:
            # 修复：先启动Listener，再join（通过with语句自动管理启动/停止）
            def listen():
                with Listener(on_press=self._on_key_press) as listener:
                    listener.join()  # 此时Listener已启动，可安全join

            # 创建并启动监听线程（守护线程）
            self._listener_thread = Thread(target=listen, daemon=True)
            self._listener_thread.start()
            print("✅ ESC键监听已启动（按ESC键退出程序）")

    def should_exit(self) -> bool:
        """判断是否需要退出（供主循环调用）"""
        return self._exit_flag

    def stop(self):
        """手动停止监听（可选调用）"""
        self._exit_flag = True
        if self._listener_thread is not None:
            self._listener_thread.join(timeout=1)  # 等待线程结束
            self._listener_thread = None
            print("✅ ESC键监听已停止")


# 测试代码
if __name__ == "__main__":
    handler = KeyboardInterruptHandler()
    handler.start()
    
    while not handler.should_exit():
        print("运行中...")
        time.sleep(1)
    # handler.stop()