from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_STR}/tokens/")

token_dep = Annotated[str, Depends(oauth2_scheme)]
