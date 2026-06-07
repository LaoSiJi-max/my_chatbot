from typing import Any, Optional, Tuple
from tools.i18n import I18n
from tools.text_utils import RegexPatterns
from communication.auth_comm import AuthComm

class AuthController:
    @staticmethod
    def login(username: str, password: str, language: str) -> Tuple[str, Optional[str]]:
        """
        用户登录的控制器方法。

        Args:
            username (str): 用户名。
            password (str): 密码。
            language (str): 语言代码。

        Returns:
            Tuple[str, Optional[str]]: 提示语和令牌。
        """
        # 验证用户名
        if not bool(RegexPatterns.EMAIL.value.match(username)):
            return I18n.get("invalid_username", language), None
        
        # 验证密码
        if not bool(RegexPatterns.PASSWORD.value.match(password)):
            return I18n.get("invalid_password", language), None
        
        # 获取登陆结果
        result = AuthComm.call_login_api(username, password)

        # 登陆成功时
        if result["status"] == "success":
            return I18n.get("login_success", language).format(username=username), result["access_token"]
        # 账号或者密码错误时
        elif result["status"] == "auth_failed":
            return I18n.get("login_failure", language), None
        # 未获取到 token 时
        elif result["status"] == "access_token_failed":
            return I18n.get("login_unauthorized", language), None
        # 服务器错误时
        elif result["status"] == "server_error":
            return I18n.get("login_server_error", language), None
        # 网络及其他异常时
        elif result["status"] == "network_error":
            return I18n.get("login_network_error", language), None
        # 其他情况时
        else:
            return I18n.get("login_unknown_error", language), None
    
    @staticmethod
    def register(username: str, password: str, language: str) -> str:
        """
        用户注册的控制器方法。

        Args:
            username (str): 用户名。
            password (str): 密码。
            language (str): 语言代码。

        Returns:
            str: 提示语。
        """
        # 验证用户名
        if not bool(RegexPatterns.EMAIL.value.match(username)):
            return I18n.get("invalid_username", language)
        
        # 验证密码
        if not bool(RegexPatterns.PASSWORD.value.match(password)):
            return I18n.get("invalid_password", language)
        
        result = AuthComm.call_register_api(username, password, language)
        
        # 注册成功时
        if result["status"] == "success":
            return I18n.get("register_success", language)
        # 账号存在时
        elif result["status"] == "auth_failed":
            return I18n.get("user_exists", language)
        # 服务器错误时
        elif result["status"] == "server_error":
            return I18n.get("register_server_error", language)
        # 网络及其他异常时
        elif result["status"] == "network_error":
            return I18n.get("register_network_error", language)
        # 其他情况时
        else:
            return I18n.get("register_unknown_error", language)
        
    @staticmethod
    def get_user_message(access_token: str, language: str) -> Tuple[Optional[str], Optional[dict[str, Any]]]:
        """
        获取用户信息。

        Args:
            access_token (str): 令牌。
            language (str): 语言代码。

        Returns:
            Tuple[Optional[str], Optional[dict[str, Any]]]: 提示语和保存用户信息的字典。
        """
        # 获取用户信息
        result = AuthComm.call_me_api(access_token)

        # 成功时不用提示，只返回用户信息
        if result["status"] == "success":
            return None, result
        # 失败时返回提示
        else:
            return I18n.get("me_failure", language), None
        
    @staticmethod
    def update_language(access_token: str, language: str) -> Tuple[Optional[str], bool]:
        """
        更新用户语言首选项。

        Args:
            access_token (str): 令牌。
            language (str): 语言代码。

        Returns:
            Tuple[Optional[str], bool]: 提示语和表示成功与否的布尔值。
        """
        # 准备要更新的字段
        update_fields = {"language": language}

        # 调用更新 API
        result = AuthComm.update_user_api(access_token, update_fields)
        
        # 成功时不提示，只返回 True
        if result["status"] == "success":
            return None, True
        # 失败时提示，并返回 False
        else:
            return I18n.get("language_update_failed", language), False