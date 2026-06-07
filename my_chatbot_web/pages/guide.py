import streamlit as st
from tools.i18n import I18n


# 加载介绍文档
st.markdown(I18n.get("project_intro", st.session_state.language))

# 加载架构图
st.image("static/images/system_architecture.png", caption=I18n.get("system_architecture", st.session_state.language))

# 加载架构介绍文档
st.markdown(I18n.get("architecture_intro", st.session_state.language))