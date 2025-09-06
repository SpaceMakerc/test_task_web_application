from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from small_web.serializers import (
    CustomUsersSignUpSerializer,
    CustomUsersSignInSerializer,
    CustomUserInfoSerializer,
    CustomSerializerUpdateInfoSerializer
)
from small_web.utils.utils_jwt import encode_jwt
from small_web.utils.utils_password import validate_registered_user
from small_web.utils.utils_user_auth import checker_auth

from small_web.dao.user_dao import CustomUserDAO

# Create your views here.


class IndexAPI(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "index.html"

    def get(self, request):
        return Response(template_name="index.html")


class SignUpAPI(APIView):
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
            user_dao = CustomUserDAO(instance=serializer.instance)
            user_dao.create_access()
        else:
            return Response({"serializer": serializer})
        return Response(template_name="index.html")


class SignInAPI(APIView):
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


class AccountAPI(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "account.html"

    @checker_auth
    def get(self, request):
        user_dao = CustomUserDAO(user_info=request.user_info["sub"])
        permission = user_dao.get_permissions()
        data = user_dao.get_sample(permission=permission)
        serializer = CustomUserInfoSerializer(data, many=True)
        return Response({"serializer": serializer})


class ChangeUserInfoAPI(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "change_user.html"

    @checker_auth
    def get(self, request, user_id):
        user_dao = CustomUserDAO(user_info=request.user_info["sub"])
        permission = user_dao.get_permissions()
        data = user_dao.get_sample(permission=permission, mark=user_id)
        serializer = CustomSerializerUpdateInfoSerializer(data[0])
        return Response({"serializer": serializer})

    @checker_auth
    def post(self, request, user_id):
        user_dao = CustomUserDAO(user_info=request.user_info["sub"])
        permission = user_dao.get_permissions()
        data = user_dao.get_sample(permission=permission, mark=user_id)
        if user_dao.post_sample(permission=permission):
            serializer = CustomSerializerUpdateInfoSerializer(
                data=request.POST, instance=data[0]
            )
            if serializer.is_valid():
                serializer.save()
                return Response(template_name="index.html")
            return Response({"serializer": serializer})
