from fastapi import Depends
import boto3
import os

from schemas.image import S3URL, ImageRecordModel
import config.database as db

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
        print("SERVICE")

        # Generate a presigned S3 POST URL
        s3_client = boto3.client('s3',
                                aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
                                aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"))
        response = s3_client.generate_presigned_post("maskdetections3bucket",
                                                    object_name,
                                                    Fields=None,
                                                     Conditions=None,
                                                     ExpiresIn=3600)
        return response
    
    def create_image_record(self, image_record: ImageRecordModel) -> ImageRecordModel:
        return db.create_image_record(image_record)
    
    def update_image_record(self, image_record: ImageRecordModel) -> ImageRecordModel:
        return db.update_image_record(image_record)