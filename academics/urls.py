from django.urls import path

from . import views

app_name = "academics"

urlpatterns = [
    path("", views.programme_list, name="list"),
    path("<slug:slug>/", views.programme_detail, name="detail"),
]
