import re
from enum import Enum
from wcwidth import wcswidth


class RegexPatterns(Enum):
    """
    保存正则表达式的枚举类。

    Members:
        EMAIL: 验证邮件格式的正则表达式。
        PASSWORD: 验证密码格式的正则表达式。
    """
    EMAIL = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")
    PASSWORD = re.compile(r"^[A-Za-z0-9]{6,}$")


def shorten_text(text: str, max_width: int) -> str:
    """
    根据字符显示宽度截断字符串，兼容中英文字符宽度。

    Args:
        text (str): 原始文本。
        max_width (int): 最大允许的显示宽度。

    Returns:
        str: 截断后的字符串，若超出则末尾添加 "…"
    """
    current_width = 0
    result = ""

    for char in text:
        w = wcswidth(char)
        if current_width + w > max_width - 1:  # 留1位给省略号
            return result + "…"
        result += char
        current_width += w

    return result
