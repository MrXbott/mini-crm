from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from mini_crm.schemas.sources_operators import SourceOperatorFromDB
from mini_crm.models.sources_operators import SourceOperatorModel

class SourceOperatorRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def _get(self, source_id: int, operator_id: int) -> SourceOperatorModel:
        return await self.session.get(SourceOperatorModel, {'source_id': source_id, 'operator_id': operator_id})

    async def assign_operator(self, source_id: int, operator_id: int, weight: int) -> SourceOperatorFromDB:
        assoc = await self._get(source_id, operator_id)
        if assoc:
            raise Exception('This operator already assigned to the source')
        
        assoc = SourceOperatorModel(source_id=source_id, operator_id=operator_id, weight=weight)

        self.session.add(assoc)
        await self.session.commit()
        return SourceOperatorFromDB.model_validate(assoc)

    async def update_weight(self, source_id: int, operator_id: int, weight: int) -> SourceOperatorFromDB:
        assoc = await self._get(source_id, operator_id)
        if not assoc:
            raise Exception('Operator not assigned to this source')

        assoc.weight = weight
        await self.session.commit()
        return SourceOperatorFromDB.model_validate(assoc)

    async def list_operators_for_source(self, source_id: int) -> list[SourceOperatorFromDB]:
        result = await self.session.execute(
            select(SourceOperatorModel)
            .where(SourceOperatorModel.source_id == source_id)
        )
        return [SourceOperatorFromDB.model_validate(operator) for operator in result.scalars().all()]
    
