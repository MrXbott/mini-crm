from fastapi import FastAPI
from contextlib import asynccontextmanager

from mini_crm.models.base import Base
from mini_crm.db import async_engine
from mini_crm.api.v1 import contacts, operators, sources, leads
from mini_crm.settings import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(contacts.router, prefix=settings.api_prefix)
app.include_router(operators.router, prefix=settings.api_prefix)
app.include_router(sources.router, prefix=settings.api_prefix)
app.include_router(leads.router, prefix=settings.api_prefix)


