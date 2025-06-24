from fastapi import APIRouter, Depends
from app.services import passwords as password_service, auth as auth_service

from app.models.users import User, UserConfirmForgotPassword, UserChangePassword, Me
from app.models.messages import MessageForgotPassword, MessageConfirmForgotPassword, MessageUserEnable
from app.models.responses import generic_responses_1

router = APIRouter()


@router.post(
    '/forgot_password',
    status_code=201,
    response_model=MessageForgotPassword,
    responses=generic_responses_1
)
async def forgot_password(user: User):
    """
        Request a challenge to be able to reset your password:

        ### Json payload structure:
        - **email**: required
    """
    return password_service.forgot_password(user)



@router.post(
    '/confirm_forgot_password',
    status_code=201,
    response_model=MessageConfirmForgotPassword,
    responses=generic_responses_1
)
async def confirm_forgot_password(user: UserConfirmForgotPassword):
    """
        Accept the challenge to reset your password:

        ### Json payload structure:
        - **email**: required
        - **password**: required
        - **confirm_code**: required
    """
    password_service.confirm_forgot_password(user)
    return MessageConfirmForgotPassword()


@router.post(
    '/change_password',
    status_code=201,
    response_model=MessageConfirmForgotPassword,
    responses=generic_responses_1
)
async def change_password(user: UserChangePassword, access_token: str = Depends(auth_service.get_token)):
    """
        Change your current password:

        ### Authentication: cookies `x-icyte-token-auth` and `x-icyte-refresh-auth`

        ### Json payload structure:
        - **previous_password**: required
        - **new_password**: required
    """
    password_service.change_password(user, access_token)
    return MessageConfirmForgotPassword()


@router.post(
    '/admin_reset_password',
    status_code=201,
    response_model=MessageUserEnable,
    responses=generic_responses_1,
    dependencies=[Depends(auth_service.api_key_protected)]
)
async def admin_reset_password(user: User):
    """
        Reset your admin password:

        ### Authentication: `x-api-key`

        ### Json payload structure:
        - **email**: required
    """
    password_service.admin_reset_password(user)
    return MessageUserEnable()
