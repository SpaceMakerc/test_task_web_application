class GetUserMiddleware:
    def __init__(self, next):
        self.next = next

    def __call__(self, request, *args, **kwargs):
        response = self.next(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        cookie = request.COOKIES
        token = cookie.get("Access-Token", None)
        if token:
            token = token.split(" ")[1]
        request.custom_user = token
        return None
