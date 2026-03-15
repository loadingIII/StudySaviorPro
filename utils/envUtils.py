import os
from pathlib import Path
from dotenv import load_dotenv

from utils.path_tool import get_abs_path

load_dotenv(get_abs_path(".env"))

qwen_api_key = os.getenv("QWEN_API_KEY")
qwen_url = os.getenv("QWEN_URL")
qwen_model_name = os.getenv("QWEN_MODEL_NAME")
zhi_pu_api_key = os.getenv("ZHI_PU_API_KEY")

tongyi_xiaomi_url = os.getenv("TONGYI_XIAOMI_URL")
tongyi_xiaomi_model_name = os.getenv("TONGYI_XIAOMI_MODEL_NAME")


jwt_secret_key = os.getenv("JWT_SECRET_KEY")
jwt_algorithm = os.getenv("ALGORITHM")


if __name__ == "__main__":
    print("QWEN_API_KEY:", zhi_pu_api_key)