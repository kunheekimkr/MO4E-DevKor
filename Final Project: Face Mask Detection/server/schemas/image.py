from pydantic import BaseModel
from typing import Optional


class S3URL(BaseModel):
    url: str
    fields: Optional[dict] = None

class ImageRecordModel(BaseModel):
    fileName: str
    predicted: bool = False
    is_correct: bool = False
    