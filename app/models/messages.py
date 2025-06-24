from pydantic import BaseModel


class MessageCookiesCreated(BaseModel):
    message: str = 'Authentication cookies created!'


class MessageNewUserCreated(BaseModel):
    message: str = 'New user created!'


class MessageLogout(BaseModel):
    message: str = 'Bye see you later :)'


class MessageNewUserDeleted(BaseModel):
    message: str = 'User deleted!'


class MessageForgotPassword(BaseModel):
    type: str = "CODE"
    message: str = 'You will get a verification code'


class MessageUserForceChangePassword(BaseModel):
    type: str = "USER_STATUS_PROBLEM"
    message: str = 'There is a problem with your account, please contact the administrator'


class MessageForgotPasswordUserNotFound(BaseModel):
    type: str = "USER_NOT_FOUND"
    message: str = 'User Does not exists'


class MessageForgotPasswordUserForceChangePassword(BaseModel):
    type: str = "RESEND"
    message: str = 'You will get a verification code'


class MessageConfirmForgotPassword(BaseModel):
    message: str = 'Your password was changed'


class MessageUserDisable(BaseModel):
    message: str = 'User Disable'


class MessageUserEnable(BaseModel):
    message: str = 'User Enable'


class MessageUserAttributeUpdated(BaseModel):
    message: str = 'Attribute Updated'
