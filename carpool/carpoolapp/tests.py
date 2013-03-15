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


    def testAdd1(self):
        respData = self.makeRequest("/driver/addroute", method="POST", data = { 'user' : 1, 'depart-long' : '-122.080078', 'depart-lat' : '37.579413', 'dest-long' : '-122.000078', 'dest-lat' : '37.509413'} )
        print(respData)
        self.assertResponse(respData, testLib.RestTestCase.SUCCESS)

    """
    def testAdd2(self):
        respData = self.makeRequest("/driver/addroute", method="POST", data = { 'user' : 2, 'start' : '7075 Brooktree Way, San Jose, CA', 'end' : '6583 Jeremie Drive San Jose'} )
        print(respData)
        self.assertResponse(respData, testLib.RestTestCase.SUCCESS)

    def testAdd3(self):
        respData = self.makeRequest("/driver/addroute", method="POST", data = { 'user' : 2, 'start' : 'Berkeley', 'end' : '6583 Jeremie Drive San Jose'} )
        print(respData)
        self.assertResponse(respData, testLib.RestTestCase.SUCCESS)

    def testAdd4(self):
        respData = self.makeRequest("/driver/addroute", method="POST", data = { 'user' : 1, 'start' : 'berkeley', 'end' : 'new york'} )
        print(respData)
        self.assertResponse(respData, testLib.RestTestCase.SUCCESS)
    """
class SearchTest(testLib.RestTestCase):
    def assertResponse(self, respData, errCode = testLib.RestTestCase.SUCCESS):
        #Check that the response data dictionary matches the expected values
        expected = { 'errCode' : errCode }
        #if respData.get(count, None) is not None:
        #   expected['count']  = count
        self.assertDictEqual(expected, respData)


    def testSearch1(self):
        respData = self.makeRequest("/rider/search", method="GET", data = { 'user' : 1, 'start' : 'Berkeley', 'end' : 'San Jose'} )
        print "testSearch1"
        self.assertEquals(respData.get("errCode",-1), testLib.RestTestCase.SUCCESS)

    def testSearch2(self):
        respData = self.makeRequest("/rider/search", method="GET", data = { 'user' : 1, 'start' : 'Berkeley', 'end' : 'San Jose'} )
        print "testSearch2"
        t = (respData.get("size", -1) >= 0)
        self.assertEquals(t, True)

    def testSearch3(self):
        respData = self.makeRequest("/driver/addroute", method="POST", data = { 'user' : 2, 'start' : 'Berkeley', 'end' : '6583 Jeremie Drive San Jose'} )
        respData = self.makeRequest("/rider/search", method="GET", data = { 'user' : 1, 'start' : 'Berkeley', 'end' : 'San Jose'} )
        print "testSearch3"
        size = len(respData.get("rides",[]))
        t = (size > 0)
        self.assertEquals(t, True)

    def testSearch4(self):
        respData = self.makeRequest("/rider/search", method="GET", data = { 'user' : 1, 'start' : 'Berkeley', 'end' : 'San Jose'} )
        print "testSearch4"
        self.assertEquals(respData.get("errCode",-1), testLib.RestTestCase.SUCCESS)
        

class Select_RideTest(testLib.RestTestCase):
  def assertResponse(self, respData, errCode = testLib.RestTestCase.SUCCESS):
        #Check that the response data dictionary matches the expected values
        expected = { 'errCode' : errCode }
        #if respData.get(count, None) is not None:
        #   expected['count']  = count
        self.assertDictEqual(expected, respData)

  def testSelect_Good_Ride(self):
    respData = self.makeRequest("/rider/select", method="POST", data = { 'rider_id' : 1, 'route_id' : 2} )

    print(respData)
    self.assertResponse(respData, testLib.RestTestCase.SUCCESS)

  def testSelect_BAD_Ride(self):
    respData = self.makeRequest("/rider/select", method="POST", data = { 'rider_id' : 1, 'route_id' : 2000} )

    print(respData)
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

    print(respData)
    self.assertResponse(respData, testLib.RestTestCase.SUCCESS)

  def test_Accept_BAD_Ride(self):
    respData = self.makeRequest("/driver/accept", method="GET", data = {  'route_id' : 2000} )

    print(respData)
    self.assertResponse(respData, testLib.RestTestCase.ERR_BAD_SERVER_RESPONSE)

