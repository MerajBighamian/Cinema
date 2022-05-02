from django.urls import path

from . import views

app_name = 'ticketing_app' # app_name for clean url routing
urlpatterns = [
    path('movie/list', views.movie_list, name='movie_list'), # view for show movie list
    path('movie/details/<int:movie_id>/', views.movie_details, name='movie_datails'), # view for show movie detail with specify movie_id
    path('cinema/details/<int:cinema_id>', views.cinema_details, name='cinema_details'), # view for show cinema detail with specify cinema_id
    path('cinema/list', views.cinema_list, name='cinema_list'), # view for show cinema list
    path('showtime/list', views.showtime_list, name='showtime_list'), # view for show showtimes list
    path('showtime/details/<int:showtime_id>', views.showtime_details, name="showtime_details"), # view for show showtime detail with specify showtime_id
    path('ticket/list', views.ticket_list, name='ticket_list'), # view for show ticket list
    path('ticket/details/<int:ticket_id>/', views.ticket_details, name='ticket_details') # view for show ticket detail with specify ticket_id
]
