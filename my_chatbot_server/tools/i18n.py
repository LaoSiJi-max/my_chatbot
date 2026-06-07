import locale
import platform


def get_system_locale() -> str:
    """
    获取当前设备的语言设置项，并转换为聊天机器人系统支持的对应的语言代码。
    中文的情况下，港澳台地区返回繁体中文，其他返回简体中文。
    日语的情况下，返回日语。
    英语及其他系统不支持的语言，一律返回英语。
    该方法提供 Windows 系统支持。

    Returns:
            str: 语言代码，使用简化的 BCP 47 格式。
    """
    # 获取本地设备语言，缺省值为 'en_us'
    language = locale.getlocale()[0] or "en_us"

    # Windows 系统的情况下，由于返回的不是 BCP 47 格式，需要进行转换
    if platform.system() == "Windows":
        # 先转换成小写，后续一律按小写处理
        language = language.lower()
        
        # 简体中文
        if "simplified" in language:
            return "zh_cn"
        # 繁体中文
        elif "traditional" in language:
            return "zh_tw"
        # 日语
        elif "japanese" in language:
            return "ja_jp"
        # 英语及其他语言一律按照英语处理
        else:
            return "en_us"
    # 其它系统的情况
    else:
        return normalize_language(language)
        

def normalize_language(language: str) -> str:
    """
    将输入的语言代码转换为聊天机器人系统支持的对应的语言代码。
    中文的情况下，港澳台地区返回繁体中文，其他返回简体中文。
    日语的情况下，返回日语。
    英语及其他系统不支持的语言，一律返回英语。

    Args:
            language (str): 符合 BCP 47 格式的语言代码。

    Returns:
            str: 语言代码，使用简化的 BCP 47 格式。
    """
    # 获取本地设备语言，缺省值为 'en_us'
    language = language or "en_us"
    language = language.lower()     # 先转换成小写，后续一律按小写处理

    # 以 'zh' 开头的情况下被视为中文，要按简体中文和繁体中文分别处理
    if language.startswith("zh"):
        # 港澳台都按繁体中文处理，统一返回 'zh_tw'
        if language in ("zh_hk", "zh_mo", "zh_tw"):
            return "zh_tw"
        # 其他情况按简体中文处理，返回 'zh_cn'
        else:
            return "zh_cn"
    # 以 'ja' 开头的情况都被视为日语，返回 'ja_jp'
    elif language.startswith("ja"):
        return "ja_jp"
    # 英语及其他语言都按英语来处理，返回 'en_us'
    else:
        return "en_us"