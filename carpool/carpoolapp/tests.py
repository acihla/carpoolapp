"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
import testLib

class SimpleTest(testLib.RestTestCase):
    def assertResponse(self, respData, count = 1, errCode = testLib.RestTestCase.SUCCESS):
    	#Check that the response data dictionary matches the expected values
        expected = { 'errCode' : errCode }
        #if respData.get(count, None) is not None:
	#   expected['count']  = count
	self.assertDictEqual(expected, respData)

    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

    def testAdd1(self):
        respData = self.makeRequest("driver/addRoute", method="POST", data = { 'user' : 'testUserAddRoute', 'start' : 'Berkeley', 'end' : 'San Jose'} )
        self.assertResponse(respData, testLib.RestTestCase.SUCCESS)

    
    def testAdd2(self):
        respData = self.makeRequest("driver/addRoute", method="POST", data = { 'user' : 'testUserAddRoute', 'start' : '7075 Brooktree Way, San Jose, CA', 'end' : '6583 Jeremie Drive San Jose'} )
        self.assertResponse(respData, testLib.RestTestCase.SUCCESS)

    def testAdd3(self):
        respData = self.makeRequest("driver/addRoute", method="POST", data = { 'user' : 'testUserAddRoute3', 'start' : 'Berkeley', 'end' : '6583 Jeremie Drive San Jose'} )
        self.assertResponse(respData, testLib.RestTestCase.SUCCESS)

    def testAdd4(self):
        respData = self.makeRequest("driver/addRoute", method="POST", data = { 'user' : 'testUserAddRoute4', 'start' : 'berkeley', 'end' : 'new york'} )
        self.assertResponse(respData, testLib.RestTestCase.SUCCESS)
