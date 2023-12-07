# tasks.py
from celery import Celery
from mask_recognition import mask_recognition


# Celery configuration
celery = Celery('tasks', broker='redis://localhost:6379', backend='redis://localhost:6379')

# Celery task
@celery.task(bind=True)
def mask_recognition_task(self, image_url, upload_info, file_name):
    pred_result = mask_recognition(image_url, upload_info, file_name)
    return pred_result
