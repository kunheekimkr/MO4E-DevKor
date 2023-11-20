from fastapi import FastAPI

from server.routes.member import router as MemberRouter

app = FastAPI()

app.include_router(MemberRouter, tags=["Student"], prefix="/member")
