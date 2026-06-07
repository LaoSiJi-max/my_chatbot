"""
在控制台环境下运行的调试程序。

"""


import os
import asyncio
import httpx
import getpass


# 参数
API_HOST = "localhost"  # 服务端 IP
API_PORT = 58000        # 端口号

async def test_login(username: str, password: str) -> str | None:
    """
    测试用的登录功能。

    Args:
        username (str): 邮箱地址。
        password (str): 密码。

    Returns:
        str | None: 登录成功时返回 access_token，失败时返回 None。
    """

    async with httpx.AsyncClient() as client:
        try:
            # 登录获取 access_token
            login_resp = await client.post(
                "http://localhost:58001/auth/jwt/login",
                data={"username": username, "password": password},
            )
            login_resp.raise_for_status()
            access_token = login_resp.json()["access_token"]
            print(f"✅ {username} 登录成功。\n")
            return access_token

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                print("❌ 登录失败：用户名或密码错误。\n")
            else:
                print(f"❌ 登录失败，状态码：{e.response.status_code}，错误信息：{e.response.text}\n")
            return None

        except Exception as e:
            print(f"❌ 登录请求发生异常：{str(e)}\n")
            return None
    

async def test_get_history(access_token: str, thread_id: str="temp"):
    """
    测试用的获取历史消息功能。
    对应 thread_id 的历史消息将会输出到控制台。

    Args:
        access_token (str): 合法访问的令牌。
        thread_id (str): 线程 id。
    """
    with httpx.Client(timeout=60) as client:
            response = client.post(
                f"http://{API_HOST}:{API_PORT}/get_history/",
                params={"thread_id": thread_id},
                headers={"Authorization": f"Bearer {access_token}"},
            )

            history = response.json()
        
            for h in history:
                print(f"{h['role']}: {h['content']}")


async def test_reply(human_message: str, access_token: str, thread_id: str="temp", language: str="zh_cn"):
    """
    测试用的非流式输出的回复功能。

    Args:
        human_message (str): 用户的回复。
        access_token (str): 合法访问的令牌。
        thread_id (str): 线程 id。
        language (str): 用户的语言首选项。
    """
    url = f"http://{API_HOST}:{API_PORT}/reply/"

    json_data = {
        "user_message": human_message,
        "thread_id": thread_id,
        "callbacks": [],
        "language": language,
    }

    headers = {"Authorization": f"Bearer {access_token}"}
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=json_data, headers=headers, timeout=60)
        data = response.json()
        print(data["content"])


async def test_stream_reply(human_message: str, access_token: str, thread_id: str="temp", language: str="zh_cn"):
    """
    测试用的流式输出的回复功能。

    Args:
        human_message (str): 用户的回复。
        access_token (str): 合法访问的令牌。
        thread_id (str): 线程 id。
        language (str): 用户的语言首选项。
    """
    url = f"http://{API_HOST}:{API_PORT}/stream/"

    json_data = {
        "user_message": human_message,
        "thread_id": thread_id,
        "callbacks": [],
        "language": language,
    }

    headers = {"Authorization": f"Bearer {access_token}"}

    async with httpx.AsyncClient(timeout=60) as client:
        async with client.stream("POST", url, json=json_data, headers=headers) as response:
            async for chunk in response.aiter_text():
               print(chunk, end="")

    print()


if __name__ == "__main__":
    # 参数设定
    test_target = test_stream_reply #指定希望测试的功能
    thread_id = "temp"  # 线程 id

    print("调试程序已启动。")
    print("请输入用户 id 和密码以登录。\n")

    # 登录环节
    access_token = None
    while access_token is None:
        username = input("用户 id: ")
        password = getpass.getpass("密码: ")    # 使用 getpass 隐藏密码输入
        access_token = asyncio.run(test_login(username, password))
    
    # 清空控制台
    os.system("clear")

    # 载入历史记录
    asyncio.run(test_get_history(access_token, thread_id=thread_id))

    # 聊天环节
    while True:
        human_message = input("user: ")
        print("assistant: ", end="")
        asyncio.run(test_target(human_message, access_token, thread_id=thread_id, language="zh_cn"))