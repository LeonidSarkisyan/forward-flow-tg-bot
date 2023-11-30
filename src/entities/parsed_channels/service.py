from src.repository import RepositoryInterface, IntegrityException

from src.entities.parsed_channels.repository import parsed_channel_repository


class ParsedChannelService:

    def __init__(self, repository: RepositoryInterface):
        self.repository = repository

    async def add_parsed_channel(self, user_id: int, username: str):
        data = {"id": user_id, "username": username, "role_id": 1}
        try:
            await self.repository.create(data)
        except IntegrityException:
            print("Пользователь такой уже есть!")