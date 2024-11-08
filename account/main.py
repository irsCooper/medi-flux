from contextlib import asynccontextmanager
from fastapi import FastAPI

from sqlalchemy.orm.strategy_options import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.core.db_helper import db
from src.authentication.router import router as router_authentication

import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await db.dispose()



app = FastAPI(
    title="Account Microservices", 
    docs_url='/ui-swagger',
    lifespan=lifespan
)

app.include_router(router_authentication)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8000)