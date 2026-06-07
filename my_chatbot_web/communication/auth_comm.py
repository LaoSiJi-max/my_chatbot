import httpx
from typing import Any


class AuthComm:
    @staticmethod
    def call_login_api(username: str, password: str) -> dict[str, Any]:
        """
        登录验证的通信。

        Args:
            username (str): 邮箱地址
            password (str): 密码

        Returns:
            dict[str, Any]: 包含登录结果和 token 信息的字典
        """
        try:
            # 和接口通信
            with httpx.Client(timeout=10) as client:
                response = client.post(
                    "http://localhost:58001/auth/jwt/login",
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                    data={"username": username, "password": password},
                )
                response.raise_for_status()
                result = response.json()
                
                if result.get("access_token"):
                    result["status"] = "success"
                else:
                    result["status"] = "access_token_failed"

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
    def call_register_api(username: str, password: str, language: str) -> dict[str, Any]:
        """
        注册的通信。

        Args:
            username (str): 邮箱地址
            password (str): 密码

        Returns:
            dict[str, Any]: 包含登录结果和 token 信息的字典
        """
        try:
            # 和接口通信
            with httpx.Client(timeout=10) as client:
                response = client.post(
                    "http://localhost:58001/auth/register",
                    headers={"Content-Type": "application/json"},
                    json={"email": username, "password": password, "language": language}
                )
                response.raise_for_status()
                result = response.json()
                result["status"] = "success"

                # 返回结果
                return result
        # 服务器异常
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 400:
                # 重复注册
                return {"status": "auth_failed"}
            else:
                return {"status": "server_error"}
        # 其他异常
        except Exception:
            return {"status": "network_error"}
        
    @staticmethod
    def call_me_api(access_token: str) -> dict[str, Any]:
        """
        使用 token 获取当前用户信息的通信。

        Args:
            access_token (str): 登录后获得的 JWT 访问令牌。

        Returns:
            dict[str, Any]: 包含用户信息的字典，或错误状态。
        """
        try:
            # 和接口通信
            with httpx.Client(timeout=10) as client:
                response = client.get(
                    "http://localhost:58001/users/me",
                    headers={"Authorization": f"Bearer {access_token}"}
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
    def update_user_api(access_token: str, update_fields: dict[str, str]) -> dict[str, Any]:
        """
        使用 token 更新当前用户信息的通信。

        Args:
            access_token (str): 登录后获得的 JWT 访问令牌。
            update_fields (dict[str, str]): 要更新的字段及其新值，例如 {"language": "ja_jp"}。

        Returns:
            dict[str, Any]: 包含更新结果状态的字典。
        """
        try:
            # 和接口通信
            with httpx.Client(timeout=10) as client:
                response = client.patch(
                    "http://localhost:58001/users/me",
                    headers={
                        "Authorization": f"Bearer {access_token}",
                        "Content-Type": "application/json"
                    },
                    json=update_fields
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