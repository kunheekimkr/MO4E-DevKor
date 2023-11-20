from typing_extensions import Literal
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class MemberSchema(BaseModel):
    name: str = Field(...)
    birthDate: str = Field(..., pattern="^\\d{4}-\\d{2}-\\d{2}$")
    role: Literal["admin", "student"] = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "name": "John Doe",
                "birthDate": "1999-01-01",
                "role": "student",
            }
        }


class UpdateMemberModel(BaseModel):
    name: Optional[str]
    birthDate: Optional[str] = Field(None, pattern="^\\d{4}-\\d{2}-\\d{2}$")
    role: Optional[Literal["admin", "student"]]

    class Config:
        schema_extra = {
            "example": {
                "name": "John Doe",
                "birthDate": "1999-01-01",
                "role": "admin",
            }
        }


def ResponseModel(data, code,message):
    return {
        "data": [data],
        "code": code,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}