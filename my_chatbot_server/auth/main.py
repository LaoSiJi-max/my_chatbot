"""
用户验证服务端的入口文件。

加载环境变量，创建 FastAPI 实例，并挂载所有 API 路由。
"""


from dotenv import load_dotenv
# 加载环境变量
load_dotenv()

from auth.app import app
app_auth = app