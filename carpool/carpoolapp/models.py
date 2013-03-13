from django.db import models


class User(models.Model):
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    dob = models.DateField()
    sex = models.CharField(max_length=10)
    password = models.CharField(max_length=200)
    cellphone = models.CharField(max_length=200)
    driver = models.BooleanField(default=0)
    comments = models.CharField(max_length=200)
    avg_rating = models.IntegerField()

    def __unicode__(self):
        return self.username

class DriverInfo(models.Model):
    driver = models.ForeignKey(User)
    license_no = models.CharField(max_length=200)
    license_exp = models.DateField()
    car_make = models.CharField(max_length=200)
    car_type = models.CharField(max_length=200)
    car_mileage = models.CharField(max_length=200)
    max_passengers = models.IntegerField()

    def __unicode__(self):
        return self.license_no

class Rating(models.Model):
	owner = models.ForeignKey(User)
	author = models.CharField(max_length=200)
	rating = models.IntegerField()
	comment = models.CharField(max_length=400)


class Route(models.Model):
    driver = models.ForeignKey(User)
    rider = models.CharField(max_length=200)
    depart_time = models.DateTimeField()
    #arrival_time = models.DateTimeField()
    #depart_lat = models.CharField(max_length=200)
    #depart_lg = models.CharField(max_length=200)
    #arrive_lat = models.CharField(max_length=200)
    #arrive_lg = models.CharField(max_length=200)
    maps_info = models.CharField(max_length=5000)
    status = models.BooleanField(default=0)

class SampleKey(models.Model):
    name = models.CharField(max_length=200)
    
class Sample(models.Model):
    driver = models.ForeignKey(SampleKey)
    rider = models.CharField(max_length=200)

