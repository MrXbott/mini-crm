from fastapi import APIRouter, HTTPException, Depends

from mini_crm.schemas.contacts import ContactCreateData
from mini_crm.schemas.contacts import ContactCreateData, ContactFromDB
from mini_crm.services.contact import ContactService
from mini_crm.dependencies.services import get_contact_service


router = APIRouter(prefix='/contacts')

@router.get('/', response_model=list[ContactFromDB])
async def list_contacts(service: ContactService = Depends(get_contact_service)):
    try:
        return await service.get_all_contacts()
    except Exception as e:
        raise HTTPException(500, str(e))


@router.post('/', response_model=ContactFromDB)
async def create_contact(data: ContactCreateData, contact_service: ContactService = Depends(get_contact_service)):
    try:
        return await contact_service.create_new_contact(data)
    except Exception as e:
        raise HTTPException(500, str(e))
    
@router.post('/{contact_id}/assign_operator', response_model=ContactFromDB)
async def assign_operator_to_contact(contact_id: int, contact_service: ContactService = Depends(get_contact_service)):
    pass
