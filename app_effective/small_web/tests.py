from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from small_web.utils.utils_password import modify_password
from small_web.models import (
    CustomUsers,
    AccessTypes,
    UserAccess,
    CustomPermissions
)


class SignUpAPITestCase(APITestCase):
    """
    Тестирование API регистрации в системе
    """

    def setUp(self):
        self.url = reverse("signup_page")

    def test_get_signup_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, "signup.html")

    def test_post_signup_view(self):
        data = {
            "name": "test_user",
            "surname": "user_test",
            "email": "test_user@mail.ru",
            "password": modify_password("12345qwerty")
        }
        response = self.client.post(path=self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_signup_view_with_incorrect_data(self):
        """
        Ответ 200 так как выполняется валидация пустых полей и система
        возвращает прошлую страницу с пояснениями
        """
        data = {
            "name": "test_user",
            "surname": "",
            "email": "test_user@mail.ru",
            "password": modify_password("12345qwerty")
        }
        response = self.client.post(path=self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(
            response=response, text="Поле Фамилия не может быть пустым"
        )


class SignIpAPITestCase(APITestCase):
    """
    Тестирование API входа в систему
    """

    def setUp(self):
        self.user = CustomUsers.objects.create(
            name="test_user",
            surname="user_test",
            email="test_user@mail.ru",
            password=modify_password("12345qwerty")
        )
        self.url = reverse("signin_page")

    def test_get_signin_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, "signin.html")

    def test_post_signin_view(self):
        data = {
            "email": "test_user@mail.ru",
            "password": "12345qwerty"
        }
        response = self.client.post(path=self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_signin_view_with_incorrect_data(self):
        """
        Ответ 200 так как выполняется валидация пустых полей и система
        возвращает прошлую страницу с пояснениями
        """
        data = {
            "email": "test_user@mail.ru",
            "password": ""
        }
        response = self.client.post(path=self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(
            response=response, text="Поле пароль не может быть пустым"
        )


class AccountAPITestCase(APITestCase):
    """
    Тестирование API вход в личный кабинет
    """

    def setUp(self):
        self.user = CustomUsers.objects.create(
            name="test_user",
            surname="user_test",
            email="test_user@mail.ru",
            password=modify_password("12345qwerty")
        )
        self.access_type = AccessTypes.objects.create(name="base_user")
        UserAccess.objects.create(users=self.user, access=self.access_type)
        CustomPermissions.objects.create(
            get=True,
            post=True,
            table_name="custom_users",
            description="test_description",
            access_type=self.access_type,
            all_samples=False
        )
        self.url = reverse("account_page")
        self.client.post(
            data={"email": "test_user@mail.ru", "password": "12345qwerty"},
            path=reverse("signin_page")
        )

    def test_get_account_view(self):
        response = self.client.get(path=self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_account_view_without_logging(self):
        """
        Если пользователь не прошёл аутентификацию, система не пропустит его
        на страницы требующие определенных прав
        """
        self.client.get(reverse("logout_page"))
        response = self.client.get(path=self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ChangeUserInfoAPITestCase(APITestCase):
    """
    Тестирование API изменение данных в личном кабинете
    """

    def setUp(self):
        self.user = CustomUsers.objects.create(
            name="test_user",
            surname="user_test",
            email="test_user@mail.ru",
            password=modify_password("12345qwerty")
        )
        self.admin = CustomUsers.objects.create(
            name="test_user_admin",
            surname="user_test_admin",
            email="test_admin@mail.ru",
            password=modify_password("qwerty12345"),
            is_admin=True
        )
        self.access_type = AccessTypes.objects.create(name="base_user")
        self.access_type2 = AccessTypes.objects.create(name="admin")
        UserAccess.objects.create(users=self.user, access=self.access_type)
        UserAccess.objects.create(users=self.admin, access=self.access_type2)
        CustomPermissions.objects.create(
            get=True,
            post=True,
            table_name="custom_users",
            description="test_description",
            access_type=self.access_type,
            all_samples=False
        )
        CustomPermissions.objects.create(
            get=True,
            post=True,
            table_name="custom_users",
            description="test_description",
            access_type=self.access_type2,
            all_samples=True
        )
        self.url = reverse("change_user_page", kwargs={"user_id": self.user.id})
        self.url_admin = reverse(
            "change_user_page", kwargs={"user_id": self.admin.id}
        )
        self.client.post(
            data={"email": "test_user@mail.ru", "password": "12345qwerty"},
            path=reverse("signin_page")
        )

    def test_get_account_change_view(self):
        response = self.client.get(path=self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_account_change_view_without_logging(self):
        """
        Если пользователь не прошёл аутентификацию, система не пропустит его
        на страницы требующие определенных прав
        """
        self.client.get(reverse("logout_page"))
        response = self.client.get(path=self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_account_change_view(self):
        data = {
            "name": "new_test_user",
            "surname": "user_test",
            "email": "test_user@mail.ru",
        }
        response = self.client.post(path=self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotContains(
            response=response, text="Пользователь с такой почтой уже существует"
        )
        self.assertTrue(
            CustomUsers.objects.filter(name="new_test_user").exists()
        )

    def test_post_account_change_view_with_incorrect_data(self):
        """
        Попытка указать почту существующего пользователя приведёт к ответу 200
        с пояснением ошибки и без изменений в бд. Пользователь может ещё раз
        попробовать внести изменения
        """
        CustomUsers.objects.create(
            name="test_user2",
            surname="user_test2",
            email="test_user_admin@mail.ru",
            password=modify_password("12345qwerty")
        )
        data = {
            "name": "new_test_user",
            "surname": "user_test",
            "email": "test_user_admin@mail.ru",
        }
        response = self.client.post(path=self.url, data=data)
        self.assertContains(
            response=response, text="Пользователь с такой почтой уже существует"
        )

    def test_get_account_change_view_admin(self):
        self.client.post(
            data={"email": "test_admin@mail.ru", "password": "qwerty12345"},
            path=reverse("signin_page")
        )
        response = self.client.get(path=self.url_admin)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PermissionPageForAdminAPITestCase(APITestCase):
    """
    Тестирование API получения всех прав пользователем с правами admin
    """

    def setUp(self):
        self.user = CustomUsers.objects.create(
            name="test_user",
            surname="user_test",
            email="test_user@mail.ru",
            password=modify_password("12345qwerty")
        )
        self.admin = CustomUsers.objects.create(
            name="test_user_admin",
            surname="user_test_admin",
            email="test_admin@mail.ru",
            password=modify_password("qwerty12345"),
            is_admin=True
        )
        self.access_type = AccessTypes.objects.create(name="base_user")
        self.access_type2 = AccessTypes.objects.create(name="admin")
        UserAccess.objects.create(users=self.user, access=self.access_type)
        UserAccess.objects.create(users=self.admin, access=self.access_type2)
        permission1 = CustomPermissions.objects.create(
            get=True,
            post=True,
            table_name="custom_users",
            description="test_description",
            access_type=self.access_type,
            all_samples=False
        )
        CustomPermissions.objects.create(
            get=True,
            post=True,
            table_name="custom_users",
            description="test_description, check this phrase",
            access_type=self.access_type2,
            all_samples=True
        )
        CustomPermissions.objects.create(
            get=True,
            post=True,
            table_name="custom_permission",
            description="test_description",
            access_type=self.access_type2,
            all_samples=True
        )
        CustomPermissions.objects.create(
            get=False,
            post=False,
            table_name="custom_permission",
            description="test_description",
            access_type=self.access_type,
            all_samples=False
        )
        self.url_get = reverse("permissions_admin_page")
        self.url_get_admin = reverse("permissions_admin_page")
        self.url_post = reverse(
            "change_permission_page", kwargs={"access_id": permission1.id}
        )
        self.url_post_admin = reverse(
            "change_permission_page", kwargs={"access_id": permission1.id}
        )
        self.client.post(
            data={"email": "test_admin@mail.ru", "password": "qwerty12345"},
            path=reverse("signin_page")
        )

    def test_get_permission_view_admin(self):
        response = self.client.get(path=self.url_get_admin)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(
            response=response, text="test_description, check this phrase"
        )

    def test_post_permission_view_admin(self):
        data = {
            "get": False,
            "post": False,
            "table_name": "custom_permission",
            "description": "test_description NEW",
            "access_type": self.access_type,
            "all_samples": False,
        }
        response = self.client.post(path=self.url_post_admin, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            CustomPermissions.objects.filter(description="test_description NEW")
        )

    def test_post_permission_view_admin_with_incorrect_data(self):
        """
        При указании некорректных данных система вернёт страницу с ответом 200
        и сообщением об ошибке, после пользователь сможет скорректировать
        информацию
        """
        data = {
            "get": False,
            "post": False,
            "table_name": "custom_permission",
            "description": "test_description NEW",
            "access_type": "test_access_type",
            "all_samples": False,
        }
        response = self.client.post(path=self.url_post_admin, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(
            response=response, text="Несуществующий тип доступа"
        )

    def test_get_permission_view_user(self):
        """
        Пользователь с обычными правами не может зайти на эту страницу. В
        ответе получает страницу с кодом 403
        """
        self.client.post(
            data={"email": "test_user@mail.ru", "password": "12345qwerty"},
            path=reverse("signin_page")
        )
        response = self.client.get(path=self.url_get)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_permission_view_user(self):
        self.client.post(
            data={"email": "test_user@mail.ru", "password": "12345qwerty"},
            path=reverse("signin_page")
        )
        data = {
            "get": False,
            "post": False,
            "table_name": "custom_permission",
            "description": "test_description NEW",
            "access_type": self.access_type,
            "all_samples": False,
        }
        response = self.client.post(path=self.url_post_admin, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
