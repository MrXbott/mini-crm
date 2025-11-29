from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from mini_crm.db import get_db_session

from mini_crm.repos.operator import OperatorRepo
from mini_crm.repos.lead import LeadRepo
from mini_crm.repos.source import SourceRepo
from mini_crm.repos.source_operator import SourceOperatorRepo
from mini_crm.repos.contact import ContactRepo

from mini_crm.services.operator import OperatorService
from mini_crm.services.lead import LeadService
from mini_crm.services.source import SourceService
from mini_crm.services.source_operator import SourceOperatorService
from mini_crm.services.contact import ContactService

async def get_operator_service(session: AsyncSession = Depends(get_db_session)) -> OperatorService:
    return OperatorService(repo=OperatorRepo(session=session))

async def get_lead_service(session: AsyncSession = Depends(get_db_session)) -> LeadService:
    return LeadService(repo=LeadRepo(session=session))

async def get_source_service(session: AsyncSession = Depends(get_db_session)) -> SourceService:
    return SourceService(repo=SourceRepo(session=session))

async def get_source_operator_service(session: AsyncSession = Depends(get_db_session)) -> SourceOperatorService:
    return SourceOperatorService(repo=SourceOperatorRepo(session=session))

async def get_contact_service(session: AsyncSession = Depends(get_db_session), 
                              operator_service=Depends(get_operator_service), 
                              source_service=Depends(get_source_service), 
                              lead_service=Depends(get_lead_service)
                              ) -> ContactService:
    return ContactService(repo=ContactRepo(session=session), 
                          operator_service=operator_service,
                          source_service=source_service,
                          lead_service=lead_service
                          )