from fastapi import APIRouter, HTTPException, Depends

from mini_crm.dependencies.services import get_operator_service
from mini_crm.schemas import OperatorCreateData, OperatorUpdateData, OperatorFromDB
from mini_crm.services import OperatorService

router = APIRouter(prefix='/operators')

@router.post('/', response_model=OperatorFromDB)
async def create_operator(data: OperatorCreateData, service: OperatorService = Depends(get_operator_service)):
    try:
        return await service.create_new_operator(data)
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get('/', response_model=list[OperatorFromDB])
async def list_operators(service: OperatorService = Depends(get_operator_service)):
    try:
        return await service.get_all_operators()
    except Exception as e:
        raise HTTPException(500, str(e))

@router.patch('/{operator_id}', response_model=OperatorFromDB)
async def update_operator(operator_id: int, data: OperatorUpdateData, service: OperatorService = Depends(get_operator_service)):
    try:
        return await service.update_operator(operator_id, data)
    except ValueError as e:
        raise HTTPException(400, str(e))
    except LookupError as e:
        raise HTTPException(404, str(e))
    
