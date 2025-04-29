from fastapi import FastAPI
from api.routes import climate

app = FastAPI()

app.include_router(climate.router, prefix="/api", tags=["Climate"])