from fastapi import FastAPI

from app.api import routes

app = FastAPI()
app.include_router(router=routes.api_router)
