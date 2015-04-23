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
#from WindowControl import *
##GTKDYNAMO_ROOT   = os.environ.get('GTKDYNAMO_ROOT')
##GTKDYNAMO_ROOT   = '/home/fernando/Dropbox/GTKPyMOL'
##GTKDYNAMO_ROOT   = '/home/labio/Dropbox/GTKPyMOL'
##GTKDYNAMO_ROOT = os.getcwd()

'''

Adicionar um textbox que pertimte o usuario adicionar comentarios
comentarios serao salvos no history dos processos

'''

class AboutDialog():

    def __init__(self, GTKDynamoSession = None):
        """ Class initialiser """
        if GTKDynamoSession != None:
            self.project          = GTKDynamoSession.project
            self.main_builder     = GTKDynamoSession.builder
            self.GTKDynamoSession = GTKDynamoSession        
            self.window_control   = GTKDynamoSession.window_control
            self.GTKDYNAMO_ROOT   = GTKDynamoSession.GTKDYNAMO_ROOT
            self.GTKDYNAMO_GUI    = GTKDynamoSession.GTKDYNAMO_GUI 
        
        self.builder          = gtk.Builder()
        self.builder.add_from_file(
            os.path.join(self.GTKDYNAMO_GUI, 'DialogAbout',  'About.glade'))
        self.builder.connect_signals(self)
        self.dialog = self.builder.get_object('aboutdialog')

        '''
		--------------------------------------------------
		-                                                -
		-	              WindowControl                  -
		-                                                -
		--------------------------------------------------
		'''
        #self.window_control = WindowControl(self.builder)

        ##----------------- Setup ComboBoxes -------------------------#
        #combobox = '02_window_combobox_minimization_method'          #
        #combolist = ["Conjugate Gradient", "Steepest Descent", "LBFGS"]
        #self.window_control.SETUP_COMBOBOXES(combobox, combolist, 0)
        #------------------------------------------------------------#


def main():
    dialog = About_Dialog()
    dialog.dialog.run()
    dialog.dialog.hide()
if __name__ == '__main__':
    main()
