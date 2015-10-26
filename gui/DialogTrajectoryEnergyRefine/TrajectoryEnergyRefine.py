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
import time
import gobject
from WindowControl import *

# pDynamo
from pBabel           import *
from pCore            import *
from pMolecule        import *
from pMoleculeScripts import *

from pDynamoMethods.pDynamoScan   import *
from pDynamoMethods.pDynamoTrajectoryEnergyRefine import *

from pprint import pprint
from DualTextLogFileWriter3 import *


      
class TrajectoryEnergyRefineDialog():

    def runTrajectoryEnergyRefine (self, button):
        """ Function doc """
        trajectory = self.builder.get_object('filechooserbutton1').get_filename()
        system    = self.project.system
        data_path = self.project.settings['data_path']
        
        pDynamoTrajectoryEnergyRefine ( system = system, 
                                     data_path = data_path, 
                                    trajectory = trajectory, 
                                         _type = '1D')
        
        
    





    def on_combobox1_changed(self, button):
        _type        = self.builder.get_object('combobox1').get_active_text()
        """ Function doc """
        if _type == 'folder - pDynamo':
            self.builder.get_object('filechooserbutton2').hide()
            self.builder.get_object('filechooserbutton1').show()
        else:
            self.builder.get_object('filechooserbutton2').show()
            self.builder.get_object('filechooserbutton1').hide()


    def __init__(self, GTKDynamoSession = None):

        self.builder = gtk.Builder()
        if GTKDynamoSession != None:
            self.project          = GTKDynamoSession.project
            self.main_builder     = GTKDynamoSession.builder
            self.window_control   = GTKDynamoSession.window_control
            self.GTKDynamoSession = GTKDynamoSession
            self.GTKDYNAMO_ROOT   = GTKDynamoSession.GTKDYNAMO_ROOT
            self.GTKDYNAMO_GUI    = GTKDynamoSession.GTKDYNAMO_GUI 
            
            
            #      - - - importing ORCA PATH from GTKDynamoConfig file. - - -        
            #-----------------------------------------------------------------------#
            try:                                                                    #
                ORCA                  = GTKDynamoSession.GTKDynamoConfig['ORCAPATH']#
            except:                                                                 #
                ORCA = ''                                                           #
            #-----------------------------------------------------------------------#

        self.builder.add_from_file(
            os.path.join(self.GTKDYNAMO_GUI, 'DialogTrajectoryEnergyRefine','TrajectoryEnergyRefine.glade'))
                
        self.builder.connect_signals(self)
        self.dialog = self.builder.get_object('dialog1')

        self.window_control = WindowControl(self.builder)
        self.builder.get_object('filechooserbutton2').hide()
        
        #----------------- Setup ComboBoxes -------------------------#
        combobox = 'combobox1'         #
        combolist = ["folder - pDynamo", "trj - AMBER", "dcd - CHARMM", 'xtc - GROMACS']
        self.window_control.SETUP_COMBOBOXES(combobox, combolist, 0)




def main():
    dialog = TrajectoryEnergyRefineDialog()
    dialog.dialog.run()
    dialog.dialog.hide()
if __name__ == '__main__':
    main()
