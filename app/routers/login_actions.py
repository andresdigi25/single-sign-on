from fastapi import APIRouter, Response, Request
from ichain_configurator.configurator import get_config
from app.services import login as login_service
from app.models.users import Authenticate, AuthenticateChallengeResponse, AuthenticateChallenge, Tokens
from app.models.messages import MessageLogout
from app.models.responses import generic_responses_1, generic_responses_2
from app.services.cookies import set_access_cookie, set_refresh_cookie, delete_cookies, extract_token_from_cookie
from app.services.login import sign_out

router = APIRouter()

config = get_config()
domain = config.get('DOMAIN', 'localhost')
max_age = int(config.get('COOKIE_MAX_AGE', 3600))
cookie_token_name = config.get('COOKIE_TOKEN_NAME', 'x-icyte-token-auth')
cookie_refresh_token_name = config.get('COOKIE_REFRESH_TOKEN_NAME', 'x-icyte-refresh-auth')


@router.post(
    '/login',
    status_code=200,
    response_model=AuthenticateChallengeResponse,
    responses=generic_responses_2
)
async def login(user: Authenticate, response: Response):
    """
        Login the user and return the required info to the UI to interpret the workflow like show reset, forgot or client page:

        ### Json payload structure:
        - **email**: required
        - **password**: required
    """

    authenticate_response = login_service.authenticate(user)

    if authenticate_response.get('access_token'):
        set_access_cookie(response, authenticate_response.get('access_token'), cookie_token_name, domain, max_age)

    if authenticate_response.get('refresh_token'):
        set_refresh_cookie(response, authenticate_response.get('refresh_token'), cookie_refresh_token_name,domain, max_age)


    return AuthenticateChallengeResponse(**authenticate_response)


@router.post(
    '/challenge',
    status_code=200,
    response_model=Tokens,
    responses=generic_responses_1
)
async def challenge(challenge_inf: AuthenticateChallenge, response: Response):
    """
        Accept the challenge to be able to activate your account:

        ### Json payload structure:
        - **email**: required
        - **password**: required
        - **session**: required - You can get this value using the **Login** resource explained above.
    """

    authenticate_response = login_service.authenticate_challenge(challenge_inf)

    if authenticate_response.get('access_token'):
        set_access_cookie(response, authenticate_response.get('access_token'), cookie_token_name,domain, max_age)

    if authenticate_response.get('refresh_token'):
        set_refresh_cookie(response, authenticate_response.get('refresh_token'),cookie_refresh_token_name, domain, max_age)

    return authenticate_response


@router.get(
    '/logout',
    status_code=200,
    response_model=MessageLogout,
    responses=generic_responses_1
)
async def logout(request: Request, response: Response):
    """
        Logout the user deleting the `x-icyte-token-auth` and `x-icyte-refresh-auth` cookie by environment:
    """
    access_token = extract_token_from_cookie(request, cookie_token_name)
    delete_cookies(request, response, cookie_token_name, cookie_refresh_token_name, domain)
    if access_token is not None:
        sign_out(access_token)
    return MessageLogout()

@router.get('/slo-url',
            status_code=200)
async def get_slo_url():
    """
        Get the SLO URL from the request.
    """
    cognito_domain = config.get('COGNITO_USER_POOL_DOMAIN')
    client_id =  config.get('COGNITO_CLIENT_ID')
    if not cognito_domain or not client_id:
        raise ValueError("Cognito domain or client ID is not configured.")
    logout_url = f"{cognito_domain}/logout?client_id={client_id}"
    return {
        "success": True,
        "requires_redirect": True,
        "logout_url": logout_url
    }