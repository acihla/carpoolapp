from datetime import *
#from carpoolapp.models import *
from django.conf import models

#User 1
dob = date(1990,0,3,15)
u = User(firstname="Peter", lastname="Lee", email="nadapeter@gmail.com", dob = dob, sex="male", password = "asfd", cellphone = "510-910-2613", driver=True, comments = "hihih hihi comments", avg_rating = 3)
u.save()
l_exp = date(2016,1,11)
driver = DriverInfo(driver = u, license_no = "ABV32C", license_exp = l_exp, car_make = "Toyota", car_type = "Coupe", car_mileage = "13123", max_passengers = 4) 

driver.save()

depart_t = datetime.now()
route = Route(driver_info=driver, rider=None, depart_time=depart_t, depart_lat="40.111", depart_lg="112.3242", arrive_lat="40.999", arrive_lg="112.888", maps_info = "MAPPS INFOO", status = False)
route.save()

#User 2
dob = date(1995,2,15)
u2 = User(firstname = "Steph",lastname = "Ku",username = "sku",  email = "wrarr@wraarrr.com", dob = dob, sex = "female", password = "asdf", cellphone = "523293-2613", driverOrRider = "rider", comments = "hi I'm Stephanie", avg_rating = 3)
u2.save()
l_exp = date(2016,1,11)
driver2 = DriverInfo(driver = u2, license_no = "GEKKEK", license_exp = l_exp, car_make = "Toyota", car_type = "Coupe", car_mileage = "13123", max_passengers = 4)
driver2.save()
depart_t = datetime.now()
route = Route(driver_info=driver2, rider=None, depart_time=depart_t, depart_lat="38.2323", depart_lg="123.3242", arrive_lat="38.999", arrive_lg="123.888", maps_info = "MAPPS INFOO", status = False)
route.save()

dob = date(1991,2,15)
u3 = User(firstname = "Sam",lastname = "Vu",username = "svu",  email = "samvu@gmail.com", dob = dob, sex = "male", password = "asdf", cellphone = "4583848-3", driverOrRider = "rider", comments = "I iz Sam", avg_rating = 3)
u3.save()
l_exp = date(2016,1,11)
driver3 = DriverInfo(driver = u3, license_no = "BAEWKWE", license_exp = l_exp, car_make = "Toyota", car_type = "Coupe", car_mileage = "13123", max_passengers = 4)
driver3.save()
depart_t = datetime.now()
route = Route(driver_info=driver3, rider=None, depart_time=depart_t, depart_lat="45.2323", depart_lg="130.3242", arrive_lat="45.999", arrive_lg="130.888", maps_info = "MAPPS INFOO", status = False)
route.save()


