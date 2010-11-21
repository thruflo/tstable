#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

from zope.component import getGlobalSiteManager, provideAdapter
from zope.component.interfaces import IFactory

from model import *
from interfaces import *

DEFAULT_SETTINGS = {}

TEST_SETTINGS = {
    'mode': 'dev', # @@ should be prod when implemented
    'debug': False,
    'sqlite_path': 'sqlite:///:memory:'
}

def _bootstrap_integration_test():
    """
    """
    
    bootstrapper = Bootstrapper(settings=TEST_SETTINGS)
    bootstrapper.setup_components()
    
    gsm = getGlobalSiteManager()
    session = gsm.getUtility(ISQLAlchemySession)
    session.expunge_all()
    
    return gsm
    


class Bootstrapper(object):
    """
    """
    
    _supported_modes = ['prod', 'dev']
    
    def setup_components(self):
        """ Setup component registrations. 
        """
        
        gsm = getGlobalSiteManager()
        
        # content factories
        gsm.registerUtility(userFactory, IFactory, 'user')
        
        # adapters
        provideAdapter(UserAuthenticator)
        
        # utilities
        mode = self.settings['mode']
        modes = self._supported_modes
        if not mode in modes:
            raise ValueError(u'Mode `{}` must be in {}'.format(mode, modes))
        elif mode == 'dev':
            session = SQLiteSQLAlchemySession(self.settings['sqlite_path'])
            gsm.registerUtility(session, ISQLAlchemySession)
        elif mode == 'prod':
            raise NotImplementedError
            
        
    
    
    def __init__(self, settings=DEFAULT_SETTINGS):
        self.settings = settings
        
    
    




