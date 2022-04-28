from http.server import BaseHTTPRequestHandler, HTTPServer
import time

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>https:test.com</title></head>", "utf-8"))
        # self.wfile.write(bytes("<p>Request: {self.path}</p>","utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(bytes("<p>Hello World!</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))

    def server_connect(hostName,serverPort):      
        webServer = HTTPServer((hostName, serverPort), MyServer)
        print(f'Server started {hostName}{serverPort}')

        try:
            webServer.serve_forever()
        except KeyboardInterrupt:
            pass

        webServer.server_close()
        print("Server stopped.")