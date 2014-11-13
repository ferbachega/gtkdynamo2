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
from PyMOLScripts import *
from WindowControl import *
#GTKDYNAMO_ROOT   = os.environ.get('GTKDYNAMO_ROOT')
#GTKDYNAMO_ROOT   = '/home/fernando/Dropbox/GTKPyMOL'
#GTKDYNAMO_ROOT   = '/home/labio/Dropbox/GTKPyMOL'
GTKDYNAMO_ROOT = os.getcwd()
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
        trajectory                    = self.builder.get_object('NEBDialog_NEB__pd_traj_out').get_text()
        
        parameters = { 'NEB_number_of_structures':   NEB_number_of_structures,
                       'NEB_maximum_interations' :   NEB_maximum_interations ,
                       'NEB_grad_tol'            :   NEB_grad_tol            ,
                       'trajectory'              :   trajectory              }
                          
        for i in parameters:
            print i, parameters[i]
		

        if self.project != None:
            data_path = self.project.data_path
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

        print reactants_file
        print products_file
       
       
        #trajectory           = self.builder.get_object("02_window_entry_traj_name").get_text()
        #maximumIterations    = int(self.builder.get_object("02_window_entry_max_int").get_text())
        #logFrequency         = int(self.builder.get_object("02_window_entry_log_freq").get_text())
        #trajectory_freq      = int(self.builder.get_object("02_window_entry_traj_freq").get_text())
        #rmsGradientTolerance = float(self.builder.get_object("02_window_entry_rmsGRAD").get_text())
        #method               = self.builder.get_object("02_window_combobox_minimization_method").get_active_text()
        #AmberTrajectoryFlag  = self.builder.get_object("02_window_AMBER_trajectory_checkbox").get_active()
        #TrajectoryFlag       = self.builder.get_object("02_window_Output_trajectory_checkbox").get_active()

        #parameters = {'trajectory'          : trajectory,
        #              'maximumIterations'   : maximumIterations,
        #              'logFrequency'        : logFrequency,
        #              'trajectory_freq'     : trajectory_freq,
        #              'rmsGradientTolerance': rmsGradientTolerance,
        #              'method'              : method,
        #              'AmberTrajectoryFlag' : AmberTrajectoryFlag,
        #              'TrajectoryFlag'      : TrajectoryFlag}


        #if self.project.system is not None:
        #   #------------------------------------------------------------------#
        #   #                     Geometry optmization                         #
        #   #                                                                  #
        #   #    requires: method = 'Conjugate Gradient', parameters = None    #
        #   # -----------------------------------------------------------------#
        #   self.project.Minimization(method, parameters)


    
    def __init__(self, project=None, window_control=None, main_builder=None):
        """ Class initialiser """
        self.project = project
        self.window_control = window_control
        self.builder = gtk.Builder()
        self.main_builder = main_builder

        self.builder.add_from_file(
            os.path.join(GTKDYNAMO_GUI, 'NEBDialog.glade'))
        self.builder.connect_signals(self)
        self.dialog = self.builder.get_object('NEBDialog')

        '''
		--------------------------------------------------
		-                                                -
		-	              WindowControl                  -
		-                                                -
		--------------------------------------------------
		'''
        self.window_control = WindowControl(self.builder)
        
        self.builder.get_object("NEBDialog_filechooserbutton_REACTANTS").hide()
        self.builder.get_object("NEBDialog_filechooserbutton_PRODUCTS").hide()
        #----------------- Setup ComboBoxes -------------------------#
        #combobox = '02_window_combobox_minimization_method'          #
        #combolist = ["Conjugate Gradient", "Steepest Descent", "LBFGS"]
        #self.window_control.SETUP_COMBOBOXES(combobox, combolist, 0)
        #------------------------------------------------------------#


def main():
    dialog = NEBDialog()
    dialog.dialog.run()
    dialog.dialog.hide()
if __name__ == '__main__':
    main()
