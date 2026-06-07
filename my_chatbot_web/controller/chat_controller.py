from typing import Any, Generator, Optional, Tuple
from wcwidth import wcswidth
from tools.i18n import I18n
from communication.chat_comm import ChatComm


class ChatController:
    @staticmethod
    def chat_get_history(access_token: str, thread_id: str, language: str) -> Tuple[Optional[str], Optional[dict[str, Any]]]:
        """
        获取用户指定线程 ID 的历史消息。

        Args:
            access_token (str): 用户的访问令牌。
            thread_id (str): 会话线程 ID。
            language (str): 语言代码。

        Returns:
            Tuple[Optional[str], Optional[dict[str, Any]]]: 提示语和存储历史消息的字典。
        """
        # 通信以获取历史消息
        result = ChatComm.call_get_history_api(access_token, thread_id)

        # 成功时不提示，只返回历史消息列表（注意可能是一个空的列表，但是成功）
        if result["status"] == "success":
            return None, result["history"]
        # 失败时提示
        else:
            return I18n.get("get_history_failed", language), None
    
    @staticmethod
    def chat_stream_reply(human_message: str, access_token: str, thread_id: str, language: str) -> Generator[str, None, None]:
        """
        以流式输出的方式回复用户的最新消息。

        Args:
            human_message (str): 用户消息。
            access_token (str): 用户的访问令牌。
            thread_id (str): 会话线程 ID。
            language (str): 语言代码。

        Returns:
            Generator[str, None]: 以流式输出返回的聊天机器人的最新回复。
        """
        return ChatComm.call_stream_api(human_message, access_token, thread_id, language)
    
    @staticmethod
    def chat_create_new_chat(access_token: str, language: str) -> Tuple[Optional[str], Optional[str]]:
        """
        为用户创建一个新会话。

        Args:
            access_token (str): 用户的访问令牌。
            language (str): 语言代码。

        Returns:
            Tuple[Optional[str], Optional[str]]: 提示语和新会话的线程 ID。
        """
        # 通信以创建新会话
        result = ChatComm.call_create_chat_api(access_token)

        # 成功时提示，并返回新的 thread_id
        if result["status"] == "success":
            return I18n.get("chat_create_success", language), result["thread_id"]
        # 失败时提示
        else:
            return I18n.get("chat_create_failed", language), None
        
    @staticmethod
    def chat_delete_chat(access_token: str, thread_id: str, language: str) -> Tuple[Optional[str], Optional[bool]]:
        """
        为用户删除一个指定的新会话。

        Args:
            access_token (str): 用户的访问令牌。
            thread_id (str): 会话线程 ID。
            language (str): 语言代码。

        Returns:
            Tuple[Optional[str], Optional[bool]]: 提示语和反应删除是否成功的布尔值。
        """
        # 通信以删除指定 thread_id 对应的会话
        result = ChatComm.call_delete_chat_api(access_token, thread_id)

        # 成功时提示，并返回 True
        if result["status"] == "success":
            return I18n.get("chat_delete_success", language), True
        # 失败时提示，并返回 False
        else:
            return I18n.get("chat_delete_failed", language), False
        

    @staticmethod
    def chat_rename_chat(access_token: str, thread_id: str, new_thread_name: str, language: str) -> Tuple[Optional[str], Optional[bool]]:
        """
        为用户重命名一个指定的新会话。

        Args:
            access_token (str): 用户的访问令牌。
            thread_id (str): 会话线程 ID。
            new_thread_name (str): 重命名后的会话名。
            language (str): 语言代码。

        Returns:
            Tuple[Optional[str], Optional[bool]]: 提示语和反应重命名是否成功的布尔值。
        """
        # 检查长度大于 16 时，提示用户名字过长。注意此处全角文字按 2 个单位来计算，半角按 1 个单位来计算。
        if wcswidth(new_thread_name) > 16:
            return I18n.get("chat_name_to_long", language), False
        
        # 检查并提示用户不能为空
        if wcswidth(new_thread_name) <= 0:
            return I18n.get("chat_name_empty", language), False
        
        # 通信以重命名指定 thread_id
        result = ChatComm.call_rename_chat_api(access_token, thread_id, new_thread_name)
        
        # 成功时提示，并返回 True
        if result["status"] == "success":
            return I18n.get("chat_rename_success", language), True
        # 失败时提示，并返回 False
        else:
            return I18n.get("chat_rename_failed", language), False