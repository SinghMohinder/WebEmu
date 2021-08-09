## **WebEmu**

`Web Service emulator : Spawn multiple instances of HTTP/HTTPS servers for testing/debugging purpose`

### **Description**:

WebEmu is webservice emulator to create multiple instances of HTTP/HTTPS servers will smaller fooprint


### Features:

* Create any number of HTTP/HTTPS servers on one linux machine, just specify range of ports to be used by respective Server(s).

* Specify HTTPS server certificate as required

* Client Header must include 'content-type' & 'user-agent' for all GET requests

* Client Header must include 'content-type', 'user-agent' & 'content-length' for all POST requests

* Each Server instance HTTP or HTTPS is logged separately in 'logs/' folder 

### Requirements:

* All Hermes Driver and HermesNode must be executed with debian/ubuntu linux with python2.7.18
* All development was done with python2.7.18 (core libraries), No external library/modules is required.

### Execution Steps 

    python webEmu.py -m server -p https -i 8081:8083
    run mode of tNode : server  
    Invoking HTTPS server instance(s)
    (8081, 8083)
    Initializing HTTP Server with port : 8081
    Initializing HTTP Server with port : 8082
    Initializing HTTP Server with port : 8083
    Starting server, use <Ctrl-C> to stop
    Starting server, use <Ctrl-C> to stop
    Starting server, use <Ctrl-C> to stop

    192.168.1.98 - - [09/Aug/2021 12:00:10] "GET /admin/v1/report HTTP/1.1" 200 -
    192.168.1.98 - - [09/Aug/2021 12:00:49] "GET /admin/v1/report HTTP/1.1" 200 -
    192.168.1.98 - - [09/Aug/2021 12:00:55] "GET /admin/v1/report HTTP/1.1" 200 -


    $python webEmu.py -m server -p http -i 9001:9010 
    run mode of tNode : server
    Invoking HTTP server instance(s)
    (9001, 9010)
    Initializing HTTP Server with port : 9001
    Initializing HTTP Server with port : 9002
    Initializing HTTP Server with port : 9003
    Initializing HTTP Server with port : 9004
    Initializing HTTP Server with port : 9005
    Initializing HTTP Server with port : 9006
    Initializing HTTP Server with port : 9007
    Initializing HTTP Server with port : 9008
    Initializing HTTP Server with port : 9009
    Initializing HTTP Server with port : 9010
    Starting server, use <Ctrl-C> to stop
    Starting server, use <Ctrl-C> to stop
    Starting server, use <Ctrl-C> to stop
    Starting server, use <Ctrl-C> to stop
    Starting server, use <Ctrl-C> to stop
    Starting server, use <Ctrl-C> to stop
    Starting server, use <Ctrl-C> to stop
    Starting server, use <Ctrl-C> to stop
    Starting server, use <Ctrl-C> to stop
    Starting server, use <Ctrl-C> to stop
    127.0.0.1 - - [09/Aug/2021 17:36:15] code 400, message INVALID REQUEST
    127.0.0.1 - - [09/Aug/2021 17:36:15] "GET /app HTTP/1.1" 400 -

#### Issues and Feedback:
Reach out to 'msingh.resume@gmail.com'


