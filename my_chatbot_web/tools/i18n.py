class I18n:
    """
    管理国际化资源的类。

    Attributes:
        RESOURCES (dict[str, dict[str, str]]): 保存国际化资源的字典。
    """

    RESOURCES: dict[str, dict[str, str]] = {
        # English
        "en_us": {
            "language": "Language",
            "user_id": "User ID",
            "password": "Password",
            "login_title": "User Login",
            "register_title": "User Registration",
            "login": "Login",
            "logout": "Logout",
            "register": "Register",
            "input_placeholder": "Please enter your message here",
            "generating": "Generating response...",
            "invalid_username": "Invalid username format. Please enter a valid email.",
            "invalid_password": "Invalid password format. Must be at least 6 characters, including letters and numbers.",
            "login_success": "Login successful. Welcome, {username}!",
            "login_failure": "Login failed. Incorrect username or password.",
            "login_unauthorized": "Unauthorized login attempt.",
            "login_server_error": "Login failed due to server error.",
            "login_network_error": "Login failed due to network or system error.",
            "login_unknown_error": "Login failed due to an unknown error.",
            "logout_success": "You have successfully logged out.",
            "logout_not_logged_in": "You are not logged in.",
            "register_success": "Registration successful!",
            "user_exists": "User already exists.",
            "register_server_error": "Registration failed due to server error.",
            "register_network_error": "Registration failed due to network or system error.",
            "register_unknown_error": "Registration failed due to an unknown error.",
            "me_failure": "Failed to retrieve user information. Please try again.",
            "me_is_not_active": "This user has been deactivated.",
            "language_update_failed": "Failed to update language preference.",
            "get_history_failed": "Failed to load chat history.",
            "chat_list": "Chat List",
            "chat_new": "Start New Chat",
            "chat_create_success": "New chat created successfully.",
            "chat_create_failed": "Failed to create new chat.",
            "chat_delete_success": "Chat deleted successfully.",
            "chat_delete_failed": "Failed to delete chat. Please try again later.",
            "chat_name_to_long": "Chat name is too long.",
            "chat_name_empty": "Chat name cannot be empty.",
            "chat_rename_success": "Chat renamed successfully.",
            "chat_rename_failed": "Failed to rename chat. Please try again later.",
            "section_features": "Main Features",
            "guide": "Introduction",
            "chatbot": "Chatbot",
            "system_architecture": "System Architecture",
            "project_intro": """# Project Introduction: Chatbot System (Preview Version)

This system is a preview version of a chatbot platform, providing basic account management, conversation management, and streaming message interaction experience, with multi-language support. The following core features have been implemented:

- ✅ Streamlit frontend interaction experience  
- ✅ Basic user registration and authentication  
- ✅ Multi-turn contextual conversation memory  
- ✅ Each user can create, delete, and rename multiple independent conversation threads  
- ✅ Supports interface switching among English, Simplified Chinese, Traditional Chinese, and Japanese  

---

## 🛠️ Core Technologies

This project adopts a frontend-backend separated architecture:

### 🖥️ Frontend  
- Built with [Streamlit](https://streamlit.io/) for a simple and intuitive user interface.  

### 🗄️ Backend  
- Built with [FastAPI](https://fastapi.tiangolo.com/) for high-performance APIs.  
- Conversation management logic is based on [LangChain](https://www.langchain.com/) and [LangGraph](https://docs.langchain.com/langgraph/).  
- Integrated with [DeepSeek](https://deepseek.com/) large language model.  
- Communication method: Standard HTTP API.  
- Database: [PostgreSQL](https://www.postgresql.org/) for storing user data and conversation records.  

---
""",
            "architecture_intro": """## 🧱 Project Architecture Overview

### 🖥️ Frontend Structure

1. **`pages` layer**  
   The view layer. A Streamlit-based web UI responsible for rendering pages and enabling user interactions.  
2. **`controller` layer**  
   The controller layer handles business logic behind UI components, decoupling the view from logic. It processes user inputs and prepares them for the next layer.  
3. **`communication` layer**  
   The communication layer interacts with the backend Web API via HTTP and passes the results and returned data to the controller layer.

### 🗄️ Backend Structure

4. **`api` layer** (Interface Layer)  
   Divided into two parts:  
   - **4.1 `Chat API` (api)**: Chat service interface built with FastAPI, responsible for receiving requests, parameter validation, message replies, history lookup, and session management.  
   - **4.2 `Authorize API` (auth)**: User authentication interface built with FastAPI-Users, responsible for user registration, login, info management, and access control.  
5. **`bll` layer** (Business Logic Layer)  
   Encapsulates the logic for calling LangChain and LangGraph, processes returned data, and ensures business flow correctness and result stability.  
6. **`core` layer** (Core Layer)  
   The core of the system. Manages LangChain / LangGraph resources, constructs LangGraph workflows, and integrates with DeepSeek API and PostgreSQL database.  
"""
        },

        # 简体中文
        "zh_cn": {
            "language": "语言",
            "user_id": "用户 id",
            "password": "密码",
            "login_title": "用户登录",
            "register_title": "用户注册",
            "login": "登录",
            "logout": "退出登录",
            "register": "注册",
            "input_placeholder": "请在此输入内容",
            "generating": "正在输入...",
            "invalid_username": "用户名格式错误，请输入有效邮箱。",
            "invalid_password": "密码格式错误，需至少6位，包含数字和字母。",
            "login_success": "登录成功，您好，{username}！",
            "login_failure": "登录失败，用户名或密码错误。",
            "login_unauthorized": "非法登录。",
            "login_server_error": "由于服务器错误，登录失败。",
            "login_network_error": "由于网络或系统错误，登录失败。",
            "login_unknown_error": "由于未知错误，登录失败。",
            "logout_success": "您已成功退出登录。",
            "logout_not_logged_in": "您尚未登录。",
            "register_success": "注册成功！",
            "user_exists": "该用户已存在。",
            "register_server_error": "由于服务器错误，注册失败。",
            "register_network_error": "由于网络或系统错误，注册失败。",
            "register_unknown_error": "由于未知错误，注册失败。",
            "me_failure": "获取用户信息失败，请重试。",
            "me_is_not_active": "该用户已被禁用。",
            "language_update_failed": "语言首选项更新失败。",
            "get_history_failed": "载入历史消息失败。",
            "chat_list": "会话列表",
            "chat_new": "开启新会话",
            "chat_create_success": "成功创建新会话。",
            "chat_create_failed": "创建新会话失败。",
            "chat_delete_success": "删除会话成功。",
            "chat_delete_failed": "删除会话失败，请稍后重试。",
            "chat_name_to_long": "会话名长度过长。",
            "chat_name_empty": "会话名不能为空。",
            "chat_rename_success": "重命名会话成功。",
            "chat_rename_failed": "重命名会话失败，请稍后重试。",
            "section_features": "主要功能",
            "guide": "项目介绍",
            "chatbot": "聊天机器人",
            "system_architecture": "系统架构图",
            "project_intro": """# 项目介绍：聊天机器人系统（预览版）

本系统为一个预览版的聊天机器人平台，提供基本的账户管理、对话管理与消息流式交互体验，支持多语言。当前已实现以下核心功能：

- ✅ Streamlit 前端交互体验
- ✅ 基本的用户注册与身份验证
- ✅ 多轮上下文记忆对话
- ✅ 每位用户可创建、删除、重命名多个独立会话线程
- ✅ 支持英语、简体中文、繁体中文、日语四种语言界面的切换

---

## 🛠️ 核心技术

本项目采用前后端分离架构：

### 🖥️ 前端
- 基于 [Streamlit](https://streamlit.io/) 实现简洁直观的用户界面。

### 🗄️ 后端
- 使用 [FastAPI](https://fastapi.tiangolo.com/) 构建高性能 API。
- 对话管理逻辑基于 [LangChain](https://www.langchain.com/) 与 [LangGraph](https://docs.langchain.com/langgraph/)。
- 接入 [DeepSeek](https://deepseek.com/) 大语言模型。
- 通信方式：通过标准 HTTP 接口交互。
- 数据库：使用 [PostgreSQL](https://www.postgresql.org/) 存储用户信息与对话记录。

---
""",
            "architecture_intro": """## 🧱 项目架构介绍

### 🖥️ 前端结构

1. **`pages` 层**  
   视图层，基于 Streamlit 实现的 Web 用户界面，负责页面的渲染与展示，用于用户交互操作。
2. **`controller` 层**  
   控制器层，负责视图层控件背后的业务逻辑，实现视图与逻辑的解耦。该层处理用户输入，并为提交到下一层做准备。
3. **`communication` 层**  
   通信层，通过 HTTP 与后端 Web API 进行交互，并将通信结果与返回数据传递给 controller 层。

### 🗄️ 后端结构

4. **`api` 层**（接口层）  
   分为两个部分：
   - **4.1 `Chat API`(api)**：基于 FastAPI 构建的聊天服务接口，负责接收请求、参数校验、消息回复、历史记录查询与会话管理。
   - **4.2 `Authorize API`(auth)**：基于 FastAPI-Users 实现的用户认证接口，负责用户注册、登录、信息管理与访问权限控制。
5. **`bll` 层**（业务逻辑层）  
   封装对 LangChain 与 LangGraph 的调用逻辑，处理返回数据，确保业务流程合理与结果稳定。
6. **`core` 层**（核心层）  
   系统的核心部分。负责管理 LangChain / LangGraph 资源，构建 LangGraph 流程图，并与 DeepSeek API 和 PostgreSQL 数据库进行对接。
""", 
        },

        # 繁体中文
        "zh_tw": {
            "language": "語言",
            "user_id": "使用者 ID",
            "password": "密碼",
            "login_title": "使用者登入",
            "register_title": "使用者註冊",
            "login": "登入",
            "logout": "登出",
            "register": "註冊",
            "input_placeholder": "請在此輸入內容",
            "generating": "正在輸出...",
            "invalid_username": "使用者名稱格式錯誤，請輸入有效的電子郵件。",
            "invalid_password": "密碼格式錯誤，需至少6位，包含數字與字母。",
            "login_success": "登入成功，您好，{username}！",
            "login_failure": "登入失敗，帳號或密碼錯誤。",
            "login_unauthorized": "非法登入。",
            "login_server_error": "由於伺服器錯誤，登入失敗。",
            "login_network_error": "由於網路或系統錯誤，登入失敗。",
            "login_unknown_error": "由於未知錯誤，登入失敗。",
            "logout_success": "您已成功登出。",
            "logout_not_logged_in": "您尚未登入。",
            "register_success": "註冊成功！",
            "user_exists": "該使用者已存在。",
            "register_server_error": "由於伺服器錯誤，註冊失敗。",
            "register_network_error": "由於網路或系統錯誤，註冊失敗。",
            "register_unknown_error": "由於未知錯誤，註冊失敗。",
            "me_failure": "無法取得使用者資訊，請再試一次。",
            "me_is_not_active": "該使用者已被停用。",
            "language_update_failed": "語言偏好設定更新失敗。",
            "get_history_failed": "載入歷史訊息失敗。",
            "chat_list": "會話列表",
            "chat_new": "開始新會話",
            "chat_create_success": "成功建立新會話。",
            "chat_create_failed": "建立新會話失敗。",
            "chat_delete_success": "刪除會話成功。",
            "chat_delete_failed": "刪除會話失敗，請稍後再試。",
            "chat_name_to_long": "會話名稱過長。",
            "chat_name_empty": "會話名稱不能為空。",
            "chat_rename_success": "重新命名會話成功。",
            "chat_rename_failed": "重新命名會話失敗，請稍後再試。",
            "section_features": "主要功能",
            "guide": "專案介紹",
            "chatbot": "聊天機器人",
            "system_architecture": "系統架構圖",
            "project_intro": """# 專案介紹：聊天機器人系統（預覽版）

本系統為一個預覽版的聊天機器人平台，提供基本的帳號管理、對話管理與訊息串流互動體驗，支援多語言。目前已實現以下核心功能：

- ✅ Streamlit 前端互動體驗  
- ✅ 基本的用戶註冊與身份驗證  
- ✅ 多輪上下文記憶對話  
- ✅ 每位用戶可建立、刪除、重新命名多個獨立會話執行緒  
- ✅ 支援英語、簡體中文、繁體中文、日語四種語言介面切換  

---

## 🛠️ 核心技術

本專案採用前後端分離架構：

### 🖥️ 前端  
- 基於 [Streamlit](https://streamlit.io/) 實現簡潔直觀的使用者介面。  

### 🗄️ 後端  
- 使用 [FastAPI](https://fastapi.tiangolo.com/) 構建高效能 API。  
- 對話管理邏輯基於 [LangChain](https://www.langchain.com/) 與 [LangGraph](https://docs.langchain.com/langgraph/)。  
- 接入 [DeepSeek](https://deepseek.com/) 大型語言模型。  
- 通訊方式：透過標準 HTTP 介面互動。  
- 資料庫：使用 [PostgreSQL](https://www.postgresql.org/) 儲存用戶資訊與對話記錄。  

---
""",        
            "architecture_intro": """## 🧱 專案架構介紹

### 🖥️ 前端結構

1. **`pages` 層**  
   視圖層，基於 Streamlit 實現的 Web 使用者介面，負責頁面的渲染與展示，用於使用者互動操作。  
2. **`controller` 層**  
   控制器層，負責視圖層控件背後的業務邏輯，實現視圖與邏輯的解耦。此層負責處理使用者輸入，並為提交到下一層做準備。  
3. **`communication` 層**  
   通訊層，透過 HTTP 與後端 Web API 進行互動，並將通訊結果與回傳資料傳遞給 controller 層。

### 🗄️ 後端結構

4. **`api` 層**（介面層）  
   分為兩部分：  
   - **4.1 `Chat API`(api)**：基於 FastAPI 建構的聊天服務介面，負責接收請求、參數驗證、訊息回覆、歷史查詢與會話管理。  
   - **4.2 `Authorize API`(auth)**：基於 FastAPI-Users 實現的使用者認證介面，負責使用者註冊、登入、資訊管理與訪問權限控制。  
5. **`bll` 層**（業務邏輯層）  
   封裝對 LangChain 與 LangGraph 的調用邏輯，處理返回資料，確保業務流程合理與結果穩定。  
6. **`core` 層**（核心層）  
   系統的核心部分。負責管理 LangChain / LangGraph 資源，構建 LangGraph 流程圖，並與 DeepSeek API 及 PostgreSQL 資料庫對接。  
""", 
        },

        # 日语
        "ja_jp": {
            "language": "言語",
            "user_id": "ユーザーID",
            "password": "パスワード",
            "login_title": "ユーザーログイン",
            "register_title": "ユーザー登録",
            "login": "ログイン",
            "logout": "ログアウト",
            "register": "登録",
            "input_placeholder": "ここに入力してください",
            "generating": "応答を生成中...",
            "invalid_username": "メールアドレスの形式が正しくありません。",
            "invalid_password": "パスワードの形式が正しくありません。6文字以上、英数字を含めてください。",
            "login_success": "ログイン成功、こんにちは {username}！",
            "login_failure": "ログインに失敗しました。ユーザー名またはパスワードが正しくありません。",
            "login_unauthorized": "不正なログインです。",
            "login_server_error": "サーバーエラーのため、ログインに失敗しました。",
            "login_network_error": "ネットワークまたはシステムエラーのため、ログインに失敗しました。",
            "login_unknown_error": "不明なエラーのため、ログインに失敗しました。",
            "logout_success": "正常にログアウトしました。",
            "logout_not_logged_in": "ログインしていません。",
            "register_success": "登録に成功しました！",
            "user_exists": "このユーザーはすでに存在します。",
            "register_server_error": "サーバーエラーのため、登録に失敗しました。",
            "register_network_error": "ネットワークまたはシステムエラーのため、登録に失敗しました。",
            "register_unknown_error": "不明なエラーのため、登録に失敗しました。",
            "me_failure": "ユーザー情報の取得に失敗しました。もう一度お試しください。",
            "me_is_not_active": "このユーザーは無効化されています。",
            "language_update_failed": "言語設定の更新に失敗しました。",
            "get_history_failed": "履歴メッセージの読み込みに失敗しました。",
            "chat_list": "チャット一覧",
            "chat_new": "新しいチャットを開始",
            "chat_create_success": "新しいチャットを作成しました。",
            "chat_create_failed": "チャットの作成に失敗しました。",
            "chat_delete_success": "チャットを削除しました。",
            "chat_delete_failed": "チャットの削除に失敗しました。後でもう一度お試しください。",
            "chat_name_to_long": "チャット名が長すぎます。",
            "chat_name_empty": "チャット名を空にすることはできません。",
            "chat_rename_success": "チャット名を変更しました。",
            "chat_rename_failed": "チャット名の変更に失敗しました。後でもう一度お試しください。",
            "section_features": "主な機能",
            "guide": "プロジェクト紹介",
            "chatbot": "チャットボット",
            "system_architecture": "システム構成図",
            "project_intro": """# プロジェクト紹介：チャットボットシステム（プレビュー版）

本システムはプレビュー版のチャットボットプラットフォームであり、基本的なアカウント管理、会話管理、メッセージのストリーミング対話体験を提供し、多言語に対応しています。現在、以下の主要機能を実装済みです：

- ✅ Streamlit によるフロントエンドのインタラクション体験  
- ✅ 基本的なユーザー登録と認証  
- ✅ 複数ターンに渡る文脈を保持した会話機能  
- ✅ 各ユーザーが複数の会話スレッドを作成・削除・名前変更可能  
- ✅ 英語・簡体字中国語・繁体字中国語・日本語の4言語に対応したUI切替機能  

---

## 🛠️ コア技術

本プロジェクトはフロントエンドとバックエンドを分離したアーキテクチャを採用しています：

### 🖥️ フロントエンド  
- [Streamlit](https://streamlit.io/) により、シンプルで直感的なユーザーインターフェースを構築。  

### 🗄️ バックエンド  
- [FastAPI](https://fastapi.tiangolo.com/) により高性能なAPIを構築。  
- 会話管理ロジックは [LangChain](https://www.langchain.com/) と [LangGraph](https://docs.langchain.com/langgraph/) に基づいて構築。  
- [DeepSeek](https://deepseek.com/) 大規模言語モデルを導入。  
- 通信方式：標準HTTP APIを使用。  
- データベース：ユーザー情報と会話記録は [PostgreSQL](https://www.postgresql.org/) に保存。  

---
""",
            "architecture_intro": """## 🧱 プロジェクトアーキテクチャ紹介

### 🖥️ フロントエンド構成

1. **`pages` 層**  
   ビュー層。Streamlit に基づいて構築された Web ユーザーインターフェースで、画面の描画とユーザーとの操作を担当します。  
2. **`controller` 層**  
   コントローラー層。ビュー層の背後にあるビジネスロジックを処理し、ビューとロジックを分離します。ユーザー入力を処理し、次の層への準備を行います。  
3. **`communication` 層**  
   通信層。HTTP 経由でバックエンドの Web API と通信を行い、結果と返却データを controller 層に渡します。

### 🗄️ バックエンド構成

4. **`api` 層**（インターフェース層）  
   以下の2つに分かれています：  
   - **4.1 `Chat API`(api)**：FastAPI に基づくチャットサービスインターフェースで、リクエストの受信、パラメータ検証、メッセージ応答、履歴取得、会話管理を担当。  
   - **4.2 `Authorize API`(auth)**：FastAPI-Users に基づくユーザー認証インターフェースで、ユーザー登録、ログイン、情報管理、アクセス制御を担当。  
5. **`bll` 層**（ビジネスロジック層）  
   LangChain と LangGraph の呼び出しロジックをカプセル化し、返却データを処理。ビジネスフローの整合性と安定性を確保します。  
6. **`core` 層**（コア層）  
   システムの中核部分。LangChain / LangGraph のリソースを管理し、LangGraph のワークフローを構築し、DeepSeek API および PostgreSQL データベースと連携します。  
"""
        },
    }

    @staticmethod
    def get(key: str, language: str = "en_us") -> str:
        """
        返回所指定的键和语言对应的文字资源。

        Args:
            key (str): 文字资源的键。
            language (int): 文字资源的语言。

        Returns:
            str: 国际化的文字资源。
        """
        return I18n.RESOURCES[language][key]