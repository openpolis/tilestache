This project contains configuration files and instructions needed to install and deploy Tilestache_ server

A tilestache server can be used to serve raster or vectorial tiles for google maps style applications.

Requirements and Tilestache installation
----------------------------------------

The Tilestache python package need to be installed within a virtualenv_. It requires some image-processing,
so some libraries need to be installed as OS packages, to handle jpeg, png and other image types.

As for a Ubuntu 12.04 linux distribution::

    apt-get install build_essentials python_devel libpng12_dev libjpeg62_dev zlib1g_dev
    ln -s /usr/lib`uname -i`-linux-gnu/libpng.so /usr/lib
    ln -s /usr/lib`uname -i`-linux-gnu/libjpeg.so /usr/lib
    ln -s /usr/lib`uname -i`-linux-gnu/libfreetype.so /usr/lib
    ln -s /usr/lib`uname -i`-linux-gnu/libz.so /usr/lib
    apt-get install python-pip
    pip install virtualenv virtualenvwrapper

The libraries need to be linked in the `/usr/lib` path in order to correctly compile PIL_, which is a required package.

Setup the virtualenvwrapper environment variables within ``.bashrc``::

    cat bashrc >> ~/.bashrc

Generate the virtualenv::

    mkvirtualenv tilestache
    git clone git@github.com:openpolis/tilestache.git
    cd tilestache
    setvirtualenvproject

Install the Tilestache_ python package::

    workon tilestache
    pip install Tilestache

.. _PIL: http://www.pythonware.com/products/pil/
.. _virtualenv: https://pypi.python.org/pypi/virtualenv

Test
----

The Tileserver is a WSGI application.
Provided a `tiles.cfg` configuration file, it can be run, for debugging purposes, through werkzeug_, by::

    python test.py

The server will answer on port 8083, and you can test it through::

    curl http://localhost:8083/ => "TileStache bellows hello."
    curl http://localhost:8083/cm/2/2/2.png > tile.png => a correct png image


The sample configuration presented in the repository only shows how to set up a proxy
for the a particular Cloudmade.com map style, for which you need an API_KEY.
See the Tilestache_ documentation to check many other possible possibilities.

Extremely fast tiles serving can be obtained through redis_ based caching.

.. _Tilestache: http://tilestache.org
.. _werkzeug: http://werkzeug.pocoo.org/
.. _redis:  http://redis.io


Deploy Architecture (suggested)
-------------------------------

Your mileage may vary here, but the suggested architecture is:
Nginx_ plus UWSGI_ set in empereor mode, started through Supervisor_

.. _Nginx: http://wiki.nginx.org/Main
.. _UWSGI: http://uwsgi-docs.readthedocs.org/en/latest/
.. _Supervisor: http://supervisord.org/


Deploy instructions
-------------------

::

    apt-get install nginx-full uwsgi uwsgi-plugin-python supervisor
    ln -s supervisor.conf /etc/supervisor/conf.d/uwsgi-emperor.conf
    /etc/init.d/supervisor restart

    ln -s nginx.conf /etc/nginx/sites-enabled/tilestache
    /etc/init.d/nginx restart

    ln -s uwsgi.ini /etc/uwsgi/vassals/tilestache.ini
    supervisorctl stop uwsgi-emperor
    supervisorctl start uwsgi-emperor


The service configured as above, will look for a configuration file in the ``CONFIG_FILE``
environment variable, cascading to ``tiles.cfg`` by default.
``CONFIG_FILE`` can contain a URL, so that dynamically generated config files are possible
(as is the cas in the OpenCoesione project).

The uwsgi is launched through supervisor and logs the activity of the tilestache server.
The logging level can be specified in the logging section of tiles.cfg.

Mapnik note
-----------

TileStache can be used to serve mapnik layers, but the mapnik2_ package needs to be installed.
Compilations problems are known to exist and detailed instructions for installation within a virtualenv
can not be written at the current time.

.. _mapnik2: https://github.com/mapnik/mapnik/wiki/Mapnik2