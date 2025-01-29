from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi_pagination import add_pagination

from db.session import create_db_and_tables
from endpoints.wallet import wallet_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(wallet_router)

add_pagination(app)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", log_level="info", reload=True)
