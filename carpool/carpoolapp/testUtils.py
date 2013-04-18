from django.db import models
from datetime import *
from carpoolapp.models import *
import string
import random

def genUser(driver = False):
	first = id_gen(1, string.ascii_uppercase) + id_gen(random.randint(1,10), string.ascii_lowercase)
	last = id_gen(1, string.ascii_uppercase) + id_gen(random.randint(1,10), string.ascii_lowercase)
	email = id_gen(random.randint(5,10), string.ascii_lowercase+string.digits) + "@carpoolapp.com"
	year = 1930 + random.randint(0,70)
	month = random.randint(1,12)
	day = random.randint(1,28)
	dob = date(year, month, day)
	s = ["male", "female"]
	sex = random.choice(s)
	password = id_gen(random.randint(5,10), string.ascii_lowercase+string.digits)
	cellphone = id_gen(3, string.digits) + "-" + id_gen(3, string.digits) + "-" + id_gen(4, string.digits)
	drr = ["driver", "rider"]
	dOrR = random.choice(drr)
	comments = id_gen(50, string.ascii_lowercase+" ")
	avg_rating = 5.0 * random.random()
	u = User(firstname = first,lastname = last, email = email, dob = dob, sex = sex, password = password, cellphone = cellphone, driver = driver, comments = comments, avg_rating = avg_rating)
	u.apikey = u.generate_apikey()
	u.save()
	return u

def genDriver():
	user = genUser(True)
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
	delta = timedelta(days=random.randint(1,2), hours = random.randint(-23,23), minutes=random.randint(0,59))
	depart_t = datetime.now() + delta
	dlat = str(37.8717 + random.uniform(-1, 1))[0:10]
	dlong = str(-122.2728 + random.uniform(-1, 1))[0:10]
	alat = str(37.8717 + random.uniform(-1, 1))[0:10]
	along = str(-122.2728 + random.uniform(-1, 1))[0:10]
	route = Route(driver_info=driver, rider=None, depart_time=depart_t, depart_lat=dlat, depart_lg=dlong, arrive_lat=alat, arrive_lg=along, maps_info = "MAPPS INFO...", status = False)
	route.save()
	return route


#from http://stackoverflow.com/questions/2257441/python-random-string-generation-with-upper-case-letters-and-digits
def id_gen(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for x in range(size))