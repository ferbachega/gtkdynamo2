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
#from pymol import cmd
#from PyMOLScripts import *
from WindowControl import *
#GTKDYNAMO_ROOT   = os.environ.get('GTKDYNAMO_ROOT')
#GTKDYNAMO_ROOT   = '/home/fernando/Dropbox/GTKPyMOL'
#GTKDYNAMO_ROOT   = '/home/labio/Dropbox/GTKPyMOL'
#GTKDYNAMO_ROOT = os.getcwd()
#GTKDYNAMO_ROOT = os.environ.get('GTKDYNAMO_ROOT')
GTKDYNAMO_GUI = ''



'''

Adicionar um textbox que pertimte o usuario adicionar comentarios
comentarios serao salvos no history dos processos

'''

class ImportCoordinatesDialog():
    """ Class doc """
    def on_on_button_import_coordinates_clicked(self, button):
		""" Function doc """
		self.project = self.GTKDynamoSession.project
		filename     = self.builder.get_object("filechooserbutton_import_coord_from_file").get_filename()
		self.project.load_coordinate_file_to_system(filename, dualLog=None)
		self.project.From_PDYNAMO_to_GTKDYNAMO(type_='Coord', log =  None)

		#self.project.ExportStateToFile(self, filename, type_)

    def __init__(self, GTKDynamoSession = None):
        """ Class initialiser """
        self.builder          = gtk.Builder()
        
        if GTKDynamoSession != None:
            self.project          = GTKDynamoSession.project
            self.main_builder     = GTKDynamoSession.builder
            self.GTKDynamoSession = GTKDynamoSession        
            self.window_control   = GTKDynamoSession.window_control
            self.GTKDYNAMO_GUI    = GTKDynamoSession.GTKDYNAMO_GUI 
        
        else:
            self.GTKDYNAMO_ROOT = ''
            self.GTKDYNAMO_GUI  = ''

        self.builder.add_from_file(
            os.path.join(self.GTKDYNAMO_GUI,'DialogChargeRescale', 'ImportCoordinates.glade'))
        self.builder.connect_signals(self)
        self.dialog = self.builder.get_object('ImportCoordinatesDialog')

        '''
		--------------------------------------------------
		-                                                -
		-	              WindowControl                  -
		-                                                -
		--------------------------------------------------
		'''
        #self.window_control = WindowControl(self.builder)
        #
        ##----------------- Setup ComboBoxes -------------------------#
        #combobox = '02_window_combobox_minimization_method'          #
        #combolist = ["Conjugate Gradient", "Steepest Descent", "LBFGS"]
        #self.window_control.SETUP_COMBOBOXES(combobox, combolist, 0)
        ##------------------------------------------------------------#

class ExportCoordinatesDialog():
    """ Class doc """
    def on_button_SAVE_FRAME_clicked(self, button):
		""" Function doc """
		
		filename     = self.builder.get_object("entry_file_name").get_text()
		folder       = self.builder.get_object("directory_save_file").get_filename()
		type_        = self.builder.get_object("combobox_file_type").get_active_text()
		filename     = os.path.join(folder, filename + '.'+type_)
		print filename
		
		
		self.project = self.GTKDynamoSession.project
		self.project.ExportStateToFile(filename, type_)

    
    def __init__(self, GTKDynamoSession = None):
		""" Class initialiser """
		self.builder          = gtk.Builder()

		if GTKDynamoSession != None:
			self.project          = GTKDynamoSession.project
			self.main_builder     = GTKDynamoSession.builder
			self.GTKDynamoSession = GTKDynamoSession        
			self.window_control   = GTKDynamoSession.window_control
			self.GTKDYNAMO_GUI    = GTKDynamoSession.GTKDYNAMO_GUI 

		else:
			self.GTKDYNAMO_ROOT = ''
			self.GTKDYNAMO_GUI  = ''


		self.builder.add_from_file(
			os.path.join(self.GTKDYNAMO_GUI,'DialogChargeRescale','ExportCoordinates.glade'))
		self.builder.connect_signals(self)
		self.dialog = self.builder.get_object('ExportCoordinates')

		combolist = ["xyz","pdb","mol2","pkl","yaml","mol","cif","psf","crd"]
		combobox = 'combobox_file_type'
		
		
		'''
		--------------------------------------------------
		-                                                -
		-	              WindowControl                  -
		-                                                -
		--------------------------------------------------
		'''
		
		#cbox = self.builder.get_object(combobox)  # remover isso depois ----> combobox_MM_model
		#store = gtk.ListStore(gobject.TYPE_STRING)# remover isso depois
		#cbox.set_model(store)                     # remover isso depois
        #                                          # remover isso depois
		#for i in combolist:                       # remover isso depois
		#	cbox.append_text(i)                   # remover isso depois
        #                                          # remover isso depois
		#cell = gtk.CellRendererText()             # remover isso depois
		#cbox.pack_start(cell, True)               # remover isso depois
		#cbox.add_attribute(cell, 'text', 0)       # remover isso depois
		#cbox.set_active(0)                        # remover isso depois
		
		
		self.window_control = WindowControl(self.builder)
		
		#----------------- Setup ComboBoxes -------------------------#
		combolist = ["xyz","pdb","mol2","pkl","yaml","mol","cif","psf","crd"]
		combobox = 'combobox_file_type'
		self.window_control.SETUP_COMBOBOXES(combobox, combolist, 0)
		#------------------------------------------------------------#






def main():
    dialog = ImportCoordinatesDialog()
    dialog.dialog.run()
    dialog.dialog.hide()
if __name__ == '__main__':
    main()
