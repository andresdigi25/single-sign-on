import boto3
from ichain_configurator.configurator import get_config
from ichain_logger.logger import logger

from app.models.messages import MessageForgotPassword, \
    MessageForgotPasswordUserForceChangePassword, MessageUserForceChangePassword
from app.models.users import User, UserConfirmForgotPassword, UserChangePassword, NewUser
from app.services.users import get_user, create_new_user

client = boto3.client('cognito-idp', region_name='us-east-1')
config = get_config()


def forgot_password(user: User):
    cognito_user_info = None
    try:
        cognito_user_info = get_user(user.email)
    except Exception as ex:
        logger.error(str(ex))
    if cognito_user_info and cognito_user_info.get('UserStatus') != 'FORCE_CHANGE_PASSWORD':
        client.forgot_password(ClientId=config['COGNITO_CLIENT_ID'], Username=user.email)
        return MessageForgotPassword()
    else:
        return MessageUserForceChangePassword()


def confirm_forgot_password(user: UserConfirmForgotPassword):
    client.confirm_forgot_password(
        ClientId=config['COGNITO_CLIENT_ID'],
        Username=user.email,
        ConfirmationCode=user.confirm_code,
        Password=user.password
    )


def change_password(user: UserChangePassword, access_token: str):
    client.change_password(
        PreviousPassword=user.previous_password,
        ProposedPassword=user.new_password,
        AccessToken=access_token
    )


def admin_reset_password(user: User):
    client.admin_reset_user_password(
        UserPoolId=config['COGNITO_POOL_ID'],
        Username=user.email
    )
