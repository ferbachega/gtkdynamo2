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
from pDynamoMethods.pDynamoMolecularDynamics import *
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





class MolecularDynamicsWindow():

    """ Class doc """

    def on_MMDialog_button1_RUN_DYNAMICS_clicked(self, button):
        self.project        = self.GTKDynamoSession.project
                    
        trajectory_name     = self.builder.get_object      ("MMDialog_entry_trajectory_name").get_text()
        nsteps              = int(self.builder.get_object  ('MMDialog_n_steps_dy').get_text())
        log_freq            = int(self.builder.get_object  ("MMDialog_entry_log_freq_dy").get_text())
        trajectory_freq     = int(self.builder.get_object  ("MMDialog_entry_traj_freq_dy").get_text())
        timestep            = float(self.builder.get_object('MMDialog_timestep').get_text())
        method              = self.builder.get_object      ("MMDialog_combobox_molecular_dynamics_method").get_active_text()
        seed                = int(self.builder.get_object  ('MMDialog_entry_seed_dy').get_text())
        temperature         = int(self.builder.get_object  ('MMDialog_temperature').get_text())
        temp_scale_freq     = int(self.builder.get_object  ('MMDialog_temp_scale_freq').get_text())
        coll_freq           = int(self.builder.get_object  ('MMDialog_collision_frequency').get_text())
        AmberTrajectoryFlag = self.builder.get_object      ("MMDialog_AMBER_trajectory_checkbox1").get_active()
        TrajectoryFlag      = self.builder.get_object      ("MMDialog_Output_trajectory_checkbox1").get_active()
        
        parameters = {'trajectory_name'    : trajectory_name    ,
                      'nsteps'             : nsteps             ,
                      'log_freq'           : log_freq           ,
                      'trajectory_freq'    : trajectory_freq    ,
                      'timestep'           : timestep           ,
                      'method'             : method             ,
                      'seed'               : seed               ,
                      'temperature'        : temperature        ,
                      'temp_scale_freq'    : temp_scale_freq    ,
                      'coll_freq'          : coll_freq          ,
                      'TrajectoryFlag'     : TrajectoryFlag     , 
                      'AmberTrajectoryFlag': AmberTrajectoryFlag}
                    
        #print parameters
        self.project.MolecularDynamics(parameters)
        #RunMolecularDynamics(parameters, self.project)
 

    def __init__(self, GTKDynamoSession = None):
        """ Class initialiser """
        self.builder          = gtk.Builder()
        if GTKDynamoSession != None:
            self.project          = GTKDynamoSession.project
            self.main_builder     = GTKDynamoSession.builder
            self.GTKDynamoSession = GTKDynamoSession        
            self.window_control   = GTKDynamoSession.window_control


        self.builder.add_from_file(
            os.path.join(GTKDYNAMO_GUI,'DialogMolecularDynamics', 'MolecularDynamicsDialog.glade'))
        self.builder.connect_signals(self)
        self.dialog = self.builder.get_object('MMDialog_molecular_dynamics')

        '''
		--------------------------------------------------
		-                                                -
		-	              WindowControl                  -
		-                                                -
		--------------------------------------------------
		'''
        self.window_control = WindowControl(self.builder)

        #----------------- Setup ComboBoxes -------------------------#
        combobox = 'MMDialog_combobox_molecular_dynamics_method'         #
        combolist = ["Velocity Verlet Dynamics", "Leap Frog Dynamics","Langevin Dynamics"]
        self.window_control.SETUP_COMBOBOXES(combobox, combolist, 0)
        #------------------------------------------------------------#






def main():
    dialog = MolecularDynamicsWindow()
    dialog.dialog.run()
    dialog.dialog.hide()
if __name__ == '__main__':
    main()
