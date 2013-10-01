This is the directory where tilestache is configured and the caches are kept.
Tilestache server can be launched through uwsgi with

    uwsgi --ini ~/Workspace/TileStache/uwsgi.ini

The configuration look for an application.py python wsgi app, 
and the application loads the tiles.cfg layers definition.

The tiles.cfg is loaded from a URL, so that it can dynamically be generated.

The uwsgi is launched standalone, on port 8099, not daeomized, so that 
log can be analyzed (it is supposed to be launched in a dev environment)

You can run this outside a virtualenv, if you want, but you have to install both 
uwsgi and mapnik.

To install uwsgi, use pip install uwsgi, as it wiull download the latest version.

To install mapnik, try sudo port install py26-mapnik (or py27-mapnik), as it usually
should be a smoother pattern than using pip.



