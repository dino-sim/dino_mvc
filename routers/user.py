from fastapi import APIRouter
from fastapi import HTTPException
from passlib.context import CryptContext
from pydantic import BaseModel, Field
from starlette import status

from models.user import Users
from .deps import user_dependency, db_dependency

router = APIRouter()


# for DI


def no_user(user):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')


bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class UserRequest(BaseModel):
    password: str
    new_password: str = Field(min_length=4)


def authenticated_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.password):
        return False
    return user


@router.get('/', status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail='Cannot found user info')
    return user_model


@router.put('/change_pwd', status_code=status.HTTP_204_NO_CONTENT)
async def change_pwd(user: user_dependency, db: db_dependency, user_request: UserRequest):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    if not bcrypt_context.verify(user_request.password, user_model.password):
        raise HTTPException(status_code=401, detail='Error on password change')
    user_model.password = bcrypt_context.hash(user_request.password)
    db.add(user_model)
    db.commit()
