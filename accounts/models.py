
# Create your models here.
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Birthdata(models.Model):
    screen_name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100)
    user_id = models.IntegerField()
    date_of_birth = models.DateField(max_length=20)
    time_of_birth = models.CharField(max_length=250)
    birth_city_sate = models.CharField(max_length=250)
    longitude = models.CharField(max_length=250)
    lattitude = models.CharField(max_length=250)
    your_current_location = models.CharField(max_length=250)
    transits_chart_date = models.DateField(max_length=20)
    email = models.EmailField(max_length=100)
    cell_number = models.CharField(max_length=15)
    message = models.CharField(max_length=1000)

# This is rate your reading..


class RateyourReading(models.Model):

    screen_name = models.CharField(max_length=100)
    user_id = models.IntegerField()
    email = models.EmailField(max_length=100)
    rate_synchronic = models.CharField(max_length=100)
    message = models.CharField(max_length=1000)


class Contact(models.Model):
    # sno = models.AutoField(PrimaryKey=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    message = models.CharField(max_length=100)

    def __str__(self):
        return self.name
