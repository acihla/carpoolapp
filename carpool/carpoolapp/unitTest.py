from django.test import TestCase
from django.utils import unittest
import json
import testLib
import testUtils
import os
from datetime import date, datetime, time, timedelta
from django.test.client import Client
import views
import models


#responses to be handled by application
SUCCESS               =   1  # : a success
ERR_BAD_DEPARTURE  =  -1  # : Departure location is not valid
ERR_BAD_DESTINATION       =  -2  # : Destination location is not valid
ERR_BAD_USERID      =  -3  # : UID does not exist in db, or is not a driver
ERR_BAD_TIME     =  -4   #format for time is bad
ERR_DATABASE_SEARCH_ERROR   = -5  
ERR_BAD_HEADER= -6
ERR_BAD_SERVER_RESPONSE = -7
MAX_LENGTH_IN = 200  #max length for all datums in our db
MAX_LENGTH_FIRST_LAST_PASS = 15 #max length for first and last name and password
MAX_LENGTH_EMAIL = 50  #max length email
COORD_LENGTH_IN = 20 # max length of coordinates
ERR_BAD_KEY = -8
ERR_NOT_USER = -9
ERR_BAD_EMAIL = -10
ERR_BAD_INPUT_OR_LENGTH = -11
ERR_BAD_DOB = -12
ERR_BAD_JSON = -13
ERR_USER_EXISTS =-14
ERR_EXPIRED_LICENSE =-15
ERR_BAD_APIKEY = -16
ERR_REQUEST_EXISTS =-17
ERR_KEY_VAL_DOES_NOT_EXISTS =-18
ERR_BAD_DRIVER_INFO = -19
ERR_BAD_CREDENTIALS = -20

class UnitTest(unittest.TestCase):
        """
        Unittests for the Users model class (a sample, incomplete)
        """
        def setUp(self):
            os.environ['DJANGO_SETTINGS_MODULE'] = "mysite.settings"
            testUtils.genDriver()
            testUtils.genDriver()
            testUtils.genUser()
            testUtils.genUser()
            self.users = models.User()
            self.routes = models.Route()

        #successful addition of a user
        def testAddUser1(self):
            newrequest = views.request
            newrequest.body = json.dumps({ 'firstname' : 'AJ', 'lastname' : 'Cihla', 'email' : 'alex.cihla@yahoo.com', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'password', 'cellphone' : '408-826-9366', 'driver' : 0})
            response = views.signup(newrequest)
            response = json.loads(response.content)
            print(response)
            self.assertEquals(testLib.RestTestCase.SUCCESS, response.get("errCode"))
        
        #checking that destination coordinates received from front end are legit and will be mappable if neccessary
        def testUnitHandleRouteDataCleaner1(self):
            #Tests that adding a user works
            self.assertEquals(testLib.RestTestCase.SUCCESS, views.handleRouteData(1, "-122.080078", "37.279413","-122.088878", "37.579413"))

        def testUnitHandleRouteDataCleaner2(self):
            #Tests that adding a route fails with bad destination location coordinates
            self.assertEquals(testLib.RestTestCase.ERR_BAD_DESTINATION , views.handleRouteData(1, "-122.080078", "37.279413","-122.088878", "98.579413"))

        def testUnitHandleRouteDataCleaner3(self):
            #Tests that adding a route fails with bad destination location coordinates
            self.assertEquals(testLib.RestTestCase.ERR_BAD_DESTINATION, views.handleRouteData(1, "-122.080078", "37.279413","182.088878", "37.579413"))

        def testUnitHandleRouteDataCleaner4(self):
            #Tests that adding a route fails with bad destination location coordinates
            self.assertEquals(testLib.RestTestCase.ERR_BAD_DESTINATION, views.handleRouteData(1, "-122.080078", "37.279413","-122.088878", "97.579413"))

        def testUnitHandleRouteDataCleaner5(self):
            #Tests that adding a route fails with bad destination location coordinates
            self.assertEquals(testLib.RestTestCase.ERR_BAD_DESTINATION, views.handleRouteData(1, "-122.080078", "37.279413","-192.088878", "37.579413"))

        def testUnitHandleRouteDataCleaner6(self):
            #Tests that adding a route fails with bad destination location coordinates
            self.assertEquals(testLib.RestTestCase.ERR_BAD_DESTINATION, views.handleRouteData(1, "-122.080078", "37.279413","-122.088878", "97.523322223479413"))

        def testUnitHandleRouteDataCleaner7(self):
            #Tests that adding a route fails with bad destination location coordinates
            self.assertEquals(testLib.RestTestCase.ERR_BAD_DESTINATION, views.handleRouteData(1, "-122.080078", "37.279413","-182.08823434223878", "37.579413"))

        #checking that departure coordinates received from front end are legit and will be mappable if neccessary
        def testUnitHandleRouteDataCleaner8(self):
            #Tests that adding a route fails with bad departure location coordinates
            self.assertEquals(testLib.RestTestCase.ERR_BAD_DEPARTURE, views.handleRouteData(1, "-190.080078", "37.279413","-122.088878", "37.579413"))

        def testUnitHandleRouteDataCleaner9(self):
            #Tests that adding a route fails with bad departure location coordinates
            self.assertEquals(testLib.RestTestCase.ERR_BAD_DEPARTURE, views.handleRouteData(1, "-122.080078", "91.279413","-122.088878", "37.579413"))

        def testUnitHandleRouteDataCleaner10(self):
            #Tests that adding a route fails with bad departure location coordinates
            self.assertEquals(testLib.RestTestCase.ERR_BAD_DEPARTURE, views.handleRouteData(1, "192.080078", "37.279413","-132.088878", "37.579413"))

        def testUnitHandleRouteDataCleaner11(self):
            #Tests that adding a route fails with bad departure location coordinates
            self.assertEquals(testLib.RestTestCase.ERR_BAD_DEPARTURE, views.handleRouteData(1, "-122.080078", "-137.279413","-122.088878", "65.579413"))

        def testUnitHandleRouteDataCleaner12(self):
            #Tests that adding a route fails with bad departure location coordinates
            self.assertEquals(testLib.RestTestCase.ERR_BAD_DEPARTURE, views.handleRouteData(1, "-192.082333234320078", "37.279413","-122.088878", "37.579413"))

        def testUnitHandleRouteDataCleaner13(self):
            #Tests that adding a route fails with bad departure location coordinates
            self.assertEquals(testLib.RestTestCase.ERR_BAD_DEPARTURE, views.handleRouteData(1, "-122.0823378", "91.272349234234413","-122.088878", "37.579413"))

        #checking with different BAD userid numbers... they should always fail ASSUMING THAT WE DONT CREATE MORE THAN 999999999 users
        def testUnitHandleRouteDataCleaner14(self):
            #Tests that adding a route with bad userid fails
            self.assertEquals(testLib.RestTestCase.ERR_BAD_USERID, views.handleRouteData(-233, "-122.080078", "37.279413","-122.088878", "37.579413"))

        def testUnitHandleRouteDataCleaner15(self):
            #Tests that adding a route with bad userid fails
            self.assertEquals(testLib.RestTestCase.ERR_BAD_USERID, views.handleRouteData(99999999, "-122.080078", "37.279413","-122.088878", "37.579413"))

        def testUnitHandleRouteDataCleaner16(self):
            #Tests that adding a route with bad userid fails
            self.assertEquals(testLib.RestTestCase.ERR_BAD_USERID, views.handleRouteData(-1, "-122.080078", "37.279413","-122.088878", "37.579413"))

        def testUnitModelUserToDict(self):
            #Test if to_dict method works properly
            users = models.User.objects.all()
            if len(users) > 0:
                user = users[0]
                dic = user.to_dict()
                fields = ["firstname", "lastname", "email", "dob", "sex", "cellphone", "user_type", "comments", "avg_rating"]
                for field in fields:
                    self.assertEquals(dic.get(field,None), eval("user."+field))

        def testUnitModelUserToDictUnsecure(self):
            #Test if to_dict method works properly
            users = models.User.objects.all()
            if len(users) > 0:
                user = users[0]
                dic = user.to_dict_unsecure()
                fields = ["firstname", "lastname",  "email", "dob", "sex", "password", "cellphone", "user_type", "comments", "avg_rating"]
                for field in fields:
                    self.assertEquals(dic.get(field,None), eval("user."+field))

        def testUnitModelDriverInfoToDict(self):
            #Test if to_dict method works properly
            di = models.DriverInfo.objects.all()
            if len(di) > 0:
                di= di[0]
                dic = di.to_dict()
                fields = ["license_no", "license_exp", "car_make", "car_type", "car_mileage", "max_passengers"]
                for field in fields:
                    self.assertEquals(dic.get(field,None), eval("di."+field))

        def testUnitModelRouteToDict(self):
            #Test if to_dict method works properly
            routes = models.Route.objects.all()
            if len(routes) > 0:
                route= routes[0]
                dic = route.to_dict()
                fields = ["depart_time", "depart_lat", "depart_lg", "arrive_lat", "arrive_lg", "maps_info", "status"]
                for field in fields:
                    self.assertEquals(dic.get(field,None), eval("route."+field))

        
# If this file is invoked as a Python script, run the tests in this module
if __name__ == "__main__":
    # Add a verbose argument
    sys.argv = [sys.argv[0]] + ["-v"] + sys.argv[1:]
    unittest.main()