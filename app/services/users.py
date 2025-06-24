import csv
import json
import uuid
import boto3
from botocore.exceptions import ClientError
import pandas as pd
import requests
import backoff

from ichain_configurator.configurator import get_config
from ichain_logger.logger import logger

from app.models.users import NewUser, User, UserAttribute, ImportUser, Me
from app.tools import string_tools
from app.tools.evaluate_exceptions import fatal_code

client = boto3.client('cognito-idp', region_name='us-east-1')
config = get_config()

MAX_RETRIES = int(config.get('MAX_RETRIES', 3))
RETRY_DELAY = int(config.get('RETRY_DELAY', 3))


def get_user_by_id(user_id: str):
    return client.admin_get_user(
        UserPoolId=config['COGNITO_POOL_ID'],
        Username=user_id
    )


def filter_users(email):
    '''
COGNITO_OUTPUT_TEMPLATE	{"is_external": true, "idp_name": "azureig","source": "DEFAULT"}
IDPS_PER_DOMAIN	{"seagen.com": "azureseagen","onelogin.com":"onelogin"}
    '''
    local_config = get_config()
    output_template = json.loads(local_config.get('COGNITO_OUTPUT_TEMPLATE','{}'))
    idps_per_domain = json.loads(local_config.get('IDPS_PER_DOMAIN','{}'))
    try:
        domain = email.split('@')[1]
        idp_name = idps_per_domain.get(domain)
        if idp_name:
            output_template['is_external'] = True
            output_template['idp_name'] = idp_name
            output_template['source'] = 'DOMAIN'
            return output_template

        users = []
        next_page = None
        kwargs = {
            'UserPoolId': config['COGNITO_POOL_ID'],
            'Filter': f"email = '{email}'"
        }
        users_remain = True
        while users_remain:
            if next_page:
                kwargs['PaginationToken'] = next_page
            response = client.list_users(**kwargs)
            users.extend(response['Users'])
            next_page = response.get('PaginationToken', None)
            users_remain = next_page is not None
        response = users
        if response:
            if response[0].get('UserStatus') != 'EXTERNAL_PROVIDER':
                output_template['is_external'] = False
                output_template['idp_name'] = ''
                output_template['source'] = 'COGNITO'

        return output_template
    except Exception as e:
        print(f"There is an error listing cognito users {str(e)}")

def list_users():
    try:
        users = []
        next_page = None
        kwargs = {
            'UserPoolId': config['COGNITO_POOL_ID'],
        }
        users_remain = True
        while users_remain:
            if next_page:
                kwargs['PaginationToken'] = next_page
            response = client.list_users(**kwargs)
            users.extend(response['Users'])
            next_page = response.get('PaginationToken', None)
            users_remain = next_page is not None
        return users
    except Exception as e:
        print(f"There is an error listing cognito users {str(e)}")



def get_user(user_id: str):
    try:
        return client.admin_get_user(UserPoolId=config['COGNITO_POOL_ID'],Username=user_id)
    except Exception as ex:
        logger.error(str(ex))
        raise ex


@backoff.on_exception(
    backoff.expo,
    Exception,
    max_tries=MAX_RETRIES,
    on_backoff=lambda _: logger.error(f"retrying_get_user_info_SSO-API: {_.get('tries')} - {_.get('wait')} - {_.get('elapsed')}"),
    jitter=lambda _: RETRY_DELAY,
    giveup=fatal_code
)
def get_user_info(access_token: str, refresh_token: str):
    nickname = None
    email = None
    new_access_token = None
    is_external_user = False
    isReadOnly = None
    try:
        response = client.get_user(AccessToken=access_token)
        logger.info(f"USER INFO RAW RESPONSE: {response}")
    except ClientError as e:
        print(f'CLIENT ERROR: {str(e)}')
        if e.response.get('message') == 'Access Token has expired':
            print(f'AUTH ERROR: {str(e)}')
            print(f'GETTING NEW TOKEN ')
            new_access_token = get_new_access_token(refresh_token)
            print(f'NEW TOKEN  {new_access_token}')
            response = client.get_user(AccessToken=new_access_token)
        else:
            raise e
    try:
        user_id = response.get('Username')
        for item in response['UserAttributes']:
            if item['Name'] == 'nickname':
                nickname = item['Value']
            if item['Name'] == 'email':
                email = item['Value']
            if item['Name'] == 'identities':
                is_external_user = True
            if item['Name'] == 'custom:isReadOnly':
                isReadOnly = item['Value']
        user_info = get_user(user_id)
        logger.info(user_info)
        if is_external_user:
            nickname = email
        return Me(id=user_id, nickname=nickname, email=email,access_token=access_token,refresh_token=refresh_token ,
                  new_access_token= new_access_token, isReadOnly=isReadOnly)
    except Exception as ex:
        logger.error(str(ex))
        raise ex


def get_new_access_token(refresh_token: str):
    response = client.initiate_auth(
        ClientId=config['COGNITO_CLIENT_ID'],
        AuthFlow='REFRESH_TOKEN_AUTH',
        AuthParameters={
            'REFRESH_TOKEN': refresh_token
        }
    )

    return response['AuthenticationResult']['AccessToken']


def create_new_user(user: NewUser, resend: bool = False, supress: bool = False):
    if resend:
        client.admin_create_user(
        UserPoolId=config['COGNITO_POOL_ID'],
        Username=user.email,
        TemporaryPassword=user.password,
        MessageAction='RESEND',
        UserAttributes=[
            {
                'Name': 'nickname',
                'Value': user.nickname
            },
            {
                'Name': 'email',
                'Value': user.email
            },
            {
                'Name': 'email_verified',
                'Value': 'true'
            },
            {
                'Name': 'custom:isReadOnly',
                'Value': str(user.isReadOnly)
            }
        ]
    )
        return
    elif supress:
        client.admin_create_user(
            UserPoolId=config['COGNITO_POOL_ID'],
            Username=user.email,
            TemporaryPassword=user.password,
            MessageAction='SUPPRESS',
            UserAttributes=[
                {
                    'Name': 'nickname',
                    'Value': user.nickname
                },
                {
                    'Name': 'email',
                    'Value': user.email
                },
                {
                    'Name': 'email_verified',
                    'Value': 'true'
                },
            {
                'Name': 'custom:isReadOnly',
                'Value': str(user.isReadOnly)
            }
            ]
        )
        return
    else:
        client.admin_create_user(
            UserPoolId=config['COGNITO_POOL_ID'],
            Username=user.email,
            TemporaryPassword=user.password,
            UserAttributes=[
                {
                    'Name': 'nickname',
                    'Value': user.nickname
                },
                {
                    'Name': 'email',
                    'Value': user.email
                },
                {
                    'Name': 'email_verified',
                    'Value': 'true'
                },
            {
                'Name': 'custom:isReadOnly',
                'Value': str(user.isReadOnly)
            }
            ]
        )
        return



def delete_user(user: User):
    client.admin_delete_user(
        UserPoolId=config['COGNITO_POOL_ID'],
        Username=user.email
    )


def disable_user(user: User):
    client.admin_disable_user(
        UserPoolId=config['COGNITO_POOL_ID'],
        Username=user.email
    )


def enable_user(user: User):
    client.admin_enable_user(
        UserPoolId=config['COGNITO_POOL_ID'],
        Username=user.email
    )


def update_user_attributes(user: UserAttribute):
    client.admin_update_user_attributes(
        UserPoolId=config['COGNITO_POOL_ID'],
        Username=user.email,
        UserAttributes=[
            {
                'Name': user.attribute,
                'Value': user.value
            }
        ]
    )


def events_by_user(user: User):
    return client.admin_list_user_auth_events(
        UserPoolId=config['COGNITO_POOL_ID'],
        Username=user.email,
        MaxResults=60
    )


def cognito_job_import_users_from_csv(csv_file_buffer):
    csv_reader = csv.DictReader(csv_file_buffer)
    items = [dict(ImportUser(**i)) for i in csv_reader]

    if len(items) == 0:
        raise ValueError('Invalid CSV content at least one item with the headers line')

    columns = ['name', 'given_name', 'family_name', 'middle_name', 'nickname', 'preferred_username', 'profile',
               'picture', 'website', 'email', 'email_verified', 'gender', 'birthdate', 'zoneinfo', 'locale',
               'phone_number', 'phone_number_verified', 'address', 'updated_at', 'cognito:mfa_enabled',
               'cognito:username']

    df = pd.DataFrame(columns=columns, data=[{
        'nickname': i.get('nickname'),
        'email': i.get('email'),
        'cognito:username': i.get('email'),
        'cognito:mfa_enabled': False,
        'email_verified': True,
        'phone_number_verified': False
    } for i in items])

    csv_out = df.to_csv(encoding='utf-8', index=False)

    create_response = client.create_user_import_job(
        JobName=str(uuid.uuid4()),
        UserPoolId=config['COGNITO_POOL_ID'],
        CloudWatchLogsRoleArn=config['CLOUDWATCH_LOGS_ROLE_ARN']
    )

    user_import_job = create_response.get('UserImportJob', {})

    job_id = user_import_job.get('JobId')
    presigned_url = user_import_job.get('PreSignedUrl')

    requests.put(presigned_url, data=csv_out, headers={
        'x-amz-server-side-encryption': 'aws:kms',
        'Content-Disposition': 'attachment;filename=import-users.csv'
    })

    return client.start_user_import_job(
        UserPoolId=config['COGNITO_POOL_ID'],
        JobId=job_id
    )


def import_users_status():
    def _get_items(items, pg_token):
        p = {
            'UserPoolId': config['COGNITO_POOL_ID'],
            'MaxResults': 60
        }

        if pg_token:
            p['PaginationToken'] = pg_token

        r = client.list_user_import_jobs(**p)

        items += r.get('UserImportJobs', [])
        pg_token = r.get('PaginationToken')

        if pg_token:
            return _get_items(items, pg_token)
        else:
            return items

    return _get_items([], None)


def import_users_from_csv(csv_file_buffer):
    csv_reader = csv.DictReader(csv_file_buffer)
    items = [dict(ImportUser(**i)) for i in csv_reader]

    success = 0
    failed = 0

    for i in items:
        i['password'] = string_tools.get_random_password()

        try:
            create_new_user(NewUser(**i))

            success += 1
        except Exception as ex:
            logger.error(f'{i}: {str(ex)}')
            failed += 1

    return success, failed
