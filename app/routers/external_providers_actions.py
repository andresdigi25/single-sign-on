import requests as req
from fastapi import APIRouter, Response, Request, requests
from fastapi.responses import  RedirectResponse
from ichain_configurator.configurator import get_config
from ichain_logger.logger import logger
from app.models.users import Tokens, OauthInfo
from app.models.messages import  MessageCookiesCreated
from app.models.responses import generic_responses_2
from app.services.cookies import set_access_cookie, set_refresh_cookie, extract_token_from_cookie
from app.services import external_providers as external_providers_service


router = APIRouter()

config = get_config()
domain = config.get('DOMAIN', 'localhost')
max_age = int(config.get('COOKIE_MAX_AGE', 3600))
cookie_token_name = config.get('COOKIE_TOKEN_NAME', 'x-icyte-token-auth')
cookie_refresh_token_name = config.get('COOKIE_REFRESH_TOKEN_NAME', 'x-icyte-refresh-auth')
cognito_domain = config.get('COGNITO_USER_POOL_DOMAIN')
client_id = config.get('COGNITO_CLIENT_ID')
cognito_redirect_url = config.get('COGNITO_REDIRECT_URL')
grafana_redirect_url = config.get('GRAFANA_REDIRECT_URL')
grafana_get_cookie = config.get('GRAFANA_GET_COOKIE')


@router.post(
    '/idp-auth-from-code',
    status_code=201,
    response_model=MessageCookiesCreated,
    responses=generic_responses_2
)
async def idp_auth_from_code(oauth_info: OauthInfo, response: Response):
    """
        Login an user using and idp and the authorization code grant:

        ### Json payload structure:
        - **code**: required
        - **grant_type**: required
    """
    url = f"{cognito_domain}/token"
    payload = f'client_id={client_id}&code={oauth_info.code}&redirect_uri={cognito_redirect_url}' \
              f'&grant_type={oauth_info.grant_type}'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'XSRF-TOKEN=7ad7f2e4-edec-4cf0-88e2-05f4c478ea20'
    }
    tokens = await external_providers_service.request_tokens_from_cognito_oauth(headers, payload, response, url)
    if tokens.get('access_token') and tokens.get('refresh_token'):
        set_access_cookie(response, tokens.get('access_token'), cookie_token_name, domain, max_age)
        set_refresh_cookie(response, tokens.get('refresh_token'), cookie_refresh_token_name, domain, max_age)
    return MessageCookiesCreated()


@router.get('/sisense_sso', status_code=200)
def sisense_login(request: Request, customer: str = "default"):
    sisense_jwt_algorithm = config.get('JWT_ALGORITHM', 'HS256')
    sisense_jwt_secret = config.get('JWT_SECRET')
    sisense_redirect_url = config.get('SISENSE_REDIRECT_URL')
    if customer != "default":
        sisense_redirect_url = config.get('SISENSE_LILLY_REDIRECT_URL')
        sisense_jwt_secret = config.get('SISENSE_LILLY_JWT_SECRET')
    logger.info(f"SISENSE REDIRECT URL: {sisense_redirect_url}")
    logger.info(f"SISENSE JWT SECRET : {sisense_jwt_secret}")
    username = external_providers_service.extract_user(request, cookie_token_name, cookie_refresh_token_name)
    logger.info(f'USER NAME: {username}')
    if not username:
        return RedirectResponse(f"{cognito_redirect_url}?callback_url={sisense_redirect_url}")
    payload = external_providers_service.generate_jwt_payload(username)
    logger.info(f'PAYLOAD: {payload}')
    token = external_providers_service.enconde_jwt(payload, sisense_jwt_secret, sisense_jwt_algorithm)
    logger.info(f'TOKEN: {token}')
    return_to = request.query_params.get('return_to')
    logger.info(f"RETURN TO PARAMETER: {return_to}")
    redirect_url = f'{sisense_redirect_url}/jwt?jwt={token}'
    if return_to:
        redirect_url = f'{redirect_url}&return_to={return_to}'
    return RedirectResponse(redirect_url)


@router.get('/grafana_sso', status_code=200)
def grafana_login(request: Request):
    print('GET COOKIE')
    cookie_value = extract_token_from_cookie(request, cookie_token_name)
    username = external_providers_service.extract_user(request, cookie_token_name, cookie_refresh_token_name)
    print(f'USER NAME: {username}')
    if not username:
        return RedirectResponse(grafana_get_cookie)
    if cookie_value is None:
        print("CAN'T GET THE COOKIE")
        return RedirectResponse(grafana_get_cookie)
    grafana_url = "{0}?auth_token={1}".format(grafana_redirect_url, cookie_value)
    header = {"X-JWT-Assertion": cookie_value, "X-WEBAUTH-USER": username}
    print(f'GRAFANA URL: {grafana_url}')
    return RedirectResponse(url=grafana_url, status_code=302, headers=header)
