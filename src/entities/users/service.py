from src.repository import RepositoryInterface, IntegrityException

from src.entities.users.repository import user_repository, role_repository


class UserService:

    def __init__(self, repository: RepositoryInterface):
        self.repository = repository

    async def add_user(self, user_id: int, username: str):
        data = {"id": user_id, "username": username, "role_id": 4}
        try:
            return await self.repository.create(data)
        except IntegrityException:
            return await self.repository.get(user_id)

    async def get_user(self, user_id: int):
        return await self.repository.get(user_id)

    async def get_admins(self):
        admins = await self.repository.get_list(
            self.repository.model.role_id == 2
        )
        return admins

    async def delete_admin(self, admin_id: int):
        return await self.repository.update(
            {"role_id": 4}, entity_id=admin_id
        )


class RoleService:

    def __init__(self, repository: RepositoryInterface):
        self.repository = repository

    async def create_roles(self):
        roles = [
            {"id": 1, "name": "super_admin"},
            {"id": 2, "name": "admin"},
            {"id": 3, "name": "user"},
            {"id": 4, "name": "guest"}
        ]
        try:
            await self.repository.bulk_insert(roles)
        except IntegrityException:
            print("Роли уже были созданы!")


user_service = UserService(user_repository)
role_service = RoleService(role_repository)
