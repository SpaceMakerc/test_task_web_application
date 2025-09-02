from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

# Create your views here.


class IndexAPI(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "index.html"

    def get(self, request):
        return Response(template_name="index.html")
