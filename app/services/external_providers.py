import uuid
from datetime import datetime, timezone, timedelta
import requests
from fastapi import HTTPException
import jwt

from app.services.cookies import extract_token_from_cookie, extract_refresh_token_from_cookie
from app.services.users import get_user_info


async def request_tokens_from_cognito_oauth(headers, payload, response, url):
    res = requests.request("POST", url, headers=headers, data=payload)
    if res.status_code != 200:
        raise HTTPException(status_code=res.status_code, detail=res.json())
    tokens = res.json()
    return tokens


def _get_int_from_datetime(value: datetime) -> int:
    if not isinstance(value, datetime):  # pragma: no cover
        raise TypeError('a datetime is required')
    return int(value.timestamp())


def _get_jwt_identifier() -> str:
    return str(uuid.uuid4())


def extract_user(request, cookie_token_name, cookie_refresh_token_name):
    access_token = extract_token_from_cookie(request, cookie_token_name)
    if not access_token or access_token.strip() == '':
        return None
    refresh_token = extract_refresh_token_from_cookie(request, cookie_refresh_token_name)
    me = get_user_info(access_token, refresh_token)
    return me.email


def generate_jwt_payload(username):
    payload = {
        "sub": username,
        "email": username,
        "nickname": username,
        "iat": _get_int_from_datetime(datetime.now(timezone.utc)),
        "jti": _get_jwt_identifier()
        }
    return payload


def enconde_jwt(payload, jwt_secret, jwt_algorithm):
    token = jwt.encode(payload,jwt_secret, jwt_algorithm)
    return token

