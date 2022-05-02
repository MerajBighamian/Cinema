from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    """
    Represents a user`s profile
    """

    class Meta:
        verbose_name = 'نمایه کاربری'
        verbose_name_plural = "نمایه های کاربری"

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="حساب کاربری") # one to one field for connect profile model to user model
    # important fields that are sorted in User Model:
    # first_name, last_name, email , data_joined
    mobile = models.CharField('تلفن همراه', max_length=11)
    MALE = 1
    FEMALE = 2
    genders = ((MALE, 'مرد'), (FEMALE, 'زن'))
    gender = models.IntegerField('جنسیت', choices=genders, null=True, blank=True)
    birth_date = models.DateField('تاریخ تولد', null=True, blank=True)
    address = models.TextField('آدرس', null=True, blank=True)
    profile_image = models.ImageField('تصویر', upload_to='users/profile_images/', null=True, blank=True)

    # fields related to tickets

    balance = models.IntegerField('اعتبار', default=0) # integer filed for hold balance of user profile

    def __str__(self):
        return self.user.get_full_name() # return full name of user

    def get_balance_display(self):
        return '{} تومان'.format(self.balance) # display balance of user with toman format

    # behaviors
    def deposit(self, amount): # deposit balance of user profile
        self.balance += amount
        self.save()

    def spend(self, amount): # spend balance of user profile
        if self.balance < amount: # check amount is lowter form balance money
            return False
        self.balance -= amount
        self.save() # save spended balance in model
        return True
