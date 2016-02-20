import ConfigParser

AUTHOR = "Sylvan Mostert"
DEBUG = True
WEBROOT = "C:/Users"
EXEPATH = ""
XPOSN = 0
YPOSN = 50
STATUS = False
INFOCUS = True
FOCUS = 255
NOFOCUS = 100
CONFIGFILENAME = "config.cfg"
HOSTNAME = "localhost"
HOSTPORT = 8000


######################################################################
def ReadConfig(filename="config.cfg"):
    '''
    Reads variables from configuration file and stores them in global
    variables. This function is calle once at start of program.
    '''
    global WEBROOT, XPOSN, YPOSN, FILELIMIT, OPENBROWSER, FOCUS, NOFOCUS, HOSTPORT, EXEPATH

    config = ConfigParser.RawConfigParser(allow_no_value=True)
    config.read(filename)
    WEBROOT = config.get('IncludeReplace', 'path')
    XPOSN = config.getint('IncludeReplace', 'xposn')
    YPOSN = config.getint('IncludeReplace', 'yposn')
    FILELIMIT = config.getint('IncludeReplace', 'filelimit')
    OPENBROWSER = config.getboolean('IncludeReplace', 'openbrowser')
    HOSTPORT = config.getint('IncludeReplace', 'hostport')
    FOCUS = config.getint('IncludeReplace', 'focus')
    NOFOCUS = config.getint('IncludeReplace', 'nofocus')
    if FOCUS < 0 or FOCUS > 255:
        FOCUS = 255
    if FOCUS < 0 or FOCUS > 255:
        FOCUS = 100


######################################################################
def PrintConfig():
    global AUTHOR, DEBUG, WEBROOT, EXEPATH, XPOSN, YPOSN, FOCUS, NOFOCUS, HOSTNAME, HOSTPORT
    print "*********************"
    print "AUTHOR:       %s" % AUTHOR
    print "DEBUG:        %s" % DEBUG
    print "WEBROOT:      %s" % WEBROOT
    print "EXEPATH:      %s" % EXEPATH
    print "XPOSN:        %s" % XPOSN
    print "YPOSN:        %s" % YPOSN
    print "FOCUS:        %s" % FOCUS
    print "NOFOCUS:      %s" % NOFOCUS
    print "HOST:         %s:%s" % (HOSTNAME, HOSTPORT)
    print "*********************"
