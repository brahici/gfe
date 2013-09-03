#coding: utf-8
import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()

requires = [
    'pyramid',
    'pyramid_debugtoolbar',
    'pyramid_jinja2',
    'waitress',
    'WebTest',
    #'numpy', # for FontTools !! commented because it refuses to build !!!
    ]

setup(name='gfe',
      version='1.0',
      description='A web application to browse fonts',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        'Programming Language :: Python',
        'Framework :: Pylons',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'License :: OSI Approved :: BSD License',
        ],
      licence='BSD',
      author='Brice Vissière',
      author_email='brahici@gmail.com',
      url='https://github.com/brahici/gfe',
      keywords='web pyramid pylons',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite='gfe',
      entry_points = """\
      [paste.app_factory]
      main = gfe:main
      """,
      )

