from fastapi import HTTPException, Request, Security, Response
from fastapi.security import APIKeyHeader
from ichain_configurator.configurator import get_config

from app.models.users import Me
from app.services.cookies import set_access_cookie
from app.services.users import get_user_info

config = get_config()
cookie_token_name = config.get('COOKIE_TOKEN_NAME', 'x-icyte-token-auth')
api_key = config.get('API_KEY', '').strip()
API_KEY_NAME = "Authorization"


def api_key_protected(x_api_key: str = Security(APIKeyHeader(name=API_KEY_NAME, auto_error=False))):
    if x_api_key:
        x_api_key = x_api_key.strip()

    if api_key == '' or x_api_key == '' or x_api_key != api_key:
        raise HTTPException(status_code=401, detail='Unauthorized')

    return True


async def get_token(request: Request):
    try:
        access_token = request.cookies.get(cookie_token_name)
        return access_token
    except Exception as ex:
        print(str(ex))
        raise HTTPException(status_code=401, detail='Unauthorized :(')


