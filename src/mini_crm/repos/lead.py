from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from mini_crm.schemas import LeadCreateData, LeadFromDB
from mini_crm.models import LeadModel

class LeadRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: LeadCreateData):
        lead_data = data.model_dump()
        lead = LeadModel(**lead_data)
        self.session.add(lead)
        await self.session.commit()
        await self.session.refresh(lead)
        return LeadFromDB.model_validate(lead)

    async def list_all(self) -> list[LeadFromDB]:
        result = await self.session.execute(select(LeadModel))
        leads = result.scalars().all()
        return [LeadFromDB.model_validate(lead) for lead in leads]
    
    async def get_by_email(self, email: str) -> LeadFromDB|None:
        result = await self.session.execute(select(LeadModel).where(LeadModel.email==email))
        return result.scalar_one_or_none()

        