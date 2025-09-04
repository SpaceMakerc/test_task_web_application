from django.urls import path

from small_web import views

urlpatterns = [
    path("", views.IndexAPI().as_view(), name="index_page"),
    path("signup/", views.SignUp().as_view(), name="signup_page"),
    path("signin/", views.SignIn().as_view(), name="signin_page"),
]
