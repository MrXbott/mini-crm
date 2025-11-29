from fastapi import APIRouter, Depends, HTTPException

from mini_crm.dependencies.services import get_lead_service
from mini_crm.services.lead import LeadService
from mini_crm.schemas.leads import LeadCreateData, LeadFromDB

router = APIRouter(prefix='/leads')

@router.post('/', response_model=LeadFromDB)
async def create_lead(data: LeadCreateData, service: LeadService = Depends(get_lead_service)):
    try:
        return await service.create_new_lead(data)
    except Exception as e:
        raise HTTPException(detail=str(e))

@router.get('/', response_model=list[LeadFromDB])
async def list_all_leads(service: LeadService = Depends(get_lead_service)):
    return await service.get_all_lead()

    