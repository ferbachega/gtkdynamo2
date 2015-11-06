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
#EasyHybrid_ROOT   = os.environ.get('EasyHybrid_ROOT')
#EasyHybrid_ROOT   = '/home/fernando/Dropbox/GTKPyMOL'
#EasyHybrid_ROOT   = '/home/labio/Dropbox/GTKPyMOL'
#EasyHybrid_ROOT = os.getcwd()
EasyHybrid_ROOT = os.environ.get('EasyHybrid_ROOT')

EasyHybrid_GUI = os.path.join(EasyHybrid_ROOT, "gui")



'''

Adicionar um textbox que pertimte o usuario adicionar comentarios
comentarios serao salvos no history dos processos

'''

class MinimizationWindow():

    """ Class doc """

    def on_02_window_button_RUN_MINIMIZATION1_clicked(self, button):
		""" Function doc """
		self.project          = self.EasyHybridSession.project

		trajectory           = self.builder.get_object("02_window_entry_traj_name").get_text()
		maximumIterations    = int(self.builder.get_object("02_window_entry_max_int").get_text())
		logFrequency         = int(self.builder.get_object("02_window_entry_log_freq").get_text())
		trajectory_freq      = int(self.builder.get_object("02_window_entry_traj_freq").get_text())
		rmsGradientTolerance = float(self.builder.get_object("02_window_entry_rmsGRAD").get_text())
		method               = self.builder.get_object("02_window_combobox_minimization_method").get_active_text()
		AmberTrajectoryFlag  = self.builder.get_object("02_window_AMBER_trajectory_checkbox").get_active()
		TrajectoryFlag       = self.builder.get_object("02_window_Output_trajectory_checkbox").get_active()

		parameters = {'trajectory'          : trajectory,
					  'maximumIterations'   : maximumIterations,
					  'logFrequency'        : logFrequency,
					  'trajectory_freq'     : trajectory_freq,
					  'rmsGradientTolerance': rmsGradientTolerance,
					  'method'              : method,
					  'AmberTrajectoryFlag' : AmberTrajectoryFlag,
					  'TrajectoryFlag'      : TrajectoryFlag}


		if self.project.system is not None:
			#------------------------------------------------------------------#
			#                     Geometry optimization                         #
			#                                                                  #
			#    requires: method = 'Conjugate Gradient', parameters = None    #
			# -----------------------------------------------------------------#
			self.project.Minimization(method, parameters)

			''' 
			toda esta parte abaixo ficou obsoleta devido ao novo metodo no pDynamoProject -  
			 
			 
								  From_PDYNAMO_to_EasyHybrid
			 
				esse metodo eh responsavel por:
					contar o passo
					exportar o frame atual para o pymol
					exportar as informacoes relevantes para as treeviews
					e adicionar informacoes ao history 
				 
			'''
    def __init__(self, EasyHybridSession = None):
        """ Class initialiser """
        self.builder          = gtk.Builder()
        if EasyHybridSession != None:
            self.project          = EasyHybridSession.project
            self.main_builder     = EasyHybridSession.builder
            self.EasyHybridSession = EasyHybridSession        
            self.window_control   = EasyHybridSession.window_control
            

        self.builder.add_from_file(
            os.path.join(EasyHybrid_GUI,'DialogMinimization', 'MinimizationDialog.glade'))
        self.builder.connect_signals(self)
        self.dialog = self.builder.get_object('02_MinimizationWindow')

        '''
		--------------------------------------------------
		-                                                -
		-	              WindowControl                  -
		-                                                -
		--------------------------------------------------
		'''
        self.window_control = WindowControl(self.builder)

        #----------------- Setup ComboBoxes -------------------------#
        combobox = '02_window_combobox_minimization_method'          #
        combolist = ["Conjugate Gradient", "Steepest Descent", "LBFGS"]
        self.window_control.SETUP_COMBOBOXES(combobox, combolist, 0)
        #------------------------------------------------------------#


def main():
    dialog = MinimizationWindow()
    dialog.dialog.run()
    dialog.dialog.hide()
if __name__ == '__main__':
    main()
