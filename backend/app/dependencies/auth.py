import binascii
from base64 import b64decode
from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, HTTPException, status, Query, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.security.utils import get_authorization_scheme_param

from app.utils.auth import verify_password, get_user

security = HTTPBasic()


def get_current_user(credentials: HTTPBasicCredentials = Depends(security)) -> str:
    user = get_user(credentials.username)
    if not user or not verify_password(credentials.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user["username"]


def get_current_user_ws(authorization: str = Query(...)) -> str:
    # This is a WebSocket connection, so the Authorization header is not available
    scheme, param = get_authorization_scheme_param(authorization)
    if not authorization or scheme.lower() != "basic":
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Not authenticated",
        )

    invalid_user_credentials_exc = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail="Invalid authentication credentials",
    )
    try:
        data = b64decode(param).decode("ascii")
    except (ValueError, UnicodeDecodeError, binascii.Error):
        raise invalid_user_credentials_exc  # noqa: B904
    username, separator, password = data.partition(":")
    if not separator:
        raise invalid_user_credentials_exc

    user = get_user(username)
    if not user or not verify_password(password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )

    return user["username"]


UserDep = Annotated[str, Depends(get_current_user)]
