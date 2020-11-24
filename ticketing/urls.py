from django.urls import path

from . import views

app_name = 'ticketing_app'
urlpatterns = [
    path('movie/list', views.movie_list, name='movie_list'),
    path('movie/details/<int:movie_id>/', views.movie_details, name='movie_datails'),
    path('cinema/details/<int:cinema_id>', views.cinema_details, name='cinema_details'),
    path('cinema/list', views.cinema_list, name='cinema_list'),
    path('showtime/list', views.showtime_list, name='showtime_list'),
    path('showtime/details/<int:showtime_id>', views.showtime_details, name="showtime_details"),
    path('ticket/list', views.ticket_list, name='ticket_list'),
    path('ticket/details/<int:ticket_id>/', views.ticket_details, name='ticket_details')
]