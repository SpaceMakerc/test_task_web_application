import bcrypt


def modify_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    modified_password = password.encode()
    return bcrypt.hashpw(password=modified_password, salt=salt)


def check_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(
        password=password.encode(), hashed_password=hashed_password
    )
