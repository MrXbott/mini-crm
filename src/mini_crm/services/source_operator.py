from mini_crm.repos import SourceOperatorRepo
from mini_crm.schemas import SourceOperatorData, SourceOperatorFromDB


class SourceOperatorService:
    def __init__(self, repo: SourceOperatorRepo):
        self.repo = repo

    async def assign_operator_to_source(self, source_id: int, data: SourceOperatorData) -> SourceOperatorFromDB:
        return await self.repo.assign_operator(source_id, data.operator_id, data.weight)
    
    async def update_weight(self, source_id: int, operator_id: int, weight: int) -> SourceOperatorFromDB:
        return await self.repo.update_weight(source_id, operator_id, weight)

    async def list_operators_for_source(self, source_id: int) -> list[SourceOperatorFromDB]:
        return await self.repo.list_operators_for_source(source_id)
