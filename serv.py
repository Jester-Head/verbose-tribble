from cgitb import html
from http.server import BaseHTTPRequestHandler, HTTPServer
from importlib.resources import path
import time
import http.server
import socketserver


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
           self.path = '/results.html'
        try:
           file_to_open = open(self.path[1:]).read()
           self.send_response(200)
        except:
           file_to_open = "File not found"
           self.send_response(404)
        self.end_headers()
        self.wfile.write(bytes(file_to_open, 'utf-8'))



    def server_connect(hostName,serverPort):      
        webServer = HTTPServer((hostName, serverPort), MyServer)
        print(f'Server started {hostName}{serverPort}')
        try:
            webServer.serve_forever()
        except KeyboardInterrupt:
            webServer.server_close()
            print("Server stopped.")

            
