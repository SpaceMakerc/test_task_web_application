from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from small_web.serializers import CustomUsersSignUpSerializer
from small_web.utils.utils_jwt import encode_jwt

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
            payload = {
                "sub": serializer.validated_data["email"],
                "username": serializer.validated_data["name"],
            }
            token = encode_jwt(payload)
            print(token)
            serializer.save()
        else:
            return Response({"serializer": serializer})
        return Response(template_name="index.html")
