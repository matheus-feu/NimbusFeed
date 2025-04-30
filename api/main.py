from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.db.base_model import Base
from api.db.session import engine
from api.routes import climate_route, download_route

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(climate_route.router, prefix="/api", tags=["Climate"])
app.include_router(download_route.router, prefix="/api", tags=["Reports"])

Base.metadata.create_all(bind=engine)
