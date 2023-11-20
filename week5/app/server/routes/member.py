from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from server.database import (
    add_member,
    delete_member,
    retrieve_member,
    retrieve_members,
    update_member,
)
from server.models.member import (
    ErrorResponseModel,
    ResponseModel,
    MemberSchema,
    UpdateMemberModel
)

router = APIRouter()

# Create
@router.post("/", response_description="Member data added into the database")
async def add_member_data(member: MemberSchema = Body(...)):
    member = jsonable_encoder(member)
    new_member = await add_member(member)
    return ResponseModel(new_member, 201, "Member added successfully.")

# Read
@router.get("/", response_description="Members retrieved")
async def get_members():
    members = await retrieve_members()
    if members:
        return ResponseModel(members, 200, "Members data retrieved successfully")
    return ResponseModel(members, 200,"Empty list returned")


@router.get("/{id}", response_description="Member data retrieved")
async def get_member_data(id):
    member = await retrieve_member(id)
    if member:
        return ResponseModel(member, 200, "Member data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Member doesn't exist.")

# Update
@router.put("/{id}")
async def update_member_data(id: str, req: UpdateMemberModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_member = await update_member(id, req)
    if updated_member:
        return ResponseModel(
            "Member with ID: {} update is successful".format(id),200,
            "Member data updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the member data.",
    )

# Delete
@router.delete("/{id}", response_description="Member data deleted from the database")
async def delete_member_data(id: str):
    deleted_member = await delete_member(id)
    if deleted_member:
        return ResponseModel(
            "Member with ID: {} removed".format(id), 200, "Member deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Member with id {0} doesn't exist".format(id)
    )