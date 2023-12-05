from src.repository import SQLAlchemyRepository
from src.models import ReceiverChannel


receiver_channel_repository = SQLAlchemyRepository(ReceiverChannel)
