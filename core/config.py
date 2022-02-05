from pydantic import BaseModel
from environs import Env

# Environment
env = Env()
env.read_env()


class FastAPISettings:
    API_V1_STR: str = "/api/v1"
    IPDATA_API_KEY: str = env("IPDATA_API_KEY", default="test")

    AUTH_JWT_SECRET_KEY: str = env("AUTH_JWT_SECRET_KEY", default="secret")
    AUTH_JWT_TOKEN_ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 1
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    # 60 minutes * 24 hours * x days = x days

    # MySQL Settings
    MYSQL_DATABASE: str = env("MYSQL_DATABASE", default="mysql_db")
    MYSQL_USER: str = env("MYSQL_USER", default="mysql")
    MYSQL_PASSWORD: str = env("MYSQL_PASSWORD", default="mysql")
    MYSQL_ROOT_PASSWORD: str = env("MYSQL_ROOT_PASSWORD", default="mysql")
    MYSQL_HOST: str = env("MYSQL_HOST", default="db")
    MYSQL_PORT: int = env.int("MYSQL_PORT", default=3306)

    # RabbitMQ Settings
    RABBITMQ_USER: str = env("RABBITMQ_DEFAULT_USER", default="rabbit")
    RABBITMQ_PASSWORD: str = env("RABBITMQ_DEFAULT_PASS ", default="rabbit")
    RABBITMQ_PORT: str = env.int("RABBITMQ_PORT", default=5672)

    # Celery Settings
    CELERY_BROKER_URL = f"pyamqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@rabbitmq:{RABBITMQ_PORT}//"
    CELERY_RESULT_BACKEND = f"db+mysql://root:{MYSQL_ROOT_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"


settings = FastAPISettings()


class AuthJWTSettings(BaseModel):
    authjwt_secret_key: str = settings.AUTH_JWT_SECRET_KEY
    authjwt_token_location: set = {"cookies"}
    authjwt_cookie_secure: bool = False  # Only allow JWT cookies to be sent over https
    authjwt_cookie_csrf_protect: bool = False  # Change it on production
