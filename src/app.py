from src.users.routes import router as user_router
from fastapi import FastAPI

app = FastAPI()
app.include_router(user_router)

