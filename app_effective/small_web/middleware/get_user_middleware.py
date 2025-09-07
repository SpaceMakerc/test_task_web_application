class GetUserMiddleware:
    def __init__(self, next):
        self.next = next

    def __call__(self, request, *args, **kwargs):
        response = self.next(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        cookie = request.COOKIES
        access_token = cookie.get("Access-Token", None)
        refresh_token = cookie.get("Refresh-Token", None)
        request.access_token = access_token
        request.refresh_token = refresh_token
        return None
