import datetime

from src.repository import RepositoryInterface
from src.entities.media.repository import media_repository


class MediaService:

    def __init__(self, repository: RepositoryInterface):
        self.repository = repository

    async def create_media(
            self, type_media: str,
            file_id: str, media_group_id: str,
            datetime_create: datetime.datetime,
            caption: str = None
    ):
        data = {
            "type": type_media,
            "file_id": file_id,
            "media_group_id": media_group_id,
            "datetime_created": datetime_create,
            "caption": caption
        }
        await self.repository.create(data)

    async def get_media(self, media_group_id: str):
        return await self.repository.get_date(
            self.repository.model.media_group_id == media_group_id
        )

    async def get_last_media(self):
        return await self.repository.get_last()


media_service = MediaService(media_repository)
