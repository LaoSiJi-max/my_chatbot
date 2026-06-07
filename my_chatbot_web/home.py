import streamlit as st
from tools.i18n import I18n
from controller.auth_controller import AuthController


# 设置默认值
st.session_state.setdefault("language", "en_us")    # 每个页面都必须设置语言的默认值

# 语言切换下拉框
with st.popover("🌐"):
    lang_map = {
        "English": "en_us",
        "简体中文": "zh_cn",
        "繁體中文": "zh_tw",
        "日本語": "ja_jp"
    }

    # 语言显示和语言代码的映射字典
    reverse_map = {v: k for k, v in lang_map.items()}
    default_label = reverse_map.get(st.session_state.language, "English")

    # 语言切换下拉框的控件
    lang = st.radio(
        "language selection",                               # 注意此处不能加载国际化资源，否则会出问题，应该是 streamlit 机制不支持导致的
        options=list(lang_map.keys()),                      # 设置选项
        index=list(lang_map.keys()).index(default_label),   # 此处设置选定值和 session_state 同步
        label_visibility="collapsed"                        # 隐藏文字提示
    )

    # 如果检测到切换的举动
    if lang_map[lang] != st.session_state.language:
        st.session_state.language = lang_map[lang]  # 同步设置到 session_state

        # 如果是已登录的用户，还要为用户修改语言首选项
        if st.session_state.get("access_token"):
            # 更新语言首选项
            tips, successed = AuthController.update_language(st.session_state.access_token, st.session_state.language)

            # 需要显示提示的时候则显示
            if tips:
                st.toast(tips, icon="✅" if successed else "❌")

        st.rerun()


def logout():
    # 如果是登陆状态，则清空所有 session_state 中相关的数据
    if st.session_state.get("access_token"):
        st.session_state.access_token = None
        st.session_state.thread_id = None
        st.session_state.username = None
        st.session_state.chats = None
        st.session_state.logout_message = I18n.get("logout_success", st.session_state.language)
    else:
        st.session_state.logout_message = I18n.get("logout_not_logged_in", st.session_state.language)

    st.rerun()
    st.switch_page("pages/login.py")  # 跳转到登录


# 全局的主页导航
if st.session_state.get("access_token"):    # 登陆以后的导航
    pages = {
        I18n.get("section_features", st.session_state.language): [
            st.Page("pages/chat.py", title=I18n.get("chatbot", st.session_state.language)),             # 聊天机器人
            st.Page("pages/guide.py", title=I18n.get("guide", st.session_state.language)),          # 介绍文档
            st.Page(logout, title=I18n.get("logout", st.session_state.language)),                       # 退出登录
        ],
    }
# 登陆之前的导航
else:
    pages = {
        I18n.get("section_features", st.session_state.language): [
            st.Page("pages/login.py", title=I18n.get("login", st.session_state.language)),              # 登录
            st.Page("pages/register.py", title=I18n.get("register_title", st.session_state.language)),  # 注册
            st.Page("pages/guide.py", title=I18n.get("guide", st.session_state.language)),          # 介绍文档
            
        ],
    }

pg = st.navigation(pages, position="top")
pg.run()