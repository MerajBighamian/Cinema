from django.db import models


class Movie(models.Model):
    """
    define Movie Model
    """

    class Meta:
        verbose_name = "فیلم"
        verbose_name_plural = "فیلم ها"

    name = models.CharField(max_length=100, verbose_name="نام فیلم")
    director = models.CharField(max_length=50, verbose_name="کارگردان فیلم")
    year = models.IntegerField(default=1380, verbose_name="سال ساخت فیلم")
    length = models.IntegerField(default=120, verbose_name="زمان فیلم")
    description = models.TextField("توضیحات", null=True)
    poster = models.ImageField("پوستر", upload_to='imageposter/')

    def __str__(self):
        return self.name


class Cinema(models.Model):
    """
    define Cinema Model
    """

    class Meta:
        verbose_name = "سینما"
        verbose_name_plural = "سینماها"

    cinema_code = models.IntegerField("کد سینما", primary_key=True)
    name = models.CharField("نام سینما", max_length=50)
    city = models.CharField("شهر سینما", max_length=40, default='اصفهان')
    phone = models.IntegerField("شماره تلفن سینما", null=True)
    capacity = models.IntegerField("ظرفیت سینما", default=100)
    address = models.TextField("آدرس سینما", null=True)
    poster = models.ImageField('پوستر', upload_to='imageposter/', null=True, blank=True)

    def __str__(self):
        return self.name


class ShowTime(models.Model):
    """
    define ShowTime Model
    """

    class Meta:
        verbose_name = "سانس"
        verbose_name_plural = "سانس ها"

    movie = models.ForeignKey('Movie', on_delete=models.PROTECT, verbose_name="نام فیلم")
    cinema = models.ForeignKey('Cinema', on_delete=models.PROTECT, verbose_name="نام سینما")
    start_time = models.DateTimeField("زمان سانس")
    price = models.IntegerField("قیمت")
    sabale_seats = models.IntegerField('تعداد صندلی ها')
    free_seats = models.IntegerField("تعداد صندلی خالی")
    SALE_NOT_STARTED = 1
    SALE_OPEN = 2
    TICKETS_SALE = 3
    SALE_CLOSED = 4
    MOVIE_PLAYED = 5
    SHOW_CANSELED = 6
    status_choice = (
        (SALE_NOT_STARTED, "فروش آغاز نشده"),
        (SALE_OPEN, "در حال فروش بلیط"),
        (TICKETS_SALE, "بلیط ها تمام شد"),
        (SALE_CLOSED, "فروش بلیط بسته شد"),
        (MOVIE_PLAYED, "فیلم پخش شد"),
        (SHOW_CANSELED, "سانس لغو شد"),
    )
    # status for showtime of film
    status = models.IntegerField("وضعیت", choices=status_choice)

    def __str__(self):
        return '{} - {} - {}'.format(self.movie, self.cinema, self.start_time)

    def get_price_display(self):
        return "{} تومان".format(self.price)

    def get_status_display(self):
        return self.status_choice[self.status - 1][1]

    def reserve_seat(self, seat_count):
        assert isinstance(seat_count, int) and seat_count > 0, 'Number of seats is no valid'
        assert self.status == ShowTime.SALE_OPEN, 'sale is not open'
        assert self.free_seats >= seat_count, 'not enough free seats'
        self.free_seats -= seat_count
        if self.free_seats == 0:
            self.status = ShowTime.TICKETS_SALE
        self.save()

        # this is a query of show time model -------->      ShowTimw.objects.filter(movie__year__gt=1380,
    # cinema__city="Tehran").exclude(price__lt=1000)


class Ticket(models.Model):
    """
    Represents one or more ticket , bought by a user in an order
    """

    class Meta:
        verbose_name = 'بلیت'
        verbose_name_plural = 'ها'

    showtime = models.ForeignKey('ShowTime', on_delete=models.PROTECT, verbose_name='سانس')
    customer = models.ForeignKey('accounts.Profile', on_delete=models.PROTECT, verbose_name="کاربر")
    seat_count = models.IntegerField('تعداد صندلی')
    order_time = models.DateTimeField('زمان خرید', auto_now_add=True)

    def __str__(self):
        return '{} بلیت به نام {} برای فیلم {}'.format(self.seat_count, self.customer, self.showtime.movie)
