
G. fonts explorer
=================

G. fonts explorer, or simply gfe, is a web application to browse fonts. I
use it primarily to explore a local copy of Google web fonts.

It's powered by Pyramid and jQuery.

gfe uses some javascript libraries:

- jQuery for ajax calls and DOM handling (http://jquery.com)
- spin.js for spinner (http://fgnass.github.com/spin.js/)


Licence
-------

gfe is released under BSD licence. See LICENCE.


Installation
------------

I recommand to use a virtual environment with virtualenvwrapper:
http://www.doughellmann.com/projects/virtualenvwrapper/

Install gfe and dependencies::

    $ python setup.py install

gfe relies on FontTools, which can not be installed from PyPI. Download an
archive from http://sourceforge.net/projects/fonttools/ and install with
a regular ``pip install fonttools-2.3.tar.gz``. If you don't use a virtual
environment, you may check whether a FontTools package exists for your OS.
FontTools requires numpy, available at PyPI and in most Linux distributions.

spin.js is shipped with gfe. jQuery is loaded from ajax.googleapis.com.

You can perform unitests::

    $ python setup.py test

Before running, you have to configure (in development.ini and/or production.ini)
the path where the application will look up for the fonts.
In ``[app:main]`` section, set the appropriate path in ``fonts_path``. This can
be an absolute path, or a relative one. By default, ``fonts_path`` is set to
``assets``, where are fonts used for unit tests

If you want to have a bunch of fonts, clone Google web fonts repository (be
patient, more than 2Gb to download)::

    $ hg clone https://code.google.com/p/googlefontdirectory/


Running
-------

Standalone::

    $ pserve production.ini

Standalone with auto restart ::

    $ pserve --reload development.ini

