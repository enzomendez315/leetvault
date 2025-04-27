from fastapi import APIRouter

router = APIRouter(prefix="/problems", tags=["problems"])

@router.get("/")
async def get_problems():
    return {"problems": "Here are the problems"}