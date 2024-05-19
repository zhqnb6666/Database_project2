from urllib.parse import quote_plus

class Config:
    username = 'zhq'
    password = quote_plus('abc@1234')  # 使用 URL 编码对密码进行编码
    hostname = 'localhost'
    database = 'project2'
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{username}:{password}@{hostname}/{database}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
