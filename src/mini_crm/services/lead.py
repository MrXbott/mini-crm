from mini_crm.repos import LeadRepo
from mini_crm.schemas import LeadCreateData, LeadFromDB

class LeadService:
    def __init__(self, repo: LeadRepo) -> None:
        self.repo = repo

    async def create_new_lead(self, data: LeadCreateData) -> LeadFromDB:
        return await self.repo.create(data)

    async def get_all_lead(self) -> list[LeadFromDB]:
        return await self.repo.list_all()
    
    async def get_lead_by_email(self, email:str) -> LeadFromDB|None:
        return await self.repo.get_by_email(email)