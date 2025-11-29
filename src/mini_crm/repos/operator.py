from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from mini_crm.schemas.operators import OperatorCreateData, OperatorUpdateData, OperatorFromDB
from mini_crm.models.operators import OperatorModel

class OperatorRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: OperatorCreateData):
        operator_data = data.model_dump()
        operator = OperatorModel(**operator_data)
        self.session.add(operator)
        await self.session.commit()
        await self.session.refresh(operator)
        return OperatorFromDB.model_validate(operator)

    async def list_all(self) -> list[OperatorFromDB]:
        result = await self.session.execute(select(OperatorModel))
        operators = result.scalars().all()
        return [OperatorFromDB.model_validate(operator) for operator in operators]
    
    async def update(self, operator_id: int, data: OperatorUpdateData) -> OperatorFromDB:
        update_data = data.model_dump(exclude_unset=True)

        if not update_data:
            raise ValueError('No data for update')
        
        
        result = await self.session.execute(
            update(OperatorModel)
            .where(OperatorModel.id == operator_id)
            .values(**update_data)
            .returning(OperatorModel)
        )

        updated_operator = result.scalar_one_or_none()

        if not updated_operator:
            raise LookupError('Operator not found')
        
        await self.session.commit()

        return OperatorFromDB.model_validate(updated_operator)
    

    

        
