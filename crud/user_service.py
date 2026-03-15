from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import hashlib

from model.Users import Users
from schemas.user_schemas import UserLogin, UserResponse
from utils.jwtUtils import encode_jwt


async def login_by_pd(db: AsyncSession, user_login: UserLogin):
    """处理用户账密登录的逻辑"""
    phone = user_login.phone
    password = hashlib.md5(user_login.password.encode('utf-8')).hexdigest()

    result = await db.execute(select(Users).where(Users.phone == phone))
    user = result.scalars().one_or_none()
    if user and user.password_hash == password:
        data = {"user_id": user.id, "username": user.username}
        jwt = encode_jwt(data)
        return UserResponse(id=user.id, Authorization="Bearer "+jwt)
    else:
        return None


if __name__ == "__main__":
    # 测试密码加密
    password = "123456"
    hashed_password = hashlib.md5(password.encode('utf-8')).hexdigest()
