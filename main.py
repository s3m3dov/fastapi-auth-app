import uvicorn
from fastapi import FastAPI

from core import settings

from db import models
from db.init_db import mysql_db
from api import api_router


mysql_db.connect()
mysql_db.create_tables([models.User, models.Item])
mysql_db.close()


app = FastAPI(
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
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
