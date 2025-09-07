import jwt
from jwt.exceptions import InvalidTokenError

from rest_framework.response import Response

from datetime import datetime, timedelta
from typing import Union

from app_effective import settings


def create_jwt(user: dict, all_tokens: bool = True):
    payload = {
        "sub": user.get("email"),
        "email": user.get("email"),
        "name": user.get("name")
    }
    if all_tokens:
        access_token = create_access_token(payload=payload)
        refresh_token = create_refresh_token(payload=payload)
        return access_token, refresh_token
    access_token = create_access_token(payload=payload)
    return access_token


def create_access_token(payload: dict) -> str:
    payload.update({"type": "access"})
    return encode_jwt(
        payload=payload,
        expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    )


def create_refresh_token(payload: dict) -> str:
    payload.update({"type": "refresh"})
    return encode_jwt(
        payload=payload,
        expire_timedelta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )


def encode_jwt(
        payload: dict,
        private_key: str = settings.PRIVATE_KEY_PATH.read_text(),
        algorithm: str = settings.ALGORITHM,
        expire_minutes: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        expire_timedelta: Union[timedelta, None] = None
):
    current_time = datetime.utcnow()
    to_encode = payload.copy()
    if expire_timedelta:
        expire = current_time + expire_timedelta
    else:
        expire = current_time + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire,
        iat=current_time
    )
    access_token = jwt.encode(to_encode, private_key, algorithm)
    return access_token


def decode_jwt(
        token: str,
        public_key: str = settings.PUBLIC_KEY_PATH.read_text(),
        algorithm: str = settings.ALGORITHM
):
    try:
        decoded = jwt.decode(jwt=token, key=public_key, algorithms=algorithm)
    except InvalidTokenError:
        return None
    return decoded


def set_cookie(
        response: Response,
        access_token: str = None,
        refresh_token: str = None,
        all_tokens: bool = True
) -> Response:
    if all_tokens:
        response.set_cookie(key="Token-type", value="Bearer")
        response.set_cookie(
            key="Access-Token", value=access_token
        )
        response.set_cookie(
            key="Refresh-Token", value=refresh_token
        )
        return response
    response.set_cookie(key="Access-Token", value=access_token)
    return response
