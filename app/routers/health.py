from fastapi import APIRouter, Depends
from ichain_configurator.configurator import get_config
from app.services import auth

router = APIRouter()

config = get_config()


@router.get('/ping')
async def pong():
    return {'ping': 'pong!'}


@router.get('/config', dependencies=[Depends(auth.api_key_protected)])
async def pong():
    return config


