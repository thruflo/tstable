#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

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
    """
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
        elif not self.hasattr('_public_key'):
            self._public_key = hashlib.md5(self.password)
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
        
    
    
    @classmethod
    def authenticate(self, username=None, password=None, public_key=None):
        if username is not None and password is not None:
            params = dict(username=username, password=password)
        elif public_key is not None:
            params = dict(public_key=public_key)
        else:
            raise ValueError(u'Provide `username` & `password` or `public_key`')
        query = self.session.query(self.context)
        query.filter_by(**params)
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
        
    
    

