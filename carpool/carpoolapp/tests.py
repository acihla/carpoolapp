"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.utils import unittest
import StringIO
import json
import testLib
import testUtils
import os
from datetime import date, datetime, time, timedelta
from django.test.client import Client
from carpoolapp.unitTest import *
import views
from carpoolapp.models import *
import unittest


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
ERR_UNKOWN_IN_SIGNUP = -21
ERR_UNKNOWN_ROUTE = -22
ERR_NO_RIDER_DRIVER_CONTACT =-23
ERR_BAD_PASSWORD = -24


class TestUnit(testLib.RestTestCase):


    """Issue a REST API request to run the unit tests, and analyze the result"""
    def testUnit(self):
        buffer = StringIO.StringIO()
        suite = unittest.TestLoader().loadTestsFromTestCase(UnitTest)
        result = unittest.TextTestRunner(stream = buffer, verbosity = 2).run(suite)
        rv = {"totalTests": result.testsRun, "nrFailed": len(result.failures), "output": buffer.getvalue()}
        self.assertTrue('output' in rv)
        print ("Unit tests output:\n"+
               "\n***** ".join(rv['output'].split("\n")))
        self.assertTrue('totalTests' in rv)
        print "***** Reported "+str(rv['totalTests'])+" unit tests"
        # When we test the actual project, we require at least 40 unit tests
        minimumTests = 40
        if "SAMPLE_APP" in os.environ:
            minimumTests = 4

        self.assertTrue(rv['totalTests'] >= minimumTests,
                        "at least "+str(minimumTests)+" unit tests. Found only "+str(rv['totalTests'])+". use SAMPLE_APP=1 if this is the sample app")
        self.assertEquals(0, rv['nrFailed'])





class ZAddRouteTest(testLib.RestTestCase):
    def assertResponse(self, respData, errCode = testLib.RestTestCase.SUCCESS):
        #Check that the response data dictionary matches the expected values
        expected = { 'errCode' : errCode }
        #if respData.get(count, None) is not None:
        #   expected['count']  = count
        self.assertDictEqual(expected, respData)

    def testAddForRoutesPrep1(self): 
        #try:
        #    testDriver = User.objects.get(email = "alex.samuel@yahoo.com")
            
        #except User.DoesNotExist:
        respData = self.makeRequest("/signup", method="POST", data = { 'firstname' : 'AJ', 'lastname' : 'Cihla', 'email' : 'alex.samuel@yahoo.com', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'password', 'cellphone' : '408-826-9366', 'driver' : 1, 'license_no' : '20934089sf', 'license_exp' : '03-12-2015', 'car_make' : 'Honda Accord', 'car_type' : 'Sedan', 'car_mileage' : 30, 'max_passengers' : 2} )
        #    self.assertResponse(respData, testLib.RestTestCase.SUCCESS)
        #    print("testAddforPREP!!!!")
        self.assertTrue(respData.get("errCode") == testLib.RestTestCase.SUCCESS)
        print("testAddForRoutesPrep1")

    def testAddForRoutesPrep2(self):
        respData = self.makeRequest("/signup", method="POST", data = { 'firstname' : 'AJ', 'lastname' : 'Cihla', 'email' : 'alex.peter@bs7.com', 'dob' : '04-17-1992', 'sex' : 'male', 'password' : 'password', 'cellphone' : '(408)8269366', 'driver' : 0} )
        self.assertTrue(respData.get("errCode") == testLib.RestTestCase.SUCCESS)
        print("testAddForRoutesPrep2")

    #generic first add route test with legitimate coordinates
    def testzAddGood1(self):
        testApi = User.objects.get(email = 'alex.samuel@yahoo.com').apikey
        #testApi = self.makeRequest("/TESTAPI/getTestDriver", method ="POST", data= {}) #User.objects.get(email = "alex.gatech@berkeley.edu").apikey
        #if testApi["apikey"] != "None":
        respData = self.makeRequest("/driver/addroute", method="POST", data = { 'apikey' : testApi,"edt":"0:36","dest-lat":"37.83421105081068","depart-long":"-122.27687716484068","depart-lat":"37.856989109666834","date":"04-09-2013","dest-long":"-122.27281998842956"} )
        self.assertResponse(respData, testLib.RestTestCase.SUCCESS)
        print("testAddGood1")
        
    """
    def testAddGoodUnit1(self):
        testDriver = testUtils.genDriver()
        driverApi = testDriver.driver.apikey
        data = { 'apikey' : 'f2b8b1a60723c5763422d6d5ba25a0594ee2cecc',"edt":"0:36","dest-lat":"37.83421105081068","depart-long":"-122.27687716484068","depart-lat":"37.856989109666834","date":"04-09-2013","dest-long":"-122.27281998842956"}
        request =  = json.loads('data' : { 'apikey' : 'f2b8b1a60723c5763422d6d5ba25a0594ee2cecc',"edt":"0:36","dest-lat":"37.83421105081068","depart-long":"-122.27687716484068","depart-lat":"37.856989109666834","date":"04-09-2013","dest-long":"-122.27281998842956"} )
        response = views.addroute(request)
        self.assertResponse(response, testLib.RestTestCase.SUCCESS)

    """
    def testzAddGood2(self):
        testApi = User.objects.get(email = 'alex.samuel@yahoo.com').apikey
        #testApi = self.makeRequest("/TESTAPI/getTestDriver", method ="POST", data= {})
        respData = self.makeRequest("/driver/addroute", method="POST", data = { 'apikey' : testApi,"edt":"23:36","dest-lat":"37.83421105081068","depart-long":"-122.27687716484068","depart-lat":"37.856989109666834","date":"04-17-2013","dest-long":"-122.27281998842956"} )
        print("testAddGood2")
        self.assertResponse(respData, testLib.RestTestCase.SUCCESS)

    def testzAddGood3(self):
        testApi = User.objects.get(email = 'alex.samuel@yahoo.com').apikey
        #testApi = self.makeRequest("/TESTAPI/getTestDriver", method ="POST", data= {})
        respData = self.makeRequest("/driver/addroute", method="POST", data = { 'apikey' : testApi,"edt":"2:36","dest-lat":"37.83421105081068","depart-long":"-122.27687716484068","depart-lat":"37.856989109666834","date":"04-17-2013","dest-long":"-172.27281998842956"} )
        print("testAddGood3")
        self.assertResponse(respData, testLib.RestTestCase.SUCCESS)

    def testzAddGood4(self):
        testApi = User.objects.get(email = 'alex.samuel@yahoo.com').apikey
        #testApi = self.makeRequest("/TESTAPI/getTestDriver", method ="POST", data= {})
        respData = self.makeRequest("/driver/addroute", method="POST", data = { 'apikey' : testApi,"edt":"2:36","dest-lat":"87.83421105081068","depart-long":"-172.27687716484068","depart-lat":"85.856989109666834","date":"04-17-2013","dest-long":"-128.27281998842956"} )
        print("testAddGood4")
        self.assertResponse(respData, testLib.RestTestCase.SUCCESS)

    #checks that coordinates on departure are good
    def testzAddBadDep5(self):
        testApi = User.objects.get(email = 'alex.samuel@yahoo.com').apikey
        #testApi = self.makeRequest("/TESTAPI/getTestDriver", method ="POST", data= {})
        respData = self.makeRequest("/driver/addroute", method="POST", data = { 'apikey' : testApi,"edt":"2:36","dest-lat":"37.83421105081068","depart-long":"-192.080078","depart-lat":"37.856989109666834","date":"04-17-2013","dest-long":"-122.27281998842956"} )
        print("testAddBadDep5")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_DEPARTURE)

    def testzAddBadDep6(self):
        testApi = User.objects.get(email = 'alex.samuel@yahoo.com').apikey
        #testApi = self.makeRequest("/TESTAPI/getTestDriver", method ="POST", data= {})
        respData = self.makeRequest("/driver/addroute", method="POST", data = { 'apikey' : testApi,"edt":"2:36","dest-lat":"67.83421105081068","depart-long":"-162.080078","depart-lat":"97.856989109666834","date":"04-17-2013","dest-long":"-122.27281998842956"} )
        print("testAddBadDep6")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_DEPARTURE)

    def testzAddBadDep7(self):
        testApi = User.objects.get(email = 'alex.samuel@yahoo.com').apikey
        #testApi = self.makeRequest("/TESTAPI/getTestDriver", method ="POST", data= {})
        respData = self.makeRequest("/driver/addroute", method="POST", data = { 'apikey' : testApi,"edt":"2:36","dest-lat":"37.83421105081068","depart-long":"192.080078","depart-lat":"37.856989109666834","date":"04-17-2013","dest-long":"-122.27281998842956"} )
        print("testAddBadDep8")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_DEPARTURE)

    def testzAddBadDep8(self):
        testApi = User.objects.get(email = 'alex.samuel@yahoo.com').apikey
        #testApi = (User.objects.get(email = 'alex.gatech@berkeley.edu')).apikey
        respData = self.makeRequest("/driver/addroute", method="POST", data = { 'apikey' : testApi,"edt":"2:36","dest-lat":"37.83421105081068","depart-long":"-132.080078","depart-lat":"-91.856989109666834","date":"04-17-2013","dest-long":"-122.27281998842956"} )
        print("testAddBadDep8")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_DEPARTURE)

    #checks that coordinates on destination are good
    def testzAddBadDest9(self):
        testApi = User.objects.get(email = 'alex.samuel@yahoo.com').apikey
        #testApi = self.makeRequest("/TESTAPI/getTestDriver", method ="POST", data= {})
        respData = self.makeRequest("/driver/addroute", method="POST", data = { 'apikey' : testApi,"edt":"2:36","dest-lat":"37.83421105081068","depart-long":"-142.080078","depart-lat":"37.856989109666834","date":"04-17-2013","dest-long":"-182.27281998842956"} )
        print("testAddBadDest9")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_DESTINATION)

    def testzAddBadDest10(self):
        testApi = User.objects.get(email = 'alex.samuel@yahoo.com').apikey
        #testApi = self.makeRequest("/TESTAPI/getTestDriver", method ="POST", data= {})
        respData = self.makeRequest("/driver/addroute", method="POST", data = { 'apikey' : testApi,"edt":"2:36","dest-lat":"97.83421105081068","depart-long":"-162.080078","depart-lat":"37.856989109666834","date":"04-17-2013","dest-long":"-122.27281998842956"} )
        print("testAddBadDest10")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_DESTINATION)

    def testzAddBadDest11(self):
        testApi = User.objects.get(email = 'alex.samuel@yahoo.com').apikey
        #testApi = self.makeRequest("/TESTAPI/getTestDriver", method ="POST", data= {})
        respData = self.makeRequest("/driver/addroute", method="POST", data = { 'apikey' : testApi,"edt":"2:36","dest-lat":"97.83421105081068","depart-long":"-122.080078","depart-lat":"37.856989109666834","date":"04-17-2013","dest-long":"132.27281998842956"} )
        print("testAddBadDest11")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_DESTINATION)

    def testzAddBadDest12(self):
        testApi = User.objects.get(email = 'alex.samuel@yahoo.com').apikey
        #testApi = self.makeRequest("/TESTAPI/getTestDriver", method ="POST", data= {})
        respData = self.makeRequest("/driver/addroute", method="POST", data = { 'apikey' : testApi,"edt":"2:36","dest-lat":"37.83421105081068","depart-long":"-133.080078","depart-lat":"37.856989109666834","date":"04-17-2013","dest-long":"192.27281998842956"} )
        print("testAddBadDest12")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_DESTINATION)

    #to check that adding route only works for established drivers
    def testzAddGoodUser13(self):
        testApi = User.objects.get(email = 'alex.samuel@yahoo.com').apikey
        #testApi = self.makeRequest("/TESTAPI/getTestDriver", method ="POST", data= {})
        respData = self.makeRequest("/driver/addroute", method="POST", data = { 'apikey' : testApi,"edt":"2:36","dest-lat":"37.83421105081068","depart-long":"-132.080078","depart-lat":"37.856989109666834","date":"04-17-2013","dest-long":"-122.27281998842956"} )
        print("testAddGoodUser13")
        self.assertResponse(respData, testLib.RestTestCase.SUCCESS)

    def testzAddBadUser14(self):
        respData = self.makeRequest("/driver/addroute", method="POST", data = { 'apikey' : '27d006284191d231b9639018d9bcf6947641',"edt":"2:36","dest-lat":"37.83421105081068","depart-long":"-162.080078","depart-lat":"37.856989109666834","date":"04-17-2013","dest-long":"-122.27281998842956"} )
        print("testAddBadUser14")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_APIKEY)

    def testzAddBadUser15(self):
        respData = self.makeRequest("/driver/addroute", method="POST", data = { 'apikey' : '27d006284191d231b9639d18d9bcf6947641',"edt":"2:36","dest-lat":"37.83421105081068","depart-long":"-12.080078","depart-lat":"37.856989109666834","date":"04-17-2013","dest-long":"-122.27281998842956"} )
        print("testAddBadUser15")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_APIKEY)

    def testzAddBadUser16(self):
        respData = self.makeRequest("/driver/addroute", method="POST", data = { 'apikey' : '27d006284191d23190bc9d18d9bcf6947641',"edt":"2:36","dest-lat":"37.83421105081068","depart-long":"-122.080078","depart-lat":"37.856989109666834","date":"04-17-2013","dest-long":"-122.27281998842956"} )
        print("testAddBadUser16")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_APIKEY)
        

class ZSearchTest(testLib.RestTestCase):
    def assertResponse(self, respData, errCode = testLib.RestTestCase.SUCCESS):
        #Check that the response data dictionary matches the expected values
        expected = { 'errCode' : errCode }
        #if respData.get(count, None) is not None:
        #   expected['count']  = count
        self.assertDictEqual(expected, respData)

    
    def testzSearch1(self):
        print "testSearch1"
        respData = self.makeRequest("/rider/search", method="GET", data = { 'user' : 1, 'start' : 'Berkeley', 'end' : 'San Jose'} )
        self.assertEquals(respData.get("errCode",-1), testLib.RestTestCase.SUCCESS)

    def testzSearch2(self):
        print "testSearch2"
        respData = self.makeRequest("/rider/search", method="GET", data = { 'user' : 1, 'start' : 'Berkeley', 'end' : 'San Jose'} )
        t = (respData.get("size", -1) >= 0)
        self.assertEquals(t, True)

    def testzSearch3(self):
        print "testSearch3"
        respData = self.makeRequest("/rider/search", method="GET", data = { 'user' : 1, 'start' : 'Berkeley', 'end' : 'San Jose'} )
        t = (respData.get("size", -1) > 0)
        if t:
            rides = respData.get("rides", None)
            self.assertTrue(rides != None);
            for ride in rides:
                status = ride.get("status", None)
                self.assertEquals(status, "valid")

    def testzSearch4(self):
        print "testSearch4"
        respData = self.makeRequest("/rider/search", method="GET", data = { 'user' : 1, 'start' : 'Berkeley', 'end' : 'San Jose'} )
        t = (respData.get("size", -1) > 0)
        if t:
            rides = respData.get("rides", None)
            self.assertTrue(rides != None);
            for ride in rides:
                driver_info = ride.get("driver_info", None)
                self.assertTrue(driver_info != None)

    def testzSearch5(self):
        print "testSearch5"
        respData = self.makeRequest("/rider/search", method="GET", data = { 'user' : 1, 'start' : 'Berkeley', 'end' : 'San Jose'} )
        t = (respData.get("size", -1) > 0)
        if t:
            rides = respData.get("rides", None)
            self.assertTrue(rides != None);
            for ride in rides:
                driver_info = ride.get("driver_info", None)
                self.assertTrue(driver_info != None)
                driver = driver_info.get("driver", None)
                self.assertTrue(driver != None)

class ZManageRouteTest(testLib.RestTestCase):
    def assertResponse(self, respData, errCode = testLib.RestTestCase.SUCCESS):
        #Check that the response data dictionary matches the expected values
        expected = { 'errCode' : errCode }
        #if respData.get(count, None) is not None:
        #   expected['count']  = count
        self.assertDictEqual(expected, respData)

    def testzzManageRoute1(self):
        print "testManageRoute1"
        respData = self.makeRequest("/driver/manageRoute", method="GET", data = { 'apikey' : '06284191d231b96390bc9d18d9bcf6947641'} )
        self.assertTrue(respData.get("errCode",-1) == testLib.RestTestCase.SUCCESS)

    def testzzManageRoute2(self):
        print "testManageRoute2"
        respData = self.makeRequest("/driver/manageRoute", method="GET", data = { 'apikey' : '27d00231b96390bc9d18d9bcf6947641'} )
        self.assertTrue(respData.get("errCode",-1) == testLib.RestTestCase.ERR_BAD_APIKEY)

    def testzzManageRoute3(self):
        print "testManageRoute3"
        respData = self.makeRequest("/driver/manageRoute", method="GET", data = { 'apikey' : '28b1f28813b70771cc26838e40fe9199167b4c76'} )
        self.assertTrue(respData.get("errCode",-1) == testLib.RestTestCase.ERR_BAD_DRIVER_INFO)
'''
class RiderStatusTest(testLib.RestTestCase):
    def assertResponse(self, respData, errCode = testLib.RestTestCase.SUCCESS):
        #Check that the response data dictionary matches the expected values
        expected = { 'errCode' : errCode }
        #if respData.get(count, None) is not None:
        #   expected['count']  = count
        self.assertDictEqual(expected, respData)

     
    def testUserPendingRides(self):
        print "testing user pending status"
        print "testUserPendingRides"
        
        print "before the function is called"
        self.makeRequest("/rider/select", method="POST", data = { 'apikey' : "d4a0fb1919d3a5c353c60279a3081f437465959c", 'route_id' : 30} ) 
        print "before the second function is called"
        self.makeRequest("/rider/select", method="POST", data = { 'apikey' : "d4a0fb1919d3a5c353c60279a3081f437465959c", 'route_id' : 20} )
        expected_dict = {}
        expected_dict[20]={"driver_lastname": "Vmsfbagdzxx", "route_arrive_lg": "-121.59343", "route_depart_lat": "38.4712594", "route_arrive_lat": "38.3945351", "route_depart_lg": "-123.04618", "driver_firstname": "Rwot"}
        expected_dict[30]={"driver_lastname": "Qzcytk", "route_arrive_lg": "-121.46535", "route_depart_lat": "38.6293819", "route_arrive_lat": "38.0733824", "route_depart_lg": "-122.51328", "driver_firstname": "Fgmemnvg"}
        respData = self.makeRequest("/rider/rides_pending", method="POST", data = { 'rider_apikey':"d4a0fb1919d3a5c353c60279a3081f437465959c"} )
        self.assertEquals(respData, expected_dict.values())
    
    def testUserDeniedRides(self):
   
        print "testUserDeniedRides "
        self.makeRequest("/rider/select", method="POST", data = { 'apikey' : "61057bca46cb9a6ecd3e4acb9aa0a484a5c5a725", 'route_id' : 28} )
        self.makeRequest("/driver/accept?from=61057bca46cb9a6ecd3e4acb9aa0a484a5c5a725&to=28&route_id=28&response=0", method="GET")
        expected_dict={}
        expected_dict[28]={"driver_lastname": "Rw", "route_arrive_lg": "-122.61246", "route_depart_lat": "36.8855946", "route_arrive_lat": "38.4072551", "route_depart_lg": "-122.29165", "driver_firstname": "Sxjp"}
        respData = self.makeRequest("/rider/rides_denied", method="POST", data = {  'rider_apikey':"61057bca46cb9a6ecd3e4acb9aa0a484a5c5a725"} )
        self.assertEquals(respData, expected_dict.values())
    
    def testUserCanceledRides(self):
        print "testUserCanceledRides"
        
        self.makeRequest("/rider/select", method="POST", data = { 'apikey' : "d13e5d1dbf9bf7741662e3862e23f455b7304579", 'route_id' : 28} )
        self.makeRequest("/rider/select", method="POST", data = { 'apikey' : "d13e5d1dbf9bf7741662e3862e23f455b7304579", 'route_id' : 35} )
        self.makeRequest("/rider/cancel_ride", method="POST", data = { 'apikey' : "d13e5d1dbf9bf7741662e3862e23f455b7304579", 'route_id' : 28} )
        self.makeRequest("/rider/cancel_ride", method="POST", data = { 'apikey' : "d13e5d1dbf9bf7741662e3862e23f455b7304579", 'route_id' : 35} )
        expected_dict = {}
        expected_dict[35]={"driver_lastname": "Xbzmutsi", "route_arrive_lg": "-122.21085", "route_depart_lat": "36.8800639", "route_arrive_lat": "37.1069058", "route_depart_lg": "-123.07194", "driver_firstname": "Eosobpdurt"}
        expected_dict[28]={"driver_lastname": "Rw", "route_arrive_lg": "-122.61246", "route_depart_lat": "36.8855946", "route_arrive_lat": "38.4072551", "route_depart_lg": "-122.29165", "driver_firstname": "Sxjp"}
        respData = self.makeRequest("/rider/rides_canceled", method="POST", data = { 'rider_apikey':"d13e5d1dbf9bf7741662e3862e23f455b7304579"} )
        self.assertEquals(respData, expected_dict.values())
    
    def testUserAcceptedRides(self):
        print "testUserAcceptedRides "
        self.makeRequest("/rider/select", method="POST", data = { 'apikey' : "49d53e86a23ddb6ecbdfdcd2dd915689e0db18e8", 'route_id' : 43} )
        self.makeRequest("/rider/select", method="POST", data = { 'apikey' : "49d53e86a23ddb6ecbdfdcd2dd915689e0db18e8", 'route_id' : 45} )

        self.makeRequest("/driver/accept?from=49d53e86a23ddb6ecbdfdcd2dd915689e0db18e8&to=43&route_id=43&response=1", method="GET")
        self.makeRequest("/driver/accept?from=49d53e86a23ddb6ecbdfdcd2dd915689e0db18e8&to=45&route_id=45&response=1", method="GET")

        expected_dict={}
        expected_dict[43]={"driver_lastname": "Mdlwopwc", "route_arrive_lg": "-122.02138", "route_depart_lat": "36.9985756", "route_arrive_lat": "37.9152692", "route_depart_lg": "-122.46316", "driver_firstname": "Mysifhs"}
        expected_dict[45]={"driver_lastname": "Qiyq", "route_arrive_lg": "-121.67304", "route_depart_lat": "36.9734151", "route_arrive_lat": "37.9390983", "route_depart_lg": "-121.42658", "driver_firstname": "Tcec"}
        respData = self.makeRequest("/rider/rides_accepted", method="POST", data = {  'rider_apikey':"49d53e86a23ddb6ecbdfdcd2dd915689e0db18e8"} )
        self.assertEquals(respData, expected_dict.values())
    

   
        

'''
class Select_RideTest(testLib.RestTestCase):
  def assertResponse(self, respData, errCode = testLib.RestTestCase.SUCCESS):
        #Check that the response data dictionary matches the expected values
        expected = { 'errCode' : errCode }
        #if respData.get(count, None) is not None:
        #   expected['count']  = count
        self.assertDictEqual(expected, respData)

  def testSelect_Good_Ride(self):
    print "before the function is called"
    respData = self.makeRequest("/rider/select", method="POST", data = { 'apikey' : "d4a0fb1919d3a5c353c60279a3081f437465959c", 'route_id' : 30} )
    print "after the function is being called"
    print("testSelect_Good_Ride")
    self.assertResponse(respData, testLib.RestTestCase.SUCCESS)
  
  def testSelect_BAD_Ride(self):
    respData = self.makeRequest("/rider/select", method="POST", data = { 'rider_id' : 1, 'route_id' : 2000,'comment':''} )
    print("testSelect_BAD_Ride")
    self.assertResponse(respData, testLib.RestTestCase.ERR_DATABASE_SEARCH_ERROR)

'''
class Accept_OR_Deny_RideTest(testLib.RestTestCase):
  def assertResponse(self, respData, errCode = testLib.RestTestCase.SUCCESS):
        #Check that the response data dictionary matches the expected values
        expected = { 'errCode' : errCode }
        #if respData.get(count, None) is not None:
        #   expected['count']  = count
        self.assertDictEqual(expected, respData)
  
  def test_Accept_Good_Ride(self):
        self.makeRequest("/rider/select", method="POST", data = { 'apikey' : "acdd1ad1353d8c25407ff8f9fb5080937495ca08", 'route_id' : 4} ) 
        respData=self.makeRequest("/driver/accept?from=acdd1ad1353d8c25407ff8f9fb5080937495ca08&to=4&route_id=4&response=0", method="GET")
        print("test_Accept_Good_Ride")
        self.assertResponse(respData, testLib.RestTestCase.SUCCESS)

  def test_Accept_BAD_Ride(self):
    respData = self.makeRequest("/driver/accept?from=-1&to=-10&route_id=0&response=0", method="GET")
    print("test_Accept_BAD_Ride")
    self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_SERVER_RESPONSE)
  '''
