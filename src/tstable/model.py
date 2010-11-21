#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

__all__ = [
    'User', 'userFactory', 'UserAuthenticator', 
    'SQLiteSQLAlchemySession'
]

import hashlib

from zope.interface import implements
from zope.component import adapts
from zope.component.factory import Factory

from sqlalchemy import create_engine, desc, func
from sqlalchemy import Table, Column, MetaData, ForeignKey
from sqlalchemy import Boolean, Date, Integer, PickleType, Unicode, UnicodeText
from sqlalchemy.orm import relation, synonym
from sqlalchemy.orm.session import Session

from sqlalchemy.ext.declarative import declarative_base
SQLModel = declarative_base()

from interfaces import *

class User(SQLModel):
    """ A user.  Can be instantiated with property values
      as keyword arguments::
      
          >>> user = User(first_name=u'James')
          >>> user.first_name
          u'James'
      
      Public key is derived from password.  Specifically, it's `None`
      if the password is `None`::
      
          >>> user.password = None
          >>> user.public_key
      
      And a `sha1` hash of the `password`::
          
          >>> user = User(password=u'...')
          >>> user.public_key
          '6eae3a5b062c6d0d79f070c26e6d62486b40cb46'
      
      As long as password is a `basestring`::
      
          >>> user.password = 0
          >>> user.public_key #doctest: +NORMALIZE_WHITESPACE
          Traceback (most recent call last):
          ...
          ValueError: password must be a basestring
          
      
    """
    
    implements(IUser)
    
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, nullable=False)
    
    first_name = Column(Unicode)
    last_name = Column(Unicode)
    email = Column(Unicode, unique=True)
    
    username = Column(Unicode, unique=True)
    password = Column(Unicode)
    
    @property
    def public_key(self):
        if self.password is None:
            return None
        elif not isinstance(self.password, basestring):
            raise ValueError('password must be a basestring')
        elif not hasattr(self, '_public_key'):
            self._public_key = hashlib.sha1(self.password).hexdigest()
        return self._public_key
        
    
    
    def __init__(
            self, 
            first_name=None, 
            last_name=None,
            email=None,
            username=None,
            password=None
        ):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        
        self.username = username
        self.password = password
        
    
    

userFactory = Factory(User, 'User')

class UserAuthenticator(object):
    """
    """
    
    adapts(IUserCredentials, ISQLAlchemySession)
    implements(IAuthenticator)
    
    def __init__(self, context, session):
        self.context = context
        self.session = session
        
    
    
    def authenticate(self, username=None, password=None, public_key=None):
        query = self.session.query(self.context)
        if username is not None and password is not None:
            query.filter_by(username=username, password=password)
        elif public_key is not None:
            query.filter_by(public_key=public_key)
        else:
            raise ValueError(u'Provide `username` & `password` or `public_key`')
        return query.first()
        
    
    


class SQLAlchemySession(Session):
    """
    """
    
    implements(ISQLAlchemySession)
    

class SQLiteSQLAlchemySession(SQLAlchemySession):
    
    def __init__(self, sqlite_path, **kwargs):
        """
        """
        
        kwargs['bind'] = engine = create_engine(sqlite_path, echo=False)
        SQLModel.metadata.create_all(engine)
        super(SQLiteSQLAlchemySession, self).__init__(**kwargs)
        
    
    

