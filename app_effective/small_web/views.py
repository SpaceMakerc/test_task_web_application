from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from small_web.serializers import CustomUsersSignUpSerializer

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
        result = request.POST
        return Response(template_name="index.html")
