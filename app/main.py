from fastapi import FastAPI
from .api import endpoints

app = FastAPI(
    title="ActiveCampaign MySQL Bridge",
    description="Sync ActiveCampaign contacts to MySQL",
    version="1.0"
)

app.include_router(endpoints.router)
