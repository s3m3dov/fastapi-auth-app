import uvicorn

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException

from core import settings
from db import models
from db.init_db import mysql_db

from api import api_router
from schemas.auth_jwt_config import Settings

mysql_db.connect()
mysql_db.create_tables([models.User, models.Item])
mysql_db.close()

app = FastAPI(
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)


@AuthJWT.load_config
def get_config():
    return Settings()


@app.exception_handler(AuthJWTException)
def auth_jwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


app.include_router(api_router, prefix=settings.API_V1_STR)


# Run Fast API app
if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        proxy_headers=True,
        forwarded_allow_ips='*',
    )
