from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from mini_crm.db import get_db_session

from mini_crm.repos import (OperatorRepo,
                            LeadRepo,
                            SourceRepo,
                            SourceOperatorRepo,
                            ContactRepo)

from mini_crm.services import (OperatorService, 
                               LeadService,
                               SourceService,
                               SourceOperatorService,
                               ContactService)


# ----- repos -----

async def get_operator_repo(session: AsyncSession = Depends(get_db_session)) -> OperatorRepo:
    return OperatorRepo(session)

async def get_lead_repo(session: AsyncSession = Depends(get_db_session)) -> LeadRepo:
    return LeadRepo(session)

async def get_source_repo(session: AsyncSession = Depends(get_db_session)) -> SourceRepo:
    return SourceRepo(session)

async def get_source_operator_repo(session: AsyncSession = Depends(get_db_session)) -> SourceOperatorRepo:
    return SourceOperatorRepo(session)

async def get_contact_repo(session: AsyncSession = Depends(get_db_session)) -> ContactRepo:
    return ContactRepo(session)

# ----- services -----

async def get_operator_service(repo: OperatorRepo = Depends(get_operator_repo)) -> OperatorService:
    return OperatorService(repo)

async def get_lead_service(repo: LeadRepo = Depends(get_lead_repo)) -> LeadService:
    return LeadService(repo)

async def get_source_service(repo: SourceRepo = Depends(get_source_repo)) -> SourceService:
    return SourceService(repo)

async def get_source_operator_service(repo: SourceOperatorRepo = Depends(get_source_operator_repo)) -> SourceOperatorService:
    return SourceOperatorService(repo)

async def get_contact_service(repo: ContactRepo = Depends(get_contact_repo), 
                              operator_repo: OperatorRepo = Depends(get_operator_repo), 
                              source_repo: SourceRepo = Depends(get_source_repo), 
                              lead_repo: LeadRepo = Depends(get_lead_repo)
                              ) -> ContactService:
    return ContactService(repo=repo, 
                          operator_repo=operator_repo,
                          source_repo=source_repo,
                          lead_repo=lead_repo
                          )