import re
from paddleocr import PaddleOCR

class MathExpressionOCR:
    def __init__(self):
        # 初始化 OCR 引擎
        # MacOS 上需设置 enable_mkldnn=False，否则可能报错
        self.ocr = PaddleOCR(
            enable_mkldnn=False,
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            use_textline_orientation=False
        )

    def process_image(self, image_path):
        """
        处理本地图片，识别文字并从倒数第三个内容中提取数学表达式，计算其结果。
        返回：表达式计算结果的字符串形式（如 "42"），若失败则返回 ""。
        """
        try:
            # 使用 OCR 引擎识别图像内容
            result = self.ocr.predict(image_path)

            # 检查是否识别成功且包含 rec_texts 字段
            if not result or 'rec_texts' not in result[0]:
                print(f"❌没有识别到任何文本")
                return ""

            # 获取识别到的文字列表（只取第一个结果）
            rec_texts = result[0]['rec_texts']

            # 如果识别内容少于1个，说明没有目标表达式，返回空
            if len(rec_texts) < 1:
                print(f"❌识别内容小于3个，不正常")
                return ""

            # 获取倒数第一项，通常为目标数学表达式
            expression_str = rec_texts[0]
            print(f'👁OCR识别结果：{expression_str}')
                        
            # 清洗表达式，只保留数字和 + - * / 四种运算符
            # cleaned_expr = re.sub(r"[^\d\+\-\*\/]", "", expression_str)
            cleaned_expr = expression_str
            
            # 使用 eval 安全计算表达式结果
            result_value = eval(cleaned_expr)
            print(f"✅表达式：{cleaned_expr}={result_value}")

            # 返回结果的字符串形式
            return str(result_value)

        except Exception:
            # 任意步骤出错则返回空字符串
            return ""


# -- 测试 --
if __name__ == "__main__":
    ocr_tool = MathExpressionOCR()
    output = ocr_tool.process_image("ocr_input/last_code2.png")
    print("计算结果：", output)
