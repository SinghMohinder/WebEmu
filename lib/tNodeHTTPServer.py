from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
from logging.handlers import RotatingFileHandler
import datetime
import os
import threading
import json

_LOG_FILE = None
# version > 0.9 - Simple simulator
# version > 1.0 - Support for AUTH
# version > 1.1 - Support for MIME
_VERSION = 0.9

class tNodeHTTPRequestHandler(BaseHTTPRequestHandler):
    """ Request Handler for each tNode HTTP server instance, will support GET, POST
        GET: validate headers send 200, 400 etc.
        POST: validate headers, add result items to json and return result - send 200, 400 accordingly


    """
    def __init__(self, request, client_address, server):
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)
        self.server.logH.info("Handle for Request Initialized")
        return

    def setup(self):
        self.server.logH.debug("request received")
        self.server.logH.info("Request arrived @ : {}".format(self.log_date_time_string()))
        return BaseHTTPRequestHandler.setup(self)

    def validateRequest(self):
        """This method will validate request parameters from per instance attributes and return respective HTTP status code"""
        self.server.logH.debug("In validateRequest")
        if self.command == 'GET':
            self.server.logH.debug(" Request Type : {}".format(self.command))
            self.server.logH.info(" Received command : GET ")
            self.server.logH.info(" Request came from : Client - {}, Port - {} ". format(self.client_address[0], self.client_address[1]))
            self.server.logH.info(" Request version - {} ".format(self.request_version))
            self.server.logH.info(" Request Headers:  ")
            self.server.logH.info("  Payload  ")
            headerList = []
            for name, value in self.headers.items():
                self.server.logH.debug(" %15s = %s "%(name, value.rstrip()))
                headerList.append(name)
            if self.protocol_version != 'HTTP/1.1':
                self.protocol_version = 'HTTP/1.1'
            if ('content-type' not in headerList):
                self.server.logH.debug("GET condition NOT met, content-type missing in Request Headers")
                return 400
            elif ('user-agent' not in headerList):
                self.server.logH.debug("GET condition NOT met, user-agent missing in Request Headers")
                return 400
            else:
                self.server.logH.debug("GET condition met")
                return 200
        elif self.command == 'POST':
            self.server.logH.debug(" Request Type : {}".format(self.command))
            self.server.logH.info(" Received command : POST ")
            self.server.logH.info(" Request came from : Client - {}, Port - {} ". format(self.client_address[0], self.client_address[1]))
            self.server.logH.info(" Request version - {} ".format(self.request_version))
            self.server.logH.info(" Request Headers: {} ")
            headerList = []
            for name, value in self.headers.items():
                self.server.logH.debug(" %15s = %s "%(name, value.rstrip()))
                headerList.append(name)
            if self.protocol_version != 'HTTP/1.1':
                self.protocol_version = 'HTTP/1.1'
            if ('content-type' not in headerList):
                self.server.logH.debug("POST condition NOT met, content-type missing in Request Headers")
                return 400
            elif ('user-agent' not in headerList):
                self.server.logH.debug("POST condition NOT met, user-agent missing in Request Headers")
                return 400
            elif ('content-length' not in headerList):
                self.server.logH.debug("POST condition NOT met, content-length missing in Request Headers")
                return 400
            else:
                self.server.logH.debug("POST condition met")
                return 200
        else:
            self.server.logH.critical("command not yet supported")
            return 400

    def prepareResponse(self):
        """This method will prepare the response to each request depending on the command"""
        self.server.logH.debug("In prepareResponse")
        if self.command == 'GET':
            self.send_response(200)
            self.server.logH.debug(" Response: ")
            self.send_header('Connection', 'close')
            self.server.logH.debug(" Connection : 'close' ")
            self.send_header('Cache-Control', 'private')
            self.server.logH.debug(" Cache-Control : 'private' ")
            self.send_header('Age', 4)
            self.server.logH.debug(" Age : '4' ")
            self.end_headers()
            self.wfile.write(' %s ' % ("REQUEST SERVED"))
            self.server.logH.debug(' %s ' % ("REQUEST SERVED"))
            return
        elif self.command == 'POST':
            self.send_response(201)
            self.server.logH.debug(" Response: ")
            self.send_header('Connection', 'close')
            self.server.logH.debug(" Connection : 'close' ")
            self.send_header('Cache-Control', 'private')
            self.server.logH.debug(" Cache-Control : 'private' ")
            self.send_header('Age', 4)
            self.server.logH.debug(" Age : '4' ")
            self.end_headers()
            self.data=json.loads(self.rfile.read(int(self.headers['Content-Length'])))
            self.wfile.write(' %s  %s'%("REQUEST SERVED",self.data))
            self.server.logH.debug(' %s  %s'%("REQUEST SERVED",self.data))
            return
        else:
            return None

    def do_GET(self):
        self.server.logH.debug("IN GET")
        if (str(self.validateRequest()) == '200'):
            self.server.logH.debug("GOT 200")
            self.prepareResponse()
            return
        elif (str(self.validateRequest()) == '400'):
            self.server.logH.debug("GOT 400")
            self.send_error(400, 'INVALID REQUEST')
            self.server.logH.debug(" Response Code: 400 ")
            self.send_header('Connection', 'close')
            self.server.logH.debug(" Connection : 'close' ")
            self.send_header('Cache-Control', 'private')
            self.server.logH.debug(" Cache-Control : 'private' ")
            self.send_header('Age', 4)
            self.server.logH.debug(" Age : '4' ")
            self.end_headers()
            self.wfile.write(' %s ' % ("REQUEST FAILED : STATUS CODE : 400"))
            self.server.logH.debug(' %s ' % ("REQUEST FAILED : STATUS CODE : 400"))
            return
        else:
            self.server.logH.error("Failed to handle GET request")
            self.send_error(400, 'INVALID REQUEST')
            self.end_headers()
            self.wfile.write(' %s ' % ("REQUEST FAILED : STATUS CODE : 400"))
            self.server.logH.debug(' %s ' % ("REQUEST FAILED : STATUS CODE : 400"))
            return

    def do_POST(self):
        if (str(self.validateRequest()) == '200'):
            self.prepareResponse()
            return
        elif (str(self.validateRequest()) == '400'):
            self.server.logH.debug(" Response Code: 400 ")
            self.send_error(400, 'INVALID REQUEST')
            self.send_header('Connection', 'close')
            self.server.logH.debug(" Connection : 'close' ")
            self.send_header('Cache-Control', 'private')
            self.server.logH.debug(" Cache-Control : 'private' ")
            self.send_header('Age', 4)
            self.server.logH.debug(" Age : '4' ")
            self.end_headers()
            self.wfile.write(' %s ' % ("REQUEST FAILED : STATUS CODE : 400"))
            self.server.logH.debug(' %s ' % ("REQUEST FAILED : STATUS CODE : 400"))
            return
        else:
            self.server.logH.error("Failed to handle POST request")
            self.send_error(400, 'INVALID REQUEST')
            self.end_headers()
            self.wfile.write(' %s ' % ("REQUEST FAILED : STATUS CODE : 400"))
            self.server.logH.debug(' %s ' % ("REQUEST FAILED : STATUS CODE : 400"))
            return

    def do_HEAD(self):
        self.server.logH.debug(" Request Type : {}".format(self.command))
        self.send_response(200)
        self.server.logH.debug(" Response: ")
        self.send_header('Connection', 'close')
        self.server.logH.debug(" Connection : 'close' ")
        self.send_header('Cache-Control', 'private')
        self.server.logH.debug(" Cache-Control : 'private' ")
        self.send_header('Age', 4)
        self.server.logH.debug(" Age : '4' ")
        self.end_headers()
        self.wfile.write(' %s ' % ("REQUEST SERVED"))
        self.server.logH.debug(' %s ' % ("REQUEST SERVED"))
        return

    def do_PATCH(self):
        self.server.logH.debug(" Request Type : {}".format(self.command))
        self.send_response(200)
        self.server.logH.debug(" Response: ")
        self.send_header('Connection', 'close')
        self.server.logH.debug(" Connection : 'close' ")
        self.send_header('Cache-Control', 'private')
        self.server.logH.debug(" Cache-Control : 'private' ")
        self.send_header('Age', 4)
        self.server.logH.debug(" Age : '4' ")
        self.end_headers()
        self.data = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
        self.wfile.write(' %s  %s' % ("REQUEST SERVED", self.data))
        self.server.logH.debug(' %s  %s' % ("REQUEST SERVED", self.data))
        return


    def finish(self):
        self.server.logH.debug("request processed")
        self.server.logH.info("Response sent @ : {}".format(self.log_date_time_string()))
        return BaseHTTPRequestHandler.finish(self)


class tNodeHTTPServer(ThreadingMixIn, HTTPServer):

    """Handle requests in a separate thread."""
    def __init__(self, server_address, logH, handler_class=tNodeHTTPRequestHandler):
        self.logH = logH
        HTTPServer.__init__(self, server_address, handler_class)
        self.logH.info("Initialized Server with logH")
        return