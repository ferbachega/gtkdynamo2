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
from pymol import cmd
from PyMOLScripts.PyMOLScripts import *
from WindowControl import *
from pDynamoMethods.pDynamoSAWandNEB   import *


#GTKDYNAMO_ROOT   = os.environ.get('GTKDYNAMO_ROOT')
#GTKDYNAMO_ROOT   = '/home/fernando/Dropbox/GTKPyMOL'
#GTKDYNAMO_ROOT   = '/home/labio/Dropbox/GTKPyMOL'
#GTKDYNAMO_ROOT = os.getcwd()
GTKDYNAMO_ROOT = os.environ.get('GTKDYNAMO_ROOT')

GTKDYNAMO_GUI = os.path.join(GTKDYNAMO_ROOT, "gui")



'''

Adicionar um textbox que pertimte o usuario adicionar comentarios
comentarios serao salvos no history dos processos

'''

class NEBDialog():

    """ Class doc """

    def checkbutton_change(self,checkbutton ):
        if checkbutton == self.builder.get_object("NEBDialog_checkbutton_PRODUCTS"):
            if self.builder.get_object("NEBDialog_checkbutton_PRODUCTS").get_active():
                self.builder.get_object("NEBDialog_filechooserbutton_PRODUCTS").show()
                self.builder.get_object("NEBDialog_entry_PRODUCTS").hide()
            else:
                self.builder.get_object("NEBDialog_filechooserbutton_PRODUCTS").hide()
                self.builder.get_object("NEBDialog_entry_PRODUCTS").show()
        if checkbutton == self.builder.get_object("NEBDialog_checkbutton_REACTANTS"):
            if self.builder.get_object("NEBDialog_checkbutton_REACTANTS").get_active():
                self.builder.get_object("NEBDialog_filechooserbutton_REACTANTS").show()
                self.builder.get_object("NEBDialog_entry_REACTANTS").hide()
            else:
                self.builder.get_object("NEBDialog_filechooserbutton_REACTANTS").hide()
                self.builder.get_object("NEBDialog_entry_REACTANTS").show()
            
            
    def RunNEB(self, button):
        """ Function doc """
        NEB_number_of_structures      = int(self.builder.get_object('NEBDialog_NEB_number_of_structures').get_text())
        NEB_maximum_interations       = int(self.builder.get_object('NEBDialog_NEB_maximum_interations').get_text())
        NEB_grad_tol                  = float(self.builder.get_object('NEBDialog_NEB_grad_tol').get_text())
        trajectory_name               = self.builder.get_object('trajectory_name').get_text()
        
        if self.GTKDynamoSession.project != None:
            data_path = self.GTKDynamoSession.project.settings['data_path']
        else:
            data_path = "/home/teste"

        # reactants
        if self.builder.get_object('NEBDialog_checkbutton_REACTANTS').get_active():
            reactants_file          = self.builder.get_object('NEBDialog_filechooserbutton_REACTANTS').get_filename()
        else:
            pymol_object            = self.builder.get_object('NEBDialog_entry_REACTANTS').get_text()
            label       	        = pymol_object + " XYZ file - REACTANTS"
            file_out                = "reactants_NEB.xyz"	
            reactants_file          = PyMOL_export_XYZ_to_file(pymol_object, label, data_path, file_out, -1)			

        if self.builder.get_object('NEBDialog_checkbutton_PRODUCTS').get_active():
            products_file       = self.builder.get_object('NEBDialog_filechooserbutton_PRODUCTS').get_filename()
        else:
            pymol_object            = self.builder.get_object('NEBDialog_entry_PRODUCTS').get_text()
            label       	        = pymol_object + " XYZ file - PRODUCTS"
            file_out                = "products_NEB.xyz"	
            products_file           =PyMOL_export_XYZ_to_file(pymol_object, label, data_path, file_out, -1)

        #print reactants_file
        #print products_file
        plot_flag = False
  
        
        parameters = {
                     'reactants_file'           : reactants_file                 , 
                     'products_file'            : products_file                  , 
                     'data_path'                : data_path                      , 
                     'NEB_number_of_structures' : int(NEB_number_of_structures)  , 
                     'NEB_maximum_interations'  : int(NEB_maximum_interations )  , 
                     'NEB_grad_tol'             : float(NEB_grad_tol      )      , 
                     'trajectory_name'          : trajectory_name                ,
                     'plot_flag'                : plot_flag
                     }
        
        
       
        logFile = pDynamoNEB(project  = self.GTKDynamoSession.project, parameters = parameters )
        #-------------------------------------------------------------------------------------------------#
        self.GTKDynamoSession.project.From_PDYNAMO_to_GTKDYNAMO(type_='neb', log =  logFile)


       

    
    def __init__(self, GTKDynamoSession):
        """ Class initialiser """
        #self.project = project
        self.GTKDynamoSession = GTKDynamoSession
        self.window_control   = GTKDynamoSession.window_control
        self.builder = gtk.Builder()
        self.main_builder = GTKDynamoSession.builder

        self.builder.add_from_file(
            os.path.join(GTKDYNAMO_GUI,'DialogNEB', 'NEBDialog.glade'))
        self.builder.connect_signals(self)
        self.dialog = self.builder.get_object('NEBDialog')

        '''
		--------------------------------------------------
		-                                                -
		-	              WindowControl                  -
		-                                                -
		--------------------------------------------------
		'''
        #self.window_control = WindowControl(self.builder)
        
        self.builder.get_object("NEBDialog_filechooserbutton_REACTANTS").hide()
        self.builder.get_object("NEBDialog_filechooserbutton_PRODUCTS").hide()
        #----------------- Setup ComboBoxes -------------------------#
        #combobox = '02_window_combobox_minimization_method'          #
        #combolist = ["Conjugate Gradient", "Steepest Descent", "LBFGS"]
        #self.window_control.SETUP_COMBOBOXES(combobox, combolist, 0)
        #------------------------------------------------------------#


class SAWDialog():

    """ Class doc """

    def checkbutton_change(self,checkbutton ):
        if checkbutton == self.builder.get_object("SAWDialog_checkbutton_PRODUCTS"):
            if self.builder.get_object("SAWDialog_checkbutton_PRODUCTS").get_active():
                self.builder.get_object("SAWDialog_filechooserbutton_PRODUCTS").show()
                self.builder.get_object("SAWDialog_entry_PRODUCTS").hide()
            else:
                self.builder.get_object("SAWDialog_filechooserbutton_PRODUCTS").hide()
                self.builder.get_object("SAWDialog_entry_PRODUCTS").show()
        if checkbutton == self.builder.get_object("SAWDialog_checkbutton_REACTANTS"):
            if self.builder.get_object("SAWDialog_checkbutton_REACTANTS").get_active():
                self.builder.get_object("SAWDialog_filechooserbutton_REACTANTS").show()
                self.builder.get_object("SAWDialog_entry_REACTANTS").hide()
            else:
                self.builder.get_object("SAWDialog_filechooserbutton_REACTANTS").hide()
                self.builder.get_object("SAWDialog_entry_REACTANTS").show()
            
            
    def RunSAW(self, button):
        """ Function doc """
        SAW_number_of_structures      = int(self.builder.get_object('SAWDialog_SAW_number_of_structures').get_text())
        SAW_maximum_interations       = int(self.builder.get_object('SAWDialog_SAW_maximum_interations').get_text())
        SAW_gamma                     = float(self.builder.get_object('SAWDialog_SAW_grad_tol').get_text())
        trajectory                    = self.builder.get_object('SAWDialog_SAW__pd_traj_out').get_text()
        
        parameters = { 'SAW_number_of_structures':   SAW_number_of_structures,
                       'SAW_maximum_interations' :   SAW_maximum_interations ,
                       'SAW_gamma'               :   SAW_gamma               ,
                       'trajectory'              :   trajectory              }
                          
        for i in parameters:
            print i, parameters[i]
		

        if self.GTKDynamoSession.project != None:
            data_path = self.GTKDynamoSession.project.settings['data_path']
        else:
            data_path = "/home/teste"

        
                
        # reactants
        if self.builder.get_object('SAWDialog_checkbutton_REACTANTS').get_active():
            reactants_file          = self.builder.get_object('SAWDialog_filechooserbutton_REACTANTS').get_filename()
        else:
            pymol_object            = self.builder.get_object('SAWDialog_entry_REACTANTS').get_text()
            label       	        = pymol_object + " XYZ file - REACTANTS"
            file_out                = "reactants_SAW.xyz"	
            reactants_file          = PyMOL_export_XYZ_to_file(pymol_object, label, data_path, file_out, -1)			

        if self.builder.get_object('SAWDialog_checkbutton_PRODUCTS').get_active():
            products_file       = self.builder.get_object('SAWDialog_filechooserbutton_PRODUCTS').get_filename()
        else:
            pymol_object            = self.builder.get_object('SAWDialog_entry_PRODUCTS').get_text()
            label       	        = pymol_object + " XYZ file - PRODUCTS"
            file_out                = "products_SAW.xyz"	
            products_file           =PyMOL_export_XYZ_to_file(pymol_object, label, data_path, file_out, -1)

        #print reactants_file
        #print products_file
       

        plot_flag = False
    
  
        #data_path = self.GTKDynamoSession.project.settings['data_path']
  
  
  
        
        parameters = {
                     'reactants_file'           : reactants_file                 , 
                     'products_file'            : products_file                  , 
                     'data_path'                : data_path                      , 
                     'SAW_number_of_structures' : int(SAW_number_of_structures)  , 
                     'SAW_maximum_interations'  : int(SAW_maximum_interations )  , 
                     'SAW_grad_tol'             : float(SAW_grad_tol      )      , 
                     'trajectory_name'          : trajectory_name                ,
                     'plot_flag'                : plot_flag
                     }
        
        
       
        logFile = pDynamoSAW(project  = self.GTKDynamoSession.project, parameters = parameters )
        #-------------------------------------------------------------------------------------------------#
        self.GTKDynamoSession.project.From_PDYNAMO_to_GTKDYNAMO(type_='saw', log =  logFile)






    
    def __init__(self, GTKDynamoSession = None):
        """ Class initialiser """
        #self.project = project
        self.GTKDynamoSession = GTKDynamoSession
        self.window_control   = GTKDynamoSession.window_control
        self.builder          = gtk.Builder()
        self.main_builder     = GTKDynamoSession.builder

        self.builder.add_from_file(
            os.path.join(GTKDYNAMO_GUI,'DialogNEB', 'SAWDialog.glade'))
        self.builder.connect_signals(self)
        self.dialog = self.builder.get_object('SAWDialog')

        '''
		--------------------------------------------------
		-                                                -
		-	              WindowControl                  -
		-                                                -
		--------------------------------------------------
		'''
        #self.window_control = WindowControl(self.builder)
        
        self.builder.get_object("SAWDialog_filechooserbutton_REACTANTS").hide()
        self.builder.get_object("SAWDialog_filechooserbutton_PRODUCTS").hide()
        #----------------- Setup ComboBoxes -------------------------#
        #combobox = '02_window_combobox_minimization_method'          #
        #combolist = ["Conjugate Gradient", "Steepest Descent", "LBFGS"]
        #self.window_control.SETUP_COMBOBOXES(combobox, combolist, 0)
        #------------------------------------------------------------#










def main():
    dialog = SAWDialog()
    dialog.dialog.run()
    dialog.dialog.hide()
if __name__ == '__main__':
    main()
