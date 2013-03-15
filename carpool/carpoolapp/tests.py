"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
import json
import testLib
import os


class TestUnit(testLib.RestTestCase):
    """Issue a REST API request to run the unit tests, and analyze the result"""
    def testUnit(self):
        respData = self.makeRequest("/TESTAPI/unitTests", method="POST")
        self.assertTrue('output' in respData)
        print ("Unit tests output:\n"+
               "\n***** ".join(respData['output'].split("\n")))
        self.assertTrue('totalTests' in respData)
        print "***** Reported "+str(respData['totalTests'])+" unit tests"
        # When we test the actual project, we require at least 10 unit tests
        minimumTests = 40
        if "SAMPLE_APP" in os.environ:
            minimumTests = 4
        self.assertTrue(respData['totalTests'] >= minimumTests,
                        "at least "+str(minimumTests)+" unit tests. Found only "+str(respData['totalTests'])+". use SAMPLE_APP=1 if this is the sample app")
        self.assertEquals(0, respData['nrFailed'])



class AddRouteTest(testLib.RestTestCase):
    def assertResponse(self, respData, errCode = testLib.RestTestCase.SUCCESS):
        #Check that the response data dictionary matches the expected values
        expected = { 'errCode' : errCode }
        #if respData.get(count, None) is not None:
        #   expected['count']  = count
        self.assertDictEqual(expected, respData)

    #generic first add route test with legitimate coordinates
    def testAddGood1(self):
        respData = self.makeRequest("/driver/addroute", method="POST", data = { 'user' : 1, 'depart-long' : '-122.080078', 'depart-lat' : '37.579413', 'dest-long' : '-122.000078', 'dest-lat' : '37.509413'} )
        print("testAddGood1")
        self.assertResponse(respData, testLib.RestTestCase.SUCCESS)
    
    def testAddGood2(self):
        respData = self.makeRequest("/driver/addroute", method="POST", data = { 'user' : 1, 'depart-long' : '-142.080078', 'depart-lat' : '27.50233', 'dest-long' : '-12.000078', 'dest-lat' : '-37.509413'} )
        print("testAddGood2")
        self.assertResponse(respData, testLib.RestTestCase.SUCCESS)

    def testAddGood3(self):
        respData = self.makeRequest("/driver/addroute", method="POST", data = { 'user' : 2, 'depart-long' : '-122.080078', 'depart-lat' : '-37.579413', 'dest-long' : '-122.000078', 'dest-lat' : '-37.509413'} )
        print("testAddGood3")
        self.assertResponse(respData, testLib.RestTestCase.SUCCESS)

    def testAddGood4(self):
        respData = self.makeRequest("/driver/addroute", method="POST", data = { 'user' : 2, 'depart-long' : '-122.080078', 'depart-lat' : '37.579234413', 'dest-long' : '-122.000078', 'dest-lat' : '37.509413'} )
        print("testAddGood4")
        self.assertResponse(respData, testLib.RestTestCase.SUCCESS)

    #checks that coordinates on departure are good
    def testAddBadDep5(self):
        respData = self.makeRequest("/driver/addroute", method="POST", data = { 'user' : 2, 'depart-long' : '-192.080078', 'depart-lat' : '37.579234413', 'dest-long' : '-122.000078', 'dest-lat' : '37.509413'} )
        print("testAddBadDep5")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_DEPARTURE)

    def testAddBadDep6(self):
        respData = self.makeRequest("/driver/addroute", method="POST", data = { 'user' : 1, 'depart-long' : '-122.080078', 'depart-lat' : '100.579234413', 'dest-long' : '-122.000078', 'dest-lat' : '37.509413'} )
        print("testAddBadDep6")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_DEPARTURE)

    def testAddBadDep7(self):
        respData = self.makeRequest("/driver/addroute", method="POST", data = { 'user' : 2, 'depart-long' : '182.080078', 'depart-lat' : '97.579234413', 'dest-long' : '-122.000078', 'dest-lat' : '37.509413'} )
        print("testAddBadDep8")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_DEPARTURE)

    def testAddBadDep8(self):
        respData = self.makeRequest("/driver/addroute", method="POST", data = { 'user' : 1, 'depart-long' : '-192.080078', 'depart-lat' : '-92.579234413', 'dest-long' : '-122.000078', 'dest-lat' : '37.509413'} )
        print("testAddBadDep8")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_DEPARTURE)

    #checks that coordinates on destination are good
    def testAddBadDest9(self):
        respData = self.makeRequest("/driver/addroute", method="POST", data = { 'user' : 2, 'depart-long' : '-142.080078', 'depart-lat' : '37.579234413', 'dest-long' : '-182.000078', 'dest-lat' : '37.509413'} )
        print("testAddBadDest9")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_DESTINATION)

    def testAddBadDest10(self):
        respData = self.makeRequest("/driver/addroute", method="POST", data = { 'user' : 1, 'depart-long' : '-122.080078', 'depart-lat' : '60.579234413', 'dest-long' : '-122.000078', 'dest-lat' : '97.509413'} )
        print("testAddBadDest10")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_DESTINATION)

    def testAddBadDest11(self):
        respData = self.makeRequest("/driver/addroute", method="POST", data = { 'user' : 2, 'depart-long' : '122.080078', 'depart-lat' : '47.579234413', 'dest-long' : '-192.000078', 'dest-lat' : '-97.509413'} )
        print("testAddBadDest11")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_DESTINATION)

    def testAddBadDest12(self):
        respData = self.makeRequest("/driver/addroute", method="POST", data = { 'user' : 1, 'depart-long' : '-132.080078', 'depart-lat' : '-12.579234413', 'dest-long' : '182.000078', 'dest-lat' : '137.509413'} )
        print("testAddBadDest12")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_DESTINATION)

    #to check that adding route only works for established drivers
    def testAddGoodUser13(self):
        respData = self.makeRequest("/driver/addroute", method="POST", data = { 'user' : 2, 'depart-long' : '-142.080078', 'depart-lat' : '37.579234413', 'dest-long' : '-122.000078', 'dest-lat' : '37.509413'} )
        print("testAddGoodUser13")
        self.assertResponse(respData, testLib.RestTestCase.SUCCESS)

    def testAddBadUser14(self):
        respData = self.makeRequest("/driver/addroute", method="POST", data = { 'user' : -1234, 'depart-long' : '-122.080078', 'depart-lat' : '60.579234413', 'dest-long' : '-122.000078', 'dest-lat' : '17.509413'} )
        print("testAddBadUser14")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_USERID)

    def testAddBadUser15(self):
        respData = self.makeRequest("/driver/addroute", method="POST", data = { 'user' : 99999999, 'depart-long' : '122.080078', 'depart-lat' : '47.579234413', 'dest-long' : '-132.000078', 'dest-lat' : '-37.509413'} )
        print("testAddBadUser15")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_USERID)

    def testAddBadUser16(self):
        respData = self.makeRequest("/driver/addroute", method="POST", data = { 'user' : -1, 'depart-long' : '-123.080078', 'depart-lat' : '-12.579234413', 'dest-long' : '132.000078', 'dest-lat' : '27.509413'} )
        print("testAddBadUser16")
        self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_USERID)

class SearchTest(testLib.RestTestCase):
    def assertResponse(self, respData, errCode = testLib.RestTestCase.SUCCESS):
        #Check that the response data dictionary matches the expected values
        expected = { 'errCode' : errCode }
        #if respData.get(count, None) is not None:
        #   expected['count']  = count
        self.assertDictEqual(expected, respData)

    
    def testSearch1(self):
        print "testSearch1"
        respData = self.makeRequest("/rider/search", method="GET", data = { 'user' : 1, 'start' : 'Berkeley', 'end' : 'San Jose'} )
        self.assertEquals(respData.get("errCode",-1), testLib.RestTestCase.SUCCESS)

    def testSearch2(self):
        print "testSearch2"
        respData = self.makeRequest("/rider/search", method="GET", data = { 'user' : 1, 'start' : 'Berkeley', 'end' : 'San Jose'} )
        t = (respData.get("size", -1) >= 0)
        self.assertEquals(t, True)

    def testSearch3(self):
        print "testSearch3"
        respData = self.makeRequest("/rider/search", method="GET", data = { 'user' : 1, 'start' : 'Berkeley', 'end' : 'San Jose'} )
        t = (respData.get("size", -1) > 0)
        if t:
            rides = respData.get("rides", None)
            self.assertTrue(rides != None);
            for ride in rides:
                status = ride.get("status", None)
                self.assertEquals(status, "False")

    def testSearch4(self):
        print "testSearch4"
        respData = self.makeRequest("/rider/search", method="GET", data = { 'user' : 1, 'start' : 'Berkeley', 'end' : 'San Jose'} )
        t = (respData.get("size", -1) > 0)
        if t:
            rides = respData.get("rides", None)
            self.assertTrue(rides != None);
            for ride in rides:
                driver_info = ride.get("driver_info", None)
                self.assertTrue(driver_info != None)

    def testSearch5(self):
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

        

class Select_RideTest(testLib.RestTestCase):
  def assertResponse(self, respData, errCode = testLib.RestTestCase.SUCCESS):
        #Check that the response data dictionary matches the expected values
        expected = { 'errCode' : errCode }
        #if respData.get(count, None) is not None:
        #   expected['count']  = count
        self.assertDictEqual(expected, respData)

  def testSelect_Good_Ride(self):
    respData = self.makeRequest("/rider/select", method="POST", data = { 'rider_id' : 1, 'route_id' : 2} )
    print("testSelect_Good_Ride")
    self.assertResponse(respData, testLib.RestTestCase.SUCCESS)

  def testSelect_BAD_Ride(self):
    respData = self.makeRequest("/rider/select", method="POST", data = { 'rider_id' : 1, 'route_id' : 2000} )
    print("testSelect_BAD_Ride")
    self.assertResponse(respData, testLib.RestTestCase.ERR_DATABASE_SEARCH_ERROR)

class Accept_OR_Deny_RideTest(testLib.RestTestCase):
  def assertResponse(self, respData, errCode = testLib.RestTestCase.SUCCESS):
        #Check that the response data dictionary matches the expected values
        expected = { 'errCode' : errCode }
        #if respData.get(count, None) is not None:
        #   expected['count']  = count
        self.assertDictEqual(expected, respData)

  def test_Accept_Good_Ride(self):
    respData = self.makeRequest("/driver/accept", method="GET", data = { 'route_id' : 2} )
    print("test_Accept_Good_Ride")
    self.assertResponse(respData, testLib.RestTestCase.SUCCESS)

  def test_Accept_BAD_Ride(self):
    respData = self.makeRequest("/driver/accept", method="GET", data = {  'route_id' : 2000} )
    print("test_Accept_BAD_Ride")
    self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_SERVER_RESPONSE)

