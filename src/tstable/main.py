#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

# import getpass

import logging
import sys

from zope.component import getGlobalSiteManager, provideAdapter
from zope.component.interfaces import IFactory

# from thruflo.webapp import web

from model import userFactory, UserAuthenticator, SQLiteSQLAlchemySession
from interfaces import ISQLAlchemySession

# from urls import mapping
mapping = []

class WSGIApplicationFactory(object):
    """ n.b.: should adapt a wsgiapp and return it when called
      but for now...
    """
    
    def setup_registrations(self, site_manager):
        site_manager.registerUtility(userFactory, IFactory, 'user')
        provideAdapter(UserAuthenticator)
        if self.settings['mode'] == 'dev':
            session = SQLiteSQLAlchemySession(self.settings['sqlite_path'])
            site_manager.registerUtility(session, ISQLAlchemySession)
        elif self.settings['mode'] == 'test':
            session = SQLiteSQLAlchemySession(self.settings['sqlite_path'])
            site_manager.registerUtility(session, ISQLAlchemySession)
        elif self.settings['mode'] == 'prod':
            raise NotImplementedError
        else:
            raise ValueError
        
    
    def configure_logging(self):
        LOG_LEVEL_1 = self.settings['debug'] and logging.DEBUG or logging.INFO
        LOG_LEVEL_2 = self.settings['debug'] and logging.INFO or logging.WARNING
        
        logging.basicConfig(level=LOG_LEVEL_1)
        logging.getLogger('beaker').setLevel(LOG_LEVEL_2)
        logging.getLogger('gunicorn.arbiter').setLevel(LOG_LEVEL_2)
        
    
    def __init__(self, global_config, local_config):
        s = global_config
        s.update(local_config)
        s['debug'] = bool(s['debug'] == 'true')
        self.settings = s
        
    
    


def app_factory(global_config, **local_config):
    """
    """
    
    site_manager = getGlobalSiteManager()
    
    factory = WSGIApplicationFactory(global_config, local_config)
    factory.configure_logging()
    factory.setup_registrations(site_manager)
    
    if factory.settings['mode'] == 'test':
        sys.argv = [sys.argv[0], '-c', '/env/sandbox/tstable/nose.cfg']
        import nose
        nose.run()
    
    if factory.settings.has_key('shell'):
        import code
        code.interact(local=locals())
    
    return factory()(mapping, settings=factory.settings)
    

