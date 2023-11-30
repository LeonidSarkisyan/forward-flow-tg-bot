from src.repository import SQLAlchemyRepository
from src.models import ParsedChannel


parsed_channel_repository = SQLAlchemyRepository(ParsedChannel)
