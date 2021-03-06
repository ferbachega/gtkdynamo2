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
EasyHybrid_ROOT = os.environ.get('EasyHybrid_ROOT')

EasyHybrid_GUI = os.path.join(EasyHybrid_ROOT, "gui")



'''

Adicionar um textbox que pertimte o usuario adicionar comentarios
comentarios serao salvos no history dos processos

'''

class PreferencesDialog():
    """ Class doc """
    def SavePreferences (self, button):
        """ Function doc """
        atom_color       = self.builder.get_object('combobox1').get_active_text()
        fixed_atom_color = self.builder.get_object('combobox2').get_active_text()
        bq_color         = self.builder.get_object('combobox3').get_active_text()
        
        QC_representations  = {'lines'  : self.builder.get_object('QC_lines').get_active(),
                               'sticks' : self.builder.get_object('QC_sticks').get_active(),
                               'spheres': self.builder.get_object('QC_spheres').get_active(),
                               'dots'   : self.builder.get_object('QC_dots').get_active(),
                                }
        
        FIX_representations = {'lines'  : self.builder.get_object('FIX_lines').get_active(),
                               'sticks' : self.builder.get_object('FIX_sticks').get_active(),
                               'spheres': self.builder.get_object('FIX_spheres').get_active(),
                               'dots'   : self.builder.get_object('FIX_dots').get_active(),
                                }

        #FIX_representations = {'lines' : self.builder.get_object('FIX_lines').get_active()
        #                        }
        #
        self.EasyHybridSession.EasyHybridConfig['bg_color'] = bq_color     
        self.EasyHybridSession.EasyHybridConfig['fixed'   ] = fixed_atom_color
        self.EasyHybridSession.EasyHybridConfig['color'   ] = atom_color        
        self.EasyHybridSession.EasyHybridConfig['QC']       = QC_representations
        self.EasyHybridSession.EasyHybridConfig['FIX']      = FIX_representations

        self.EasyHybridSession.Save_EasyHybrid_ConfigFile()
        self.EasyHybridSession.project.SystemCheck(      status = True, 
                                                         PyMOL = True, 
                                                        _color = True, 
                                                         _cell = True, 
                                           treeview_selections = True,
                                                   ORCA_backup = False 
                                                )
    




    def __init__(self, EasyHybridSession = None):
        """ Class initialiser """
        self.builder          = gtk.Builder()

        if EasyHybridSession != None:
            self.project          = EasyHybridSession.project
            self.main_builder     = EasyHybridSession.builder
            self.EasyHybridSession = EasyHybridSession        
            self.window_control   = EasyHybridSession.window_control
            

        self.builder.add_from_file(
            os.path.join(EasyHybrid_GUI,'DialogPreferences', 'Preferences.glade'))
        self.builder.connect_signals(self)
        self.dialog = self.builder.get_object('dialog_preferences')

        '''
		--------------------------------------------------
		-                                                -
		-	              WindowControl                  -
		-                                                -
		--------------------------------------------------
		'''
        self.window_control = WindowControl(self.builder)

        #colors = [ ]
        #colors = [
        #'actinium','darksalmon','iodine','palecyan','sodium',
        #'aluminum','dash','iridium','palegreen','splitpea',
        #'americium','deepblue','iron','paleyellow','strontium',
        #'antimony','deepolive','krypton','palladium','sulfur',
        #'aquamarine','deeppurple','lanthanum','phosphorus','tantalum',
        #'argon','deepsalmon','lawrencium','pink','teal',
        #'arsenic','deepsalmon','lead','platinum','technetium',
        #'astatine','deepteal','lightblue','plutonium','tellurium',
        #'atomic','default','lightmagenta','polonium','terbium',
        #'auto','density','lightorange','potassium','thallium',
        #'barium','deuterium','lightpink','praseodymium','thorium',
        #'berkelium','dirtyviolet','lightteal','promethium','thulium',
        #'beryllium','dubnium','lime','protactinium','tin',
        #'bismuth','dysprosium','limegreen','pseudoatom','titanium',
        #'black','einsteinium','limon','purple','tungsten',
        #'blue','erbium','lithium','purpleblue','tv_blue',
        #'bluewhite','europium','lonepair','radium','tv_green',
        #'bohrium','fermium','lutetium','radon','tv_orange',
        #'boron','firebrick','magenta','raspberry','tv_red',
        #'brightorange','fluorine','magnesium','red','tv_yellow',
        #'bromine','forest','manganese','rhenium','uranium',
        #'brown','francium','marine','rhodium','vanadium',
        #'cadmium','gadolinium','meitnerium','rubidium','violet',
        #'calcium','gallium','mendelevium','ruby','violetpurple',
        #'californium','germanium','mercury','ruthenium','warmpink',
        #'carbon','gold','molybdenum','rutherfordium','wheat',
        #'cerium','gray','neodymium','salmon','white',
        #'cesium','green','neon','samarium','xenon',
        #'chartreuse','greencyan','neptunium','sand','yellow',
        #'chlorine','grey','nickel','scandium','yelloworange',
        #'chocolate','hafnium','niobium','seaborgium','ytterbium',
        #'chromium','hassium','nitrogen','selenium','yttrium',
        #'cobalt','helium','nobelium','silicon','zinc',
        #'copper','holmium','olive','silver','zirconium',
        #'curium','hotpink','orange','skyblue'
        #'current','hydrogen','osmium','slate'
        #'cyan','indium','oxygen','smudg'
        #]
        
        colors = [
        'darksalmon','palecyan','palegreen','deepblue','deeppurple','deepsalmon',
        'deepsalmon','lightblue','lightorange','lightpink','dirtyviolet','lime',
        'tin','limegreen','black','limon','purple','blue',
        'purpleblue','tv_blue','bluewhite','tv_green','radon','tv_orange','firebrick',
        'magenta','raspberry','tv_red','brightorange','red','tv_yellow',
        'forest','brown','marine','violet','ruby','violetpurple','warmpink',
        'wheat','gray','salmon','white','green','greencyan','sand','yellow','yelloworange',
        'chocolate','olive','hotpink','orange','skyblue','slate','cyan','smudg'
        ]


        fixed_colors = ['black','grey10','grey20','grey30', 'grey40','grey50','grey60','grey70','grey80','grey90','white']

        bg_color = ['white', 'grey', 'black']

        #----------------- Setup ComboBoxes -------------------------#
        combobox = 'combobox1'          #
        self.window_control.SETUP_COMBOBOXES(combobox, colors, 0)
        #------------------------------------------------------------#

        #----------------- Setup ComboBoxes -------------------------#
        combobox = 'combobox2'          #
        self.window_control.SETUP_COMBOBOXES(combobox, fixed_colors, 0)
        #------------------------------------------------------------#

        #----------------- Setup ComboBoxes -------------------------#
        combobox = 'combobox3'          #
        self.window_control.SETUP_COMBOBOXES(combobox, bg_color, 0)
        #------------------------------------------------------------#


def main():
    dialog = PreferencesDialog()
    dialog.dialog.run()
    dialog.dialog.hide()
if __name__ == '__main__':
    main()
