from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from mini_crm.models import ContactModel
from mini_crm.schemas import ContactFromDB

class ContactRepo:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, source_id: int, lead_id: int, operator_id: int = None) -> ContactFromDB:
        result = await self.session.execute(
            select(ContactModel)
            .where(ContactModel.source_id==source_id, ContactModel.lead_id==lead_id)
        )
        contact_exists = result.scalar_one_or_none()
        if contact_exists:
            raise Exception('Contact with the source and the lead already exists')
        
        contact = ContactModel(source_id=source_id, lead_id=lead_id, operator_id=operator_id)
        self.session.add(contact)
        await self.session.commit()
        await self.session.refresh(contact)
        return ContactFromDB.model_validate(contact)

    async def list_all(self) -> list[ContactFromDB]:
        result = await self.session.execute(select(ContactModel))
        contacts = result.scalars().all()
        return [ContactFromDB.model_validate(contact) for contact in contacts]
    
    async def get_operator_current_capacity(self, operator_id: int) -> int:
        result = await self.session.execute(
            select(func.count())
            .select_from(ContactModel)
            .where(
                ContactModel.operator_id == operator_id,
                ContactModel.status == 'open'
            )
        )
        (capacity,) = result.one()
        return int(capacity)