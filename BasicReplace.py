import os
import re

cSSI = re.compile(r'<!--#include +virtual="(/[^"]*)"[^>]*>')
cphptag = re.compile(r'<\?php.*?\?>', re.DOTALL)
cSrcHref = re.compile(r'(src|href)="(/[^"]*)"')

######################################################################
def GetFile(filename):
    insertStr = ""
    try:
        insertStr = open(filename, 'r').read()
    except IOError:
        print "Cannot read %s!" % filename
    return insertStr

def BasicReplace(droppedfile, WEBROOT):
    global cSSI, cphptag, cSrcHref
    ospathsplit = os.path.split(droppedfile)
    name = os.path.splitext(ospathsplit[1])[0]
    ext = os.path.splitext(ospathsplit[1])[1]
    mainfile = droppedfile;

    if ext == '.shtml':
        pass
    elif ext == '.inc':
        mainfile = "%s\\%s.shtml" % (ospathsplit[0], name)
    else:
        mainfile = ""

    try:
        newFile = open(mainfile, 'r').read()

        newFile = cSSI.sub(lambda match: "{0}".format(GetFile("%s%s" % (WEBROOT, match.group(1)))), newFile)
        newFile = cSrcHref.sub(r'\g<1>="%s\g<2>"' % WEBROOT, newFile)
        newFile = cphptag.sub('', newFile)

        f = open("temp-%s.html" % name, 'w')
        f.write(newFile)
        f.close()

        return "temp-%s.html" % name

    except IOError:
        print "Cannot read %s!" % mainfile

        return None


