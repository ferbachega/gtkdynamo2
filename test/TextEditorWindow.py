#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  TextEditorWindow.py
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


import sys
import os
import gtk
import pango

class GTKDynamoTextEditor:
    
    def load_file(self, filename):
        # add Loading message to status bar and ensure GUI is current
        self.statusbar.push(self.statusbar_cid, "Loading %s" % filename)
        while gtk.events_pending(): gtk.main_iteration()
        
        try:
            # get the file contents
            fin = open(filename, "r")
            text = fin.read()
            fin.close()
            
            # disable the text view while loading the buffer with the text
            self.text_view.set_sensitive(False)
            buff = self.text_view.get_buffer()
            buff.set_text(text)
            buff.set_modified(False)
            self.text_view.set_sensitive(True)
            
            # now we can set the current filename since loading was a success
            self.filename = filename
            
        except:
            # error loading file, show message to user
            self.error_message ("Could not open file: %s" % filename)
            
        # clear loading status and restore default 
        self.statusbar.pop(self.statusbar_cid)
        #self.reset_default_status()

    def __init__(self):
        # Default values
        self.filename     = None
        self.about_dialog = None
        
        # use GtkBuilder to build our interface from the XML file 

        builder = gtk.Builder()
        builder.add_from_file(" /home/fernando/Documents/gtkdynamo2/TextEditor/TextEditorWindow.glade") 
        #builder.add_from_file("TextEditorWindow.glade") 

            
        # get the widgets which will be referenced in callbacks
        self.window    = builder.get_object("window1")
        self.statusbar = builder.get_object("statusbar1")
        self.text_view = builder.get_object("textview1")
        
        # connect signals
        builder.connect_signals(self)
        
        # set the text view font
        self.text_view.modify_font(pango.FontDescription("monospace 10"))
        
        # set the default icon to the GTK "edit" icon
        gtk.window_set_default_icon_name(gtk.STOCK_EDIT)
        
        # setup and initialize our statusbar
        self.statusbar_cid = self.statusbar.get_context_id("Tutorial GTK+ Text Editor")
        #self.reset_default_status()
    
    def main(self):
        self.window.show()
        gtk.main()
    
if __name__ == "__main__":
    editor = GTKDynamoTextEditor()
    editor.load_file('/home/fernando/pDynamoWorkSpace/glucose_Dec_13_2014/2_step_GeometryOptmization/2_step_GeometryOptmization.log')
    
    editor.main()
