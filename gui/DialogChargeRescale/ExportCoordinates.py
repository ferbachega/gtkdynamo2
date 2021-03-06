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
#EasyHybrid_ROOT   = os.environ.get('EasyHybrid_ROOT')
#EasyHybrid_ROOT   = '/home/fernando/Dropbox/GTKPyMOL'
#EasyHybrid_ROOT   = '/home/labio/Dropbox/GTKPyMOL'
#EasyHybrid_ROOT = os.getcwd()
#EasyHybrid_ROOT = os.environ.get('EasyHybrid_ROOT')
EasyHybrid_GUI = ''



'''

Adicionar um textbox que pertimte o usuario adicionar comentarios
comentarios serao salvos no history dos processos

'''

class ImportCoordinatesDialog():
    """ Class doc """
    def on_button_SAVE_FRAME_clicked(self, button):
		""" Function doc """
		
		filename     = self.builder.get_object("entry_file_name").get_text()
		folder       = self.builder.get_object("directory_save_file").get_filename()
		type_        = self.builder.get_object("combobox_file_type").get_active_text()
		filename     = os.path.join(folder, filename + '.'+type_)
		print filename
		
		
		self.project = self.EasyHybridSession.project
		self.project.ExportStateToFile(filename, type_)

    
    def __init__(self, EasyHybridSession = None):
		""" Class initialiser """
		self.builder          = gtk.Builder()

		if EasyHybridSession != None:
			self.project          = EasyHybridSession.project
			self.main_builder     = EasyHybridSession.builder
			self.EasyHybridSession = EasyHybridSession        
			self.window_control   = EasyHybridSession.window_control
			self.EasyHybrid_GUI		  = EasyHybridSession.EasyHybrid_GUI

		self.builder.add_from_file(
			os.path.join(self.EasyHybrid_GUI, 'ExportCoordinates.glade'))
		self.builder.connect_signals(self)
		self.dialog = self.builder.get_object('ExportCoordinates')

		combolist = ["xyz","pdb","pkl","yaml"]#,"mol","cif","psf","crd","mol2"]



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
		combobox = '02_window_combobox_minimization_method'          #
		combolist = ["Conjugate Gradient", "Steepest Descent", "LBFGS"]
		self.window_control.SETUP_COMBOBOXES(combobox, combolist, 0)
		#------------------------------------------------------------#


def main():
    dialog = ImportCoordinatesDialog()
    dialog.dialog.run()
    dialog.dialog.hide()
if __name__ == '__main__':
    main()
