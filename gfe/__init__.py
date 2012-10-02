#!/usr/bin/python
#encoding: utf-8
import os

from pyramid.config import Configurator
from pyramid.renderers import JSONP

from gfe import fontsdata

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    def get_fonts_registry(request):
        return fonts_registry
    settings['fonts_path'] = os.path.realpath(
            os.path.expanduser(settings['fonts_path']))
    fonts_registry = fontsdata.register_fonts(settings['fonts_path'])
    config = Configurator(settings=settings)
    config.set_request_property(get_fonts_registry, 'fonts', reify=True)
    config.include('pyramid_jinja2')
    config.add_jinja2_search_path('gfe:templates')
    config.add_renderer('jsonp', JSONP())
    config.add_static_view(settings['static_url'], 'static',
            cache_max_age=3600)
    config.add_static_view(settings['fonts_url'], settings['fonts_path'])
    config.add_route('gfe', '/')
    config.add_route('search_font', '/search_font')
    config.scan()
    return config.make_wsgi_app()
