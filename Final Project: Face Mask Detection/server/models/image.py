from pydantic import BaseModel

class ImageRecordModel(BaseModel):
    fileName: str
    predicted: bool = False
    is_correct: bool = False
