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
import pango

from gui.FileChooserWindow                                   import *           

#from pymol import cmd
#from PyMOLScripts import *
#from WindowControl import *
#GTKDYNAMO_ROOT   = os.environ.get('GTKDYNAMO_ROOT')
#GTKDYNAMO_ROOT   = '/home/fernando/Dropbox/GTKPyMOL'
#GTKDYNAMO_ROOT   = '/home/labio/Dropbox/GTKPyMOL'
#GTKDYNAMO_ROOT = os.getcwd()
GTKDYNAMO_ROOT = os.environ.get('GTKDYNAMO_ROOT')

GTKDYNAMO_GUI = os.path.join(GTKDYNAMO_ROOT, "gui")
from pprint import pprint


'''

Adicionar um textbox que pertimte o usuario adicionar comentarios
comentarios serao salvos no history dos processos

'''

class WHAMEquationSolverDialog():

    
    def on_treeview_PyMOL_Objects_button_release_event(self, tree, event):
        
        pass
        #if event.button == 3:
        #    selection     = tree.get_selection()
        #    model         = tree.get_model()
        #    (model, iter) = selection.get_selected()
        #    if iter != None:
        #        print 'open MEnu'
        #
        #if event.button == 2:
        #    selection     = tree.get_selection()
        #    model         = tree.get_model()
        #    (model, iter) = selection.get_selected()
        #    pymol_object  = model.get_value(iter, 0) 
        #    
        #
        #   
        #if event.button == 1:
        #    selection     = tree.get_selection()
        #    model         = tree.get_model()
        #    (model, iter) = selection.get_selected()
        #    
        #    if iter != None:
        #        true_or_false = model.get_value(iter, 0)
        #        if true_or_false == False:
        #            true_or_false = True
        #            model.set(iter, 0, true_or_false)
        #            print 'event.button == 1'
        #        
        #        else:
        #            true_or_false = False
        #            model.set(iter, 0, true_or_false)
        #            print 'event.button == 1'
        #

        
    def  on_cellrenderertoggle1_toggled(self, cell, path):
        """ Function doc """
        print 'on_treeview_select_cursor_parent'
        model = self.builder.get_object('liststore1')
        iter = model.get_iter(path)  # @+
        true_or_false     = model.get_value(iter, 0)
        trajectory_block  = model.get_value(iter, 1)
        
        #print trajectory_block
        #self.FileNames[trajectory_block] = 
        
        if true_or_false == False:
            true_or_false = True
            model.set(iter, 0, true_or_false)
            
    
        else:
            true_or_false = False
            model.set(iter, 0, true_or_false)
    
        self.FileNames[trajectory_block] = true_or_false
        pprint (self.FileNames)


    def add_files_to_the_treeview (self, button):
        """ Function doc """
        FileChooser = FileChooserWindow()
        FileNames = FileChooser.GetFolderName(self.dialog, multiple = True)
        #print FileNames
        
        for File in FileNames:
            self.FileNames[File] = True
        
        pprint (self.FileNames)
        
        liststore = self.builder.get_object('liststore1')
        #
        self.WHAM_TREEVIEW_ADD_DATA (liststore = liststore, trajectory_blocks=self.FileNames)
    
    
    
    
    
    
    
    def WHAM_TREEVIEW_ADD_DATA(self, liststore=None, trajectory_blocks = {}):
        """ Function doc """

        model = liststore  
        model.clear()
        n = 0
      
        for trajectory_block in trajectory_blocks:
            data = [trajectory_blocks[trajectory_block], trajectory_block]
            model.append(data)
            n = n + 1
        



    def __init__(self, GTKDynamoSession = None):
        """ Class initialiser """
        self.builder          = gtk.Builder()
        
        
        
        if GTKDynamoSession != None:
            self.project          = GTKDynamoSession.project
            self.main_builder     = GTKDynamoSession.builder
            self.GTKDynamoSession = GTKDynamoSession        
            self.window_control   = GTKDynamoSession.window_control
            

        self.builder.add_from_file(
            os.path.join(GTKDYNAMO_GUI,'DialogWHAM', 'WHAM.glade'))
        self.builder.connect_signals(self)
        self.dialog = self.builder.get_object('dialog1')

        self.FileNames = {
                         # '/home/farminf/Programas/gtkdynamo2/gui/DialogWHAM' : True,
                         }
