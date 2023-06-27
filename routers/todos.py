from pydantic import BaseModel, Field
from fastapi import APIRouter, Path
from starlette import status

from fastapi import HTTPException

from models.todo import Todos
from .deps import db_dependency, user_dependency
from util.errors import no_user

router = APIRouter()


class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool


# @router.get("/", status_code=status.HTTP_200_OK)
# async def read_all(user: user_dependency, db: db_dependency):
#     if user is None:
#         raise HTTPException(status_code=401, detail='Authentication Failed')
#     todo_model = db.query(Todos).filter(Todos.owner_id == user.get('id')).all()
#     if todo_model is not None:
#         return todo_model
#     raise HTTPException(status_code=404, detail='data is not exist')

@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    todo_model = db.query(Todos).all()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail='data is not exist')


@router.get("/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    no_user(user)
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail='data is not exist')


@router.post("/create_todo", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency, db: db_dependency, todo_request: TodoRequest):
    no_user(user)
    todo_model = Todos(**todo_request.dict(), owner_id=user.get('id'))
    db.add(todo_model)
    db.commit()


@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user: user_dependency, db: db_dependency, todo_request: TodoRequest, todo_id: int = Path(gt=0)):
    no_user(user)
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='todo not found')

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    no_user(user)
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='todo not found')
    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()
