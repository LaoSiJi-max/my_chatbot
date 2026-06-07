import uuid
from typing import Any
from copy import deepcopy
from datetime import datetime
from wcwidth import wcswidth
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi import HTTPException
from tools.i18n import normalize_language
from tools.validation import validate_thread_id
from bll.chat_logic import ChatLogic
from api.models import ReplyRequest, ThreadRequest
from auth.db import User, get_user_db
from auth.users import current_active_user


router = APIRouter()
chat_service = ChatLogic()


@router.post("/reply/")
async def reply(reply_info: ReplyRequest, user: User = Depends(current_active_user)) -> dict[str, Any]:
    """
    接收用户输入消息，并返回聊天机器人的回复。
    此接口为非流式对话接口，每次调用仅返回一条完整回复。
    如需流式输出，请使用 /stream/` 接口。

    Args:
        info (ReplyRequest): 封装了用户消息、线程 ID、回调函数和语言首选项的模型。
        user (User, optional): 当前认证的用户对象，由依赖注入获得。仅认证通过的用户才会被传入此参数。

    Returns:
        dict[str, Any]: 聊天机器人的回复结果，结构为 langchain_core.messages.ai.AIMessage 类格式的字典化结果。
    """
    # 校验并处理
    # 校验 thread_id 是否符合 uuid4 规范
    if not validate_thread_id(reply_info.thread_id):
        raise HTTPException(status_code=400, detail="Invalid 'thread_id' format.")
    
    # 整理语言首选项
    reply_info.language = normalize_language(reply_info.language)

    # 调用获取回复的业务逻辑
    reply = await chat_service.get_reply(reply_info.user_message, reply_info.thread_id, reply_info.callbacks, reply_info.language)

    # 转换为字典并返回
    return reply.model_dump()


@router.post("/stream/")
async def stream(reply_info: ReplyRequest, user: User = Depends(current_active_user)) -> StreamingResponse:
    """
    接收用户输入消息，并以流式输出返回聊天机器人的回复。

    Args:
        info (ReplyRequest): 封装了用户消息、线程 ID、回调函数和语言首选项的模型。
        user (User, optional): 当前认证的用户对象，由依赖注入获得。仅认证通过的用户才会被传入此参数。

    Returns:
        StreamingResponse: 以流式输出返回聊天机器人的回复结果。
    """
    # 校验并处理
    # 校验 thread_id 是否符合 uuid4 规范
    if not validate_thread_id(reply_info.thread_id):
        raise HTTPException(status_code=400, detail="Invalid 'thread_id' format.")
    
    # 整理语言首选项
    reply_info.language = normalize_language(reply_info.language)

    # 获取迭代器
    token_generator = chat_service.get_stream_reply(reply_info.user_message, reply_info.thread_id, reply_info.callbacks, reply_info.language)

    # 返回流
    return StreamingResponse(token_generator, media_type="text/plain")


@router.post("/get_history/")
async def get_history(thread_info: ThreadRequest, user: User = Depends(current_active_user)) -> list[dict[str, str]]:
    """
    接收一个线程 ID，并返回此线程 ID对应的所有聊天记录。
    注意：此接口仅用于 streamlit。

    Args:
        thread_info (ThreadRequest): 线程 ID 信息。
        user (User, optional): 当前认证的用户对象，由依赖注入获得。仅认证通过的用户才会被传入此参数。

    Returns:
            list[dict[str, str]]: 存储聊天记录的列表。每条记录为包含 'role' 和 'content' 字段的字典，其中 'role' 为 'user' 或 'assistant'。
    """
    # 校验并处理
    # 校验 thread_id 是否符合 uuid4 规范
    if not validate_thread_id(thread_info.thread_id):
        raise HTTPException(status_code=400, detail="Invalid 'thread_id' format.")
    
    # 校验当前用户是否拥有该 thread_id
    if not any(chat.get("thread_id") == thread_info.thread_id for chat in (user.chats or [])):
        raise HTTPException(status_code=403, detail="Access denied: thread_id does not belong to user.")
    
    return await chat_service.get_history_for_streamlit(thread_info.thread_id)


@router.post("/create_chat/")
async def create_chat(user: User = Depends(current_active_user), user_db: SQLAlchemyUserDatabase = Depends(get_user_db)) -> dict[str, Any]:
    """
    为当前用户生成一个新的会话并插入会话列表。

    Args:
        user (User): 当前认证用户。
        user_db (SQLAlchemyUserDatabase): 用户数据库操作对象。

    Returns:
        dict[str, Any]: 包含新生成的 thread_id 的字典或失败信息。
    """
    # 创建一个新的 uuid，并加入到字典
    new_thread_id = str(uuid.uuid4())
    new_chat = {"thread_id": new_thread_id, "thread_name": datetime.now().strftime("%Y-%m-%d %H:%M")}

    # 插入新会话的记录
    new_chats = deepcopy(user.chats or [])
    new_chats.insert(0, new_chat)
    
    # 提交更新
    await user_db.update(user, {"chats": new_chats})

    # 返回
    return {"thread_id": new_thread_id}


@router.post("/delete_chat/")
async def delete_chat(thread_info: ThreadRequest, user: User = Depends(current_active_user), user_db: SQLAlchemyUserDatabase = Depends(get_user_db)) -> dict[str, Any]:
    """
    删除指定 thread_id 的会话。

    Args:
        thread_info (ThreadRequest): 线程 ID 信息。
        user (User): 当前认证用户。
        user_db (SQLAlchemyUserDatabase): 用户数据库操作对象。

    Returns:
        dict[str, Any]: 包含新生成的 thread_id 的字典或失败信息。
    """
    # 校验并处理
    # 校验 thread_id 是否符合 uuid4 规范
    if not validate_thread_id(thread_info.thread_id):
        raise HTTPException(status_code=400, detail="Invalid 'thread_id' format.")

    # 删除指定的会话的记录
    new_chats = [chat for chat in user.chats if chat["thread_id"] != thread_info.thread_id]
    
    # 提交更新
    await user_db.update(user, {"chats": new_chats})

    # 返回
    return {"deleted_thread_id": thread_info.thread_id}


@router.post("/rename_chat/")
async def rename_chat(thread_info: ThreadRequest, user: User = Depends(current_active_user), user_db: SQLAlchemyUserDatabase = Depends(get_user_db)) -> dict[str, Any]:
    """
    重命名指定 thread_id 的会话的名称。

    Args:
        thread_info (ThreadRequest): 线程 ID 信息。
        user (User): 当前认证用户。
        user_db (SQLAlchemyUserDatabase): 用户数据库操作对象。

    Returns:
        dict[str, Any]: 包含新生成的 thread_id 的字典或失败信息。
    """
    # 校验并处理
    # 校验 thread_id 是否符合 uuid4 规范
    
    if not validate_thread_id(thread_info.thread_id):
        raise HTTPException(status_code=400, detail="Invalid 'thread_id' format.")
    
    if not thread_info.thread_name or wcswidth(thread_info.thread_name) > 16:
        raise HTTPException(status_code=400, detail="'thread name' must not be empty or exceed 16 characters.")
    
    # 修改指定的会话的记录
    new_chats = deepcopy(user.chats or [])
    updated = False

    for chat in new_chats:
        if chat["thread_id"] == thread_info.thread_id:
            chat["thread_name"] = thread_info.thread_name
            updated = True
            break
    
    if not updated:
        raise HTTPException(status_code=400, detail="'thread_id' not found.")
    
    # 提交更新
    await user_db.update(user, {"chats": new_chats})

    # 返回
    return {"renamed_thread_id": thread_info.thread_id, "new_name": thread_info.thread_name}