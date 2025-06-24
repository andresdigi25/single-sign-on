from datetime import datetime
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from app.tools import string_tools


class NoExtraBaseModel(BaseModel):
    class Config:
        extra = 'forbid'


class ImportUser(NoExtraBaseModel):
    nickname: str
    email: EmailStr

    @field_validator('nickname', mode='before')
    def validate_empty_string(cls, value):
        if string_tools.is_empty_string(value):
            raise ValueError('Empty value not allowed')

        return value


class NewUser(BaseModel):
    nickname: str
    email: EmailStr
    password: str
    isReadOnly: Optional[bool] = False

    @field_validator('nickname', 'password', mode='before')
    def validate_empty_string(cls, value):
        if string_tools.is_empty_string(value):
            raise ValueError('Empty value not allowed')
        
        return value

    class Config:
        json_schema_extra = {
            'example': {
                'nickname': 'Pepito',
                'email': 'user@integrichain.com',
                'password': 'Ichain@123',
                'isReadOnly': False
            }
        }


class Authenticate(BaseModel):
    email: EmailStr
    password: str

    class Config:
        json_schema_extra = {
            'example': {
                'email': 'user@integrichain.com',
                'password': 'Ichain@123'
            }
        }


class Tokens(BaseModel):
    access_token: str
    refresh_token: str


class OauthInfo(BaseModel):
    code: str
    grant_type: str


class Me(BaseModel):
    id: str
    nickname: str
    email: EmailStr
    new_access_token: Optional[str]
    access_token: Optional[str]
    refresh_token:Optional[str]
    isReadOnly: Optional[bool] = False


class RefreshToken(BaseModel):
    refresh_token: str


class AuthenticateChallengeResponse(BaseModel):
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    challenge_name: Optional[str] = None
    session: Optional[str] = None
    email: Optional[EmailStr] = None


class AuthenticateChallenge(BaseModel):
    email: Optional[EmailStr]
    password: Optional[str]
    session: Optional[str]

    class Config:
        json_schema_extra = {
            'example': {
                'email': 'user@integrichain.com',
                'password': 'Ichain@123',
                'session': 'the session value returned by the Login resource'
            }
        }


class UserConfirmForgotPassword(BaseModel):
    email: EmailStr
    password: str
    confirm_code: str

    class Config:
        json_schema_extra = {
            'example': {
                'email': 'user@integrichain.com',
                'password': 'Ichain@123',
                'confirm_code': 'The confirm code that you received via email.'
            }
        }


class User(BaseModel):
    email: EmailStr

    class Config:
        json_schema_extra = {
            'example': {
                'email': 'user@integrichain.com'
            }
        }


class UserChangePassword(BaseModel):
    previous_password: str
    new_password: str

    class Config:
        json_schema_extra = {
            'example': {
                'previous_password': 'Ichain@123',
                'new_password': 'Ichain@1234'
            }
        }


class UserAttribute(BaseModel):
    email: EmailStr
    attribute: str
    value: str

    class Config:
        json_schema_extra = {
            'example': {
                'email': 'user@integrichain.com',
                'attribute': 'nickname',
                'value': 'Pepito 2'
            }
        }


class ImportUsersResponse(BaseModel):
    job_id: str

    class Config:
        json_schema_extra = {
            'example': {
                'job_id': 'import-LrjUOAtCAw'
            }
        }


class ImportUserStatusResponse(BaseModel):
    status: Optional[str]
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    imported_users: Optional[int]
    skipped_users: Optional[int]
    failed_users: Optional[int]
    message: Optional[str]


class ImportUsersResponse2(BaseModel):
    imported_users: int
    failed_users: int

    class Config:
        json_schema_extra = {
            'example': {
                'imported_users': 5,
                'failed_users': 2
            }
        }
