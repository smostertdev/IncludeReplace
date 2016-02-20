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
import irsicon
import BasicReplace
import confsvr
import ServerReplace
import threading
import webbrowser



######################################################################
class WorkerThread(threading.Thread):

    #--------------------------------------------------------------------#
    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    #--------------------------------------------------------------------#
    def run(self):
        if confsvr.DEBUG: print "Server Running (http://%s:%s/)" % (confsvr.HOSTNAME, confsvr.HOSTPORT)
        self.server = ServerReplace.WebServer()
        self.server.create_webserver()
        self.server.start_webserver()
        confsvr.STATUS = True

    #--------------------------------------------------------------------#
    def abort(self):
        if confsvr.DEBUG: print "Server Stopped"
        if self.server:
            self.server.stop_webserver()
            confsvr.STATUS = False


######################################################################
def getlocalhostpath(file):
    try:
        return "http://localhost:%s/%s" % (confsvr.HOSTPORT, os.path.relpath(file, confsvr.WEBROOT))
    except Exception as e:
        errorbox("%s" % e)
        if confsvr.DEBUG: print "%s" % e
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
        #print the number of files dropped.
        filenumber = len(filenames)
        self.obj.SetInsertionPointEnd()
        self.obj.WriteText("%d file(s) dropped\n\n" % (filenumber))

        if filenumber > confsvr.FILELIMIT:
            errorbox("Do not add more than %s files!\nYou can change the FILELIMIT in the \'config.cfg\' file." % confsvr.FILELIMIT)
        else:
            for file in filenames:

                if confsvr.STATUS:
                    openpath = getlocalhostpath(file)
                else:
                    #BasicReplace will interpret all of the Server Side Includes
                    openpath = BasicReplace.BasicReplace(file, confsvr.WEBROOT)

                #print what file was dropped
                self.obj.WriteText("%s\n\n" % file)

                if not None and confsvr.OPENBROWSER:
                    if confsvr.DEBUG: print openpath
                    if openpath:
                        webbrowser.open_new(openpath)
                    else:
                        self.obj.WriteText("Cannot open!")



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

        self.buttonsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.button = wx.Button(self, id=0, label='Stopped', size=(-1, 40))
        self.button.SetFont(wx.Font(15, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, u'Times'))
        self.button.SetBackgroundColour('red')
        self.button.SetForegroundColour('white')
        self.buttonsizer.Add(self.button, proportion=1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT)
        self.sizer.Add(self.buttonsizer, proportion=0, flag=wx.EXPAND|wx.LEFT|wx.RIGHT)

        self.SetSizer(self.sizer)




######################################################################
class MainFrame(wx.Frame):
    '''Main GUI window'''

    #--------------------------------------------------------------------#
    def __init__(self):
        displaySize = wx.DisplaySize()
        self.height = (displaySize[1] - 100)
        self.width = 140
        self.x = confsvr.XPOSN
        self.y = confsvr.YPOSN

        wx.Frame.__init__(self, parent=None, title="Include Replace Server", pos=(self.x, self.y), size=(self.width, self.height), style=wx.DEFAULT_FRAME_STYLE|wx.STAY_ON_TOP)
        self.SetMinSize((140, 130))
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.SetIcon(irsicon.icon.GetIcon())

        self.InitMenu()
        self.Show()

        self.panel = MainPanel(self)

        self.panel.text.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
        self.panel.text.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
        self.panel.button.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
        self.panel.button.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)

        self.worker = None
        self.panel.button.Bind(wx.EVT_BUTTON, self.OnClick, self.panel.button)

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
        confsvr.INFOCUS = True
        self.SetTransparent(confsvr.FOCUS)

    #--------------------------------------------------------------------#
    def OnKillFocus(self, event):
        confsvr.INFOCUS = False
        self.SetTransparent(confsvr.NOFOCUS)

    #--------------------------------------------------------------------#
    def OnClick(self, event):
        if confsvr.STATUS:
            self.OnStop()
        else:
            self.OnStart()

    #--------------------------------------------------------------------#
    def OnStart(self):
        os.chdir(confsvr.WEBROOT)
        if not self.worker:
            if confsvr.DEBUG: print "CWD: %s" % os.getcwd()
            self.panel.button.SetLabel("Running")
            self.statusbar.SetStatusText("localhost:%s/" % confsvr.HOSTPORT)
            self.panel.button.SetBackgroundColour('green')
            self.panel.button.SetForegroundColour('black')
            self.worker = WorkerThread()
        else:
            print "Localhost already running."

    #--------------------------------------------------------------------#
    def OnStop(self):
        os.chdir(confsvr.EXEPATH)
        if self.worker:
            if confsvr.DEBUG: print "CWD: %s" % os.getcwd()
            self.panel.button.SetLabel("Stopped")
            self.statusbar.SetStatusText("")
            self.panel.button.SetBackgroundColour('red')
            self.panel.button.SetForegroundColour('white')
            if self.worker:
                self.worker.abort()
            self.worker = None

    #--------------------------------------------------------------------#
    def OnReset(self, event):
        self.SetSize((self.width, self.height))
        self.SetPosition((self.x, self.y))

    #--------------------------------------------------------------------#
    def OnClose(self, event):
        '''
        Removes all temporary files with format 'temp-.*?\.html'
        '''
        #TODO: create temp files in a directory format
        try:
            if self.worker:
                self.worker.abort()
            for f in os.listdir(confsvr.EXEPATH):
                if re.search(r'temp-.*?\.html', f):
                    os.remove(os.path.join(confsvr.EXEPATH, f))
            self.Destroy()
        except Exception as e:
            errorbox("OnClose(): %s" % e)




######################################################################
if __name__ == "__main__":
    app = wx.App(0)


    try:
        #try to read configuration file
        try:
            confsvr.EXEPATH = os.getcwd()
            print confsvr.EXEPATH

            if os.path.isfile("%s/config.cfg" % confsvr.EXEPATH):
                confsvr.ReadConfig(confsvr.CONFIGFILENAME)
            else:
                raise IOError("Configuration file \'config.cfg\' does not exist!")

            if confsvr.DEBUG: confsvr.PrintConfig()

        except Exception as e:
            errorbox("Config File: %s" % e)

        #check if path in configuration file exists
        if os.path.exists(confsvr.WEBROOT):
            frame = MainFrame()
            app.MainLoop()
        else:
            raise IOError("Replace path: (\'%s\') does not exist!\nCheck 'path' in the config.cfg file." % confsvr.WEBROOT)


    except Exception as e:
        errorbox("%s" % e)
        if confsvr.DEBUG: print "%s" % e
