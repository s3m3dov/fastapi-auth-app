from pydantic import BaseModel
from core import settings


class Settings(BaseModel):
    authjwt_secret_key: str = settings.AUTH_JWT_SECRET_KEY
    authjwt_token_location: set = {"cookies"}
    authjwt_cookie_secure: bool = False  # Only allow JWT cookies to be sent over https
    authjwt_cookie_csrf_protect: bool = False  # Change it on production
