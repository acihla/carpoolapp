"""
Unit tests for the server.py module.
This is just a sample. You should have more tests for your model (at least 10)
"""

import unittest
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
        
        self.longString = "asdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdf"

        
    def testAddRoute(self):
        """
        Tests that adding a user works
        """
        self.assertEquals(1, views.handleRouteData(1, "fremont", "san jose", test_date))
    """
    def testAddExists(self):
        #Tests that adding a duplicate user name fails
        self.assertEquals(models.SUCCESS, self.users.addUser("user1", "password"))
        self.assertEquals(models.ERR_USER_EXISTS, self.users.addUser("user1", "password"))

    def testAdd2(self):
        #Tests that adding two users works
        self.assertEquals(models.SUCCESS, self.users.addUser("user1", "password"))
        self.assertEquals(models.SUCCESS, self.users.addUser("user2", "password"))

    def testAddEmptyUsername(self):
        #Tests that adding an user with empty username fails
        self.assertEquals(models.ERR_BAD_USERNAME, self.users.addUser("", "password"))

    def testLongUsername(self):
        #Tests that adding an user with long username fails
        self.assertEquals(models.ERR_BAD_USERNAME, self.users.addUser(self.longString, "password"))

    def testLongPassword(self):
        #Tests that adding an user with long password fails
        self.assertEquals(models.ERR_BAD_PASSWORD, self.users.addUser("user6", self.longString))

    def testBadLogin(self):
        
        self.assertEquals(models.ERR_BAD_CREDENTIALS, self.users.loginUser("user7", "asdf"))

    def testLogin(self):
        
        self.assertEquals(models.SUCCESS, self.users.addUser("user8", "asdf"))
        self.assertEquals(2, self.users.loginUser("user8", "asdf"))

    def testLoginCount(self):
        self.assertEquals(models.SUCCESS, self.users.addUser("user8", "asdf"))
        self.assertEquals(2, self.users.loginUser("user8", "asdf"))
        self.assertEquals(3, self.users.loginUser("user8", "asdf"))
        self.assertEquals(4, self.users.loginUser("user8", "asdf"))


    def testBadLogin2(self):
        
        self.assertEquals(models.ERR_BAD_CREDENTIALS, self.users.loginUser("user8", "wrongpassword"))
    """


# If this file is invoked as a Python script, run the tests in this module
if __name__ == "__main__":
    # Add a verbose argument
    sys.argv = [sys.argv[0]] + ["-v"] + sys.argv[1:]
    unittest.main()