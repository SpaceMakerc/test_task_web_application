from small_web.utils.utils_handle_errors import get_forbidden_answer
from small_web.utils.utils_jwt import decode_jwt, create_jwt, set_cookie

from functools import wraps


def checker_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        request = args[1]
        user_by_access_token = decode_jwt(request.access_token)
        if not user_by_access_token:
            user_by_refresh_token = decode_jwt(request.refresh_token)
            if user_by_refresh_token:
                payload = {
                    "sub": user_by_refresh_token.get("sub"),
                    "email": user_by_refresh_token.get("sub"),
                    "name": user_by_refresh_token.get("name"),
                }
                access_token = create_jwt(
                    user=payload, all_tokens=False
                )
                args[1].user_info = user_by_refresh_token
                response = func(*args, **kwargs)
                set_cookie(
                    response=response,
                    access_token=access_token,
                    refresh=True
                )
                return response
            return get_forbidden_answer()
        args[1].user_info = user_by_access_token
        return func(*args, **kwargs)
    return wrapper
