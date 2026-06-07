import os
import asyncio
import yaml
from typing import Any
from glob import glob
from psycopg.rows import dict_row
from psycopg_pool import AsyncConnectionPool
from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langgraph.graph import START, StateGraph
from langgraph.graph.state import CompiledStateGraph
from langmem.short_term import summarize_messages
from core.state import State, Prompt


class PromptManager:
    """
    用于加载和管理提示。

    Attributes:
        prompts (dict[str, dict[str, ChatPromptTemplate]]): 存储所有语言的所有提示的字典。通过self.prompts["language"]["prompt_name"]的方式来调用指定的模板。
    """
    prompts: dict[str, dict[str, ChatPromptTemplate]]

    def __init__(self):
        self.prompts = self.load_prompts()

    def load_prompts(self) -> dict[str, dict[str, ChatPromptTemplate]]:
        """
        从 yaml 文件中加载提示模板。

        Returns:
            dict[str, dict[str, ChatPromptTemplate]]: 存储所有语言的所有提示的字典。
        """
        prompts = {}    # 将要返回的字典
        yaml_files = glob(os.path.join(f"{os.environ['PROJECT_DIR']}/prompts/", "*.yaml"))  # 加载模板目录下的所有模板文件

        # 一个模板文件对应一种语言的提示，载入每种语言的提示
        for file_path in yaml_files:
            language_code = os.path.splitext(os.path.basename(file_path))[0]    # 获取文件名作为语言代码
            current_prompts = {}    # 本轮循环中所加载的语言的模板保存在此字典

            # 读取本轮的模板文件
            with open(file_path, "r", encoding="utf-8") as f:
                current_file = yaml.safe_load(f)

                # 载入默认聊天的提示
                current_prompts["chat_prompt"] = ChatPromptTemplate.from_messages([
                    ("system", current_file.get("chat_prompt", {})["system"]),
                    MessagesPlaceholder(variable_name="messages"),
                ])

                # 载入初次摘要的提示
                current_prompts["initial_summary_prompt"] = ChatPromptTemplate.from_messages([
                        ("system", current_file.get("initial_summary_prompt", {})["system"]),
                        ("placeholder", "{messages}"),
                    ])

                # 载入更新现存摘要的提示
                current_prompts["existing_summary_prompt"] = ChatPromptTemplate.from_messages([
                        ("system", current_file.get("existing_summary_prompt", {})["system"]),
                        ("placeholder", "{messages}"),
                    ])

                # 载入让聊天机器人结合摘要进行回复的提示
                current_prompts["final_prompt"] =  ChatPromptTemplate.from_messages([
                        ("placeholder", "{system_message}"),
                        ("system", current_file.get("final_prompt", {})["system"]),
                        ("placeholder", "{messages}"),
                    ])
                
            # 将本轮的结果加入到带返回的字典
            prompts[language_code] = current_prompts
        
        # 返回装载完成的字典
        return prompts
    
    def get(self, prompt: Prompt, language: str) -> dict[str, dict[str, ChatPromptTemplate]]:
        """
        获取指定的提示。

        Args:
        prompt (Prompt): 将要获取的提示的类型（枚举）。
        language (str): 将要获取的提示的语言。

        Returns:
            dict[str, dict[str, ChatPromptTemplate]]: 存储所有语言的所有提示模板的字典。通过dict[language][prompt]的方式来调用指定的模板。
        """
        return self.prompts[language][prompt.value]
    

class LazyCompiledGraph:
    """
    CompiledStateGraph 的异步延迟初始化代理。

    对外继续提供 graph.astream(...) 等调用方式，避免修改项目中的调用方。
    真正的数据库连接池、AsyncPostgresSaver 和状态图会在第一次异步调用时，
    于当前正在运行的事件循环中完成初始化。
    """

    def __init__(self, manager: "GraphManager"):
        self._manager = manager

    def astream(self, *args, **kwargs):
        """保持 CompiledStateGraph.astream() 的异步迭代接口。"""
        async def stream_generator():
            graph = await self._manager.get_compiled_graph()
            async for item in graph.astream(*args, **kwargs):
                yield item

        return stream_generator()

    async def ainvoke(self, *args, **kwargs):
        """兼容 CompiledStateGraph.ainvoke()。"""
        graph = await self._manager.get_compiled_graph()
        return await graph.ainvoke(*args, **kwargs)

    def astream_events(self, *args, **kwargs):
        """兼容 CompiledStateGraph.astream_events()。"""
        async def event_generator():
            graph = await self._manager.get_compiled_graph()
            async for item in graph.astream_events(*args, **kwargs):
                yield item

        return event_generator()

    async def abatch(self, *args, **kwargs):
        """兼容 CompiledStateGraph.abatch()。"""
        graph = await self._manager.get_compiled_graph()
        return await graph.abatch(*args, **kwargs)

    async def aget_state(self, *args, **kwargs):
        """兼容 CompiledStateGraph.aget_state()。"""
        graph = await self._manager.get_compiled_graph()
        return await graph.aget_state(*args, **kwargs)

    async def aupdate_state(self, *args, **kwargs):
        """兼容 CompiledStateGraph.aupdate_state()。"""
        graph = await self._manager.get_compiled_graph()
        return await graph.aupdate_state(*args, **kwargs)


class GraphManager:
    """
    本系统的核心组件，用于加载 LangChain 和 LangGraph 的各种组件，创建并编译状态图。

    Attributes:
        prompt_manager (PromptManager): 多语言支持的提示模板管理器。
        llms (dict[str, BaseChatModel]): 存储大语言模型对象的字典。
        db_saver (db_saver): Postgres 数据库存储器。
        graph (CompiledStateGraph): 编译完成的 LangGraph 状态图。
    """
    prompt_manager: PromptManager
    llms: dict[str, BaseChatModel]
    db_pool: AsyncConnectionPool | None
    db_saver: AsyncPostgresSaver | None
    graph: LazyCompiledGraph

    def __init__(self):
        self.prompt_manager = PromptManager()
        self.llms = self.load_llm()

        # 保持旧项目的公开接口：构造完成后 graph 始终可调用。
        self.graph = LazyCompiledGraph(self)

        # 真正的异步对象在第一次 graph.astream()/ainvoke() 时初始化。
        self.db_pool = None
        self.db_saver = None
        self._compiled_graph: CompiledStateGraph | None = None
        self._initialization_lock: asyncio.Lock | None = None

    def load_llm(self) -> dict[str, BaseChatModel]:
        """
        加载大语言模型对象。

        Returns:
            dict[str, BaseChatModel]: 存储大语言模型对象的字典。通过'summarize' 和 'chatbot' 来获取。
        """
        return {
            # 用于摘要的 DeepSeek 大语言模型对象
            "summarize": init_chat_model(
                model_provider = "deepseek",
                model = os.environ["DEEPSEEK_API_MODEL"],
                temperature = 0.2,
                streaming = False,
                max_tokens = 512,
                ),
            # 用于聊天的 DeepSeek 大语言模型对象
            "chatbot": init_chat_model(
                model_provider = "deepseek",
                model = os.environ["DEEPSEEK_API_MODEL"],
                temperature = 1.0,
                streaming = True,
                max_tokens = 256,
                ),
            }  

    async def load_db_saver(self) -> AsyncPostgresSaver:
        """
        在当前正在运行的事件循环中加载异步 Postgres 数据库存储器。

        Returns:
            AsyncPostgresSaver: 异步的 Postgres 数据库存储器对象。
        """
        username = os.environ["POSTGRES_USERNAME"]
        password = os.environ["POSTGRES_PASSWORD"]
        host = os.environ["POSTGRES_HOST"]
        port = os.environ["POSTGRES_PORT"]
        max_size = int(os.environ["POSTGRES_MAX_SIZE"])

        self.db_pool = AsyncConnectionPool(
            conninfo=(
                f"postgresql://{username}:{password}"
                f"@{host}:{port}/checkpoints"
            ),
            min_size=1,
            max_size=max_size,
            open=False,
            kwargs={
                "autocommit": True,
                "prepare_threshold": 0,
                "row_factory": dict_row,
            },
        )

        await self.db_pool.open()

        db_saver = AsyncPostgresSaver(self.db_pool)
        await db_saver.setup()
        return db_saver

    async def get_compiled_graph(self) -> CompiledStateGraph:
        """
        获取真正的 CompiledStateGraph。

        首次调用时异步初始化数据库连接池、数据库存储器和状态图；
        后续调用直接复用已初始化的对象。
        """
        if self._compiled_graph is not None:
            return self._compiled_graph

        # asyncio.Lock 在运行中的事件循环内创建，避免绑定错误的循环。
        if self._initialization_lock is None:
            self._initialization_lock = asyncio.Lock()

        async with self._initialization_lock:
            if self._compiled_graph is None:
                self.db_saver = await self.load_db_saver()
                self._compiled_graph = self.load_graph()

        return self._compiled_graph

    async def shutdown(self) -> None:
        """
        可选的显式资源释放方法。
        旧项目无需为了运行而调用；若以后增加 FastAPI lifespan，可在关闭时调用。
        """
        if self.db_pool is not None:
            await self.db_pool.close()
            self.db_pool = None

    def load_graph(self) -> CompiledStateGraph:
        """
        使用已经初始化的 AsyncPostgresSaver 编译 LangGraph。

        Returns:
            CompiledStateGraph: 编译完成的 LangGraph 状态图对象。
        """
        if self.db_saver is None:
            raise RuntimeError("AsyncPostgresSaver has not been initialized.")

        graph = StateGraph(State)
        graph.add_node("summarize", self.call_summarize)
        graph.add_node("chatbot", self.call_chatbot)
        graph.add_edge(START, "summarize")
        graph.add_edge("summarize", "chatbot")
        return graph.compile(checkpointer=self.db_saver)

    def call_summarize(self, state: State) -> dict[str, Any]:
        """
        摘要（summarize）节点的回调方法。
        当 token 累计数量到达指定标准时，会对历史消息进行摘要，摘要内容将作为新的提示的一部分作为聊天机器人节点的输入，以此优化性能。

        Args:
        state (State): 节点之间传递的状态信息。

        Returns:
            dict[str, Any]: 要更新的状态信息，根据 Langgraph 的机制，此处返回的内容会对状态图的状态进行增量更新。
        """
        # 如果token长度大于指定值，则触发历史消息摘要
        summarization_result = summarize_messages(
            state["messages"],
            running_summary = state.get("summary"),
            model = self.llms["summarize"],
            max_tokens = 512,
            max_tokens_before_summary = 1024,
            max_summary_tokens = 384,
            initial_summary_prompt = self.prompt_manager.get(Prompt.INITIAL_SUMMARY_PROMPT, state["language"]),
            existing_summary_prompt = self.prompt_manager.get(Prompt.EXISTING_SUMMARY_PROMPT, state["language"]),
            final_prompt = self.prompt_manager.get(Prompt.FINAL_PROMPT, state["language"]),
            )

        # 返回要更新的状态，其中 summarized_messages 是聊天机器人的输入，summary 是摘要
        state_update = {"summarized_messages": summarization_result.messages}
        # 如果有摘要则更新
        if summarization_result.running_summary:
            state_update["summary"] = summarization_result.running_summary
        return state_update

    def call_chatbot(self, state) -> dict[str, Any]:
        """
        聊天机器人（chatbot）节点的回调方法。
        根据传入的提示和历史消息，调用大语言模型生成新的回复。

        Args:
        state (State): 节点之间传递的状态信息。

        Returns:
            dict[str, Any]: 要更新的状态信息，根据 Langgraph 的机制，此处返回的内容会对状态图的状态进行增量更新。
        """
        # 加入默认的聊天提示模板
        prompt_messages = self.prompt_manager.get(Prompt.CHAT_PROMPT, state["language"]).invoke(state["summarized_messages"])
        # 执行用于聊天的大语言模型
        response = self.llms["chatbot"].invoke(prompt_messages)
        # 返回要更新的状态，message 为所有历史消息
        # 此处的response为大模型输出的最新消息，按照 Langgraph 的机制，此处返回后会对状态进行增量更新
        return {"messages": [response]}