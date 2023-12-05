from src.repository import SQLAlchemyRepository
from src.models import ParsedChannel, UserToParsedChannel


parsed_channel_repository = SQLAlchemyRepository(ParsedChannel)
parsed_channel_many_repository = SQLAlchemyRepository(UserToParsedChannel)
