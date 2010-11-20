#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

import unittest
from mock import Mock

from interfaces import *
from model import *

class TestUser(unittest.TestCase):
    """
    """
    
    def setUp(self):
        self.user = User(
            first_name=u'James', 
            last_name=u'Arthur',
            email=u'thruflo@geemail.com',
            username=u'thruflo',
            password=u'...'
        )
        
    
    
    def test_public_key(self):
        self.assertTrue(self.user.public_key == '2f43b42fd833d1e77420a8dae7419000')
        pwd = self.user.password
        self.user.password = None
        self.assertTrue(self.user.public_key is None)
        self.user.password = pwd
        
    
    


class TestAuthenticate(unittest.TestCase):
    """
    """
    
    def setUp(self):
        self.session = Mock()
        self.query = Mock()
        self.session.query.return_value = self.query
        self.authenticator = UserAuthenticator(User, self.session)
        
    
    
    def test_username_password_authenticate(self):
        self.authenticator.authenticate(
            username=u'thruflo', 
            password=u'...'
        )
        self.session.query.assert_called_with(User)
        self.query.filter_by.assert_called_with(
            username=u'thruflo', 
            password=u'...'
        )
        
    
    
    def test_public_key_authenticate(self):
        self.authenticator.authenticate(
            public_key='2f43b42fd833d1e77420a8dae7419000'
        )
        self.session.query.assert_called_with(User)
        self.query.filter_by.assert_called_with(
            public_key='2f43b42fd833d1e77420a8dae7419000'
        )
        
    
    
    def test_authenticate_invalid_credentials(self):
        with self.assertRaises(ValueError):
            self.authenticator.authenticate()
        with self.assertRaises(ValueError):
            self.authenticator.authenticate(username=u'thruflo')
        with self.assertRaises(ValueError):
            self.authenticator.authenticate(password=u'thruflo')
        
    
    


if __name__ == '__main__':
    unittest.main()

