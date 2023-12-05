import json

from src.repository import RepositoryInterface, IntegrityException
from src.entities.setting.repository import setting_repository


class SettingService:

    def __init__(self, repository: RepositoryInterface):
        self.repository = repository

    async def create_setting(self, receiver_channel_id: int, username: str = None):
        try:
            await self.repository.create({"id": receiver_channel_id, "link": username})
        except IntegrityException as error:
            data = {"link": username}
            await self.repository.update(data, entity_id=receiver_channel_id)

    async def add_link(self, link: str, receiver_channel_id: int):
        data = {"link": link}
        await self.repository.update(data, receiver_channel_id)

    async def get_settings(self, receiver_channel_id: int):
        return await self.repository.get(receiver_channel_id)

    async def toggle_setting(self, receiver_channel_id: int):
        setting_existing = await self.repository.get(receiver_channel_id)
        if setting_existing.change_link:
            await self.repository.update({"change_link": False}, receiver_channel_id)
            return False
        else:
            await self.repository.update({"change_link": True}, receiver_channel_id)
            return True

    async def add_words(self, words: list[str], receiver_channel_id: int) -> list:
        settings = await self.repository.get(receiver_channel_id)
        if not settings.deleted_key_words:
            data = {"deleted_key_words": "&&".join(words)}
            await self.repository.update(data, entity_id=receiver_channel_id)
            return words
        else:
            new_words: list = settings.deleted_key_words.split("&&")
            new_words.extend(words)
            data = {"deleted_key_words": "&&".join(new_words)}
            await self.repository.update(data, entity_id=receiver_channel_id)
            return new_words

    async def delete_words(self, words: list[str], receiver_channel_id: int) -> list:
        settings = await self.repository.get(receiver_channel_id)
        word = settings.deleted_key_words.split("&&")
        for delete_word in words:
            if delete_word in word:
                word.remove(delete_word)
        await self.repository.update(
            {"deleted_key_words": "&&".join(word)}, entity_id=receiver_channel_id
        )
        return word

    async def add_postscript(self, postscript: str, receiver_channel_id: int):
        data = {
            "postscript": postscript
        }
        await self.repository.update(data, receiver_channel_id)


setting_service = SettingService(setting_repository)
