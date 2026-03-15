import yaml
import os

from utils.path_tool import get_abs_path


def load_config(config_path):
    """安全加载 YAML 配置文件"""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"配置文件 {config_path} 不存在")

    with open(config_path, 'r', encoding='utf-8') as file:
        try:
            config = yaml.safe_load(file)
            return config
        except yaml.YAMLError as exc:
            raise ValueError(f"YAML 解析错误: {exc}")


db_config = load_config(get_abs_path("properties/database.yml"))

chroma_config = load_config(get_abs_path("properties/chroma.yml"))

pg_url = f"postgresql://{db_config['pg_user']}:{db_config['pg_password']}@{db_config['pg_host']}:{db_config['pg_port']}/{db_config['pg_db']}"

pg_async_url = f"postgresql+asyncpg://{db_config['pg_user']}:{db_config['pg_password']}@{db_config['pg_host']}:{db_config['pg_port']}/{db_config['pg_db']}"




if __name__ == "__main__":
    print(db_config["pg_host"])