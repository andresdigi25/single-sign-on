from enum import Enum

class Callers(str, Enum):
    dod_api = "dod-api"
    ga_api = "ga-api"
    events_api = "events-api"
    auth_api = "auth-api"
    news_api = "news-api"
    admin_api = "admin-api"
    icyte_ops = "icyte-ops"
    icyte_portal = "icyte-portal"
    jmeter = "jmeter"
    postman = "postman"
    swagger = "swagger"
    gtn = "gtn"

