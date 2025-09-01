from fastapi import FastAPI

from app.users.router import router as users_router
from app.tables.router import router as tables_router

app = FastAPI()

app.include_router(users_router)
