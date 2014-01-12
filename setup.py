import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()

requires = [
    'pyramid',
    'SQLAlchemy',
    'transaction',
    'pyramid_tm',
    'pyramid_debugtoolbar',
    'zope.sqlalchemy',
    'waitress',
    ]

setup(name='simple_media_service',
      version='0.0',
      description='simple_media_service',
      long_description=README,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='Elliot Peele',
      author_email='elliot@bentlogic.net',
      url='http://github.com/elliotpeele/simple_media_service',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='simple_media_service',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = simple_media_service:main
      [console_scripts]
      initialize_simple_media_service_db = simple_media_service.scripts.initializedb:main
      add_video_file = simple_media_service.scripts.add_file:main
      add_video_tree = simple_media_service.scripts.add_tree:main
      """,
      )
