"""
A library for functional testing of the server API
"""

import unittest
import httplib
import sys
import os
import json
import testUtils


class RestTestCase(unittest.TestCase):
    """
    Superclass for our functional tests. Defines the boilerplate for the tests
    """

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
    MAX_LENGTH_FIRST_LAST_PASS = 20 #max length for first and last name and password
    MAX_LENGTH_EMAIL = 50  #max length email
    COORD_LENGTH_IN = 15 # max length of coordinates
    ERR_BAD_KEY = -8
    ERR_NOT_USER = -9
    ERR_BAD_EMAIL = -10
    ERR_BAD_INPUT_OR_LENGTH = -11
    ERR_BAD_DOB = -12
    
    # Lookup the name of the server to test

    serverToTest = "127.0.0.1:8000"

    if "TEST_SERVER" in os.environ:
        serverToTest = os.environ["TEST_SERVER"]

    def makeRequest(self, url, method="GET", data={ }):
        """
        Make a request to the server.
        @param url is the relative url (no hostname)
        @param method is either "GET" or "POST"
        @param data is an optional dictionary of data to be send using JSON
        @result is a dictionary of key-value pairs
        """
        
        headers = { }
        body = ""  
        if data is not None:
            headers = { "content-type": "application/json" }
            body = json.dumps(data)

        try:
            self.conn.request(method, url, body, headers)
        except Exception, e:
            if str(e).find("Connection refused") >= 0:
                print "Cannot connect to the server "+RestTestCase.serverToTest+". You should start the server first, or pass the proper TEST_SERVER environment variable"
                sys.exit(1)
            raise

        self.conn.sock.settimeout(100.0) # Give time to the remote server to start and respond
        resp = self.conn.getresponse()
        #print "RESPONSE:  " + str(resp)
        data_string = "<unknown"
        try:
            if resp.status == 200:
                data_string = resp.read()
                # The response must be a JSON request
                # Note: Python (at least) nicely tacks UTF8 information on this,
                #   we need to tease apart the two pieces.
                self.assertTrue(resp.getheader('content-type') is not None, "content-type header must be present in the response")
                self.assertTrue(resp.getheader('content-type').find('application/json') == 0, "content-type header must be application/json")


                data = json.loads(data_string)
                return data
            else:
                self.assertEquals(200, resp.status)
        except:
            # In case of errors dump the whole response,to simplify debugging
            print "Got exception when processing response to url="+url+" method="+method+" data="+str(data)
            print "  Response status = "+str(resp.status)
            print "  Resonse headers: "
            for h, hv in resp.getheaders():
                print "    "+h+"  =  "+hv
            print "  Data string: "+data_string
            raise

        
    def setUp(self):
        self.conn = httplib.HTTPConnection(RestTestCase.serverToTest, timeout=1)
        testUtils.genUser
        testUtils.genUser
        testUtils.genDriver
        testUtils.genRide
        testUtils.genRide
        #self.makeRequest("/TESTAPI/resetFixture", method="GET")
        
    def tearDown(self):
        self.conn.close ()
    
