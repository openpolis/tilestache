__author__ = 'guglielmo'
import TileStache
import werkzeug
application = TileStache.WSGITileServer('tiles.cfg')
werkzeug.run_simple('0.0.0.0', 8083, application)
