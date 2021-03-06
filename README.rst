This project contains configuration files and instructions needed to install and deploy Tilestache_ server

A tilestache server can be used to serve raster or vectorial tiles for google maps style applications.

Requirements and installation
=============================

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
====

The Tileserver is a WSGI application.
Provided a `tiles.cfg` configuration file, it can be run, for debugging purposes, through werkzeug_, by::

    python test.py

The server will answer on port 8083, and you can test it through::

    curl http://localhost:8083/ => "TileStache bellows hello."
    curl http://localhost:8083/cm/2/2/2.png > tile.png => a correct png image


The sample configuration presented in the repository only shows how to set up a proxy
for the a particular Cloudmade.com map style, for which you need an API_KEY.
See the Tilestache_ documentation to check many other possible possibilities.

Extremely fast tiles serving can be obtained through caching_.

.. _Tilestache: http://tilestache.org
.. _werkzeug: http://werkzeug.pocoo.org/


Deploy instructions
===================

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

After every modifications in the `tiles.cfg` configuration, restart with::

    supervisorctl restart uwsgi-emperor


Mapnik note
===========

TileStache can be used to serve mapnik layers, but the mapnik2_ package needs to be installed.

To install mapnik in a virtualenv, under osx, the (unorthodox) procedure described at
http://lab.openpolis.it/using-mapnik-inside-a-virtualenv-on-osx.html can be followed.

.. _mapnik2: https://github.com/mapnik/mapnik/wiki/Mapnik2


Caching strategies
==================

Tilestache allows different caching_ mechanism to speedup the tile-serving process.
Add one of the following ``cache`` sections to the configuration file.

Disk cache
++++++++++

The path is relative to the ``chdir`` specified in ``uwsgi.ini``.

::

   "cache":
     {
       "name": "Disk",
       "path": "cache/",
       "umask": "0000"
     },
     ...


Redis
+++++

Requires redis_ and the `python redis package`_.

::

   "cache": {
      "name": "Redis",
      "host": "localhost",
      "port": 6379,
      "db": 0,
      "key prefix": "tilestache"
    },
    ...


.. _redis:  http://redis.io
.. _python redis package: https://pypi.python.org/pypi/redis


S3 cache
++++++++

Caches tiles to `Amazon S3`_, requires boto_

::

   "cache": {
      "name": "S3",
      "bucket": "<bucket name>",
      "access": "<access key>",
      "secret": "<secret key>",
      "reduced_redundancy": "False"
   },

.. _Amazon S3: http://aws.amazon.com/s3/
.. _boto:  https://github.com/boto/boto


Multi
^^^^^

Multi-tiered caches can be used to mix speed and storage.

::

      "cache": {
        "name": "Multi",
        "tiers": [
            {
               "name": "Redis",
               "host": "localhost",
               "port": 6379,
               "db": 3,
               "key prefix": "tilestache"
            },
            {
               "name": "S3",
               "bucket": "<bucket name>",
               "access": "<access key>",
               "secret": "<secret key>",
               "reduced_redundancy": "False"
            }
        ]
      },


.. _caching:  See http://tilestache.org/doc/#caches


Example
^^^^^^^

An example configuration is contained in ``tiles_example.cfg``. It contains a proxy to a cloudmade layer,
and a small mapnik layer, pointing to an XML file published with Tilemill.

Before running the example, copy ``tiles_sample.cfg`` into ``tiles_example.cfg``, 
and substitute your cloudmade's API_KEY and STYLE_ID.

To run the example on an OSX machine, you need to execute these scripts while in ``tilestache`` virtualenv::

    CONFIG_FILE=tiles_example.cfg; uwsgi --ini uwsgi_dev_osx.ini
    python -m SimpleHTTPServer

Then you can see a map of northern Italy, colored in shades of green, with::

    http://localhost:8000/example.html

