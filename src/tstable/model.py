#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""


class User(object):
    """
    """
    
    def __init__(self, first_name=u'Default', last_name=u'User'):
        self.first_name = first_name
        self.last_name = last_name
        
    
    
    @property
    def name(self):
        return u'{0} {1}'.format(self.first_name, self.last_name)
        
    
    
    @classmethod
    def get_foo(self):
        return 'foo'
        
    
    

