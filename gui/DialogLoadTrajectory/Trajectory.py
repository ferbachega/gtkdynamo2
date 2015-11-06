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
#from PyMOLScripts import *
from WindowControl import *



EasyHybrid_ROOT = os.environ.get('EasyHybrid_ROOT')
EasyHybrid_GUI = os.path.join(EasyHybrid_ROOT, "gui")



'''

Adicionar um textbox que pertimte o usuario adicionar comentarios
comentarios serao salvos no history dos processos

'''

class TrajectoryDialog():
    def on_TrajectoryDialog_button_load_clicked(self, button):
        """ Function doc """
        self.project     = self.EasyHybridSession.project
               
        first            = int(self.builder.get_object('TrajectoryDialog_first').get_text() )
        last             = int(self.builder.get_object('TrajectoryDialog_last').get_text()  )
        stride           = int(self.builder.get_object('TrajectoryDialog_stride').get_text())
        #traj_name        = self.builder.get_object('filechooserbutton1').get_text()
        #traj_name2       = self.builder.get_object('filechooserbutton2').get_text()
        new_pymol_object  = self.builder.get_object('entry1').get_text()
        _type             = self.builder.get_object('combobox1').get_active_text()
        
        """ Function doc """
        if _type == 'folder - pDynamo':
            traj_name        = self.builder.get_object('filechooserbutton1').get_filename()

        else:
            traj_name        = self.builder.get_object('filechooserbutton2').get_filename()

        print (first            ,
              last             ,
              stride           ,
              traj_name        ,  
              new_pymol_object ,
              _type)            
        
        frames = self.project.load_trajectory_to_system(first, last, stride, traj_name, new_pymol_object, _type)
        self.EasyHybridSession.builder.get_object('trajectory_max_entrey').set_text(str(frames))
        self.EasyHybridSession.on_TrajectoryTool_HSCALE_update()
        
    def on_combobox1_changed(self, button):
        _type        = self.builder.get_object('combobox1').get_active_text()
        """ Function doc """
        if _type == 'folder - pDynamo':
            self.builder.get_object('filechooserbutton2').hide()
            self.builder.get_object('filechooserbutton1').show()
        else:
            self.builder.get_object('filechooserbutton2').show()
            self.builder.get_object('filechooserbutton1').hide()


    def __init__(self, EasyHybridSession):
        """ Class initialiser """
        self.EasyHybridSession = EasyHybridSession
        self.project          = EasyHybridSession.project
        self.main_builder     = EasyHybridSession.builder

        self.builder = gtk.Builder()
        self.builder.add_from_file(
            os.path.join(EasyHybrid_GUI,'DialogLoadTrajectory','TrajectoryDialog.glade'))
        self.builder.connect_signals(self)
        self.dialog = self.builder.get_object('TrajectoryDialog')

        '''
		--------------------------------------------------
		-                                                -
		-	              WindowControl                  -
		-                                                -
		--------------------------------------------------
		'''
        
        self.window_control = WindowControl(self.builder)
        self.builder.get_object('filechooserbutton2').hide()
        
        #----------------- Setup ComboBoxes -------------------------#
        combobox = 'combobox1'         #
        combolist = ["folder - pDynamo", "trj - AMBER", "dcd - CHARMM", 'xtc - GROMACS']
        self.window_control.SETUP_COMBOBOXES(combobox, combolist, 0)
        #------------------------------------------------------------#


def main():
    dialog = TrajectoryDialog()
    dialog.dialog.run()
    dialog.dialog.hide()
if __name__ == '__main__':
    main()
