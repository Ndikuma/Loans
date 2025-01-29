# search/urls.py

from django.urls import path

from . import views

urlpatterns = [
    path("create-index/", views.create_index, name="create_index"),
]
