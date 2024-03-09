from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="book"),
    path("<int:book_id>/", views.detail, name="detail"),
]