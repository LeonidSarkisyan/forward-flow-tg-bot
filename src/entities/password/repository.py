from src.repository import SQLAlchemyRepository
from src.models import Password


password_repository = SQLAlchemyRepository(Password)

