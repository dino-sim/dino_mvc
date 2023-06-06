from fastapi import APIRouter

from routers import todos, auth, user

api_router = APIRouter()

api_router.include_router(todos.router, prefix='/todo', tags=['todo'])
api_router.include_router(auth.router, prefix='/auth', tags=['auth'])
api_router.include_router(user.router, prefix='/user', tags=['user'])
