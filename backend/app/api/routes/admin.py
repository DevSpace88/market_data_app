from fastapi import APIRouter, Depends
from ...auth import get_current_admin_user

router = APIRouter()

@router.get("/admin-test")
async def admin_test(current_user = Depends(get_current_admin_user)):
    return {"message": "You are an admin!"}