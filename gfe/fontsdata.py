#!/usr/bin/python
#encoding: utf-8
import os
from collections import OrderedDict

from fontTools import ttLib

opj = os.path.join
opse = os.path.splitext

TT_NAME_ID_COPYRIGHT = 0
TT_NAME_ID_FONT_FAMILY = 1
TT_NAME_ID_FONT_SUBFAMILY = 2
TT_NAME_ID_UNIQUE_ID = 3
TT_NAME_ID_FULL_NAME = 4
TT_NAME_ID_VERSION_STRING = 5
TT_NAME_ID_MANUFACTURER = 8
TT_NAME_ID_DESIGNER = 9
TT_NAME_ID_DESCRIPTION = 10
TT_NAME_ID_VENDOR_URL = 11
TT_NAME_ID_DESIGNER_URL = 12

MAP_TTNAMES_ATTRS = {
    TT_NAME_ID_COPYRIGHT: 'copyright',
    TT_NAME_ID_FONT_FAMILY: 'family',
    TT_NAME_ID_FONT_SUBFAMILY: 'subfamily',
    TT_NAME_ID_UNIQUE_ID: 'unique_id',
    TT_NAME_ID_FULL_NAME: 'name',
    TT_NAME_ID_VERSION_STRING: 'version',
    TT_NAME_ID_MANUFACTURER: 'manufacturer',
    TT_NAME_ID_DESIGNER: 'designer',
    TT_NAME_ID_DESCRIPTION: 'description',
    TT_NAME_ID_VENDOR_URL: 'vendor_url',
    TT_NAME_ID_DESIGNER_URL: 'designer_url',
}


class FontMetadataObject(object):
    def __init__(self, path):
        self.path = path
        self.font_type = path[-3:]
        for attr_name in MAP_TTNAMES_ATTRS.values():
            setattr(self, attr_name, '')
        self._extract_font_data()
        self.css_name = self.name.replace(' ', '-').lower()

    def _extract_font_data(self):
        tt = ttLib.TTFont(self.path)
        for name in tt['name'].names:
            attr_name = MAP_TTNAMES_ATTRS.get(name.nameID)
            if attr_name and not getattr(self, attr_name):
                if '\000' in name.string:
                    value = name.string.decode('utf-16-be')
                else:
                    try:
                        value = name.string.decode('utf-8')
                    except UnicodeDecodeError:
                        value = name.string.decode('latin-1')
                if isinstance(value, unicode):
                    setattr(self, attr_name, value)
                else:
                    setattr(self, attr_name, value.encode('utf-8'))


class FontMetadataDict(dict):
    def __init__(self, path):
        super(FontMetadataDict, self).__init__()
        self['path'] = path
        self['font_type'] = path[-3:]
        for attr_name in MAP_TTNAMES_ATTRS.values():
            self[attr_name] = ''
        self._extract_font_data()
        self['css_name'] = self['name'].replace(' ', '-').lower()

    def _extract_font_data(self):
        tt = ttLib.TTFont(self['path'])
        for name in tt['name'].names:
            attr_name = MAP_TTNAMES_ATTRS.get(name.nameID)
            if attr_name and not self[attr_name]:
                if '\000' in name.string:
                    value = name.string.decode('utf-16-be')
                else:
                    try:
                        value = name.string.decode('utf-8')
                    except UnicodeDecodeError:
                        value = name.string.decode('latin-1')
                if isinstance(value, unicode):
                    self[attr_name] = value
                else:
                    self[attr_name] = value.encode('utf-8')

    def __getattribute__(self, attr):
        try:
            return super(FontMetadataDict, self).__getattribute__(attr)
        except AttributeError:
            return self[attr]


class FontsRegistry(dict):
    def __init__(self, *args, **kwargs):
        try:
            font_priority = kwargs.pop('font_priority')
            assert font_priority in ('ttf', 'otf')
        except KeyError:
            font_priority = 'ttf'
        super(FontsRegistry, self).__init__(*args, **kwargs)
        self.font_priority = font_priority

    def update_fonts(self, fonts, font_priority='ttf'):
        for font in fonts:
            add_font = True
            if self.has_key(font.name):
                _font = self.get(font.name)
                add_font = not(_font.font_type == self.font_priority)
            if add_font:
                self[font.name] = font

    def sorted_fonts(self, reverse=False):
        if reverse:
            result = OrderedDict(reversed(sorted(self.items())))
        else:
            result = OrderedDict(sorted(self.items()))
        return result

    def search(self, crit_name):
        result = OrderedDict()
        for name, metadata in self.sorted_fonts().items():
            crit_name = crit_name.lower()
            test_name = name.lower()
            if crit_name in test_name:
                result[name] = metadata
        return result


def register_fonts(path, priority='ttf', meta=FontMetadataDict):
    registry = FontsRegistry(font_priority=priority)
    wlk = os.walk(path)
    file_extensions = ('.ttf', '.otf')
    while True:
        try:
            curdir, dirs, files = wlk.next()
        except StopIteration:
            break
        fonts_files = [opj(curdir, _f) for _f in files \
                if opse(_f)[-1] in file_extensions]
        fonts = [meta(font_file) for font_file in fonts_files]
        registry.update_fonts(fonts)
    return registry

