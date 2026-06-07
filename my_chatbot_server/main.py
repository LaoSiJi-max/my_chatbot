"""
系统服务端的入口文件。

加载环境变量，创建 FastAPI 实例，并挂载所有 API 路由。
"""


from dotenv import load_dotenv
# 加载环境变量
load_dotenv()


from fastapi import FastAPI
from api.routes import router


# 创建 API 的 FastAPI 并挂载路由
app_api = FastAPI()
app_api.include_router(router)