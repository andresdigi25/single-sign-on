import boto3
from ichain_configurator.configurator import get_config

from app.models.users import Authenticate, AuthenticateChallenge

client = boto3.client('cognito-idp', region_name='us-east-1')
config = get_config()


def authenticate(user: Authenticate):
    authenticate_response = {}

    cognito_response = client.initiate_auth(
        AuthFlow='USER_PASSWORD_AUTH',
        AuthParameters={
            'USERNAME': user.email,
            'PASSWORD': user.password
        },
        ClientId=config['COGNITO_CLIENT_ID']
    )

    if cognito_response.get('ChallengeName') == 'NEW_PASSWORD_REQUIRED':
        authenticate_response['challenge_name'] = cognito_response.get('ChallengeName')
        authenticate_response['session'] = cognito_response.get('Session')
        authenticate_response['email'] = user.email
    else:
        authenticate_response['access_token'] = cognito_response.get('AuthenticationResult').get('AccessToken')
        authenticate_response['refresh_token'] = cognito_response.get('AuthenticationResult').get('RefreshToken')

    return authenticate_response


def authenticate_challenge(challenge: AuthenticateChallenge):
    authenticate_response = {}

    cognito_response = client.admin_respond_to_auth_challenge(
        UserPoolId=config['COGNITO_POOL_ID'],
        ClientId=config['COGNITO_CLIENT_ID'],
        ChallengeName='NEW_PASSWORD_REQUIRED',
        ChallengeResponses={'NEW_PASSWORD': challenge.password, 'USERNAME': challenge.email},
        Session=challenge.session
    )

    authenticate_response['access_token'] = cognito_response.get('AuthenticationResult').get('AccessToken')
    authenticate_response['refresh_token'] = cognito_response.get('AuthenticationResult').get('RefreshToken')

    return authenticate_response


def sign_out(token: str):
    try:
        response = client.global_sign_out(AccessToken=token)
        print(response)
    except Exception as e:
        print(f"There is an error signing out cognito user {str(e)}")


