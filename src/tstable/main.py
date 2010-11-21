#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

# from thruflo.webapp import web

from bootstrap import Bootstrapper

# from urls import mapping
mapping = []

def _as_bool(data, key, default=False):
    result = bool(default)
    candidate = data.get(key, None)
    if candidate in [True, 1, '1', 'T', 'TRUE', 'True', 'true', 'on', 'ON', 'ok']:
        result = True
    elif candidate in [False, 0, '0', 'F', 'FALSE', 'False', 'false', 'off', 'OFF']:
        result = False
    return result
    


def _parse_config(global_config, local_config):
    settings = global_config.copy()
    settings.update(local_config)
    settings['debug'] = _as_bool(settings, 'debug')
    settings['shell'] = _as_bool(settings, 'shell')
    return settings
    


def app_factory(global_config, **local_config):
    """ Use `./bin/paster serve path/to/config.ini to 
      instantiate a WSGI application.
        
      Enter the debug shell using the command line option 
      `shell=true`.  This will start an interpreter with
      the components registry available as `gsm`.
    """
    
    # parse config
    settings = _parse_config(global_config, local_config)
    
    # bootstrap components
    bootstrapper = Bootstrapper(settings=settings)
    bootstrapper.setup_components()
    
    # if the user has set the shell 
    if settings['shell']:
        # get a handle on the component registry and interact
        from zope.component import getGlobalSiteManager
        gsm = getGlobalSiteManager()
        # interact
        import code
        code.interact(local={'gsm': gsm})
    
    # return wsgi app
    return web.WSGIApplication(mapping, settings=settings)
    

