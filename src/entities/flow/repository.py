from src.repository import SQLAlchemyRepository
from src.models import Flow


flow_repository = SQLAlchemyRepository(Flow)
