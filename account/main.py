from contextlib import asynccontextmanager
from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from src.authentication.router import router as router_authentication
from src.accounts.router import router as router_account
from src.doctors.router import router as router_doctors
from src.rabbit_mq.server import consume_rabbitmq

import uvicorn
import asyncio


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(consume_rabbitmq())
    try: 
        yield
    finally:
        task.cancel()



app = FastAPI(
    title="Account Microservices", 
    docs_url='/ui-swagger',
    lifespan=lifespan
)

app.include_router(router_authentication)
app.include_router(router_account)
app.include_router(router_doctors)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

if __name__ == "__main__":
    uvicorn.run("main:app", host='0.0.0.0', port=8081, reload=True)