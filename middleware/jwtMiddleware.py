from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from jose import jwt
import json

from schemas.result import error_response
from utils.envUtils import jwt_secret_key,jwt_algorithm
from utils.jwtUtils import decode_jwt
from utils.threadUtils import set_user_id, reset_user_id

# --- 配置 ---
SECRET_KEY = jwt_secret_key
ALGORITHM = jwt_algorithm


class JWTMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 1. 定义需要排除的路径
        excluded_paths = ["/user/login","/docs","/openapi.json", "/redoc"]

        # 2. 检查当前请求路径是否在排除列表中
        if request.url.path in excluded_paths:
            # 如果是登录接口，则直接放行，不进行任何 Token 检查
            response = await call_next(request)
            return response

        # 3. 从请求头中获取 Authorization
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            # 如果没有找到正确的 Authorization 头，返回 401
            return JSONResponse(status_code=401,content=error_response(message="无有效验证,请重新登录").model_dump())

        # 4. 提取 Token
        token = auth_header.split(" ")[1]

        # 5. 解析 JWT Token
        try:
            res = decode_jwt(token)
            # 解析成功，可以将用户信息等附加到 request 对象上，供后续处理函数使用
            request.state.user = res
            token_ctx = set_user_id(res.get('user_id'))
        except jwt.JWTError:
            # 如果解析失败（签名无效、过期等），返回 401
            return JSONResponse(status_code=401, content=error_response(message="无有效验证,请重新登录").model_dump())


        # 6. Token 验证通过，继续处理请求
        try:
            response = await call_next(request)
            return response
        finally:
            if token_ctx is not None:
                reset_user_id(token_ctx)