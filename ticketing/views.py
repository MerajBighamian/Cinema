
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from ticketing.models import Movie, Cinema, ShowTime, Ticket
from django.urls import reverse
from ticketing.forms import ShowTimeSearchForm


# view of url movie/list with name movie_list
def movie_list(request):
    # query for return all objects in Movie model
    movies = Movie.objects.all()
    # count all objects in Movie model
    count = len(movies)
    # context of render function for show data in template of view (for path movie/list)
    context = {
        'movie_list': movies,
        'movie_count': count
    }
    return render(request, 'ticketing/movielsit.html', context)
    # return response for request with template file and data(with template : movielist.html)

    # response_text = '\n'.join('{} : {}'.format(i, movie) for i, movie in enumerate(movies, start=1))
    # return HttpResponse(str(response_text))


# view of url cinema/list with name cinema_list
def cinema_list(request):
    # query for return all objects in Cinema model
    cinemas = Cinema.objects.all()
    # count all objects in Movie model
    count = len(cinemas)
    # context of render function for show data in template of view (for path cinema/list)
    context = dict(cinema_list=cinemas, cinema_count=count)
    # return response for request with template file and data(with template : cinemalist.html)
    return render(request, "ticketing/cinemalist.html", context)

# view of show details of movies
def movie_details(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id) # get movie object from model or return 404 error
    context = {
        'movie': movie
    }
    return render(request, 'ticketing/movie_details.html', context)

# view of show details of cinema by cinema_id url variable
def cinema_details(request, cinema_id):
    cinemas = get_object_or_404(Cinema, pk=cinema_id) # get movie object from model or return 404 error
    context = {
        'cinema': cinemas
    }
    return render(request, 'ticketing/cinema_details.html', context) 

# return show time list
def showtime_list(request):
    # -----------------------------------------------------------------------
    # if request.user.is_authenticated and request.user.is_active:
    # -----------------------------------------------------------------------
    search_form = ShowTimeSearchForm(request.GET) # define and bind showtime search from 
    showtime = ShowTime.objects.all() # get all object in showtime model
    if search_form.is_valid(): # validate search form fields
        showtime = showtime.filter(movie__name__contains=search_form.cleaned_data['movie_name']) # filter show times by that movie
        if search_form.cleaned_data['sale_is_open']: # filter show time by sale open status
            showtime = showtime.filter(status=ShowTime.SALE_OPEN)
        if search_form.cleaned_data['movie_length_min'] is not None: # filter show time by movie length min
            showtime = showtime.filter(movie__length__gte=search_form.cleaned_data['movie_length_min'])
        if search_form.cleaned_data['movie_length_max'] is not None: # filter show time by movie length max
            showtime = showtime.filter(movie__length__lte=search_form.cleaned_data['movie_length_max'])
        if search_form.cleaned_data['cinema'] is not None: # filter show time by cinema 
            showtime = showtime.filter(cinema=search_form.cleaned_data['cinema'])
        """
        define filter for max and min price of show time
        """
        min_price, max_price = search_form.get_price_boundries()
        if min_price is not None:
            showtime = showtime.filter(price__gte=min_price)
        if max_price is not None:
            showtime=showtime.filter(price__lt=max_price)
    showtime = showtime.order_by('start_time') # ordered showtime by start time of showtime
    context = {
        "showtimes": showtime,
        'search_form': search_form,
    }
    return render(request, "ticketing/showtime_list.html", context)


# ----------------------------------
# else:
#     return HttpResponseRedirect(reverse('accounts:login'))
# ----------------------------------

@login_required # login required decorator
"""
show time details view
"""
def showtime_details(request, showtime_id):
    showtime = ShowTime.objects.get(pk=showtime_id)
    context = {
        'showtime': showtime
    }

    if request.method == 'POST': 
        try:
            seat_count = int(request.POST['seat_count']) # seat_count
            assert showtime.status == showtime.SALE_OPEN, 'فروش بلیط برای این سانس ممکن نیست' # check showtime is sales open
            assert showtime.free_seats >= seat_count, 'این سانس به اندازه کافی صندلی خالی ندارد' # check showtime have requirments seat
            totalPrice = showtime.price * seat_count # calculate money of reserve seat of showtime
            # assert request.user.profile.balance >= totalPrice, 'موجودی کافی نیست'
            assert request.user.profile.spend(totalPrice), 'موجودی کافی نیست' # spend money of wallet in user profile
            ticket = Ticket.objects.create(showtime=showtime, customer=request.user.profile, seat_count=seat_count) # make ticket
            showtime.reserve_seat(seat_count) # apply seat count reserved
        # handle exception of try
        except Exception as e:
            context['error'] = str(e) # show error that raised
        else:
            return HttpResponseRedirect(reverse('ticketing_app:ticket_details', kwargs={'ticket_id': ticket.id})) # redirect to ticket details view
    else:
        pass
        # return HttpResponseRedirect(reverse('ticketing_app:showtime_details showtime_id=showtime_id'))
    return render(request, 'ticketing/showtime_details.html', context)


@login_required
"""
ticket list view
"""
def ticket_list(request):
    tickets = Ticket.objects.filter(customer=request.user.profile).order_by('-order_time')
    context = {
        'tickets': tickets
    }
    return render(request, 'ticketing/ticket_list.html', context)


@login_required
"""
ticket details view
"""
def ticket_details(request, ticket_id):
    ticket = Ticket.objects.get(pk=ticket_id)
    context = {
        'ticket': ticket
    }
    return render(request, 'ticketing/ticket_details.html', context)
