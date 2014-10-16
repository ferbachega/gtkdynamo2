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
from PyMOLScripts import *
from WindowControl import *
#GTKDYNAMO_ROOT   = os.environ.get('GTKDYNAMO_ROOT')
#GTKDYNAMO_ROOT   = '/home/fernando/Dropbox/GTKPyMOL'
#GTKDYNAMO_ROOT   = '/home/labio/Dropbox/GTKPyMOL'
GTKDYNAMO_ROOT = os.getcwd()
GTKDYNAMO_GUI = os.path.join(GTKDYNAMO_ROOT, "gui")


nbList = ['NBModelFull',
          'NBModelABFS',
          'NBModelGABFS',
          'NBModelSSBP']


class NonBondDialog():

    """ Class doc """
    def on_button1_apply_NBModel_clicked(self, button):
        """ Function doc """
        nbModel     = self.builder.get_object('combobox1_nb_types').get_active_text()
        innercutoff = float(self.builder.get_object('entry1').get_text())
        outercutoff = float(self.builder.get_object('entry2').get_text())
        listcutoff  = float(self.builder.get_object('entry3').get_text())
        kappa       = float(self.builder.get_object('entry4').get_text())
        
        if self.project == None:
            print (nbModel, innercutoff,
                  outercutoff,
                  listcutoff ,
                  kappa   )   
        else:

            self.project.settings['ABFS_options']  = {"innerCutoff": innercutoff, "outerCutoff": outercutoff, "listCutoff": listcutoff},
            self.project.settings['nbModel_type']  = nbModel
            self.project.set_nbModel_to_system()
        
    def QCcomboxChange(self, combobox):
        """ Function doc """
        mode = self.builder.get_object('combobox1_nb_types').get_active_text()
        if mode == 'NBModelFull':
            self.builder.get_object('entry1').set_sensitive(False)
            self.builder.get_object('entry2').set_sensitive(False) 
            self.builder.get_object('entry3').set_sensitive(False)
            self.builder.get_object('entry4').set_sensitive(False)
        if mode == 'NBModelABFS':       
            self.builder.get_object('entry1').set_sensitive(True)
            self.builder.get_object('entry2').set_sensitive(True) 
            self.builder.get_object('entry3').set_sensitive(True)
            self.builder.get_object('entry4').set_sensitive(True)
        if mode == 'NBModelGABFS':        
            self.builder.get_object('entry1').set_sensitive(True)
            self.builder.get_object('entry2').set_sensitive(True) 
            self.builder.get_object('entry3').set_sensitive(True)
            self.builder.get_object('entry4').set_sensitive(True)
        if mode == 'NBModelSSBP':        
            self.builder.get_object('entry1').set_sensitive(False)
            self.builder.get_object('entry2').set_sensitive(False) 
            self.builder.get_object('entry3').set_sensitive(False)
            self.builder.get_object('entry4').set_sensitive(False)
        if mode == 'No NB model':
            self.builder.get_object('entry1').set_sensitive(False)
            self.builder.get_object('entry2').set_sensitive(False) 
            self.builder.get_object('entry3').set_sensitive(False)
            self.builder.get_object('entry4').set_sensitive(False)       
        
        
        
        
        
    def __init__(self, project=None, window_control=None, main_builder=None):
        """ Class initialiser """
        self.project = project
        self.window_control = window_control
        self.builder = gtk.Builder()
        self.main_builder = main_builder

        self.builder.add_from_file(
            os.path.join(GTKDYNAMO_GUI, 'NonBondDialog.glade'))
        self.builder.connect_signals(self)
        self.dialog = self.builder.get_object('dialog1')

        '''
		--------------------------------------------------
		-                                                -
		-	              WindowControl                  -
		-                                                -
		--------------------------------------------------
		'''
        self.window_control = WindowControl(self.builder)

        #----------------- Setup ComboBoxes -------------------------#
        combobox = 'combobox1_nb_types'         #
        combolist = nbList
        self.window_control.SETUP_COMBOBOXES(combobox, combolist, 0)
        #------------------------------------------------------------#


def main():
    dialog = NonBondDialog()
    dialog.dialog.run()
    dialog.dialog.hide()
if __name__ == '__main__':
    main()
