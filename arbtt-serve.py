#!/usr/bin/env python3
#
# File: arbtt-serve.py
#
# Created: Monday, December  1 2014 by rejuvyesh <mail@rejuvyesh.com>
# License: GNU GPL 3 <http://www.gnu.org/copyleft/gpl.html>
#

from http.server import HTTPServer, SimpleHTTPRequestHandler
import cgi
import os
import socketserver
import sys


rootdir = os.getcwd()
os.chdir('render')


class CustomHandler(SimpleHTTPRequestHandler):
  """
  Custom http request handler
  """
  def do_GET(self):
    SimpleHTTPRequestHandler.do_GET(self)

  def doPOST(self):
    form = cgi.FieldStorage(
      fp = self.rfile,
      headers = self.headers,
      environ = {'REQUEST_METHOD':'POST', 'CONTENT_TYPE':self.headers['Content-Type']}
    )
    result = 'NOT_UNDERSTOOD'

    if self.path == '/refresh':
      # recompute jsons
      os.chdir(rootdir)
      os.system('./update') # Update the content, takes some time
      os.chdir('render')
      result = 'OK'

    self.send_response(200)
    self.send_header('Content-type','text/html')
    self.end_headers()
    self.wfile.write(result)
      
if __name__ == '__main__':
  if len(sys.argv) > 1:
    port = int(sys.argv[1])
  else:
    port = 9999
  ip = ''
  httpd = socketserver.ThreadingTCPServer((ip, port), CustomHandler)
  print("Serving on http://localhost:{}".format(port))
  httpd.serve_forever()
