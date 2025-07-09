from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
import asyncio

from src.utils import create_index_if_not_exists, wait_for_elasticsearch
from src.history.router import router as router_history
from src.rabbit_mq.server import consume_rabbitmq
from src.core.db_helper import es


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(consume_rabbitmq())

    await wait_for_elasticsearch()  
    await create_index_if_not_exists()

    try:
        yield
    finally:
        task.cancel()
        await es.close()



app = FastAPI(
    title="Documents Microservices", 
    docs_url='/ui-swagger',
    lifespan=lifespan
)

app.include_router(router_history)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

if __name__ == "__main__":
    uvicorn.run("main:app", host='0.0.0.0', port=8084, reload=True)