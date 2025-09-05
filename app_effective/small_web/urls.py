from django.urls import path

from small_web import views

urlpatterns = [
    path("", views.IndexAPI().as_view(), name="index_page"),
    path("signup/", views.SignUpAPI().as_view(), name="signup_page"),
    path("signin/", views.SignInAPI().as_view(), name="signin_page"),
    path("account/", views.AccountAPI.as_view(), name="account_page"),
    path("change_user/", views.ChangeUserInfoAPI.as_view(), name="change_user"),
]
