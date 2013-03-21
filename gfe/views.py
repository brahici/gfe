#!/usr/bin/python
#encoding: utf-8
from collections import OrderedDict
import logging

from pyramid.view import view_config

# guess what ...
log = logging.getLogger(__name__)

#for future use
TEXTS = {
    'alpha': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz',
    'fox': 'The quick brown fox jumps over the lazy dog',
    'juge': 'Portez ce vieux whisky au juge blond qui fume',
}

STYLE_TEMPLATE = u"""
<style type="text/css">
    @font-face {{
        font-family: "{name}";
        src: url({css_path});
    }}
    #ff-{css_name} {{
        font-family: "{name}";
    }}
</style>
"""

SAMPLE_TEMPLATE = u"""
<p class="font-sample-container">
    <span class="font-sample" id="ff-{css_name}">{name}</span>
</p>
"""

def fonts_informations(fonts, request):
    """Generates ready to use data for inclusion in a HTML document. Returns
    a dict with two elements:
        - style: CSS declaration for the font (see STYLE_TEMPLATE)
        - sample: a basic sample with the name of the font
        (see SAMPLE_TEMPLATE)
    """
    result = OrderedDict()
    for font in fonts.values():
        font['css_path'] = request.static_url(font['path'])
        result[font['name']] = {
            'style': STYLE_TEMPLATE.format(**font),
            'sample': SAMPLE_TEMPLATE.format(**font),
        }
    return result


class GFEViews(object):
    "Class grouping views of gfe"
    def __init__(self, request):
        "Constructor. Accepts a request as argument."
        self.request = request
        log.debug('%s %s' % (request.client_addr, request.url))

    @view_config(route_name='gfe', renderer='gfe.jinja2')
    def gfe(self):
        "Default dummy view. Returns an empty dict."
        return {}

    @view_config(route_name='search_font', renderer='jsonp',
            request_method='POST')
    def search_font(self):
        """Search fonts according to request params. Returns a dict with two
        elements:
            - fonts: an OrderedDictionary of font data (data generated with
            fonts_informations)
            - count: the number of fonts found
        """
        if self.request.POST.get('_all_fonts') == 'go_for_it' or \
                self.request.params['font_name'] == '*':
            _fonts = self.request.fonts.sorted_fonts()
        else:
            _fonts = self.request.fonts.search(self.request.params['font_name'])
        fonts = fonts_informations(_fonts, self.request)
        return {'fonts': fonts, 'count': len(fonts)}

