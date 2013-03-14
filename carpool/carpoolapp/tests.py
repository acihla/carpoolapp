"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
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
        minimumTests = 10
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
        respData = self.makeRequest("/driver/addroute", method="POST", data = { 'user' : 1, 'start' : 'Berkeley', 'end' : 'San Jose'} )
        print(respData)
        self.assertResponse(respData, testLib.RestTestCase.SUCCESS)

    
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

class SearchTest(testLib.RestTestCase):
    def assertResponse(self, respData, errCode = testLib.RestTestCase.SUCCESS):
        #Check that the response data dictionary matches the expected values
        expected = { 'errCode' : errCode }
        #if respData.get(count, None) is not None:
        #   expected['count']  = count
        self.assertDictEqual(expected, respData)


    def testSearch1(self):
        respData = self.makeRequest("/driver/addroute", method="POST", data = { 'user' : 1, 'start' : 'Berkeley', 'end' : 'San Jose'} )
        print(respData)
        self.assertResponse(respData, testLib.RestTestCase.SUCCESS)