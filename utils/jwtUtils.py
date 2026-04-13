from datetime import datetime, timedelta
from typing import Optional

from jose import jwt

from utils.envUtils import jwt_algorithm, jwt_secret_key

# --- 配置 ---
SECRET_KEY = jwt_secret_key
ALGORITHM = jwt_algorithm


def encode_jwt(data: dict, expires_delta: Optional[timedelta] = None):
    """
    此函数用于创建 JWT 访问令牌
    - data: 你想放入 Token 的核心信息，例如 {"sub": "johndoe"}
    - expires_delta: Token 的有效期
    """
    # 1. 复制一份传入的数据，避免修改原始数据
    to_encode = data.copy()

    # 2. 计算并设置过期时间
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=60)
    # 将过期时间添加到待编码的数据中
    to_encode.update({"exp": expire})

    # 3. 使用密钥和算法对数据进行编码和签名，生成最终的 Token 字符串
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_jwt(token: str):
    """
    解析 JWT Token。
    Args:
        token (str): JWT Token 字符串。
        secret_key (str): 用于解码的密钥。
        algorithm (str): 加密算法，默认为 "HS256"。

    Returns:
        dict: 解析出的 Token 内容 (Payload)。
              如果解析失败，会抛出异常。
    """
    res = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return res



if __name__ == "__main__":
    # 测试编码和解码
    sample_data = {"user_id": 1, "username": "johndoe"}
    token = encode_jwt(sample_data)
    print("Encoded JWT:", token)
    res = decode_jwt(token)
    print("Decoded JWT:", res)
