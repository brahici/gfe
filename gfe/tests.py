import os
import unittest

from pyramid import testing
from pyramid.request import Request

from .fontsdata import register_fonts
from .views import GFEViews

oprp = os.path.realpath
opeu = os.path.expanduser

FONTS_PATH = oprp(opeu('assets'))
fonts_registry = register_fonts(FONTS_PATH)


class MyDummyRequest(testing.DummyRequest):
    def __init__(self, *args, **kwargs):
        super(MyDummyRequest, self).__init__(*args, **kwargs)
        self.fonts = fonts_registry
        self.application_url = 'http://localhost:6543'


class ViewTests(unittest.TestCase):
    def setUp(self):
        settings = {
            'fonts_path': FONTS_PATH,
            'fonts_url': 'fonts',
        }
        self.config = testing.setUp(settings=settings)
        self.config.add_static_view(settings['fonts_url'],
                settings['fonts_path'])

    def tearDown(self):
        testing.tearDown()

    def test_0001_gfe_view(self):
        request = testing.DummyRequest()
        views = GFEViews(request)
        result = views.gfe()
        self.assertEqual(result, {})

    def test_0002_search_font_view_all(self):
        request = MyDummyRequest(params={'_all_fonts':'go_for_it',})
        views = GFEViews(request)
        result = views.search_font()
        self.assertEqual(result['count'], 2)
        self.assertTrue(result['fonts'].has_key('Audiowide'))
        self.assertTrue(result['fonts'].has_key('Advent Pro Regular'))

    def test_0002_search_font_view_star(self):
        request = MyDummyRequest(params={'font_name':'*',})
        views = GFEViews(request)
        result = views.search_font()
        self.assertEqual(result['count'], 2)
        self.assertTrue(result['fonts'].has_key('Audiowide'))
        self.assertTrue(result['fonts'].has_key('Advent Pro Regular'))

    def test_0003_search_font_view_one_found(self):
        request = MyDummyRequest(params={'font_name':'audio',})
        views = GFEViews(request)
        result = views.search_font()
        self.assertEqual(result['count'], 1)
        self.assertTrue(result['fonts'].has_key('Audiowide'))
        self.assertFalse(result['fonts'].has_key('Advent Pro Regular'))

    def test_0004_search_font_view_none_found(self):
        request = MyDummyRequest(params={'font_name':'python',})
        views = GFEViews(request)
        result = views.search_font()
        self.assertEqual(result['count'], 0)
        self.assertFalse(result['fonts'].has_key('Audiowide'))
        self.assertFalse(result['fonts'].has_key('Advent Pro Regular'))

    def test_0005_check_style_sample(self):
        request = MyDummyRequest(params={'font_name':'advent',})
        views = GFEViews(request)
        result = views.search_font()
        ref_style = u"""
<style type="text/css">
    @font-face {
        font-family: "Advent Pro Regular";
        src: url(http://localhost:6543/fonts/AdventPro-Regular.ttf);
    }
    #ff-advent-pro-regular {
        font-family: "Advent Pro Regular";
    }
</style>
"""
        ref_sample = u"""
<p class="font-sample-container">
    <span class="font-sample" id="ff-advent-pro-regular">Advent Pro Regular</span>
</p>
"""
        self.assertEqual(result['fonts']['Advent Pro Regular']['style'],
                ref_style)
        self.assertEqual(result['fonts']['Advent Pro Regular']['sample'],
                ref_sample)


