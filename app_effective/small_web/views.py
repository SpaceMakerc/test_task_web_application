from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from small_web.serializers import (
    CustomUsersSignUpSerializer,
    CustomUsersSignInSerializer,
)
from small_web.utils.utils_jwt import encode_jwt
from small_web.utils.utils_password import validate_registered_user

# Create your views here.


class IndexAPI(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "index.html"

    def get(self, request):
        return Response(template_name="index.html")


class SignUp(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "signup.html"

    def get(self, request):
        serializer = CustomUsersSignUpSerializer()
        return Response({"serializer": serializer})

    def post(self, request):
        user_data = request.POST
        serializer = CustomUsersSignUpSerializer(data=user_data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response({"serializer": serializer})
        return Response(template_name="index.html")


class SignIn(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "signin.html"

    def get(self, request):
        serializer = CustomUsersSignInSerializer()
        return Response({"serializer": serializer})

    def post(self, request):
        user_data = request.POST
        serializer = CustomUsersSignInSerializer(data=user_data)
        if serializer.is_valid():
            user_check = validate_registered_user(
                email=serializer.validated_data["email"],
                password=serializer.validated_data["password"]
            )
            if not user_check:
                return Response({
                    "serializer": serializer,
                    "answer": "Пользователь с такими данными не найден"
                })

            payload = {
                "sub": user_check.email,
                "username": user_check.name,
            }
            token = encode_jwt(payload)

            response = Response(template_name="index.html")
            response.set_cookie(key="Access-Token", value=f"Bearer {token}")
            return response
        else:
            return Response({"serializer": serializer})
