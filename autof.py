from werkzeug.datastructures import Headers

__author__ = 'guglielmo'
import TileStache
import werkzeug

class CORSMiddleware(object):
    """Add Cross-origin resource sharing headers to every request."""

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):

        def add_cors_headers(status, headers, exc_info=None):
            headers = Headers(headers)
            headers.add("Access-Control-Allow-Origin", "*")
            headers.add("Access-Control-Allow-Methods", "GET")
            return start_response(status, headers.to_list(), exc_info)

        if environ.get("REQUEST_METHOD") == "OPTIONS":
            add_cors_headers("200 Ok", [("Content-Type", "text/plain")])
            return [b'200 Ok']

        return self.app(environ, add_cors_headers)


application = CORSMiddleware(TileStache.WSGITileServer('autof.cfg'))
werkzeug.run_simple('0.0.0.0', 8083, application)
