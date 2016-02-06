#!/usr/bin/python
# -*- coding: utf-8 -*-

#  IncludeReplace.py
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


import wx
import os
import re
import icon
import BasicReplace
import ConfigParser
import webbrowser

AUTHOR = "Sylvan Mostert"
DEBUG = True
WEBROOT = "C:/Users"
CONFIGFILENAME = "config.cfg"
XPOSN = 0
YPOSN = 50
FILELIMIT = 25
OPENBROWSER = True
FOCUS = 255
NOFOCUS = 100
EXEPATH = os.getcwd()


######################################################################
def readconfig(filename="config.cfg"):
    '''
    Reads variables from configuration file and stores them in global
    variables. This function is calle once at start of program.
    '''
    global WEBROOT, XPOSN, YPOSN, FILELIMIT, OPENBROWSER, FOCUS, NOFOCUS, EXEPATH
    try:
        config = ConfigParser.RawConfigParser(allow_no_value=True)
        config.read(filename)
        WEBROOT = config.get('IncludeReplace', 'path')
        XPOSN = config.getint('IncludeReplace', 'xposn')
        YPOSN = config.getint('IncludeReplace', 'yposn')
        FILELIMIT = config.getint('IncludeReplace', 'filelimit')
        OPENBROWSER = config.getboolean('IncludeReplace', 'openbrowser')
        FOCUS = config.getint('IncludeReplace', 'focus')
        NOFOCUS = config.getint('IncludeReplace', 'nofocus')
        if FOCUS < 0 or FOCUS > 255:
            FOCUS = 255
        if FOCUS < 0 or FOCUS > 255:
            FOCUS = 100

    except Exception as e:
        errorbox("%s" % e)
        if DEBUG: print "%s" % e
        return None

######################################################################
def errorbox(message="No message!"):
    '''
    Simple error box to display message. Creates simple info box. This
    can only be called after app is created.
    '''
    dlg = wx.MessageDialog(None, message, 'Info', wx.OK|wx.ICON_INFORMATION)
    dlg.ShowModal()


######################################################################
class FileDropTarget(wx.FileDropTarget):
    '''
    Handles GUI's file drop target area. When files are dropped here,
    they are passed into BasicReplace module.
    '''

    #--------------------------------------------------------------------#
    def __init__(self, obj):
        wx.FileDropTarget.__init__(self)
        self.obj = obj

    #--------------------------------------------------------------------#
    def OnDropFiles(self, x, y, filenames):
        global WEBROOT

        #print the number of files dropped.
        filenumber = len(filenames)
        self.obj.SetInsertionPointEnd()
        self.obj.WriteText("%d file(s) dropped\n\n" % (filenumber))

        if filenumber > FILELIMIT:
            errorbox("Do not add more than %s files!\nYou can change the FILELIMIT in the \'config.cfg\' file." % confsvr.FILELIMIT)
        else:
            for file in filenames:
                #BasicReplace will interpret all of the Server Side Includes
                openpath = BasicReplace.BasicReplace(file, WEBROOT)
                #print what file was dropped
                self.obj.WriteText("%s\n\n" % file)

                if openpath is not None and OPENBROWSER:
                    webbrowser.open_new(openpath)
                else:
                    self.obj.WriteText("This file cannot be read!\n\n")



######################################################################
class MainPanel(wx.Panel):
    '''Main Panel'''

    #--------------------------------------------------------------------#
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, style=wx.NO_BORDER)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.text = wx.TextCtrl(self, style=wx.TE_MULTILINE)#|wx.TE_NO_VSCROLL)
        self.fdt = FileDropTarget(self.text)
        self.text.SetDropTarget(self.fdt)

        self.dropsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.dropsizer.Add(self.text, proportion=1, flag=wx.EXPAND)
        self.sizer.Add(self.dropsizer, proportion=1, flag=wx.LEFT|wx.RIGHT|wx.EXPAND)

        self.SetSizer(self.sizer)


######################################################################
class MainFrame(wx.Frame):

    #--------------------------------------------------------------------#
    def __init__(self):
        global XPOSN, YPOSN
        displaySize = wx.DisplaySize()
        self.height = (displaySize[1] - 100)
        self.width = 140
        self.x = XPOSN
        self.y = YPOSN

        wx.Frame.__init__(self, parent=None, title="Include Replace", pos=(self.x, self.y), size=(self.width, self.height), style=wx.DEFAULT_FRAME_STYLE|wx.STAY_ON_TOP)
        self.SetMinSize((140, 130))
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        self.SetIcon(icon.icon.GetIcon())


        self.InitMenu()
        self.Show()

        self.panel = MainPanel(self)

        self.panel.text.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
        self.panel.text.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
        self.statusbar = self.CreateStatusBar()


    #--------------------------------------------------------------------#
    def InitMenu(self):
        '''Initialize Menu.'''
        menubar = wx.MenuBar()

        fileMenu = wx.Menu()
        fileMenu_item3 = wx.MenuItem(fileMenu, 502, 'Reset Posn+Size')
        fileMenu.AppendItem(fileMenu_item3)
        self.Bind(wx.EVT_MENU, lambda event: self.OnReset(event), id=502)

        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)

    #--------------------------------------------------------------------#
    def OnSetFocus(self, event):
        INFOCUS = True
        self.SetTransparent(FOCUS)

    #--------------------------------------------------------------------#
    def OnKillFocus(self, event):
        INFOCUS = False
        self.SetTransparent(NOFOCUS)

    #--------------------------------------------------------------------#
    def OnReset(self, event):
        self.SetSize((self.width, self.height))
        self.SetPosition((self.x, self.y))

    #--------------------------------------------------------------------#
    def OnClose(self, event):
        '''
        Removes all temporary files with format 'temp-.*?\.html'
        '''
        for f in os.listdir(EXEPATH):
            if re.search(r'temp-.*?\.html', f):
                os.remove(os.path.join(EXEPATH, f))
        self.Destroy()




######################################################################
if __name__ == "__main__":
    app = wx.App(0)
    try:
        #check if configuration file exists
        if os.path.isfile(CONFIGFILENAME):
            #try to read configuration file
            readconfig(CONFIGFILENAME)

            #check if path in configuration file exists
            if os.path.exists(WEBROOT):
                frame = MainFrame()
                app.MainLoop()
            else:
                raise IOError("Replace path: (\'%s\') does not exist!\nCheck 'path' in the config.cfg file." % WEBROOT)
        else:
            raise IOError("Configuration file \'config.cfg\' does not exist!")

    except Exception as e:
        errorbox("%s" % e)
