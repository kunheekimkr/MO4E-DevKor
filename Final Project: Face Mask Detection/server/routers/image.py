from fastapi import APIRouter, Depends

from schemas.image import S3URL
from services.image import ImageService

router = APIRouter(
    prefix='/image',
    tags=["images"],
    responses={
        404: { "description": "Not found"}
    }
)

@router.get('/create-s3-upload-url', response_model=S3URL)
async def create_s3_upload_url(object_name: str, service: ImageService = Depends()):
    result = service.create_s3_upload_url(object_name)
    return result
