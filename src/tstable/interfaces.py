#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

from zope.interface.interface import Interface, Attribute, Method

__all__ = [
    'IUserDetails', 'IUserCredentials', 'IUser',
    'IAuthenticator', 'ISQLAlchemySession'
]

class IUserDetails(Interface):
    """
    """
    
    first_name = Attribute(u'First name')
    last_name = Attribute(u'Last name')
    email = Attribute(u'Email address')
    


class IUserCredentials(Interface):
    """
    """
    
    username = Attribute(u'First name')
    password = Attribute(u'Last name')
    public_key = Attribute(u'Public key')
    


class IUser(IUserDetails, IUserCredentials):
    """
    """
    


class IAuthenticator(Interface):
    """
    """
    
    # username=None, password=None, public_key=None
    authenticate = Method(u'Authenticate a user') 
    


class ISQLAlchemySession(Interface):
    """
      
      See `sqlalchemy.orm.session.Session.public_methods`:
          
          'add', 'add_all', 'begin', 'begin_nested', 'close', 'commit', 
          'connection', 'delete', 'execute', 'expire', 'expire_all', 
          'expunge', 'expunge_all', 'flush', 'get_bind', 'is_modified', 
          'merge', 'query', 'refresh', 'rollback', 'scalar'
      
      
    """
    

