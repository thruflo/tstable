#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

import unittest
from mock import Mock

from zope.component import getGlobalSiteManager

from bootstrap import setup_integration_test, teardown_integration_test

from interfaces import *
from model import *

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
        
    
    
    def test_authenticate_no_credentials(self):
        """ Must provide some credentials.
        """
        
        self.assertRaises(
            ValueError, 
            self.authenticator.authenticate
        )
        
    
    def test_authenticate_random_credentials(self):
        """ Can't provide random credentials.
        """
        
        self.assertRaises(
            TypeError, 
            self.authenticator.authenticate,
            foo='bar'
        )
        
    
    def test_authenticate_just_username(self):
        """ Can't just provide a username.
        """
        
        self.assertRaises(
            ValueError, 
            self.authenticator.authenticate, 
            username=u'thruflo'
        )
        
    
    def test_authenticate_just_password(self):
        """ Can't just provide a password.
        """
        
        self.assertRaises(
            ValueError, 
            self.authenticator.authenticate, 
            password=u'thruflo'
        )
        
    
    


class TestIntegration(unittest.TestCase):
    """
    """
    
    def setUp(self):
        setup_integration_test()
        gsm = getGlobalSiteManager()
        self.db = gsm.getUtility(ISQLAlchemySession)
        self.user = User(username=u'thruflo', password=u'secret')
        self.db.add(self.user)
        self.authenticator = UserAuthenticator(User, self.db)
        
    
    
    def test_success(self):
        """ Authenticating successfully returns user instance.
        """
        
        result = self.authenticator.authenticate(
            username=u'thruflo', 
            password=u'secret'
        )
        self.assertTrue(result.username == self.user.username)
        
    
    def test_failure(self):
        """ Failing to authenticate returns None.
        """
        
        result = self.authenticator.authenticate(
            username=u'thruflo', 
            password=u'wrong'
        )
        self.assertTrue(result is None)
        
    
    
    def tearDown(self):
        teardown_integration_test()
        
    
    

