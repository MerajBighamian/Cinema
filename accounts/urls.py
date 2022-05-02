from django.urls import path
from . import views

app_name = 'accounts' # app_name for clean url routing
urlpatterns = [
    path('login/', views.login_view, name='login'), # define url for login view
    path('logout/', views.logout_view, name='logout'), # define url for logout view
    path('profile/details', views.profile_details, name='profile_details') # define url for profile_details view
]
