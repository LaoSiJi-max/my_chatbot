import streamlit as st
from tools.i18n import I18n
from controller.auth_controller import AuthController


# 设置默认值
st.session_state.setdefault("language", "en_us")    # 每个页面都必须设置语言的默认值


# 样式优化
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
st.markdown(f"<h1 style='text-align: center;'>{I18n.get("register_title", st.session_state.language)}</h1>", unsafe_allow_html=True)

# 设定布局
col1, col2, col3 = st.columns([1, 2, 1])

# 注册表单
with col2:
    with st.form(key="register_form"):
        username = st.text_input(I18n.get("user_id", st.session_state.language), key="register_username")                   # 用户名
        password = st.text_input(I18n.get("password", st.session_state.language), type="password", key="register_password") # 密码
        submit_button = st.form_submit_button(I18n.get("register", st.session_state.language))                              # 提交按钮

    if submit_button:
        # 提交注册
        message = AuthController.register(username, password, st.session_state.language)

        # 显示消息
        st.info(message)