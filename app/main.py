from fastapi import FastAPI
from app.presentation.api.routes import router
from app.presentation.api.scrap.scraper_routes import router as scraper_router

from fastapi.exceptions import RequestValidationError
from app.presentation.validation_exception_handler import validation_exception_handler

app = FastAPI()
app.include_router(router)
app.include_router(scraper_router)

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler
)