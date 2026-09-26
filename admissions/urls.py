from django.urls import path

from . import views

app_name = "admissions"

urlpatterns = [
    path("", views.index, name="index"),
    path("apply/", views.apply, name="apply"),
    path("apply/thank-you/<str:reference>/", views.thanks, name="thanks"),
]
