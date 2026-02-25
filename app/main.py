from fastapi import FastAPI

from app.users.router import router as users_router
from app.tables.router import router as tables_router
from app.menu.router import router as menu_router
from app.bookings.router import router as bookings_router


app = FastAPI()

app.include_router(users_router)
app.include_router(tables_router)
app.include_router(menu_router)
app.include_router(bookings_router)