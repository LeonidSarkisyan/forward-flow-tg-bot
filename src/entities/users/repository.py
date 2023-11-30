from src.repository import SQLAlchemyRepository
from src.models import Role, User


role_repository = SQLAlchemyRepository(Role)
user_repository = SQLAlchemyRepository(User)
