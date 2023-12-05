from src.repository import SQLAlchemyRepository
from src.models import Setting


setting_repository = SQLAlchemyRepository(Setting)
