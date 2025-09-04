import jwt

from datetime import datetime, timedelta

from app_effective import settings


def encode_jwt(
        payload: dict,
        private_key: str = settings.PRIVATE_KEY_PATH.read_text(),
        algorithm: str = settings.ALGORITHM,
        expire_minutes: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES
):
    current_time = datetime.utcnow()
    to_encode = payload.copy()
    expire = current_time + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire,
        iat=current_time
    )
    encoded = jwt.encode(to_encode, private_key, algorithm)
    return encoded


def decode_jwt(
        token: str,
        public_key: str = settings.PUBLIC_KEY_PATH.read_text(),
        algorithm: str = settings.ALGORITHM
):
    decoded = jwt.decode(jwt=token, key=public_key, algorithm=algorithm)
    return decoded
