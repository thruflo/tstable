#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

import unittest
from mock import Mock

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
        
    
    
    def test_authenticate_invalid_credentials(self):
        with self.assertRaises(ValueError):
            self.authenticator.authenticate()
        with self.assertRaises(ValueError):
            self.authenticator.authenticate(username=u'thruflo')
        with self.assertRaises(ValueError):
            self.authenticator.authenticate(password=u'thruflo')
        
    
    


class TestIntegration(unittest.TestCase):
    
    def setUp(self):
        """
        """
        
        from bootstrap import _bootstrap_integration_test
        gsm = _bootstrap_integration_test()
        
        self.db = gsm.getUtility(ISQLAlchemySession)
        self.user = User(username=u'james', password=u'...')
        self.db.add(self.user)
        #try:
        #    self.db.commit()
        #except IntegrityError, err:
        #    logging.err(err)
        #    self.db.rollback()
        self.authenticator = UserAuthenticator(User, self.db)
        
    
    
    def test_successful_username_password_authenticate(self):
        result = self.authenticator.authenticate(
            username=u'thruflo', 
            password=u'wrong'
        )
        raise Exception('false positive! {}'.format(result.username))
        self.assertTrue(result.username == self.user.username)
        
    
    
    def tearDown(self):
        self.db.delete(self.user)
        
    
    


if __name__ == '__main__':
    unittest.main()
