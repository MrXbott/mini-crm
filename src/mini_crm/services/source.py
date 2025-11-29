
from mini_crm.repos import SourceRepo
from mini_crm.schemas import SourceCreateData, SourceFromDB, AssignedOperatorData
# from mini_crm.schemas.operators import AssignedOperatorData


class SourceService:
    def __init__(self, repo: SourceRepo) -> None:
        self.repo = repo

    async def create_new_source(self, data: SourceCreateData) -> SourceFromDB:
        return await self.repo.create(data)
        
    async def get_all_sources(self) -> list[SourceFromDB]:
        return await self.repo.list_all()
    
    async def get_source_by_id(self, sourse_id: int) -> SourceFromDB:
        return await self.repo.get_by_id(sourse_id)
    
    async def get_assigned_operators_for_source(self, source_id: int) -> list[AssignedOperatorData]:
        return await self.repo.get_assigned_operators(source_id)
    
    

    
    
