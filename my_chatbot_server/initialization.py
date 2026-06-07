"""
系统初始化脚本。

初次运行服务端之前，必须运行此脚本以创建 postgres 数据库和数据表。
"""


import os
import traceback
import psycopg
from dotenv import load_dotenv
from psycopg_pool import ConnectionPool
from langgraph.checkpoint.postgres import PostgresSaver
from tools.i18n import get_system_locale


try:
    print("========================================")
    print("Initializing program.")
    print("初始化程序启动。")
    print("初始化程式啟動。")
    print("初期化プログラムを起動します。")
    print("========================================")

    # 加载环境变量
    load_dotenv()

    USERNAME = os.environ["POSTGRES_USERNAME"]
    PASSWORD = os.environ["POSTGRES_PASSWORD"]
    HOST = os.environ["POSTGRES_HOST"]
    PORT = os.environ["POSTGRES_PORT"]
    MAX_SIZE = os.environ["POSTGRES_MAX_SIZE"]

    # 语言资源
    lang_resource = {
        # 英语（默认）
        "en_us": [
            "System is initializing...",
            "Detected database '{dbname}' does not exist, creating...",
            "Database '{dbname}' created successfully.",
            "Initialization complete.",
        ],
        # 简体中文
        "zh_cn": [
            "系统正在初始化...",
            "检测到数据库 '{dbname}' 不存在，正在创建...",
            "数据库 '{dbname}' 创建成功。",
            "初始化完成。",
        ],
        # 繁体中文
        "zh_tw": [
            "系統正在初始化...",
            "檢測到資料庫 '{dbname}' 不存在，正在建立...",
            "資料庫 '{dbname}' 建立成功。",
            "初始化完成。",
        ],
        # 日语
        "ja_jp": [
            "システムを初期化しています...",
            "データベース '{dbname}' が存在しません。作成しています...",
            "データベース '{dbname}' の作成に成功しました。",
            "初期化が完了しました。",
        ],
    }
    # 检测系统语言
    language = get_system_locale()

    print(lang_resource[language][0])       # 提示系统初始化

    for dbname in ["checkpoints", "auth"]:
        # 检查数据库是否存在，如果没有就创建
        with psycopg.connect(f"postgres://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/postgres", autocommit=True) as conn:
            with conn.cursor() as cur:
                # 查询数据库是否存在
                cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (dbname,))

                # 如果数据库不存在
                if not cur.fetchone():
                    print(lang_resource[language][1].format(dbname=dbname))               # 提示创建数据库
                    cur.execute(f"CREATE DATABASE {dbname}")    # 创建数据库操作
                    print(lang_resource[language][2].format(dbname=dbname))               # 提示创建数据库成功

    # 初始化表结构（此时数据库已确保存在）
    db_saver = PostgresSaver(ConnectionPool(
        conninfo = f"postgres://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/checkpoints",
        max_size = int(MAX_SIZE),
        kwargs = {"autocommit": True}
    ))
    db_saver.setup()    # 数据库初始化操作
    print(lang_resource[language][3])  # 提示初始化完成
    print("========================================")
except:
    print("========================================")
    print("Initialization error occurred.")
    print("初始化程序发生错误。")
    print("初始化程序發生錯誤。")
    print("初期化プログラムでエラーが発生しました。")
    traceback.print_exc()
    print("========================================")