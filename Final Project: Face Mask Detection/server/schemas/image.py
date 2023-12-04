from pydantic import BaseModel
from typing import Optional


class S3URL(BaseModel):
    url: str
    fields: Optional[dict] = None