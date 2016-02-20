"""Simple HTTP Server.

This module builds on BaseHTTPServer by implementing the standard GET
and HEAD requests in a fairly straightforward manner.

"""


__version__ = "0.6"

__all__ = ["SimpleHTTPRequestHandler"]

import os
import re
import posixpath
import BaseHTTPServer
import urllib
import cgi
import shutil
import threading
import StringIO
import confsvr




def get_file(filename):
    addString = ""
    try:
        addString = open(filename, 'r').read()
    except IOError:
        print "IO Error. Cannot read %s!" % filename
    return addString

def convert_htmlstring(htmlstring):
    htmlstring = re.sub(r'<!-- *#include *virtual=[\'"]([^\'"]+)[\'"] *--+>', lambda match: "{}".format(get_file(confsvr.WEBROOT + match.group(1))), htmlstring)
    phptag = re.compile(r'<\?php.*?\?>', re.DOTALL)
    htmlstring = phptag.sub('', htmlstring)
    return htmlstring


class HTTPHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    """Simple HTTP request handler with GET and HEAD commands.

    This serves files from the current directory and any of its
    subdirectories.  It assumes that all files are plain text files
    unless they have the extension ".html" in which case it assumes
    they are HTML files.

    The GET and HEAD requests are identical except that the HEAD
    request omits the actual contents of the file.

    """

    server_version = "SimpleHTTP/" + __version__

    def do_GET(self):
        """Serve a GET request."""
        f = self.send_head()
        f = convert_htmlstring(f)
        self.wfile.write(f)

    def do_HEAD(self):
        """Serve a HEAD request."""
        f = self.send_head()
        f = convert_htmlstring(f)
        self.wfile.write(f)

    def send_head(self):
        """Common code for GET and HEAD commands.

        This sends the response code and MIME headers.

        Return value is either a file object (which has to be copied
        to the outputfile by the caller unless the command was HEAD,
        and must be closed by the caller under all circumstances), or
        None, in which case the caller has nothing further to do.

        """
        path = self.translate_path(self.path)
        f = ""
        if os.path.isdir(path):
            for index in "index.shtml", "index.html", "index.htm":
                index = os.path.join(path, index)
                if os.path.exists(index):
                    path = index
                    break
            else:
                return self.list_directory(path)
        ctype = self.get_mime(path)
        if ctype.startswith('text/'):
            mode = 'r'
        else:
            mode = 'rb'
        try:
            f = open(path, mode).read()
        except IOError:
            self.send_error(404, "File not found")
        self.send_response(200)
        self.send_header("Content-type", ctype)
        self.end_headers()
        return f

    def list_directory(self, path):
        """Helper to produce a directory listing (absent index.html).

        Return value is either a file object, or None (indicating an
        error).  In either case, the headers are sent, making the
        interface the same as for send_head().

        """
        try:
            list = os.listdir(path)
        except os.error:
            self.send_error(404, "No permission to list directory")
            return None
        list.sort(lambda a, b: cmp(a.lower(), b.lower()))
        f = ""
        f = "%s<title>Directory listing for %s</title>\n" % (f, self.path)
        f = "%s<h2>Directory listing for %s</h2>\n" % (f, self.path)
        f = "%s<hr>\n<ul>\n" % f
        for name in list:
            fullname = os.path.join(path, name)
            displayname = linkname = name = cgi.escape(name)
            # Append / for directories or @ for symbolic links
            if os.path.isdir(fullname):
                displayname = "%s/" % name
                linkname = "%s/" % name
            if os.path.islink(fullname):
                displayname = "%s@" % name
                # Note: a link to a directory displays with @ and links with /
            f = '%s<li><a href="%s">%s</a>\n' % (f, linkname, displayname)
        f = "%s</ul>\n<hr>\n" % f
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        return f

    def translate_path(self, path):
        """Translate a /-separated PATH to the local filename syntax.

        Components that mean special things to the local file system
        (e.g. drive or directory names) are ignored.  (XXX They should
        probably be diagnosed.)

        """
        path = posixpath.normpath(urllib.unquote(path))
        words = path.split('/')
        words = filter(None, words)
        path = os.getcwd()
        for word in words:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word in (os.curdir, os.pardir): continue
            path = os.path.join(path, word)
        return path


    def get_mime(self, path):
        if path.endswith(".html"):
            return 'text/html'
        elif path.endswith(".shtml"):
            return 'text/html'
        elif path.endswith(".inc"):
            return 'text/html'
        elif path.endswith(".png"):
            return 'image/png'
        elif path.endswith(".jpg"):
            return 'image/jpeg'
        elif path.endswith(".jpeg"):
            return 'image/jpeg'
        elif path.endswith(".gif"):
            return 'image/gif'
        elif path.endswith(".js"):
            return 'application/javascript'
        elif path.endswith(".css"):
            return 'text/css'
        elif path.endswith(".pdf"):
            return 'application/pdf'
        else:
            return 'text/html'

    def log_message(self, format, *args):
        return




class WebServer(object):
    def create_webserver(self):
        self.server = BaseHTTPServer.HTTPServer((confsvr.HOSTNAME, confsvr.HOSTPORT), HTTPHandler)
    def start_webserver(self):
        self._webserver_died = threading.Event()
        self._webserver_thread = threading.Thread(target=self._run_webserver_thread)
        self._webserver_thread.start()

    def _run_webserver_thread(self):
        self.server.serve_forever()
        self._webserver_died.set()

    def stop_webserver(self):
        if not self._webserver_thread:
            return
        else:
            self.server.shutdown()
            if not self._webserver_died.wait(5):
                raise ValueError("Webserver unable to shutdown.")

