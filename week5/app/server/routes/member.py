from fastapi import APIRouter, Body, HTTPException
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

USER_NOT_FOUND = HTTPException(status_code=404, detail="User not found.")
router = APIRouter()

# Create
@router.post("/", response_description="Member data added into the database", status_code=201)
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
    raise USER_NOT_FOUND
# Update
@router.put("/{id}")
async def update_member_data(id: str, req: UpdateMemberModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    update_result = await update_member(id, req)
    if update_result[0]:
        return ResponseModel(
            update_result[2],update_result[1],
            "Member data updated successfully",
        )
    
    raise HTTPException(status_code=update_result[1], detail=update_result[2])

# Delete
@router.delete("/{id}", response_description="Member data deleted from the database")
async def delete_member_data(id: str):
    deleted_member = await delete_member(id)
    if deleted_member:
        return ResponseModel(
            "Member with ID: {} removed".format(id), 200, "Member deleted successfully"
        )
    raise USER_NOT_FOUND