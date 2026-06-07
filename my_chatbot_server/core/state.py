from enum import Enum
from typing import Any
from langchain_core.messages import AnyMessage
from langgraph.graph import MessagesState
from langmem.short_term import RunningSummary


class State(MessagesState):
    """
    在 LangGraph 的状态图之间传递的状态对象，内部存储了系统运行所必需的字段。

    Attributes:
        context (dict[str, Any]): 上下文信息。
        language (str): 语言代码。
        summary (RunningSummary | None): 摘要。
        summarized_messages (list[AnyMessage]): 加入摘要，并截断被摘要信息的消息记录，用于传入生成回复的大语言模型。
    """
    context: dict[str, Any]
    language: str
    summary: RunningSummary | None
    summarized_messages: list[AnyMessage]


class Prompt(str, Enum):
    """
    提示模板内容的枚举类。

    Members:
        CHAT_PROMPT: 默认聊天的提示。
        INITIAL_SUMMARY_PROMPT: 初次摘要的提示。
        EXISTING_SUMMARY_PROMPT: 更新现存摘要的提示。
        FINAL_PROMPT: 让聊天机器人结合摘要进行回复的提示。
    """
    CHAT_PROMPT = "chat_prompt"
    INITIAL_SUMMARY_PROMPT = "initial_summary_prompt"
    EXISTING_SUMMARY_PROMPT = "existing_summary_prompt"
    FINAL_PROMPT = "final_prompt"