from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


db_path = 'sqlite+aiosqlite:///.database.db'
engine = create_async_engine(db_path, echo=True)

async_session_maker = sessionmaker(engine, class_=AsyncSession)

Base = declarative_base()
