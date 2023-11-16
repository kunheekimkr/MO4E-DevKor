from enum import Enum

from fastapi import FastAPI
from pydantic import BaseModel

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
    name: str
    age: int
    role: UserRole

Users = [
    User(id=1, name="Alice", age=20, role=UserRole.ADMIN),
    User(id=2, name="Bob", age=21, role=UserRole.STUDENT),
    User(id=3, name="Charlie", age=22, role=UserRole.STUDENT),
]

@app.post("/users")
def create_user(body: UserCreate):
    new_user = User(id=len(Users)+1, name=body.name, age=body.age, role=body.role)
    Users.append(new_user)
    return new_user


@app.get("/users")
def read_users():
    return Users

@app.get("/users/{user_id}")
def read_item(user_id: int):
    return Users[user_id-1]

@app.put("/users/{user_id}")
def update_item(body: UserCreate, user_id: int):
    Users[user_id-1].name = body.name
    Users[user_id-1].age = body.age
    Users[user_id-1].role = body.role
    return Users[user_id-1]

@app.delete("/users/{user_id}")
def delete_item(user_id: int):
    Users.pop(user_id-1)
    return {
        "message": "User with id {} has been deleted".format(user_id)
    }



