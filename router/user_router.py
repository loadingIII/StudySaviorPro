from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from crud.user_service import login_by_pd
from schemas.result import success_response, error_response
from schemas.user_schemas import UserLogin
from utils.dbUtils import get_db

user_router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@user_router.post("/login")
async def login(user_login: UserLogin,db: AsyncSession = Depends(get_db)):
    user = await login_by_pd(db, user_login)
    # # 将 ORM 对象转换为 Pydantic 模型
    # user_data = UserResponse.model_validate(user)
    if user is None:
        return error_response(data=None, message="Invalid phone or password")
    return success_response(data=user,message="Login successful")