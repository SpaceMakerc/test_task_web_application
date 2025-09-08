from django.urls import path

from small_web import views

urlpatterns = [
    path(
        "",
        views.IndexAPI().as_view(),
        name="index_page"
    ),
    path(
        "signup/",
        views.SignUpAPI().as_view(),
        name="signup_page"
    ),
    path(
        "signin/",
        views.SignInAPI().as_view(),
        name="signin_page"
    ),
    path(
        "account/",
        views.AccountAPI.as_view(),
        name="account_page"
    ),
    path(
        "change_user/<int:user_id>/",
        views.ChangeUserInfoAPI.as_view(),
        name="change_user"
    ),
    path(
        "admin_permissions/",
        views.PermissionPageForAdminAPI.as_view(),
        name="permissions_admin"
    ),
    path(
        "change_permission/<int:access_id>",
        views.ChangePermissionForAdminAPI.as_view(),
        name="change_permission"
    ),
    path(
        "account/logout/",
        views.LogoutUserAPI.as_view(),
        name="logout_page"
    ),
]
