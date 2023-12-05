from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


db_path = 'sqlite+aiosqlite:///db.db'
engine = create_async_engine(db_path, echo=False)

async_session_maker = sessionmaker(engine, class_=AsyncSession)

Base = declarative_base()
