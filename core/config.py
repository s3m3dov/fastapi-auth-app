from environs import Env

# Environment
env = Env()
env.read_env()


class Settings:
    API_V1_STR: str = "/api/v1"
    IPDATA_API_KEY: str = env("IPDATA_API_KEY", default="test")  # Your Key Here

    # Database Settings
    DATABASE_NAME: str = env("MYSQL_DATABASE", default="mysql_db")
    DATABASE_USER: str = env("MYSQL_USER", default="mysql")
    DATABASE_PASSWORD: str = env("MYSQL_PASSWORD", default="mysql")
    DATABASE_HOST: str = "db"
    DATABASE_PORT: int = env.int("MYSQL_PORT", default=3306)


settings = Settings()
