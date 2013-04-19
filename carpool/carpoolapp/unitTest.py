"""
Unit tests for the server.py module.
This is just a sample. You should have more tests for your model (at least 10)
"""

from django.utils import unittest
import os
import testLib
import sys
import models
import views
from datetime import *


test_date = date(1992,4,17)


class UnitTest(unittest.TestCase):
    """
    Unittests for the Users model class (a sample, incomplete)
    """
    

    def setUp(self):
        os.environ['DJANGO_SETTINGS_MODULE'] = "mysite.settings"
        self.users = models.User()
        self.routes = models.Route()

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

    
        #print("******\n******\n******\nData is clean\n******\n******")
        """
        def testSelectRoute(self):
            #Tests that i can select a route
            self.assertEquals(1, views.select_ride({"rider_id":1, "route_id":2})

        #def testSelectRoute(self):
        """

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
