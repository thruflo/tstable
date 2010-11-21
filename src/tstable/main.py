#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

# from thruflo.webapp import web

from bootstrap import Bootstrapper

# from urls import mapping
mapping = []

def _as_bool(value, default=False):
    """ Converts value to either `True` or `False`.
      
      Things that are meant to represent true come out `True`::
      
          >>> for value in [
          ...         True, 
          ...         1, 
          ...         '1', 
          ...         'T', 
          ...         'TRUE', 
          ...         'True', 
          ...         'true', 
          ...         'yes',
          ...         'YES',
          ...         'on', 
          ...         'ON', 
          ...         'ok',
          ...         'OK'
          ...     ]:
          ...     _as_bool(value)
          ... 
          True
          True
          True
          True
          True
          True
          True
          True
          True
          True
          True
          True
          True
      
      And things meant to represent false come out `False`::
      
          >>> for value in [
          ...         False, 
          ...         0, 
          ...         '0', 
          ...         'F', 
          ...         'FALSE', 
          ...         'False', 
          ...         'false', 
          ...         'no',
          ...         'NO',
          ...         'off', 
          ...         'OFF'
          ...     ]:
          ...     _as_bool(value)
          ... 
          False
          False
          False
          False
          False
          False
          False
          False
          False
          False
          False
      
      Random shit comes out `False` by default::
      
          >>> _as_bool('foo')
          False
      
      Unless a `default` is passed in, which is coerced to a `bool`::
      
          >>> _as_bool('foo', default='fandango')
          True
      
    """
    
    result = bool(default)
    candidate = value
    
    if candidate in [
            True, 
            1, 
            '1', 
            'T', 
            'TRUE', 
            'True', 
            'true', 
            'yes',
            'YES',
            'on', 
            'ON', 
            'ok',
            'OK'
        ]:
        result = True
    
    elif candidate in [
            False, 
            0, 
            '0', 
            'F', 
            'FALSE', 
            'False', 
            'false', 
            'no',
            'NO',
            'off', 
            'OFF'
        ]:
        result = False
    
    return result
    


def _parse_config(global_config, local_config):
    """ Merges a copy of global and local configs into a single dict
      and returns the merged dict::
      
          >>> g = {'debug': True}
          >>> l = {'shell': False}
          >>> _parse_config(g, l)
          {'debug': True, 'shell': False}
      
      Ensures there's a boolean value for 'debug' and 'shell'::
      
          >>> _as_bool = lambda x: False
          >>> g = {}
          >>> l = {'foo': 'bar'}
          >>> _parse_config(g, l)
          {'debug': False, 'shell': False, 'foo': 'bar'}
      
      Without changing the original config dicts::
      
          >>> g
          {}
          >>> l
          {'foo': 'bar'}
      
    """
    
    settings = global_config.copy()
    settings.update(local_config)
    settings['debug'] = _as_bool(settings.get('debug', None))
    settings['shell'] = _as_bool(settings.get('shell', None))
    return settings
    


def app_factory(global_config, **local_config):
    """ Use `./bin/paster serve path/to/config.ini to 
      instantiate a WSGI application.
        
      Enter the debug shell using the command line option 
      `shell=true`.  This will start an interpreter with
      the components registry available as `gsm` and the
      parsed config as `settings`.
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
        code.interact(local=locals())
    
    # return wsgi app
    return web.WSGIApplication(mapping, settings=settings)
    

