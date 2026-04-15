from fastapi import FastAPI, requests
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.routes import manager, user, auth
from app.db.database import Base,engine
from sqlalchemy.orm import Session
from app.db import models
from app.db.utils import seed_status
from app.config.settings import CustomException

Base.metadata.create_all(bind =engine)

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: requests, exc: RequestValidationError):
    return JSONResponse(
        status_code=404,
        content={
            "status": False,
            "message": "Not Found",
            "data": None
        }
    )

@app.exception_handler(404)
async def not_found_exception_handler(request: requests, exc):
    return JSONResponse(
        status_code=404,
        content={
            "status": False,
            "message": "Not Found",
            "data": None
        }
    )
@app.exception_handler(CustomException)
async def custom_exception_handler(request: requests, exc: CustomException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": False,
            "message": exc.message
        }
    )
app.include_router(auth.router)
app.include_router(manager.router)
app.include_router(user.router)
