IncludeReplace
==============

About
-----

`IncludeReplace` is a simple python application that will take [Server Side Includes](https://httpd.apache.org/docs/2.4/howto/ssi.html) (SSI) and replace them inline with the file they are directing to.


<img src="https://raw.githubusercontent.com/smostertdev/IncludeReplace/master/docs/IncludeReplace-img1.png" width="250" alt="Include Replace Screenshot" title="Include Replace Screenshot">


The GUI will allow drag-and-dropping files into the window, and it will open the corresponding file, with the SSI replaced, into the default web browser. It will remain the top window, but will become transparent when focus is lost.

Usage
-----

To use this program you must have `config.cfg` file in the root directory of the program. Change the `path` attribute to the URI of your local site. See the given config file as a template.

Run the program, and drag-and-drop the page you would like to see into the window.

Note: As of right now, this program will only change `<!--#include +virtual="(/[^"]*)"[^>]*>` directives, and change url and src attributes.


Requirements
------------

This program should be able to run on operating systems with:

* Python 2.7
* wxPython
* py2exe - you can use this (along with `setup.py`) to bundle a standalone executable for windows.


Tested on Windows and Linux (Fedora, Ubuntu).


Improvements / Bugs / Suggestions
---------------------------------

If you would like to see any improvements to this, feel free to email me or open an issue/pull request on github.

