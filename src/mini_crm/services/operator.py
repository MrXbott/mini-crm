
from mini_crm.repos import OperatorRepo
from mini_crm.schemas import OperatorCreateData, OperatorUpdateData, OperatorFromDB

class OperatorService:
    def __init__(self, repo: OperatorRepo) -> None:
        self.repo = repo

    async def create_new_operator(self, data: OperatorCreateData) -> OperatorFromDB:
        return await self.repo.create(data)
        
    async def get_all_operators(self) -> list[OperatorFromDB]:
        return await self.repo.list_all()
    
    async def update_operator(self, operator_id: int, data: OperatorUpdateData) -> OperatorFromDB:
        return await self.repo.update(operator_id, data)
    
        
    