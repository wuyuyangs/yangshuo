"""
String Utility Module
本模块包含字符串处理相关的通用函数。
"""

def is_palindrome(text: str) -> bool:
    """
    判断传入的字符串是否为回文（忽略大小写和非字母数字字符）。

    Args:
        text (str): 需要检测的字符串。

    Returns:
        bool: 如果是回文返回 True，否则返回 False。
    """
    if not isinstance(text, str):
        return False
    
    # 预处理：去除非字母数字字符并转为小写
    # 例如: "A man, a plan..." -> "amanaplan..."
    clean_text = "".join(char.lower() for char in text if char.isalnum())
    
    # 判断倒序是否与原字符串相等
    return clean_text == clean_text[::-1]