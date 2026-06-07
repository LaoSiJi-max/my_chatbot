from typing import Any, List, Optional
from pydantic import BaseModel


class ReplyRequest(BaseModel):
    """
    聊天信息请求的模型，用于向聊天机器人发送请求。

    Attributes:
        user_message (str): 用户发送的消息内容。
        thread_id (str): 对话线程的ID。
        callbacks (List[object]): 回调函数的列表。
        language (Optional[str]): 用户的语言首选项。
    """
    user_message: str
    thread_id: str
    callbacks: List[Any]
    language: str | None = None


class ThreadRequest(BaseModel):
    """
    聊天信息请求的模型，用于向聊天机器人发送请求。

    Attributes:
        thread_id (str): 对话线程的ID。
    """
    thread_id: str
    thread_name: Optional[str] = None