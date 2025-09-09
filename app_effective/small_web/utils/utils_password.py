import bcrypt

from small_web.models import CustomUsers


def modify_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    modified_password = password.encode()
    return bcrypt.hashpw(password=modified_password, salt=salt)


def check_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(
        password=password.encode(), hashed_password=hashed_password
    )


def validate_registered_user(email: str, password: str):
    result = None
    user = CustomUsers.objects.filter(email=email).first()
    if user:
        if not user.is_active:
            return result
        db_password = user.password.tobytes()
        auth = check_password(password=password, hashed_password=db_password)
        if auth:
            result = user
    return result
