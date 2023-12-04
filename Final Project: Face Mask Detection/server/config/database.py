from fastapi.encoders import jsonable_encoder
import motor.motor_asyncio
from models.image import ImageRecordModel

MONGO_DETAILS = "mongodb://localhost:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.maskdetection
collection = database.get_collection("images_collection")


async def create_image_record(image_record: ImageRecordModel) -> ImageRecordModel:
    image_record = jsonable_encoder(image_record)
    record = await collection.insert_one(image_record)
    new_record = await collection.find_one({"_id": record.inserted_id})
    return new_record

async def update_image_record(image_record: ImageRecordModel) -> ImageRecordModel:
    image_record = jsonable_encoder(image_record)
    # Find Record with matching ImageRecodModel.fileName
    record = await collection.find_one({"fileName": image_record["fileName"]})
    if record:
        # Update Record with new ImageRecordModel
        updated_record = await collection.update_one(
            {"fileName": image_record["fileName"]}, {"$set": image_record}
        )
        if updated_record:
            updated_record = await collection.find_one({"fileName": image_record["fileName"]})
            return updated_record
        return None
    else:
        return None