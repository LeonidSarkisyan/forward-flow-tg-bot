from src.repository import RepositoryInterface, IntegrityException
from src.entities.receiver_channels.repository import receiver_channel_repository


class ReceiverChannelService:

    def __init__(self, repository: RepositoryInterface):
        self.repository = repository

    async def add_receiver_channel(self, receiver_channel_id: int, receiver_channel_title: str, user_id: int):
        data = {"id": receiver_channel_id, "title": receiver_channel_title, "user_id": user_id}
        try:
            await self.repository.create(data)
        except IntegrityException:
            pass

    async def get_receiver_channel(self, receiver_channel_id: int):
        receiver_channel = await self.repository.get(receiver_channel_id)
        return receiver_channel

    async def get_receiver_channels(self, user_id: int):
        receiver_channels = await self.repository.get_list(
            self.repository.model.user_id == user_id
        )
        return receiver_channels

    async def delete_receiver_channel(self, receiver_channel_id: int):
        await self.repository.delete(receiver_channel_id)


receiver_channel_service = ReceiverChannelService(receiver_channel_repository)
