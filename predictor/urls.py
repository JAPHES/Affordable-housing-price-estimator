from django.urls import path

from . import views


app_name = "predictor"

urlpatterns = [
    path("", views.landing, name="landing"),
    path("predict/", views.predict, name="predict"),
]
