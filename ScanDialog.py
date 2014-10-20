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
GTKDYNAMO_ROOT = os.getcwd()
GTKDYNAMO_GUI = os.path.join(GTKDYNAMO_ROOT, "gui")


                
class ScanDialog():
    """ Class doc """
    def RunScan(self, button):
        print 'Run Scan'
        pass
    
    def on_ScanDialog_ImportFromPyMOL (self, button):
        """ Function doc """
        print 'Import from PyMOL'

    def on_ScanDialog_checkbutton_MassWeight (self, checkbutton):
        """ Function doc """
        print 'checkbutton_MassWeight'

    def ScanComboxChange(self, combobox):
        """ Function doc """
        mode = self.builder.get_object('ScanDialog_combobox_SCAN_reaction_coordiante_type').get_active_text()
        if mode == 'simple-distance':
            self.builder.get_object('ScanDialog_SCAN_label_coord1_atom3').set_sensitive(False)
            self.builder.get_object('ScanDialog_SCAN_entry_cood1_ATOM3').set_sensitive(False)
            self.builder.get_object('ScanDialog_SCAN_label_cood1_ATOM3_name').set_sensitive(False)
            self.builder.get_object('ScanDialog_SCAN_entry_cood1_ATOM3_name').set_sensitive(False)
            self.builder.get_object('ScanDialog_scan_checkbutton_mass_weight').set_sensitive(False)
        if mode == 'multiple-distance':
            self.builder.get_object('ScanDialog_SCAN_label_coord1_atom3').set_sensitive(True)
            self.builder.get_object('ScanDialog_SCAN_entry_cood1_ATOM3').set_sensitive(True)
            self.builder.get_object('ScanDialog_SCAN_label_cood1_ATOM3_name').set_sensitive(True)
            self.builder.get_object('ScanDialog_SCAN_entry_cood1_ATOM3_name').set_sensitive(True)
            self.builder.get_object('ScanDialog_scan_checkbutton_mass_weight').set_sensitive(True)

    def __init__(self, project=None, window_control=None, main_builder=None):
        """ Class initialiser """
        self.project = project
        self.window_control = window_control
        self.builder = gtk.Builder()
        self.main_builder = main_builder

        self.builder.add_from_file(
            os.path.join(GTKDYNAMO_GUI, 'ScanDialog.glade'))
        
        self.builder.connect_signals(self)
        self.dialog = self.builder.get_object('ScanDialog')

        '''
		--------------------------------------------------
		-                                                -
		-	              WindowControl                  -
		-                                                -
		--------------------------------------------------
		'''
        self.window_control = WindowControl(self.builder)
       
        #--------------------- Setup ComboBoxes -------------------------
        combobox  = 'ScanDialog_combobox_SCAN_reaction_coordiante_type'                                           
        combolist = ['simple-distance', 'multiple-distance']
        self.window_control.SETUP_COMBOBOXES(combobox, combolist, 0)     

        combobox  = 'ScanDialog_combobox_SCAN_minimization_method'                                           
        combolist = ['Conjugate Gradient', 'Steepest Descent','LBFGS']
        self.window_control.SETUP_COMBOBOXES(combobox, combolist, 0)     
                                                                                                                               
        #----------------------------------------------------------------
        

def main():
    dialog = ScanDialog()
    dialog.dialog.run()
    dialog.dialog.hide()
if __name__ == '__main__':
    main()
