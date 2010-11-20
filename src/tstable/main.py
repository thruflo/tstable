#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

import code
import getpass

import logging
import sys

from zope.component import getGlobalSiteManager, provideAdapter
from zope.component.interfaces import IFactory

# from thruflo.webapp import web

from model import userFactory, UserAuthenticator, SQLiteSQLAlchemySession
from interfaces import ISQLAlchemySession

# from urls import mapping
mapping = []

def app_factory(global_config, **local_conf):
    """
    """
    
    # Config
    
    settings = global_config
    settings.update(local_conf)
    settings['debug'] = bool(settings['debug'] == 'true')
    
    # Logging
    
    LOG_LEVEL_1 = settings['debug'] and logging.DEBUG or logging.INFO
    LOG_LEVEL_2 = settings['debug'] and logging.INFO or logging.WARNING
    
    logging.basicConfig(level=LOG_LEVEL_1)
    logging.getLogger('beaker').setLevel(LOG_LEVEL_2)
    logging.getLogger('gunicorn.arbiter').setLevel(LOG_LEVEL_2)
    
    # Registrations
    
    gsm = getGlobalSiteManager()
    session = SQLiteSQLAlchemySession(settings['sqlite_path'])
    gsm.registerUtility(session, ISQLAlchemySession)
    gsm.registerUtility(userFactory, IFactory, 'user')
    provideAdapter(UserAuthenticator)
    
    # Go ...
    
    # if settings.has_key('shell'):
    code.interact(local=locals())
    
    # return web.WSGIApplication(mapping, settings=settings)
    

