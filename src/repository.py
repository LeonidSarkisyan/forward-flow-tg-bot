from abc import ABC, abstractmethod

from sqlalchemy import insert, select, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

from src.database import async_session_maker, Base


class RepositoryInterface:

    @abstractmethod
    def __init__(self, model):
        self.model = model

    @abstractmethod
    async def create(self, data: dict):
        raise NotImplemented

    @abstractmethod
    async def update(self, update_date: dict, entity_id: int):
        raise NotImplemented

    @abstractmethod
    async def get(self, entity_id: int):
        raise NotImplemented

    @abstractmethod
    async def get_by_filter(self, entity_id: int, *filters):
        raise NotImplemented

    @abstractmethod
    async def get_list(self, *filters):
        raise NotImplemented

    @abstractmethod
    async def delete(self, model_id: int):
        raise NotImplemented

    @abstractmethod
    async def delete_by_filters(self, *filters):
        raise NotImplemented

    @abstractmethod
    async def bulk_insert(self, data: list):
        raise NotImplemented

    @abstractmethod
    async def get_last(self):
        raise NotImplemented

    @abstractmethod
    async def get_date(self, *filters):
        raise NotImplemented


class SQLAlchemyRepository(RepositoryInterface):

    def __init__(self, model: Base):
        self.model = model

    async def create(self, data: dict):
        async with async_session_maker() as session:
            stmt = insert(self.model).returning(self.model).values(**data)
            try:
                result = await session.execute(stmt)
            except IntegrityError:
                raise IntegrityException
            else:
                await session.commit()
                return result.scalar()

    async def get_list(self, *filters):
        async with async_session_maker() as session:
            stmt = select(self.model).filter(*filters)
            result = await session.execute(stmt)
            return result.scalars().all()

    async def get_last(self):
        async with async_session_maker() as session:
            query = select(self.model).order_by(self.model.id.desc())
            result = await session.execute(query)
            return result.scalar()

    async def get_date(self, *filters):
        async with async_session_maker() as session:
            query = select(self.model).filter(*filters).order_by(self.model.datetime_created.asc())
            result = await session.execute(query)
            return result.scalars()

    async def get(self, entity_id: int):
        async with async_session_maker() as session:
            query = select(self.model).where(self.model.id == entity_id)
            result = await session.execute(query)
            return result.scalar()

    async def get_by_filter(self, entity_id: int, *filters):
        async with async_session_maker() as session:
            query = select(self.model).where(*filters)
            result = await session.execute(query)
            return result.scalar()

    async def update(self, update_date: dict, entity_id: int):
        async with async_session_maker() as session:
            stmt = update(self.model).returning(self.model).where(self.model.id == entity_id).values(**update_date)
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar()

    async def delete(self, model_id: int):
        async with async_session_maker() as session:
            stmt = delete(self.model).returning(self.model).where(self.model.id == model_id)
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar()

    async def bulk_insert(self, data: list):
        async with async_session_maker() as session:
            try:
                result = await session.execute(insert(self.model).returning(self.model.id), data)
            except IntegrityError:
                raise IntegrityException
            else:
                await session.commit()
                return result.scalars().all()

    async def delete_by_filters(self, *filters):
        async with async_session_maker() as session:
            stmt = delete(self.model).where(*filters)
            await session.execute(stmt)
            await session.commit()


class IntegrityException(Exception):
    pass
