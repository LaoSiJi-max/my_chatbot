# My Chatbot

[中文](README.md) | [日本語](README_ja.md)

![聊天机器人运行效果](my_chatbot_web/static/images/chatbot_demo.png)

## 项目介绍

暂时没有想到更合适的名字，就叫 My Chatbot。

这是我在2025年6月用大约一个月时间，一边学习一边开发完成的对话型AI项目。

我一直对对话型AI很感兴趣，因此在学习 LangChain 和 LangGraph 后，尝试自己实现了一个能够陪用户闲聊的聊天系统。它并不追求复杂的专业功能，只是一个普通的对话机器人，不过项目本身做了比较清晰的分层，包括 Web 界面、HTTP 接口、用户认证、会话管理、数据库存储和大语言模型接入。

本仓库主要用于记录自己的学习过程和成长，代码未必完美。

## 主要功能

* 简易的用户注册与登录认证
* 基于 JWT 的接口访问认证
* AI 回复的流式输出
* 多轮对话及历史消息保存
* 为每位用户创建多个独立会话
* 会话的创建、选择、重命名和删除
* 长对话内容的自动摘要
* 英语、简体中文、繁体中文和日语界面
* 根据用户选择切换 AI 的回复语言
* 用户语言偏好与会话信息的持久化保存

## 系统结构

本项目采用前后端分离和分层设计。Streamlit 客户端通过 HTTP 接口分别访问聊天服务和用户认证服务。

![系统架构图](my_chatbot_web/static/images/system_architecture.png)

### Web 客户端

* **`pages`**
  使用 Streamlit 实现登录、注册、项目介绍和聊天页面。

* **`controller`**
  处理页面操作、输入检查、状态判断和结果提示，使界面代码与通信逻辑分离。

* **`communication`**
  使用 HTTP 访问后端接口，负责登录、注册、用户信息、聊天及会话管理等通信。

### 服务器端

* **`api`**
  提供聊天、流式回复、历史记录查询，以及会话创建、删除和重命名等接口。

* **`auth`**
  使用 FastAPI Users 实现用户注册、登录、JWT 认证和用户信息管理。

* **`bll`**
  封装聊天业务逻辑，连接 API 层和 LangGraph 核心功能。

* **`core`**
  管理大语言模型、提示模板、LangGraph 状态图、对话摘要和 PostgreSQL 持久化。

* **`prompts`**
  分别保存英语、简体中文、繁体中文和日语的提示模板。

## 对话处理流程

系统使用 LangGraph 构建了由以下两个节点组成的处理流程：

1. **对话摘要节点**
   当历史消息逐渐变长时，对已有对话进行摘要，保留重要信息并控制上下文长度。

2. **聊天机器人节点**
   将提示模板、历史消息和摘要信息传递给 DeepSeek 模型，生成新的回复。

不同会话通过独立的线程 ID 进行区分。对话状态保存在 PostgreSQL 中，因此用户重新进入会话时，仍然可以读取之前的历史记录。

## 使用技术

| 分类      | 技术                          |
| ------- | --------------------------- |
| 开发语言    | Python                      |
| Web 界面  | Streamlit                   |
| API     | FastAPI                     |
| 用户认证    | FastAPI Users、JWT           |
| AI 应用框架 | LangChain、LangGraph、LangMem |
| 大语言模型   | DeepSeek API                |
| 数据库     | PostgreSQL                  |
| 数据库访问   | SQLAlchemy、asyncpg、psycopg  |
| HTTP 通信 | httpx                       |
| 多语言提示   | YAML                        |

## 项目目录

```text
my_chatbot
├── my_chatbot_web
│   ├── pages
│   ├── controller
│   ├── communication
│   ├── static
│   └── tools
│
└── my_chatbot_server
    ├── api
    ├── auth
    ├── bll
    ├── core
    ├── prompts
    └── tools
```
