from enum import Enum

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class UserRole(Enum):
    ADMIN = "admin"
    STUDENT = "student"

class User(BaseModel):
    id: int
    name: str
    age: int
    role: UserRole

class UserCreate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    role: Optional[UserRole] = None

Users = [
    User(id=1, name="Alice", age=20, role=UserRole.ADMIN),
    User(id=2, name="Bob", age=21, role=UserRole.STUDENT),
    User(id=3, name="Charlie", age=22, role=UserRole.STUDENT),
]

# Fail response
USER_NOT_FOUND = HTTPException(status_code=400, detail="User not found.")
NAME_IS_REQUIRED = HTTPException(status_code=400, detail="Name is required.")
AGE_IS_REQUIRED = HTTPException(status_code=400, detail="Age is required.")
ROLE_IS_REQUIRED = HTTPException(status_code=400, detail="Role is required.")

@app.post("/users", status_code=201)
def create_user(body: UserCreate):
    if body.name is None:
        raise NAME_IS_REQUIRED
    if body.age is None:
        raise AGE_IS_REQUIRED
    if body.role is None:
        raise ROLE_IS_REQUIRED
    new_user = User(id=len(Users)+1, name=body.name, age=body.age, role=body.role)
    Users.append(new_user)
    return new_user


@app.get("/users")
def read_users():
    return Users

@app.get("/users/{user_id}")
def read_item(user_id: int):
    if user_id > len(Users):
        raise USER_NOT_FOUND
    return Users[user_id-1]

@app.put("/users/{user_id}")
def update_item(body: UserCreate, user_id: int):
    if user_id > len(Users):
        raise USER_NOT_FOUND
    if body.name is not None:
        Users[user_id-1].name = body.name
    if body.age is not None:
        Users[user_id-1].age = body.age
    if body.role is not None:
        Users[user_id-1].role = body.role
    return Users[user_id-1]

@app.delete("/users/{user_id}")
def delete_item(user_id: int):
    if user_id > len(Users):
        raise USER_NOT_FOUND
    Users.pop(user_id-1)
    return {
        "message": "User with id {} has been deleted".format(user_id)
    }



