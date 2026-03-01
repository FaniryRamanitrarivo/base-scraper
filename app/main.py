from fastapi import FastAPI
from app.presentation.api.routes import router
from app.presentation.api.scrap.scraper_routes import router as scraper_router

app = FastAPI()
app.include_router(router)
app.include_router(scraper_router)
