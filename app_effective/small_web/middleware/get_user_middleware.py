from django.http import HttpResponseForbidden
from django.template.loader import render_to_string


class GetUserMiddleware:
    def __init__(self, next):
        self.next = next

    def __call__(self, request, *args, **kwargs):
        response = self.next(request)
        return response

    # TODO доработай логику чтобы вытаскивать пользователя
    def process_view(self, request, view_func, view_args, view_kwargs):
        cookie = request.COOKIES
        token = cookie.get("Authorization", None)
        print(f"{token} - token")
        return None
        # if not token:
        #     answer = render_to_string(
        #         template_name="exceptions/forbidden_page.html"
        #     )
        #     return HttpResponseForbidden(answer)
