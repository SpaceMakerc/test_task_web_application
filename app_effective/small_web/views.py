from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework import status
from django.forms.models import model_to_dict

from small_web.serializers import (
    CustomUsersSignUpSerializer,
    CustomUsersSignInSerializer,
    CustomUserInfoSerializer,
    CustomSerializerUpdateInfoSerializer,
    CustomPermissionSerializer,
)
from small_web.utils.utils_jwt import create_jwt, set_cookie, delete_cookie
from small_web.utils.utils_password import validate_registered_user
from small_web.utils.utils_user_auth import checker_auth

from small_web.dao.user_dao import CustomUserDAO
from small_web.dao.permission_dao import CustomPermissionDAO

# Create your views here.


class IndexAPI(APIView):
    renderer_classes = [TemplateHTMLRenderer]

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
                    "answer": "Пользователь с такими данными не найден",
                }, status=status.HTTP_401_UNAUTHORIZED
                )

            access_token, refresh_token = create_jwt(
                user=model_to_dict(user_check)
            )

            response = Response(template_name="index.html")
            set_cookie(
                response=response,
                access_token=access_token,
                refresh_token=refresh_token
            )
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
        is_admin = permission.all_samples
        return Response({"serializer": serializer, "is_admin": is_admin})


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


class PermissionPageForAdminAPI(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "permissions_for_admin.html"

    @checker_auth
    def get(self, request):
        user_dao = CustomPermissionDAO(user_info=request.user_info["sub"])
        permission = user_dao.get_permissions()
        data = user_dao.get_sample(permission=permission)
        serializer = CustomPermissionSerializer(data, many=True)
        return Response({"serializer": serializer})


class ChangePermissionForAdminAPI(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "change_permission.html"

    @checker_auth
    def get(self, request, access_id):
        user_dao = CustomPermissionDAO(user_info=request.user_info["sub"])
        permission = user_dao.get_permissions()
        data = user_dao.get_sample(permission=permission, mark=access_id)
        serializer = CustomPermissionSerializer(data[0])
        return Response({"serializer": serializer})

    @checker_auth
    def post(self, request, access_id):
        user_dao = CustomPermissionDAO(user_info=request.user_info["sub"])
        permission = user_dao.get_permissions()
        data = user_dao.get_sample(permission=permission, mark=access_id)
        if user_dao.post_sample(permission=permission):
            serializer = CustomPermissionSerializer(
                data=request.POST, instance=data[0]
            )
            if serializer.is_valid():
                serializer.save()
                return Response(template_name="index.html")
            return Response({"serializer": serializer})


class LogoutUserAPI(APIView):
    renderer_classes = [TemplateHTMLRenderer]

    @checker_auth
    def get(self, request):
        response = Response(template_name="index.html")
        delete_cookie(response=response)
        return response


class DeleteUserAPI(APIView):
    renderer_classes = [TemplateHTMLRenderer]

    @checker_auth
    def get(self, request):
        user_dao = CustomUserDAO(user_info=request.user_info["sub"])
        permission = user_dao.get_permissions()
        user_dao.delete_user(
            permission=permission, mark=request.user_info["sub"]
        )
        response = Response(template_name="index.html")
        delete_cookie(response=response)
        return response
