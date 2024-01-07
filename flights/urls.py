from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("airports", views.airports, name="airports"),
    path("passengers", views.passengers, name="passengers"),
    path("<int:flight_id>", views.flight, name="flight"),
    path("<int:flight_id>/book", views.book, name="book"),
    path("<int:flight_id>/unbook", views.unbook, name="unbook"),
]