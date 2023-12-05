from src.repository import RepositoryInterface, IntegrityException

from src.entities.flow.repository import flow_repository


class FlowService:

    def __init__(self, repository: RepositoryInterface):
        self.repository = repository

    async def toggle_flow(self, parsed_channel_id: int, receiver_channel_id: int):
        flow_existing = await self.repository.get_by_filter(
            0,
            self.repository.model.receiver_channel_id == receiver_channel_id,
            self.repository.model.parsed_channel_id == parsed_channel_id
        )

        if not flow_existing:
            data = {"parsed_channel_id": parsed_channel_id, "receiver_channel_id": receiver_channel_id}
            await self.repository.create(data)
            return True
        else:
            await self.repository.delete_by_filters(
                self.repository.model.receiver_channel_id == receiver_channel_id,
                self.repository.model.parsed_channel_id == parsed_channel_id
            )
            return False

    async def get_flow(self, receiver_channel_id: int):
        flow = await self.repository.get_list(self.repository.model.receiver_channel_id == receiver_channel_id)
        return flow

    async def get_flow_by_parsed_channel_id(self, parsed_channel_id: int):
        flow = await self.repository.get_list(
            self.repository.model.parsed_channel_id == parsed_channel_id
        )
        return flow


flow_service = FlowService(flow_repository)
