from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response
from fastapi.security import OAuth2PasswordRequestForm

from app import crud, settings
from app.core import exceptions
from app.core.security import create_access_token, create_refresh_token, verify_token
from app.deps import session_dep
from app.schemas import AccessToken, TokenData

router = APIRouter()


@router.post("")
async def login_for_access_token(
    session: session_dep,
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> AccessToken:
    user = await crud.authenticate_user(
        session=session, username_or_email=form_data.username, password=form_data.password
    )
    if user is None:
        raise exceptions.INVALID_CREDENTIALS
    access_token = create_access_token(data={"sub": str(user.id), "power": user.power})
    refresh_token = create_refresh_token(data={"sub": str(user.id), "power": user.power})
    max_age = settings.REFRESH_TOKEN_EXPIRE_SECONDS
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="Lax",
        max_age=max_age,
    )
    return AccessToken(access_token=access_token, token_type="bearer")


@router.put("")
async def refresh_access_token(request: Request) -> AccessToken:
    """刷新访问令牌"""
    refresh_token = request.cookies.get("refresh_token")
    if refresh_token is None:
        raise exceptions.INVALID_CREDENTIALS
    token_data: TokenData | None = verify_token(refresh_token)
    if token_data is None:
        raise exceptions.INVALID_CREDENTIALS
    new_access_token = create_access_token(data={"sub": str(token_data.id), "power": token_data.power})
    return AccessToken(access_token=new_access_token, token_type="bearer")
