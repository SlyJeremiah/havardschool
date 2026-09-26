from django.urls import path

from . import views

app_name = "news"

urlpatterns = [
    path("", views.post_list, name="list"),
    path("events/", views.event_list, name="events"),
    path("events/<slug:slug>/", views.event_detail, name="event_detail"),
    path("<slug:slug>/", views.post_detail, name="detail"),
]
