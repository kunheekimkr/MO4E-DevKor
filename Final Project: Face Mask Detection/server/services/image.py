from fastapi import Depends
import boto3
import os

from schemas.image import S3URL, ImageRecordModel
import config.database as db
from tasks import mask_recognition_task

class ImageService():
    def __init__(self) -> None:
        pass
    
    def get_s3_upload_url(self, object_name:str) -> S3URL:
        """Generate a presigned URL S3 POST request to upload a file
        :param bucket_name: string
        :param object_name: string
        :param fields: Dictionary of prefilled form fields
        :param conditions: List of conditions to include in the policy
        :param expiration: Time in seconds for the presigned URL to remain valid
        :return: Dictionary with the following keys:
            url: URL to post to
            fields: Dictionary of form fields and values to submit with the POST
        :return: None if error.
        """

        # Generate a presigned S3 POST URL
        s3_client = boto3.client('s3')
        response = s3_client.generate_presigned_post("maskdetections3bucket",
                                                    object_name,
                                                    Fields=None,
                                                     Conditions=None,
                                                     ExpiresIn=3600)
        return response
    
    def get_s3_download_url(self, object_name:str) -> S3URL:
        s3_client = boto3.client('s3')
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': "maskdetections3bucket",
                                                            'Key': object_name},
                                                    ExpiresIn=3600)
        return response

    def create_image_record(self, image_record: ImageRecordModel) -> ImageRecordModel:
        return db.create_image_record(image_record)
    
    def update_image_record(self, image_record: ImageRecordModel) -> ImageRecordModel:
        return db.update_image_record(image_record)
    
    def make_prediction(self, image_record: ImageRecordModel) -> S3URL:
        image_url = self.get_s3_download_url("inputs/" + image_record.fileName)
        upload_info = self.get_s3_upload_url("results/" + image_record.fileName)
        task = mask_recognition_task.delay(image_url, upload_info, image_record.fileName)

        results: int
        try:
            results =task.get(timeout=60)
            task.forget()
            results = results
            self.update_image_record({
                "fileName": image_record.fileName,
                "predicted": True,
                "is_correct": True
            })
        except task.exceptions.TimeoutError:
            results = 500

        result_info = self.get_s3_download_url("results/" + image_record.fileName)
        return result_info







