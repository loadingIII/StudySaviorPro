from fastapi import FastAPI

from middleware.jwtMiddleware import JWTMiddleware
from router.agent_router import agent_router
from router.user_router import user_router
from router.vector_store_router import vector_store_router

app = FastAPI()


app.include_router(agent_router)
app.include_router(user_router)
app.include_router(vector_store_router)

#注册中间件
app.add_middleware(JWTMiddleware)
