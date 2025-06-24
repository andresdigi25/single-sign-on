from typing import List, Any, Dict, AnyStr, Union
from pydantic import BaseModel

JSONObject = Dict[AnyStr, Any]
JSONArray = List[Any]
JSONStructure = Union[JSONArray, JSONObject]


class Unauthorized(BaseModel):
    message: str = 'Unauthorized'


class BadRequest(BaseModel):
    message: str = 'Bad request'


class InternalServerError(BaseModel):
    message: str = 'Internal server error'


generic_responses_1 = {
    400: {'model': BadRequest},
    422: {'model': BadRequest},
    500: {'model': InternalServerError}
}

generic_responses_2 = {
    **generic_responses_1,
    **{401: {'model': Unauthorized}}
}

user_attributes_example = {
    "Username": "user@integrichain.com",
    "UserAttributes": [
        {
            "Name": "sub",
            "Value": "bc3347ca-7fd0-421b-ab1e-f2b574f47cd0"
        },
        {
            "Name": "email_verified",
            "Value": "true"
        },
        {
            "Name": "nickname",
            "Value": "Pepito"
        },
        {
            "Name": "email",
            "Value": "user@integrichain.com"
        }
    ],
    "UserCreateDate": "2022-06-06T15:40:26.340000-05:00",
    "UserLastModifiedDate": "2022-06-07T09:26:32.712000-05:00",
    "Enabled": True,
    "UserStatus": "CONFIRMED",
    "ResponseMetadata": {
        "RequestId": "158e27ec-4280-4b13-9827-a52e0cb17bc9",
        "HTTPStatusCode": 200,
        "HTTPHeaders": {
            "date": "Tue, 07 Jun 2022 19:06:16 GMT",
            "content-type": "application/x-amz-json-1.1",
            "content-length": "355",
            "connection": "keep-alive",
            "x-amzn-requestid": "158e27ec-4280-4b13-9827-a52e0cb17bc9"
        },
        "RetryAttempts": 0
    }
}

user_auth_events_example = {
    "AuthEvents": [
        {
            "EventId": "4210817f-e194-4823-911d-0e90e713e6b4",
            "EventType": "SignIn",
            "CreationDate": "2022-06-07T14:34:19.382000-05:00",
            "EventResponse": "Fail",
            "EventRisk": {
                "RiskDecision": "NoRisk",
                "CompromisedCredentialsDetected": False
            },
            "ChallengeResponses": [
                {
                    "ChallengeName": "Password",
                    "ChallengeResponse": "Failure"
                }
            ],
            "EventContextData": {
                "IpAddress": "181.136.36.176",
                "DeviceName": "0 Botocore 1, Other",
                "City": "Medellín",
                "Country": "Colombia"
            }
        }
    ],
    "ResponseMetadata": {
        "RequestId": "753b310d-0165-4bd9-8bea-dd2f021986bc",
        "HTTPStatusCode": 200,
        "HTTPHeaders": {
            "date": "Tue, 07 Jun 2022 19:34:55 GMT",
            "content-type": "application/x-amz-json-1.1",
            "content-length": "427",
            "connection": "keep-alive",
            "x-amzn-requestid": "753b310d-0165-4bd9-8bea-dd2f021986bc"
        },
        "RetryAttempts": 0
    }
}
