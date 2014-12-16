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

GTKDYNAMO_ROOT = os.getcwd()
GTKDYNAMO_GUI  = os.path.join(GTKDYNAMO_ROOT, "gui")



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

    def __init__(self, filename = None):
        # Default values
        self.filename     = None
        self.about_dialog = None
        
        # use GtkBuilder to build our interface from the XML file 

        builder = gtk.Builder()
        builder.add_from_file(os.path.join(GTKDYNAMO_ROOT, 'TextEditor',"TextEditorWindow.glade")) 
        #builder.add_from_string(glade)
            
        # get the widgets which will be referenced in callbacks
        self.window    = builder.get_object("window1")
        self.statusbar = builder.get_object("statusbar1")
        self.text_view = builder.get_object("textview1")
        
        # connect signals
        builder.connect_signals(self)
        
        # set the text view font
        self.text_view.modify_font(pango.FontDescription("monospace 10"))
        #self.text_view.modify_font(pango.weight( 'bold'))
        
        # set the default icon to the GTK "edit" icon
        gtk.window_set_default_icon_name(gtk.STOCK_EDIT)
        
        # setup and initialize our statusbar
        self.statusbar_cid = self.statusbar.get_context_id("Tutorial GTK+ Text Editor")
        #self.reset_default_status()
        
        if filename != None:
            TheFile = os.path.split(filename)
            
            fin = open(filename, "r")
            
            text = fin.read()
            fin.close()
            
            # disable the text view while loading the buffer with the text
            self.text_view.set_sensitive(False)
            buff = self.text_view.get_buffer()
            buff.set_text(text)
            buff.set_modified(False)
            self.text_view.set_sensitive(True)
            
            
            
            self.window.set_title(TheFile[-1])
            # now we can set the current filename since loading was a success
            self.filename = filename

        print filename
        self.main()

        
    def main(self):
        self.window.show()
        gtk.main()
   

glade = '''
<?xml version="1.0" encoding="UTF-8"?>
<interface>
  <requires lib="gtk+" version="2.24"/>
  <!-- interface-naming-policy project-wide -->
  <object class="GtkWindow" id="window1">
    <property name="width_request">500</property>
    <property name="height_request">500</property>
    <property name="can_focus">False</property>
    <child>
      <object class="GtkVBox" id="vbox2">
        <property name="visible">True</property>
        <property name="can_focus">False</property>
        <child>
          <object class="GtkMenuBar" id="menubar1">
            <property name="visible">True</property>
            <property name="can_focus">False</property>
            <child>
              <object class="GtkMenuItem" id="menuitem1">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="label" translatable="yes">_File</property>
                <property name="use_underline">True</property>
                <child type="submenu">
                  <object class="GtkMenu" id="menu1">
                    <property name="visible">True</property>
                    <property name="can_focus">False</property>
                    <child>
                      <object class="GtkImageMenuItem" id="imagemenuitem1">
                        <property name="label">gtk-new</property>
                        <property name="visible">True</property>
                        <property name="can_focus">False</property>
                        <property name="use_underline">True</property>
                        <property name="use_stock">True</property>
                      </object>
                    </child>
                    <child>
                      <object class="GtkImageMenuItem" id="imagemenuitem2">
                        <property name="label">gtk-open</property>
                        <property name="visible">True</property>
                        <property name="can_focus">False</property>
                        <property name="use_underline">True</property>
                        <property name="use_stock">True</property>
                      </object>
                    </child>
                    <child>
                      <object class="GtkImageMenuItem" id="imagemenuitem3">
                        <property name="label">gtk-save</property>
                        <property name="visible">True</property>
                        <property name="can_focus">False</property>
                        <property name="use_underline">True</property>
                        <property name="use_stock">True</property>
                      </object>
                    </child>
                    <child>
                      <object class="GtkImageMenuItem" id="imagemenuitem4">
                        <property name="label">gtk-save-as</property>
                        <property name="visible">True</property>
                        <property name="can_focus">False</property>
                        <property name="use_underline">True</property>
                        <property name="use_stock">True</property>
                      </object>
                    </child>
                    <child>
                      <object class="GtkSeparatorMenuItem" id="separatormenuitem1">
                        <property name="visible">True</property>
                        <property name="can_focus">False</property>
                      </object>
                    </child>
                    <child>
                      <object class="GtkImageMenuItem" id="imagemenuitem5">
                        <property name="label">gtk-quit</property>
                        <property name="visible">True</property>
                        <property name="can_focus">False</property>
                        <property name="use_underline">True</property>
                        <property name="use_stock">True</property>
                      </object>
                    </child>
                  </object>
                </child>
              </object>
            </child>
            <child>
              <object class="GtkMenuItem" id="menuitem2">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="label" translatable="yes">_Edit</property>
                <property name="use_underline">True</property>
                <child type="submenu">
                  <object class="GtkMenu" id="menu2">
                    <property name="visible">True</property>
                    <property name="can_focus">False</property>
                    <child>
                      <object class="GtkImageMenuItem" id="imagemenuitem6">
                        <property name="label">gtk-cut</property>
                        <property name="visible">True</property>
                        <property name="can_focus">False</property>
                        <property name="use_underline">True</property>
                        <property name="use_stock">True</property>
                      </object>
                    </child>
                    <child>
                      <object class="GtkImageMenuItem" id="imagemenuitem7">
                        <property name="label">gtk-copy</property>
                        <property name="visible">True</property>
                        <property name="can_focus">False</property>
                        <property name="use_underline">True</property>
                        <property name="use_stock">True</property>
                      </object>
                    </child>
                    <child>
                      <object class="GtkImageMenuItem" id="imagemenuitem8">
                        <property name="label">gtk-paste</property>
                        <property name="visible">True</property>
                        <property name="can_focus">False</property>
                        <property name="use_underline">True</property>
                        <property name="use_stock">True</property>
                      </object>
                    </child>
                    <child>
                      <object class="GtkImageMenuItem" id="imagemenuitem9">
                        <property name="label">gtk-delete</property>
                        <property name="visible">True</property>
                        <property name="can_focus">False</property>
                        <property name="use_underline">True</property>
                        <property name="use_stock">True</property>
                      </object>
                    </child>
                  </object>
                </child>
              </object>
            </child>
            <child>
              <object class="GtkMenuItem" id="menuitem3">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="label" translatable="yes">_View</property>
                <property name="use_underline">True</property>
              </object>
            </child>
            <child>
              <object class="GtkMenuItem" id="menuitem4">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="label" translatable="yes">_Help</property>
                <property name="use_underline">True</property>
                <child type="submenu">
                  <object class="GtkMenu" id="menu3">
                    <property name="visible">True</property>
                    <property name="can_focus">False</property>
                    <child>
                      <object class="GtkImageMenuItem" id="imagemenuitem10">
                        <property name="label">gtk-about</property>
                        <property name="visible">True</property>
                        <property name="can_focus">False</property>
                        <property name="use_underline">True</property>
                        <property name="use_stock">True</property>
                      </object>
                    </child>
                  </object>
                </child>
              </object>
            </child>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="fill">True</property>
            <property name="position">0</property>
          </packing>
        </child>
        <child>
          <object class="GtkToolbar" id="toolbar1">
            <property name="visible">True</property>
            <property name="can_focus">False</property>
            <child>
              <object class="GtkToolButton" id="toolbutton8">
                <property name="visible">True</property>
                <property name="can_focus">False</property>
                <property name="label" translatable="yes">toolbutton8</property>
                <property name="use_underline">True</property>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="homogeneous">True</property>
              </packing>
            </child>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="fill">True</property>
            <property name="position">1</property>
          </packing>
        </child>
        <child>
          <object class="GtkScrolledWindow" id="scrolledwindow1">
            <property name="visible">True</property>
            <property name="can_focus">True</property>
            <property name="hscrollbar_policy">automatic</property>
            <property name="vscrollbar_policy">automatic</property>
            <child>
              <object class="GtkTextView" id="textview1">
                <property name="visible">True</property>
                <property name="can_focus">True</property>
                <property name="left_margin">10</property>
                <property name="right_margin">10</property>
                <property name="indent">4</property>
              </object>
            </child>
          </object>
          <packing>
            <property name="expand">True</property>
            <property name="fill">True</property>
            <property name="position">2</property>
          </packing>
        </child>
        <child>
          <object class="GtkStatusbar" id="statusbar1">
            <property name="visible">True</property>
            <property name="can_focus">False</property>
            <property name="spacing">2</property>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="fill">True</property>
            <property name="position">3</property>
          </packing>
        </child>
      </object>
    </child>
  </object>
</interface>
'''
   
   
   
    
if __name__ == "__main__":
    editor = GTKDynamoTextEditor('/home/fernando/pDynamoWorkSpace/glucose_Dec_13_2014/2_step_GeometryOptmization/2_step_GeometryOptmization.log')
    #editor.load_file('/home/fernando/pDynamoWorkSpace/glucose_Dec_13_2014/2_step_GeometryOptmization/2_step_GeometryOptmization.log')
    
    #editor.main()
