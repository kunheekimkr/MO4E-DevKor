import motor.motor_asyncio
from bson.objectid import ObjectId

MONGO_DETAILS = "mongodb://localhost:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.members

member_collection = database.get_collection("members_collection")


# helpers

def member_helper(member) -> dict:
    return {
        "id": str(member["_id"]),
        "name": member["name"],
        "birthDate": member["birthDate"],
        "role": member["role"],
    }


# Retrieve all members present in the database
async def retrieve_members():
    members = []
    async for member in member_collection.find():
        members.append(member_helper(member))
    return members


# Add a new member into to the database
async def add_member(member_data: dict) -> dict:
    member = await member_collection.insert_one(member_data)
    new_member = await member_collection.find_one({"_id": member.inserted_id})
    return member_helper(new_member)


# Retrieve a member with a matching ID
async def retrieve_member(id: str) -> dict:
    member = await member_collection.find_one({"_id": ObjectId(id)})
    if member:
        return member_helper(member)


# Update a member with a matching ID
async def update_member(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return (False, 400, "No fields to update provided.")
    member = await member_collection.find_one({"_id": ObjectId(id)})
    if member:
        updated_member = await member_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_member:
            updated_member = await member_collection.find_one({"_id": ObjectId(id)})
            return (True, 200, member_helper(updated_member))
        return (False, 500, "An Error Occured While Updating The Member")
    else:
        return (False, 404, "Member not found")

# Delete a member from the database
async def delete_member(id: str):
    member = await member_collection.find_one({"_id": ObjectId(id)})
    if member:
        await member_collection.delete_one({"_id": ObjectId(id)})
        return True