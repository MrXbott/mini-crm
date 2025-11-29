from fastapi import APIRouter, HTTPException, Depends

from mini_crm.dependencies.services import get_source_service, get_source_operator_service
from mini_crm.services import SourceService, SourceOperatorService
from mini_crm.schemas import SourceCreateData, SourceFromDB, SourceOperatorData, SourceOperatorFromDB


router = APIRouter(prefix='/sources')

@router.post('/', response_model=SourceFromDB)
async def create_source(data: SourceCreateData, service: SourceService = Depends(get_source_service)):
    try:
        return await service.create_new_source(data)
    except Exception as e:
        raise HTTPException(500, str(e))
    
@router.get('/', response_model=list[SourceFromDB])
async def list_sources(service: SourceService = Depends(get_source_service)):
    try:
        return await service.get_all_sources()
    except Exception as e:
        raise HTTPException(500, str(e))

@router.post('/{source_id}/assign_operator', response_model=SourceOperatorFromDB)
async def assign_operator_to_source(source_id: int, data: SourceOperatorData, service: SourceOperatorService = Depends(get_source_operator_service)):
    try:
        return await service.assign_operator_to_source(source_id, data)
    except Exception as e:
        raise HTTPException(500, str(e))
    
@router.get('/{source_id}/operators', response_model=list[SourceOperatorFromDB])
async def list_operators_for_source(source_id: int, service: SourceOperatorService = Depends(get_source_operator_service)):
    return await service.list_operators_for_source(source_id)