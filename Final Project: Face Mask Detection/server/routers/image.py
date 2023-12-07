from fastapi import APIRouter, Depends, Body

from schemas.image import S3URL, ImageRecordModel
from services.image import ImageService

router = APIRouter(
    prefix='/image',
    tags=["images"],
    responses={
        404: { "description": "Not found"}
    }
)

@router.get('/get-s3-upload-url', response_model=S3URL)
async def get_s3_upload_url(object_name: str, service: ImageService = Depends()):
    result = service.get_s3_upload_url(object_name)
    return result

@router.post('/create-image-record', response_model= ImageRecordModel)
async def create_image_record(image_record: ImageRecordModel = Body(...), service: ImageService = Depends()):
    result = await service.create_image_record(image_record)
    return result

@router.put('/update-image-record', response_model= ImageRecordModel)
async def update_image_record(image_record: ImageRecordModel = Body(...), service: ImageService = Depends()):
    result = await service.update_image_record(image_record)
    return result

@router.post('/make-prediction', response_model= str)
async def make_prediction(image_record: ImageRecordModel = Body(...), service: ImageService = Depends()):
    result = service.make_prediction(image_record)
    return result

@router.get('/get-prediction-result', response_model= dict)
async def get_prediction_result(fileName: str, task_id: str, service: ImageService = Depends()):
    result = service.get_prediction_result(fileName, task_id)
    return result