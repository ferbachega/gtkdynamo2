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
import time

from gui.FileChooserWindow                                   import *           

#from pymol import cmd
#from PyMOLScripts import *
#from WindowControl import *
#EasyHybrid_ROOT   = os.environ.get('EasyHybrid_ROOT')
#EasyHybrid_ROOT   = '/home/fernando/Dropbox/GTKPyMOL'
#EasyHybrid_ROOT   = '/home/labio/Dropbox/GTKPyMOL'
#EasyHybrid_ROOT = os.getcwd()
EasyHybrid_ROOT = os.environ.get('EasyHybrid_ROOT')
EasyHybrid_GUI = os.path.join(EasyHybrid_ROOT, "gui")

from pprint import pprint
from pDynamoMethods.pDynamoUmbrellaSampling import  run_WHAM


#from   MatplotGTK.MatplotGTK          import PlotGTKWindow                                   #
#from   MatplotGTK.LogParse            import *                                      #


'''

Adicionar um textbox que pertimte o usuario adicionar comentarios
comentarios serao salvos no history dos processos

'''

class WHAMEquationSolverDialog():


    def run_WHAM_Equation_Solver (self, button):
        """ Function doc """
	mode            = self.builder.get_object('combobox1').get_active_text()
	if mode == "PMF 2D":
	    Bins = self.builder.get_object('Bins'                ).get_text()
	    Bins = [int(Bins), int(Bins)]
	
	if mode == "PMF 1D":
	    Bins = self.builder.get_object('Bins'                ).get_text()
	    Bins = [int(Bins)]

        
	LogFrequency         = self.builder.get_object('LogFrequency'        ).get_text()
        MaximumIterations    = self.builder.get_object('MaximumIterations'   ).get_text()
        RMSGradientTolerance = self.builder.get_object('RMSGradientTolerance').get_text()
        Temperature          = self.builder.get_object('Temperature'         ).get_text()
    
        model                = self.builder.get_object("liststore1") 
        data_path            = self.EasyHybridSession.project.settings['data_path']
        trajectory_blocks = []
    
        
        for i in model:
            if i[0] == True:
                trajectory_blocks.append(i[1])
            else:
                pass

        print 'Bins'                 , Bins                
        print 'LogFrequency'         , LogFrequency              
        print 'MaximumIterations'    , MaximumIterations          
        print 'RMSGradientTolerance' , RMSGradientTolerance       
        print 'Temperature'          , Temperature                
        pprint (trajectory_blocks)
        
        PARAMETERS = {
                    'Bins'                 : Bins                 ,
                    'LogFrequency'         : LogFrequency         ,
                    'MaximumIterations'    : MaximumIterations    ,
                    'RMSGradientTolerance' : RMSGradientTolerance ,
                    'Temperature'          : Temperature          ,
                    'trajectory_blocks'    : trajectory_blocks    ,
                    'output'               : data_path            ,
                    }
        
        logFile = run_WHAM (PARAMETERS)
        #parameters = ParseProcessLogFile(logFile)
        #PlotGTKWindow(parameters)
        
        #return index,atomname,atomtype,charge_table
    
    def clear_trajectory_blocks_list (self, button):
        """ Function doc """
        self.FileNames = {
                         }   
        liststore = self.builder.get_object('liststore1')
        #
        self.WHAM_TREEVIEW_ADD_DATA (liststore = liststore, trajectory_blocks=self.FileNames)
        
        
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
        



    def __init__(self, EasyHybridSession = None):
        """ Class initialiser """
        self.builder          = gtk.Builder()
        
        
        
        if EasyHybridSession != None:
            self.project          = EasyHybridSession.project
            self.main_builder     = EasyHybridSession.builder
            self.EasyHybridSession = EasyHybridSession        
            self.window_control   = EasyHybridSession.window_control
            
		

        
        self.builder.add_from_file(
            os.path.join(EasyHybrid_GUI,'DialogWHAM', 'WHAM.glade'))
        self.builder.connect_signals(self)
        self.dialog = self.builder.get_object('dialog1')


	combobox  = 'combobox1' 
        combolist = ["PMF 1D", "PMF 2D"]#, "trj - AMBER", "dcd - CHARMM", 'xtc - GROMACS']

        cbox = self.builder.get_object(combobox)  # ----> combobox_MM_model
        store = gtk.ListStore(gobject.TYPE_STRING)
        cbox.set_model(store)

        for i in combolist:
            cbox.append_text(i)

        cell = gtk.CellRendererText()
        cbox.pack_start(cell, True)
        cbox.add_attribute(cell, 'text', 0)
        cbox.set_active(0)









        self.FileNames = {
                         # '/home/farminf/Programas/EasyHybrid2/gui/DialogWHAM' : True,
                         }
