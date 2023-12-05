from src.repository import RepositoryInterface, IntegrityException

from src.entities.parsed_channels.repository import parsed_channel_repository, parsed_channel_many_repository


class ParsedChannelService:

    def __init__(self, repository: RepositoryInterface, repository_many: RepositoryInterface):
        self.repository = repository
        self.repository_many = repository_many

    async def add_parsed_channel(self, channel_id: int, username: str):
        data = {"id": channel_id, "username": username}
        try:
            await self.repository.create(data)
        except IntegrityException:
            print("Такой канал уже есть!")

    async def get_all_parsed_channels(self, user_id: int) -> list[str]:
        parsed_channels = await self.repository_many.get_list(
            self.repository_many.model.user_id == user_id
        )
        ids = [parsed_channel.parsed_channel_id for parsed_channel in parsed_channels]
        print(f"ids = {ids}")
        parsed_channels = await self.repository.get_list(
            self.repository.model.id.in_(ids)
        )
        return parsed_channels

    async def get_all_usernames(self, user_id: int) -> list[str]:
        usernames = []
        parsed_channels = await self.repository_many.get_list(
            self.repository_many.model.user_id == user_id
        )
        for parsed_channel in parsed_channels:
            usernames.append(parsed_channel.parsed_channel_username)
        return usernames

    async def bound_with_user(self, channel_id: int, channel_username: str, user_id: int):
        channel_existing = await self.get_channel_user(channel_username, user_id)
        if not channel_existing:
            data = {
                "user_id": user_id,
                "parsed_channel_id": channel_id,
                "parsed_channel_username": channel_username
            }
            await self.repository_many.create(data)

    async def get_channel_user(self, channel_username: str, user_id: int):
        channel_many = await self.repository_many.get_by_filter(
            self.repository_many.model.user_id == user_id,
            self.repository_many.model.parsed_channel_username == channel_username
        )
        return channel_many

    async def delete_channel_for_user(self, username: str, user_id: int):
        await self.repository_many.delete_by_filters(
            self.repository_many.model.parsed_channel_username == username,
            self.repository_many.model.user_id == user_id
        )


parsed_channel_service = ParsedChannelService(
    parsed_channel_repository, parsed_channel_many_repository
)
