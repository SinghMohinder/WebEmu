import argparse
import sys
import multiprocessing
import os
import sys
from lib.tNodeHTTPServer import tNodeHTTPServer, tNodeHTTPRequestHandler
import logging
import ssl
import ConfigParser



# Read Config File for relevant parameters
_CONFIG_FILE = 'config/config'

with open(_CONFIG_FILE) as _WEBEMU_CONFIGH:
    configP = ConfigParser.ConfigParser()
    configP.readfp(_WEBEMU_CONFIGH)

def startHTTPServerProcess(port):
    """start a server process"""
    address = ('', port)
    # Start a logger here and pass this to relevant classes
    _hLogger = logging.getLogger(__name__ + str(port))
    _hLogger.info("Initialing Logger")
    _hLogger.setLevel('DEBUG')
    hLogSH1 = logging.StreamHandler(sys.stdout)
    hLogFmtr = logging.Formatter('%(levelname)s - %(asctime)s.%(msecs)03d - %(module)s - %(name)s - %(funcName)s - %(message)s', datefmt='%d/%m/%Y_%I:%M:%S')
    _hLogFile = configP.get('HTTP', 'LOGS') + '/tNodeHTTPServer_' + str(port) + '.log'
    hLogFH = logging.FileHandler(_hLogFile)
    hLogFH.setFormatter(hLogFmtr)
    _hLogger.addHandler(hLogFH)
    _hLogger.info("started logger for Server")
    server = tNodeHTTPServer(address, _hLogger, tNodeHTTPRequestHandler)
    server.allow_reuse_address = True
    print 'Starting server, use <Ctrl-C> to stop'
    server.serve_forever()
    hLogFH.info("Server listening with %s" % server.server_address)

def startHTTPSServerProcess(port):
    """start a server process"""
    address = ('', port)
    # Start a logger here and pass this to relevant classes
    _hLogger = logging.getLogger(__name__ + str(port))
    _hLogger.info("Initialing Logger")
    _hLogger.setLevel('DEBUG')
    hLogSH1 = logging.StreamHandler(sys.stdout)
    hLogFmtr = logging.Formatter('%(levelname)s - %(asctime)s.%(msecs)03d - %(module)s - %(name)s - %(funcName)s - %(message)s', datefmt='%d/%m/%Y_%I:%M:%S')
    _hLogFile = configP.get('HTTPS', 'LOGS') + '/tNodeHTTPSServer_' + str(port) + '.log'
    hLogFH = logging.FileHandler(_hLogFile)
    hLogFH.setFormatter(hLogFmtr)
    _hLogger.addHandler(hLogFH)
    _hLogger.info("started logger for Server")
    server = tNodeHTTPServer(address, _hLogger, tNodeHTTPRequestHandler)
    server.allow_reuse_address = True
    server.socket = ssl.wrap_socket(server.socket, server_side=True, certfile=configP.get('HTTPS', 'ServerCertFile') , keyfile=configP.get('HTTPS', 'ServerKeyFile'))
    print 'Starting server, use <Ctrl-C> to stop'
    server.serve_forever()
    hLogFH.info("Server listening with %s" % server.server_address)


tNodeParser = argparse.ArgumentParser(usage="Hermes_tNodes:Starter Script", description="Hermes_tNodes:Starter Script",
                                      version=0.9)

tNodeParser.add_argument('-m', action="store", dest="tNodeRunMode", type=str,
                         help='{server|client} -> defines tNode mode of operation')
tNodeParser.add_argument('-p', action="store", dest="tNodeProtocol", type=str,
                         help='{http|https|ssh|ftp|tftp} -> defines protocol for communication')
tNodeParser.add_argument('-i', action="store", dest="tNodePortRange",
                         help='{8080:8090} -> specify range of ports, if -m is server, else one port number if -m is client')
tNodeParser.add_argument('-r', action="store", dest="tNodeReqPerSecond", type=int,
                         help='{10|100|50} -> defines max requests handled per second, if -m is server, else max requests created per second')

tNodeOptions = tNodeParser.parse_args()

if tNodeOptions.tNodeRunMode == 'server':
    print ("run mode of tNode : %s" % tNodeOptions.tNodeRunMode)
    if tNodeOptions.tNodeProtocol == 'http':
        print("Invoking HTTP server instance(s)")
        # parse option -i
        print (int(tNodeOptions.tNodePortRange.split(":")[0]), int(tNodeOptions.tNodePortRange.split(":")[1]))
        pList = []
        for serverInstPort in range(int(tNodeOptions.tNodePortRange.split(":")[0]),
                                    int(tNodeOptions.tNodePortRange.split(":")[1]) + 1):
            print("Initializing HTTP Server with port : %s" % serverInstPort)
            pList.append(multiprocessing.Process(target=startHTTPServerProcess, args=(serverInstPort,)))

        for proc in pList:
            proc.start()

    elif tNodeOptions.tNodeProtocol == 'https':
        print("Invoking HTTPS server instance(s)")
        # parse option -i
        print (int(tNodeOptions.tNodePortRange.split(":")[0]), int(tNodeOptions.tNodePortRange.split(":")[1]))
        pList = []
        for serverInstPort in range(int(tNodeOptions.tNodePortRange.split(":")[0]),
                                    int(tNodeOptions.tNodePortRange.split(":")[1]) + 1):
            print("Initializing HTTP Server with port : %s" % serverInstPort)
            pList.append(multiprocessing.Process(target=startHTTPSServerProcess, args=(serverInstPort,)))

        for proc in pList:
            proc.start()

    elif tNodeOptions.tNodeProtocol == 'ssh':
        print("Invoking SSH server instance(s)")

    elif tNodeOptions.tNodeProtocol == 'ftp':
        print("Invoking FTP server instance(s)")

    elif tNodeOptions.tNodeProtocol == 'tftp':
        print("Invoking TFTP server instance(s)")

    else:
        print ("Incorrect option -p : %s" % tNodeOptions.tNodeRunMode)
        sys.exit(1)

elif tNodeOptions.tNodeRunMode == 'client':
    print ("run mode of tNode : %s" % tNodeOptions.tNodeRunMode)
    print ("mode under development")
    sys.exit(0)
else:
    print ("Incorrect option -m : %s" % tNodeOptions.tNodeRunMode)
    sys.exit(1)