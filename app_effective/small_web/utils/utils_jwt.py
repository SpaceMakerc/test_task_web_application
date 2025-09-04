import jwt

from app_effective import settings


def encode_jwt(
        payload: dict,
        private_key: str = settings.PRIVATE_KEY_PATH.read_text(),
        algorithm: str = settings.ALGORITHM
):
    encoded = jwt.encode(payload, private_key, algorithm)
    return encoded


def decode_jwt(
        token: str,
        public_key: str = settings.PUBLIC_KEY_PATH.read_text(),
        algorithm: str = settings.ALGORITHM
):
    decoded = jwt.decode(jwt=token, key=public_key, algorithm=algorithm)
    return decoded
