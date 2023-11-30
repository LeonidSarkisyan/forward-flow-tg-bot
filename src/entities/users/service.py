from src.repository import RepositoryInterface, IntegrityException

from src.entities.users.repository import user_repository, role_repository


class UserService:

    def __init__(self, repository: RepositoryInterface):
        self.repository = repository

    async def add_user(self, user_id: int, username: str):
        data = {"id": user_id, "username": username, "role_id": 1}
        try:
            await self.repository.create(data)
        except IntegrityException:
            print("Пользователь такой уже есть!")


class RoleService:

    def __init__(self, repository: RepositoryInterface):
        self.repository = repository

    async def create_roles(self):
        roles = [
            {"id": 1, "name": "super_admin"},
            {"id": 2, "name": "admin"},
            {"id": 3, "name": "user"}
        ]
        try:
            await self.repository.bulk_insert(roles)
        except IntegrityException:
            print("Роли уже были созданы!")


user_service = UserService(user_repository)
role_service = RoleService(role_repository)
