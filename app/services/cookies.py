from fastapi import APIRouter, Response, Request


def set_access_cookie(response: Response, access_token: str, cookie_token_name: str, domain: str, max_age: int):
    response.set_cookie(
        key=cookie_token_name,
        value=access_token,
        domain=domain,
        samesite='none',
        secure=True,
        httponly=True,
        max_age=max_age
    )


def set_refresh_cookie(response: Response, refresh_token: str, cookie_refresh_token_name: str, domain: str, max_age: int):
    response.set_cookie(
        key=cookie_refresh_token_name,
        value=refresh_token,
        domain=domain,
        samesite='none',
        secure=True,
        httponly=True,
        max_age=max_age
    )


def delete_cookies(request: Request, response: Response, cookie_token_name: str, cookie_refresh_token_name: str, domain: str):
    response.delete_cookie(
        key=cookie_token_name,
        path='/',
        domain=domain
    )

    response.delete_cookie(
        key=cookie_refresh_token_name,
        path='/',
        domain=domain
    )


def extract_token_from_cookie(request: Request, cookie_token_name: str):
    access_token = request.cookies.get(cookie_token_name)
    if not access_token or access_token.strip() == '':
        return None
    return access_token


def extract_refresh_token_from_cookie(request: Request, cookie_refresh_token_name: str):
    refresh_token = request.cookies.get(cookie_refresh_token_name)
    if not refresh_token or refresh_token.strip() == '':
        return None
    return  refresh_token




