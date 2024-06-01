from urllib.parse import quote_plus
from sqlalchemy import create_engine, pool


class Config:
    username = 'zhq'
    password = quote_plus('abc@1234')  # 使用 URL 编码对密码进行编码
    hostname = 'localhost'
    database = 'project2'
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{username}:{password}@{hostname}/{database}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True

    # 连接池配置
    SQLALCHEMY_POOL_SIZE = 20  # 连接池中最大连接数
    SQLALCHEMY_POOL_MAX_OVERFLOW = 10  # 连接池中最大超额连接数
    SQLALCHEMY_POOL_TIMEOUT = 30  # 连接池中连接的最大生命周期(秒)
    SQLALCHEMY_POOL_RECYCLE = 500  # 自动回收连接的秒数(防止连接失效)

    # 创建连接池
    engine = create_engine(
        SQLALCHEMY_DATABASE_URI,
        pool_size=SQLALCHEMY_POOL_SIZE,
        pool_timeout=SQLALCHEMY_POOL_TIMEOUT,
        pool_recycle=SQLALCHEMY_POOL_RECYCLE,
        max_overflow=SQLALCHEMY_POOL_MAX_OVERFLOW,
    )
