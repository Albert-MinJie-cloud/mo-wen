# 数据库连接配置
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from databases import Database

from app.config import settings

# sqlachemy 同步引擎,定义模型操作
engine = create_engine(
    settings.database_url, 
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=False
    )   

# 会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ORM 模型基类
Base = declarative_base()

# database 异步数据库 , 用于fastApi查询
database=Database(settings.database_url.replace("+pymysql", ""))

async def get_db():
    # 获取数据库连接(依赖注入)
    yield database