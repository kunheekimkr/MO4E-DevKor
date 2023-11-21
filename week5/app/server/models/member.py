from typing_extensions import Literal
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field

class MemberSchema(BaseModel):
    name: str = Field(...)
    birthDate: datetime = Field(...)
    role: Literal["admin", "student"] = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "name": "John Doe",
                "birthDate": "",
                "role": "student",
            }
        }


class UpdateMemberModel(BaseModel):
    name: Optional[str] = None
    birthDate: Optional[datetime] = None
    role: Optional[Literal["admin", "student"]] = None

    class Config:
        schema_extra = {
            "example": {
                "name": "John Doe",
                "birthDate": "1999-01-01",
                "role": "admin",
            }
        }


def ResponseModel(data, code, message):
    return {
        "data": data,
        "code": code,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}