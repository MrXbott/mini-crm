from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from mini_crm.schemas import SourceCreateData, SourceFromDB, OperatorFromDB, AssignedOperatorData
from mini_crm.models import SourceModel, OperatorModel, ContactModel, SourceOperatorModel


class SourceRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: SourceCreateData) -> SourceFromDB:
        source_data = data.model_dump()
        source = SourceModel(**source_data)
        self.session.add(source)
        await self.session.commit()
        await self.session.refresh(source)
        return SourceFromDB.model_validate(source)

    async def list_all(self) -> list[SourceFromDB]:
        result = await self.session.execute(select(SourceModel))
        sources = result.scalars().all()
        return [SourceFromDB.model_validate(source) for source in sources]
    
    async def get_by_id(self, source_id: int) -> SourceFromDB:
        result = await self.session.execute(
            select(SourceModel)
            .where(SourceModel.id==source_id)
        )

        source = result.scalar_one_or_none()
        if not source:
            raise LookupError('Source not found')
        
        return SourceFromDB.model_validate(source)
    

    async def get_assigned_operators(self, source_id: int) -> list[AssignedOperatorData]:
        # get assigned operators with weights and their current capacity
        contact_counts = (
            select(
                ContactModel.operator_id,
                func.count().label('current_capacity')
            )
            .where(ContactModel.status == 'open')
            .group_by(ContactModel.operator_id)
            .subquery()
        )

        stmt = (
            select(
                SourceOperatorModel,
                OperatorModel,
                contact_counts.c.current_capacity
            )
            .join(OperatorModel, SourceOperatorModel.operator_id == OperatorModel.id)
            .outerjoin(contact_counts, contact_counts.c.operator_id == OperatorModel.id)
            .where(
                SourceOperatorModel.source_id == source_id,
                OperatorModel.is_active == True
            )
        )

        result = await self.session.execute(stmt)
        rows = result.all()

        operators = []

        for assoc, operator, current_capacity in rows:
            operators.append(
                AssignedOperatorData(
                    operator=OperatorFromDB.model_validate(operator),
                    current_capacity=current_capacity or 0,
                    source_id=assoc.source_id,
                    weight=assoc.weight,
                )
            )

        return operators

    
        
    
    
    
    