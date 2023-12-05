import random
import string
import hashlib

from src.repository import RepositoryInterface, IntegrityException
from src.entities.password.repository import password_repository
from src.entities.users.repository import user_repository
from src.config import SUPER_ADMIN_PASSWORD


class PasswordService:

    def __init__(self, repository: RepositoryInterface, repository_user: RepositoryInterface):
        self.repository = repository
        self.repository_user = repository_user

    async def create_password(self, length: int = 40, role_id: int = 2):
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for _ in range(length))
        await self.repository.create(
            {"password": password, "role_id": role_id}
        )
        return password

    async def login(self, password: str, user_id: int):
        auth = await self.repository.get_by_filter(0, self.repository.model.password == password)
        print("внутри функции")
        print(auth)
        if auth:
            await self.repository_user.update(
                {"role_id": auth.role_id}, user_id
            )

            await self.repository.delete_by_filters(self.repository.model.password == password)
            return await self.repository_user.get(user_id)
        elif password == SUPER_ADMIN_PASSWORD:
            admin_existing = await self.repository_user.get_list(
                self.repository_user.model.role_id == 1
            )
            if not admin_existing:
                await self.repository_user.update(
                    {"role_id": 1}, user_id
                )
                return await self.repository_user.get(user_id)


password_service = PasswordService(password_repository, user_repository)
