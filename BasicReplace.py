#  BasicReplace.py
#
#  Copyright 2015 Sylvan Mostert <smostert.dev@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#


import os
import re

# Regular Expressions to replace in files
cSSI     = re.compile(r'<!--#include +virtual="(/[^"]*)"[^>]*>')
cphptag  = re.compile(r'<\?php.*?\?>', re.DOTALL)
cSrcHref = re.compile(r'(src|href)="(/[^"]*)"')


######################################################################
#
#  name: unknown
#  @param filename      Receives a string that represents a file to open
#  @return              Returns the file as a string
#
def getFile(filename):
    insertStr = ""
    try:
        insertStr = open(filename, 'r').read()
    except IOError:
        print "Cannot read %s!" % filename
    return insertStr


def BasicReplace(droppedfile, WEBROOT):
    global cSSI, cphptag, cSrcHref

    ospathsplit = os.path.split(droppedfile)
    name        = os.path.splitext(ospathsplit[1])[0]
    ext         = os.path.splitext(ospathsplit[1])[1]
    mainfile    = droppedfile;

    if ext == '.shtml':
        pass
    elif ext == '.inc':
        mainfile = "%s\\%s.shtml" % (ospathsplit[0], name)
    else:
        mainfile = ""

    try:
        newFile = open(mainfile, 'r').read()

        newFile = cSSI.sub(lambda match: "{0}".format(getFile("%s%s" % (WEBROOT, match.group(1)))), newFile)
        newFile = cSrcHref.sub(r'\g<1>="%s\g<2>"' % WEBROOT, newFile)
        newFile = cphptag.sub('', newFile)

        f = open("temp-%s.html" % name, 'w')
        f.write(newFile)
        f.close()

        return "temp-%s.html" % name

    except IOError:
        print "Cannot read %s!" % mainfile

        return None


