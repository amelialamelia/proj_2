from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("data_vis/<str:date>/", views.data_vis, name = "data_vis")
]