from django.urls import path

from small_web import views

urlpatterns = [
    path("", views.index)
]
