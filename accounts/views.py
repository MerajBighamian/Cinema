from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth import authenticate, login, logout
# Create your views here.
from django.urls import reverse
# from django.contrib.auth.models import User


# define login_view
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username') # get user name
        password = request.POST.get('password') # get password
        user = authenticate(request, username=username, password=password) # authentication user
        if user is not None:
            # Succesful login
            login(request, user) # login user 
            return HttpResponseRedirect(reverse('ticketing_app:cinema_list'))
        else:
            # undefined user or wrong password

            context = {
                'username': username,
                'error': 'کاربری با این مشخصات یافت نشد'
            }

    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('ticketing_app:showtime_list'))
        context = {}
    return render(request, 'accounts/login.html', context)

# define logout view
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('accounts:login'))


@login_required
def profile_details(request): # view for show profile details
    profile = request.user.profile
    context = {
        'profile': profile,
    }
    return render(request, 'accounts/profile_details.html', context)
