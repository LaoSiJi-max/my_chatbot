import httpx
from typing import Any, Generator


class ChatComm:
    """
    聊天接口通信的类。

    """

    @staticmethod
    def call_stream_api(human_message: str, access_token: str, thread_id: str, language: str) -> Generator[str, None, None]:
        """
        调用聊天机器人流式输出回复的通信。

        Args:
            human_message (str): 用户消息。
            access_token (str): 用户的访问令牌。
            thread_id (str): 会话线程 id。
            language (str): 语言代码。

        Returns:
            Generator[str, None]: 以流式输出返回的聊天机器人的最新回复。
        """
        # 参数
        url = "http://localhost:58000/stream/"
        json_data = {
            "user_message": human_message,
            "thread_id": thread_id,
            "callbacks": [],
            "language": language,
        }
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            }

        # 通讯并返回流式输出的迭代器
        with httpx.Client(timeout=20) as client:
            with client.stream("POST", url, json=json_data, headers=headers) as response:
                for chunk in response.iter_text():
                    yield chunk


    @staticmethod
    def call_get_history_api(access_token: str, thread_id: str) -> dict[str, Any]:
        """
        调用获取历史消息的通信。

        Args:
            access_token (str): 用户的访问令牌。
            thread_id (str): 会话线程 id。

        Returns:
            dict[str, Any]: 通信结果和历史消息。
        """
        try:
            # 和接口通信
            with httpx.Client(timeout=15) as client:
                response = client.post(
                    f"http://localhost:58000/get_history/",
                    headers={
                        "Authorization": f"Bearer {access_token}",
                        "Content-Type": "application/json"
                        },
                    json={"thread_id": thread_id},
                )
        
                response.raise_for_status()
                result = response.json()
                
                # 返回结果
                return {"status": "success", "history": result}
        # 服务器异常
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 400:
                return {"status": "auth_failed"}
            else:
                return {"status": "server_error"}
        # 其他异常
        except Exception:
            return {"status": "network_error"}


    @staticmethod
    def call_create_chat_api(access_token: str) -> dict[str, Any]:
        """
        调用新建会话的通信。

        Args:
            access_token (str): 用户的访问令牌。

        Returns:
            dict[str, Any]: 通信结果和刚创建的新会话的 thread_id。
        """
        try:
            # 和接口通信
            with httpx.Client(timeout=15) as client:
                response = client.post(
                    f"http://localhost:58000/create_chat/",
                    headers={
                        "Authorization": f"Bearer {access_token}",
                        "Content-Type": "application/json"
                        },
                    json={},
                )
        
                response.raise_for_status()
                result = response.json()

                result["status"] = "success"
                
                # 返回结果
                return result
        # 服务器异常
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 400:
                return {"status": "auth_failed"}
            else:
                return {"status": "server_error"}
        # 其他异常
        except Exception:
            return {"status": "network_error"}
        
    
    @staticmethod
    def call_delete_chat_api(access_token: str, thread_id: str) -> dict[str, Any]:
        """
        调用删除会话的通信。

        Args:
            access_token (str): 用户的访问令牌。
            thread_id (str): 会话线程 id。

        Returns:
            dict[str, Any]: 通信结果和刚删除成功的新会话的 thread_id。
        """
        try:
            # 和接口通信
            with httpx.Client(timeout=15) as client:
                response = client.post(
                    f"http://localhost:58000/delete_chat/",
                    headers={
                        "Authorization": f"Bearer {access_token}",
                        "Content-Type": "application/json"
                        },
                    json={"thread_id": thread_id},
                )
        
                response.raise_for_status()
                result = response.json()

                result["status"] = "success"
                
                # 返回结果
                return result
        # 服务器异常
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 400:
                return {"status": "auth_failed"}
            else:
                return {"status": "server_error"}
        # 其他异常
        except Exception:
            return {"status": "network_error"}
        

    @staticmethod
    def call_rename_chat_api(access_token: str, thread_id: str, new_thread_name: str) -> dict[str, Any]:
        """
        调用重命名会话的通信。

        Args:
            access_token (str): 用户的访问令牌。
            thread_id (str): 会话线程 id。
            new_thread_name (str): 会话的新名字。

        Returns:
            dict[str, Any]: 通信结果和刚重命名的成功的会话的 thread_id 与会话名。
        """
        try:
            # 和接口通信
            with httpx.Client(timeout=15) as client:
                response = client.post(
                    f"http://localhost:58000/rename_chat/",
                    headers={
                        "Authorization": f"Bearer {access_token}",
                        "Content-Type": "application/json"
                        },
                    json={"thread_id": thread_id, "thread_name": new_thread_name},
                )
        
                response.raise_for_status()
                result = response.json()

                result["status"] = "success"
                
                # 返回结果
                return result
        # 服务器异常
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 400:
                return {"status": "auth_failed"}
            else:
                return {"status": "server_error"}
        # 其他异常
        except Exception:
            return {"status": "network_error"}