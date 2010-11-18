#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

import unittest

from model import User

class TestUser(unittest.TestCase):
    """
    """
    
    def setUp(self):
        self.user = User(first_name=u'James', last_name=u'Arthur')
        
    
    
    def test_name(self):
        name = self.user.name
        self.assertTrue(name == u'James Arthur')
        
    
    
    def test_get_foo(self):
        foo = User.get_foo()
        self.assertTrue(foo == 'foo')
        
    
    


if __name__ == '__main__':
    unittest.main()

