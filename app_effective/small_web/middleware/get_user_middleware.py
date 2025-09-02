class GetUserMiddleware:
    def __init__(self, next):
        self.next = next

    def __call__(self, request, *args, **kwargs):
        response = self.next(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        cookie = request.COOKIES
        print(cookie)
        token = cookie.get("Authorization", None)
        print(f"{token} - token")
        return None
