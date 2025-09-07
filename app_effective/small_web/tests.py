from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse


class SignUpAPITestCase(APITestCase):
    """
    Тестирование API входа в систему
    """

    def setUp(self):
        self.url = reverse("signup_page")

    def test_get_signup_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, "signup.html")
