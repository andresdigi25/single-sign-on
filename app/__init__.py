from app.api import app
from app.routers import health, users_actions, login_actions, password_actions, import_actions, external_providers_actions

app.include_router(
    login_actions.router,
    prefix='/users',
    tags=['Login Actions']
)

app.include_router(
    password_actions.router,
    prefix='/users',
    tags=['Password Actions']
)

app.include_router(
    users_actions.router,
    prefix='/users',
    tags=['User Actions']
)

app.include_router(
    import_actions.router,
    prefix='/users',
    tags=['Import Actions']
)

app.include_router(
    health.router,
    tags=['Health Check']
)

app.include_router(
    external_providers_actions.router,
    tags=['IDP Actions']
)
