from ichain_configurator.configurator import get_config
from pydantic import EmailStr
from fastapi import APIRouter, Depends,Request, Response, HTTPException
from app.services import users as user_service, auth as auth_service

from app.models.users import NewUser, User, UserAttribute, Me
from app.models.messages import MessageNewUserCreated, MessageNewUserDeleted, MessageUserDisable, MessageUserEnable, \
    MessageUserAttributeUpdated
from app.models.responses import generic_responses_1, user_attributes_example, user_auth_events_example
from app.services.cookies import set_access_cookie
from app.services.users import get_user_info

router = APIRouter()
config = get_config()
cookie_token_name = config.get('COOKIE_TOKEN_NAME', 'x-icyte-token-auth')
cookie_refresh_token_name = config.get('COOKIE_REFRESH_TOKEN_NAME', 'x-icyte-refresh-auth')
domain = config.get('DOMAIN', 'localhost')
max_age = int(config.get('COOKIE_MAX_AGE', 3600))



@router.post(
    '/',
    status_code=201,
    response_model=MessageNewUserCreated,
    responses=generic_responses_1#,
    #dependencies=[Depends(auth_service.api_key_protected)]
)
async def new_user(user: NewUser, resend: bool = False, supress: bool = False):
    """
        Create a user with basic information like: nickname, email:

        ### Authentication: `x-api-key`

        ### Json payload structure:
        - **nickname**: required
        - **email**: required
        - **password**: required
        - **isReadOnly**: optional
    """
    user_service.create_new_user(user, resend, supress)
    return MessageNewUserCreated()


@router.delete(
    '/',
    status_code=201,
    response_model=MessageNewUserDeleted,
    responses=generic_responses_1,
    dependencies=[Depends(auth_service.api_key_protected)]
)
async def delete_user(user: User):
    """
        Delete your account, this action can't be undone:

        ### Authentication: `x-api-key`

        ### Json payload structure:
        - **email**: required
    """

    user_service.delete_user(user)

    return MessageNewUserDeleted()


@router.delete(
    '/disable',
    status_code=201,
    response_model=MessageUserDisable,
    responses=generic_responses_1,
    dependencies=[Depends(auth_service.api_key_protected)]
)
async def disable_user(user: User):
    """
        Disable a specific user:

        ### Authentication: `x-api-key`

        ### Json payload structure:
        - **email**: required
    """

    user_service.disable_user(user)

    return MessageUserDisable()


@router.post(
    '/enable',
    status_code=201,
    response_model=MessageUserEnable,
    responses=generic_responses_1,
    dependencies=[Depends(auth_service.api_key_protected)]
)
async def enable_user(user: User):
    """
        Enable a specific user:

        ### Authentication: `x-api-key`

        ### Json payload structure:
        - **email**: required
    """

    user_service.enable_user(user)

    return MessageUserEnable()


@router.post(
    '/attributes',
    status_code=201,
    response_model=MessageUserAttributeUpdated,
    responses=generic_responses_1,
    dependencies=[Depends(auth_service.api_key_protected)]
)
async def update_user_attributes(user: UserAttribute):
    """
        Update some user attributes like nickname:

        ### Authentication: `x-api-key`

        ### Json payload structure:
        - **email**: required
        - **attribute**: required
        - **value**: required
    """

    user_service.update_user_attributes(user)

    return MessageUserAttributeUpdated()


@router.get(
    '/attributes/{email}',
    responses={**{201: {'content': {'application/json': {'example': user_attributes_example}}}}, **generic_responses_1}
)
async def user_attributes(email: EmailStr):
    """
        Get the user attributes by email:
    """

    return user_service.get_user_by_id(email)


@router.get(
    '/users',
    responses={**{201: {'content': {'application/json': {'example': user_attributes_example}}}}, **generic_responses_1}
)
async def get_users():
    """
        Get the users:
    """

    return user_service.list_users()


@router.get(
    '/users/email',
    responses={**{201: {'content': {'application/json': {'example': user_attributes_example}}}}, **generic_responses_1}
)
async def filter_users(email: EmailStr):
    """
        Filter the users:
    """

    return user_service.filter_users(email)


@router.post(
    '/users/email',
    responses={**{201: {'content': {'application/json': {'example': user_attributes_example}}}}, **generic_responses_1}
)
async def filter_users(user: User):
    """
        Filter the users:
    """

    return user_service.filter_users(user.email)


@router.post('/user/events',
             status_code=200,
             responses={**{200: {'content': {'application/json': {'example': user_auth_events_example}}}},
                        **generic_responses_1}
             )
async def events_by_user(user: User):
    """
        Get events by user:

        ### Json payload structure:
        - **email**: required
    """

    return user_service.events_by_user(user)



@router.get(
    '/me',
    status_code=200,
    response_model=Me,
    responses=generic_responses_1
)
async def me(request: Request,response: Response) -> Me:
    try:
        access_token = request.cookies.get(cookie_token_name)
        refresh_token = request.cookies.get(cookie_refresh_token_name)
        if not access_token or  access_token.strip() == '':
            raise HTTPException(status_code=401, detail='Unauthorized :(')
        me = get_user_info(access_token, refresh_token)
        if me.new_access_token:
            me.access_token = me.new_access_token
            set_access_cookie(response, me.access_token, cookie_token_name, domain, max_age)
        return me
    except Exception as ex:
        print(str(ex))
        raise HTTPException(status_code=401, detail='Unauthorized :(')
