# tasks.py
from celery import Celery
from mask_recognition import mask_recognition
import requests
from PIL import Image
from io import BytesIO


# Celery configuration
celery = Celery('tasks', broker='redis://localhost:6379', backend='redis://localhost:6379')

# Celery task
@celery.task(bind=True)
def mask_recognition_task(self, image_url, upload_info, file_name):

    # Download image
    image = requests.get(image_url).content
    image = Image.open(BytesIO(image)).convert("RGB")

    # Simulate a long-running task
    pred_result = mask_recognition(image, upload_info, file_name)
    return pred_result
