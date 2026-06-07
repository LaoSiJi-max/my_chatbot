import streamlit as st
from tools.i18n import I18n
from controller.auth_controller import AuthController


# 设置默认值
st.session_state.setdefault("language", "en_us")    # 每个页面都必须设置语言的默认值
st.session_state.setdefault("access_token", None)   # 令牌是否存在控制用户是否登陆的状态


# 如果检测已经有令牌了，则判定用户已经登陆，切换到聊天页面
if st.session_state.get("access_token"):
    st.switch_page("pages/chat.py")
# 如果没有登陆则渲染登陆页面
else:
    # 修改样式 
    st.markdown("""
    <style>
    button[data-testid="stBaseButton-secondaryFormSubmit"] {
        width: 100% !important;
        font-size: 1.1rem;
        text-align: center;
        background-color: #4CAF50;
        color: white;
        padding: 0.6em 1em;
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

    # 居中标题
    st.markdown(f"<h1 style='text-align: center;'>{I18n.get("login_title", st.session_state.language)}</h1>", unsafe_allow_html=True)

    # 设定布局
    col1, col2, col3 = st.columns([1, 2, 1])

    # 登录表单
    with col2:
        with st.form(key="register_form"):
            username = st.text_input(I18n.get("user_id", st.session_state.language), key="login_username")                      # 用户名
            password = st.text_input(I18n.get("password", st.session_state.language), type="password", key="login_password")    # 密码
            submit_button = st.form_submit_button(I18n.get("login", st.session_state.language))                                 # 提交按钮

        # 点击提交的事件
        if submit_button:
            # 登陆验证的请求
            login_message, access_token = AuthController.login(username, password, st.session_state.language)

            # 显示消息
            st.info(login_message)

            # 当获取到令牌，说明登陆成功
            if access_token:
                st.session_state.access_token = access_token    # 将令牌同步到 session_state

                # 请求更新用户信息
                tips, user_message = AuthController.get_user_message(st.session_state.access_token, st.session_state.language)

                # 获取成功的时候，同步到 user_message
                if user_message:
                    st.session_state.username = user_message["email"]
                    st.session_state.language = user_message["language"]
                    st.session_state.chats = user_message["chats"]

                st.rerun()