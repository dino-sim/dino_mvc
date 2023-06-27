from fastapi import HTTPException


def no_user(user: dict):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')


def error_msg(key: str):
    return f"{key} is not exist"


def no_model(model, data):
    if model is None:
        raise HTTPException(status_code=404, detail=f'Cannot found {data} info')
