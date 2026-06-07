import streamlit as st
from tools.i18n import I18n
from tools.text_utils import shorten_text
from controller.auth_controller import AuthController
from controller.chat_controller import ChatController


def refresh_user_msg():
    """
    更新用户信息。

    """
    # 请求更新用户信息
    tips, user_message = AuthController.get_user_message(st.session_state.access_token, st.session_state.language)

    # 需要显示提示的时候则显示
    if tips:
        st.toast(tips, icon="✅" if user_message else "❌")

    # 获取成功的时候，同步到 user_message
    if user_message:
        st.session_state.username = user_message["email"]
        st.session_state.language = user_message["language"]
        st.session_state.chats = user_message["chats"]


# 设置默认值
st.session_state.setdefault("language", "en_us")    # 每个页面都必须设置语言的默认值
st.session_state.setdefault("access_token", None)   # 令牌是否存在控制用户是否登陆的状态


# 如果检测到令牌存在，则判定用户已经登陆，渲染聊天页面
if st.session_state.get("access_token"):

    # 修改样式
    st.markdown("""
    <style>
    /* 调整 sidebar 的宽度 */
    section[data-testid="stSidebar"] {
        width: 320px !important;  /* 原来是 ~250px */
    }

    /* 同时调整主区间距，防止压缩主内容 */
    section.main {
        margin-left: 320px;  /* 比 sidebar 宽度略大 */
    }
    </style>
    """, unsafe_allow_html=True)

    # 会话列表
    st.sidebar.title("💬" + I18n.get("chat_list", st.session_state.language))   # 会话列表的标题

    # 新建会话的按钮
    if st.sidebar.button("➕" + I18n.get("chat_new", st.session_state.language), key="new_chat_button"):
        st.session_state.thread_id = None    # 线程 ID 为 None 的时候，表示当前没有当前处于活动中的会话，将判定为需要为用户开启新会话
        st.rerun()

    # 分割线
    st.sidebar.markdown("---")

    # 载入已有的会话
    for chat in st.session_state.chats:
        cols = st.sidebar.columns([0.6, 0.2, 0.2])

        # 局部变量
        is_selected = (st.session_state.get("thread_id") == chat["thread_id"])          # 用来判定本轮渲染的会话是否被用户选中
        is_editing = (st.session_state.get("editing_thread_id") == chat["thread_id"])   # 用来判定本轮渲染的会话是否处于重命名状态

        # 显示会话名的按钮，点击后将次会话设置为处于活动中的会话
        with cols[0]:
            # 如果是处于重命名状态中
            if is_editing:
                # 渲染一个输入框，用来接收会话的新名字
                new_tread_name = st.text_input(label="thread_name", value=chat["thread_name"], key=f"edit_input_{chat['thread_id']}", label_visibility="collapsed")
            # 如果并非出于重命名状态中
            else:
                # 渲染一个按钮，用户点击后，将当前会话设置为当前处于活动中的会话，存储到 session_state 中的 thread_id
                if st.button(shorten_text(chat["thread_name"], 16), key=f"chat_select_{chat['thread_id']}", type="secondary" if is_selected else "tertiary"):
                    st.session_state.thread_id = chat["thread_id"]
                    st.rerun()

        with cols[1]:
            # 如果是处于重命名状态中
            if is_editing:
                # 此时渲染为确定按钮，点击后提交重命名请求
                if st.button("✅", key=f"confirm_edit_{chat['thread_id']}", type="primary"):
                    # 提交重命名的请求
                    tips, successed = ChatController.chat_rename_chat(
                        st.session_state.access_token,
                        chat["thread_id"], new_tread_name,
                        st.session_state.language,
                        )

                    # 需要显示提示的时候则显示
                    if tips:
                        st.toast(tips, icon="✅" if successed else "❌")

                    # 如果重命名成功
                    if successed:
                        st.session_state.editing_thread_id = None   # 取消编辑状态，清空 session_state 中的值
                        refresh_user_msg()                          # 刷新用户信息
                        st.rerun()
            # 如果并非出于重命名状态中
            else:
                # 此时渲染为编辑按钮，点击后将此会话进入编辑状态
                if st.button("✏️", key=f"chat_edit_{chat["thread_id"]}", type="secondary"):
                    st.session_state.editing_thread_id = chat["thread_id"]  # 设置此会话为编辑状态，同步到 session_state
                    st.rerun()

        with cols[2]:
            # 如果是处于重命名状态中
            if is_editing:
                # 此时渲染为取消按钮，点击后取消编辑状态
                if st.button("✖️", key=f"cancel_edit_{chat['thread_id']}", type="primary"):
                    st.session_state.editing_thread_id = None       # 取消编辑状态，清空 session_state 中的值
                    st.rerun()
            # 如果并非出于重命名状态中
            else:
                # 此时渲染为删除按钮，点击后删除此会话
                if st.button("🗑️", key=f"chat_delete_{chat["thread_id"]}", type="secondary"):
                    # 提交删除请求
                    tips, successed = ChatController.chat_delete_chat(
                        st.session_state.access_token,
                        chat["thread_id"],
                        st.session_state.language
                        )

                    # 需要显示提示的时候则显示
                    if tips:
                        st.toast(tips, icon="✅" if successed else "❌")

                    # 如果成功
                    if successed:
                        # 如果此会话是处于活动中的
                        if is_selected:
                            st.session_state.thread_id = None       # 取消处于活动中的会话状态，清空 session_state 中的值

                        # 刷新用户信息
                        refresh_user_msg()
                        st.rerun()


    # 载入历史消息
    # 如果能从 session_state 中获取到 thread_id，说明此 thread_id 是处于活动中的会话，则载入此历史消息
    if st.session_state.get("thread_id"):
        # 获取历史消息
        tips, history = ChatController.chat_get_history(
            st.session_state.access_token,
            st.session_state.thread_id,
            st.session_state.language
            )

        # 需要显示提示的时候则显示
        if tips:
            st.toast(tips, icon="✅" if history else "❌")

        # 获取成功时（注意：可能是一个空消息列表，但会话存在）
        if history:
            # 遍历以渲染每一条历史消息
            for msg in history:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])


    # 聊天区
    user_message = st.chat_input(I18n.get("input_placeholder", st.session_state.language))  # 输入框，用户将输入到此处和聊天机器人进行聊天

    # 用户输入消息后
    if user_message:
        # 先将用户消息渲染到界面
        with st.chat_message("user"):
                st.markdown(user_message)

        # 如果没有 thread_id，被视为当前没有处于活动中的会话，此时需要新建会话
        if not st.session_state.get("thread_id"):
            # 提交创建新会话的请求
            tips, thread_id = ChatController.chat_create_new_chat(st.session_state.access_token, st.session_state.language)

            # 需要显示提示的时候则显示
            if tips:
                st.toast(tips, icon="✅" if thread_id else "❌")

            # 获取到新的 thread_id 被视为新会话创建成功
            if thread_id:
                st.session_state.thread_id = thread_id      # 将新会话设置为处于活动中的会话，同步到 session_state
                st.session_state.refresh_user_msg = True    # 设下一个值，以提示后续需要刷新用户信息
            
        # 重点：渲染聊天机器人以流式输出的方式回复，以避免用户等待
        with st.chat_message("assistant"):
            # 提示用户正在输出
            with st.spinner(I18n.get("generating", st.session_state.language)):
                # 开始流式输出聊天机器人的最新回复
                st.write_stream(
                    ChatController.chat_stream_reply(
                        user_message,
                        st.session_state.access_token,
                        st.session_state.thread_id,
                        st.session_state.language
                        )
                )

        # 此处用于创建新的会话以后，聊天机器人输出完成后，刷新用户信息
        if st.session_state.get("refresh_user_msg"):
            refresh_user_msg()                          # 刷新用户信息
            st.session_state.refresh_user_msg = None    # 删除用于提示的变量
            st.rerun()


# 登录页面
else:
    # 跳转到登录页面
    st.switch_page("pages/login.py")