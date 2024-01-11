from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("registration", views.registration, name="registration"),
    path("airports", views.airports, name="airports"),
    path("passengers", views.passengers, name="passengers"),
    path("<int:flight_id>", views.flight, name="flight"),
    path("<int:flight_id>/book", views.book, name="book"),
    path("<int:flight_id>/unbook", views.unbook, name="unbook"),
    path('airports/create/', views.create_airport, name='create_airport'),
    path('airports/<int:airport_id>/update/', views.update_airport, name='update_airport'),
    path('airports/<int:airport_id>/delete/', views.delete_airport, name='delete_airport'),
    path('passengers/create/', views.create_passenger, name='create_passenger'),
    path('passengers/<int:passenger_id>/update/', views.update_passenger, name='update_passenger'),
    path('passengers/<int:passenger_id>/delete/', views.delete_passenger, name='delete_passenger'),
    path('create/', views.create_flight, name='create_flight'),
    path('<int:flight_id>/update/', views.update_flight, name='update_flight'),
    path('<int:flight_id>/delete/', views.delete_flight, name='delete_flight'),
    
]