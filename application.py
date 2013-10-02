from os import environ
import TileStache

# read config file or URL from environment, defaults to tiles.cfg
config_file = environ.get('CONFIG_FILE', 'tiles.cfg')
application = TileStache.WSGITileServer(config_file)

