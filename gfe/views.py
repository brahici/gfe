#!/usr/bin/python
#encoding: utf-8
from collections import OrderedDict

from pyramid.view import view_config

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
    result = OrderedDict()
    for font in fonts.values():
        font['css_path'] = request.static_url(font['path'])
        result[font['name']] = {
            'style': STYLE_TEMPLATE.format(**font),
            'sample': SAMPLE_TEMPLATE.format(**font),
        }
    return result


class GFEViews(object):
    def __init__(self, request):
        self.request = request

    @view_config(route_name='gfe', renderer='gfe.jinja2')
    def gfe(self):
        return {}

    @view_config(route_name='search_font', renderer='jsonp',
            request_method='POST')
    def search_font(self):
        if self.request.POST.get('_all_fonts') == 'go_for_it' or \
                self.request.params['font_name'] == '*':
            _fonts = self.request.fonts.sorted_fonts()
        else:
            _fonts = self.request.fonts.search(self.request.params['font_name'])
        fonts = fonts_informations(_fonts, self.request)
        return {'fonts': fonts, 'count': len(fonts)}

