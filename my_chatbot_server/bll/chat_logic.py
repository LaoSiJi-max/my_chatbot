from typing import Any, List
from collections.abc import AsyncGenerator
from langchain_core.messages import HumanMessage, AIMessage
from core.graph import GraphManager


class ChatLogic:
    """
    聊天服务的业务逻辑类。

    Attributes
        graph_manager (GraphManager): LangGraph 的状态图管理器，里面装载了 LangChain 的核心组件。
    """

    graph_manager: GraphManager

    def __init__(self):
        self.graph_manager = GraphManager()

    async def get_reply(self, user_message: str, thread_id: str, callbacks: List[Any], language: str) -> AIMessage:
        """
        获取聊天机器人的最新回复，以非流式输出的结果返回的业务逻辑。

        Args:
            user_message (str): 用户发送的消息内容。
            thread_id (str): 对话线程的ID。
            callbacks (List[Any]): 回调函数的列表。
            language (Optional[str]): 用户的语言首选项。

        Returns:
            AIMessage: 聊天机器人的最新回复。
        """
        # 按 langchain 的标准构建参数
        input = {"messages": [HumanMessage(user_message)], "language": language}  # 消息和语言（此处的语言参数用于控制大模型的输出语言）
        config =  {"configurable": {"thread_id": thread_id,             # 线程id
                                    "language": language,},  # 语言（此处的语言参数会传递到 graph）
                   "callbacks": callbacks,      # 回调函数
                   }

        # 发送请求
        result = await self.graph_manager.graph.ainvoke(input, config)
    
        # 仅返回最后一条消息，这是 AI 回复的最新消息
        return result["messages"][-1]

    async def get_stream_reply(self, user_message: str, thread_id: str, callbacks: List[Any], language: str) -> AsyncGenerator[str, None]:
        """
        获取聊天机器人的最新回复，并以流式输出返回的业务逻辑。

        Args:
            user_message (str): 用户发送的消息内容。
            thread_id (str): 对话线程的ID。
            callbacks (List[Any]): 回调函数的列表。
            language (Optional[str]): 用户的语言首选项。

        Yields:
            str: 聊天机器人最新回复的每一个 token 输出。
        """
        # 按 langchain 的标准构建参数
        input = {"messages": [HumanMessage(user_message)], "language": language}  # 消息和语言（此处的语言参数用于控制大模型的输出语言）
        config =  {"configurable": {"thread_id": thread_id,             # 线程id
                                    "language": language,},  # 语言（此处的语言参数会传递到 graph）
                   "callbacks": callbacks,      # 回调函数
                   }
        stream_mode = "messages"    # 流的输出模式

        # 发送请求并返回一个流的迭代器
        token_generator = self.graph_manager.graph.astream(input, config, stream_mode=stream_mode)

        # 仅从迭代中筛选消息内容返回，剥离其他内容
        async for token, metadata in token_generator:
            if metadata["langgraph_node"] == "chatbot":
                yield token.content

    async def get_history_for_streamlit(self, thread_id: str) -> list[dict[str, str]]:
        """
        接收一个线程 ID，并以 streamlit 所支持的格式返回此线程 ID对应的所有聊天记录的业务逻辑。

        Args:
            thread_id (str): 线程 ID。

        Returns:
            list[dict[str, str]]: 存储聊天记录的列表。每条记录为包含 'role' 和 'content' 字段的字典，其中 'role' 为 'user' 或 'assistant'。
        """
        # 获取快照
        snapshot = await self.graph_manager.db_saver.aget({"configurable": {"thread_id": thread_id}})

        # 转化成streamlit需要的格式
        messages = []
        if snapshot:
            messages = [
                {"role": "user" if isinstance(m, HumanMessage) else "assistant", "content": m.content} for m in snapshot["channel_values"]["messages"]
            ]
        
        # 返回结果
        return messages