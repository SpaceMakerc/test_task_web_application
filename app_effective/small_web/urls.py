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
        name="change_user_page"
    ),
    path(
        "admin_permissions/",
        views.PermissionPageForAdminAPI.as_view(),
        name="permissions_admin_page"
    ),
    path(
        "change_permission/<int:access_id>",
        views.ChangePermissionForAdminAPI.as_view(),
        name="change_permission_page"
    ),
    path(
        "account/logout/",
        views.LogoutUserAPI.as_view(),
        name="logout_page"
    ),
    path(
        "account/delete_account/",
        views.DeleteUserAPI.as_view(),
        name="delete_user_page",
    )
]
