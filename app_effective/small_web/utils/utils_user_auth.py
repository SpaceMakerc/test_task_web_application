from django.http import HttpResponseForbidden
from django.template.loader import render_to_string

from small_web.utils.utils_jwt import decode_jwt

from functools import wraps


def get_forbidden_answer():
    answer = render_to_string(
        template_name="exceptions/forbidden_page.html"
    )
    return HttpResponseForbidden(answer)


def checker_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        request = args[1]
        answer = decode_jwt(request.custom_user)
        if not answer:
            return get_forbidden_answer()
        args[1].user_info = answer
        return func(*args, **kwargs)
    return wrapper
