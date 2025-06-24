import traceback

import botocore.exceptions
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from ichain_configurator.configurator import get_config
from ichain_logger.logger import logger

config = get_config()

description = """
INTEGRICHAIN ADMIN AUTH API helps you do awesome stuff. 🚀

[GitHub repository - **Integrichain Admin SSO**](https://github.integrichain.net/ProductEngineering/integrichain-admin).
"""

tags_metadata = [
    {
        "name": "Login Actions",
        "description": "Actions for user login.",
    },
    {
        "name": "Password Actions",
        "description": "Actions for user password.",
    },
    {
        "name": "User Actions",
        "description": "Actions for user.",
    },
    {
        "name": "Health Check",
        "description": "Actions to check the API is alive",
    },
    {
        "name": "IDP Actions",
        "description": "Actions IDP workflow.",
    }
]

app = FastAPI(
    title="INTEGRICHAIN AUTH API",
    description=description,
    version="2.7.2",
    openapi_tags=tags_metadata
)

app.add_middleware(GZipMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.get('API_ORIGIN', '*').split(','),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(content={
        'message': str(exc.detail)
    }, status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(content={
        'message': str(exc)
    }, status_code=400)


@app.exception_handler(ValueError)
async def value_error_exception_handler(request, exc):
    return JSONResponse(content={
        'message': str(exc)
    }, status_code=400)


@app.exception_handler(botocore.exceptions.ClientError)
async def boto_core_exception_handler(request, exc):
    logger.error(traceback.format_exc())

    message = str(exc)

    return JSONResponse(content={
        'message': f'Boto3Exception: {message}'
    }, status_code=400 if '(NotAuthorizedException)' in message else 409)


@app.exception_handler(Exception)
async def internal_server_exception_handler(request, exc):
    logger.error(traceback.format_exc())

    return JSONResponse(content={
        'message': str(exc)
    }, status_code=500)
