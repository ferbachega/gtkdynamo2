#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  mydialog.py
#
#  Copyright 2014 Fernando Bachega <fernando@bachega>
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
#
#
import os
import gtk
import gobject
import sys

#from   PyMOLScripts      import *
from   WindowControl     import *
from   gui.FileChooserWindow import FileChooserWindow


import time

class WorkSpaceDialog():
    
    def on_button_workspace_chooser_clicked (self, button):
        """ Function doc """
        window = self.builder.get_object('dialog1')
        path   = self.FileChooserWindow.GetFolderName(window)
        path   = os.path.join(path, 'pDynamoWorkSpace')
        self.builder.get_object('workspace_entry').set_text(path)
    
    
    def on_button_SelectAWorkspace_clicked (self, button ):
        """ Function doc """
        WorkSpace       = self.builder.get_object('workspace_entry').get_text()
        WorkSpaceDialog = self.builder.get_object('checkbutton_workspace').get_active()
        self.EasyHybridSession.EasyHybridConfig['HideWorkSpaceDialog'] = WorkSpaceDialog
        print WorkSpace
        self.EasyHybridSession.EasyHybridConfig['WorkSpace']           = WorkSpace
        print self.EasyHybridSession.EasyHybridConfig['WorkSpace'][0] 

        
        WorkSpace = WorkSpace.split('/')
        path = '/'
        for i in WorkSpace:
            path = os.path.join(path, i)
            if not os.path.exists (path): 
                os.mkdir (path)

        #path = os.path.join(path, 'EasyHybrid')
        #if not os.path.exists (path): 
        #    os.mkdir (path)

       
        
        print self.EasyHybridSession.EasyHybridConfig
        self.EasyHybridSession.Save_EasyHybrid_ConfigFile()
        
    
    def __init__(self, EasyHybridSession, window_control=None, main_builder=None):
        """ Class initialiser """
        self.builder           = gtk.Builder()
        self.main_builder      = main_builder
        self.EasyHybridSession  = EasyHybridSession
        self.EasyHybrid_ROOT    = EasyHybridSession.EasyHybrid_ROOT
        self.EasyHybrid_GUI     = EasyHybridSession.EasyHybrid_GUI 

        self.builder.add_from_file(
            os.path.join(self.EasyHybrid_GUI,'DialogWorkSpaceDialog', 'WorkSpaceDialog.glade'))
        self.builder.connect_signals(self)
        self.dialog = self.builder.get_object('dialog1')
        
        if not sys.platform.startswith('win'):
            self.HOME = os.environ.get('HOME')
        else:
            self.HOME = os.environ.get('PYMOL_PATH')
        
        
        
        path   = os.path.join(self.HOME, 'pDynamoWorkSpace')
        self.builder.get_object('workspace_entry').set_text(path)
        
        #-----------  FileChooserWindow  -------------#
        self.FileChooserWindow = FileChooserWindow()
        #---------------------------------------------#

        


def main():
    dialog = WorkSpaceDialog()
    dialog.dialog.run()
    dialog.dialog.hide()
if __name__ == '__main__':
    main()
