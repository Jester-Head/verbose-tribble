from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

RESULTS_FILE = Path(__file__).parent / 'results.html'
NO_RESULTS_PAGE = ('<!DOCTYPE html>\n<html lang="en">\n<head>\n\t<meta charset="UTF-8">\n\t<title>Process '
                   'Display</title>\n</head>\n<body>\n<p>No results yet. Waiting for the next Autoruns scan.</p>\n'
                   '</body>\n</html>')


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        # Only the results page is served, so a request can't read any other file
        if self.path not in ('/', '/results.html'):
            self.send_error(404, 'File not found')
            return
        try:
            page = RESULTS_FILE.read_text(encoding='utf-8')
        except FileNotFoundError:
            page = NO_RESULTS_PAGE
        body = page.encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    @staticmethod
    def server_connect(hostName, serverPort):
        """Runs the web server until Ctrl+C."""
        webServer = HTTPServer((hostName, serverPort), MyServer)
        print(f'Server started at http://{hostName}:{serverPort}')
        try:
            webServer.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            webServer.server_close()
            print('Server stopped.')
