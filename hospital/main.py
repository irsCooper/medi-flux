from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.hospitals.router import router as router_hospital
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
    title="Hospital Microsevices",
    docs_url="/ui-swagger",
    lifespan=lifespan
)

app.include_router(router_hospital)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8082, reload=True)