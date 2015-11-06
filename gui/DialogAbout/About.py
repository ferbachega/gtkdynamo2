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
##EasyHybrid_ROOT   = os.environ.get('EasyHybrid_ROOT')
##EasyHybrid_ROOT   = '/home/fernando/Dropbox/GTKPyMOL'
##EasyHybrid_ROOT   = '/home/labio/Dropbox/GTKPyMOL'
##EasyHybrid_ROOT = os.getcwd()

'''

Adicionar um textbox que pertimte o usuario adicionar comentarios
comentarios serao salvos no history dos processos

'''

class AboutDialog():

    def __init__(self, EasyHybridSession = None):
        """ Class initialiser """
        if EasyHybridSession != None:
            self.project          = EasyHybridSession.project
            self.main_builder     = EasyHybridSession.builder
            self.EasyHybridSession = EasyHybridSession        
            self.window_control   = EasyHybridSession.window_control
            self.EasyHybrid_ROOT   = EasyHybridSession.EasyHybrid_ROOT
            self.EasyHybrid_GUI    = EasyHybridSession.EasyHybrid_GUI 
        
        self.builder          = gtk.Builder()
        self.builder.add_from_file(
            os.path.join(self.EasyHybrid_GUI, 'DialogAbout',  'About.glade'))
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
