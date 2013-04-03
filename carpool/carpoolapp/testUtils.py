from django.db import models
from datetime import *
from carpoolapp.models import *
import string
import random

def genUser():
	first = id_gen(1, string.ascii_uppercase) + id_gen(random.randint(1,10), string.ascii_lowercase)
	last = id_gen(1, string.ascii_uppercase) + id_gen(random.randint(1,10), string.ascii_lowercase)
	username = id_gen(random.randint(5,10), string.ascii_lowercase+string.digits)
	email = username + "@carpoolapp.com"
	year = 1930 + random.randint(0,70)
	month = random.randint(1,12)
	day = random.randint(1,30)
	dob = date(year, month, day)
	s = ["male", "female"]
	sex = random.choice(s)
	password = id_gen(random.randint(5,10), string.ascii_lowercase+string.digits)
	cellphone = id_gen(3, string.digits) + "-" + id_gen(3, string.digits) + "-" + id_gen(4, string.digits)
	drr = ["driver", "rider"]
	dOrR = random.choice(drr)
	comments = id_gen(50, string.ascii_lowercase+" ")
	avg_rating = 5.0 * random.random()
	u = User(firstname = first,lastname = last, username = username,  email = email, dob = dob, sex = sex, password = password, cellphone = cellphone, driverOrRider = dOrR, comments = comments, avg_rating = avg_rating)
	u.save()
	return u

def genDriver():
	user = genUser()
	year = 2013
	month = 4
	day = random.randint(1,3)
	l_exp = date(year, month, day)
	license_no = id_gen()
	car_makes = ["Toyota", "Honda", "Hyundai", "BMW", "Mercedes", "Audi", "Nissan", "Ford", "Chevrolet", "Ferrari", "Lamborghini"]
	car_make = random.choice(car_makes)
	car_types = ["Coupe", "Sedan", "Truck", "SUV", "Van"]
	car_type = random.choice(car_types)
	car_mileage = random.randint(1, 100000)
	max_passengers = random.randint(1,9)
	driver = DriverInfo(driver = user, license_no = license_no, license_exp = l_exp, car_make = car_make, car_type = car_type, car_mileage = car_mileage, max_passengers = max_passengers)
	driver.save()
	return driver

def genRide():
	driver = genDriver()
	depart_t = datetime.now()
	dlat = 37.8717 + random.uniform(-1, 1)
	dlong = 122.2728 + random.uniform(-1, 1)
	alat = 37.8717 + random.uniform(-1, 1)
	along = 122.2728 + random.uniform(-1, 1)
	route = Route(driver_info=driver, rider=None, depart_time=depart_t, depart_lat=dlat, depart_lg=dlong, arrive_lat=alat, arrive_lg=along, maps_info = "MAPPS INFO...", status = False)
	route.save()
	return route


#from http://stackoverflow.com/questions/2257441/python-random-string-generation-with-upper-case-letters-and-digits
def id_gen(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for x in range(size))