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

from PyMOLScripts.PyMOLScripts    import *


from WindowControl    import *

from pCore            import *
from pBabel           import *
from pMolecule        import *
from pMoleculeScripts import *

#GTKDYNAMO_ROOT = os.getcwd()
GTKDYNAMO_ROOT = os.environ.get('GTKDYNAMO_ROOT')

GTKDYNAMO_GUI = os.path.join(GTKDYNAMO_ROOT, "gui")




                
class pDynamoSelectionWindow():
    """ Class doc """
    def  on_pDynamoSelectionsWindow_destroy(self, widget):
        """ Function doc """
        self.Visible  =  False
    
    def OpenWindow (self):
        """ Function doc """
        if self.Visible  ==  False:
            self.builder = gtk.Builder()
            self.builder.add_from_file(
                os.path.join(GTKDYNAMO_GUI,'WindowpDynamoSelections', 'pDynamoSelectionsWindow.glade'))
            
            self.builder.connect_signals(self)
            self.window = self.builder.get_object('window1')

            
            
            self.window_control =  WindowControl(self.builder)
            #--------------------- Setup ComboBoxes -----------------------#
            combobox  = 'combobox_selection_type'                          #
            combolist = ['ByComponent', 'Complement','ByLinearPolymer']    #
            self.window_control.SETUP_COMBOBOXES(combobox, combolist, 0)   #
                                                                           #
            combobox  = 'combobox_select_as_prune_fix_pymol'               #    
            combolist = ["Select in PyMOl","FIX atoms","PRUNE atoms"]      #
            self.window_control.SETUP_COMBOBOXES(combobox, combolist, 0)   #                                                                                   
            #--------------------------------------------------------------#
            
            
            # SPINBUTTON 
            spinbutton = 'selection_radius_spinbutton'                        
            config     = [0.0, 1.0, 500.0, 1.0, 0.0, 0.0]       
            self.window_control.SETUP_SPINBUTTON(spinbutton, config)
            self.builder.get_object('selection_radius_spinbutton').set_value(int(self.radius_distance))
            
            self.project = self.GTKDynamoSession.project
            self.project.importPDBInformantion()
            #self.build_treeview()
            self.window.show()                                               
            self.builder.connect_signals(self)                                   
            
            self.Visible  =  True
            gtk.main()

    
    def on_selection_radius_spinbutton_value_changed (self, widget):
        """ Function doc """
        self.radius_distance = float(self.builder.get_object("selection_radius_spinbutton").get_value_as_int())
    

    def importResidueInformation(self, button):
        #print 'button'
        #try:
        model = cmd.get_model("pk1")
        index = []
        resn = None
        resi = None 
        for a in model.atom:
            #resn = a.resn
            #resi = a.resi
            #print resn
            #print resi
            #print a.index
            index = a.index
            
            
            chain     = self.project.pdbInfo[index][1]
            resn      = self.project.pdbInfo[index][0]
            resi      = self.project.pdbInfo[index][2]
            atom_name = self.project.pdbInfo[index][3]
            
            self.builder.get_object('selection_entry1').set_text(chain)
            self.builder.get_object('selection_entry2').set_text(resn)
            self.builder.get_object('selection_entry3').set_text(str(resi))
            self.builder.get_object('selection_entry4').set_text(atom_name)
        #except:
        #    cmd.edit_mode()
        #    print "pk1 selection not found"

    

    def apply_pdynamo_selection(self, button):    #pdynamo method
        """Fucntion that permits select atoms from pDynamo arguments"""

        self.project          = self.GTKDynamoSession.project

        iter3 = self.builder.get_object('selection_entry1').get_text()
        iter2 = self.builder.get_object('selection_entry2').get_text()
        iter4 = self.builder.get_object('selection_entry3').get_text()
        iter1 = self.builder.get_object('selection_entry4').get_text()

        str_teste = "*:%s.%s:%s" %(iter2, iter4, iter1)
        
        import_type2    =       self.builder.get_object("combobox_select_as_prune_fix_pymol").get_active_text()
        import_type     =       self.builder.get_object("combobox_selection_type").get_active_text()
        selection_type  =       self.builder.get_object("combobox_selection_type").get_active_text()
        radius_distance = float(self.builder.get_object("selection_radius_spinbutton").get_value_as_int())

        print str_teste
        
        pymolIndex   = AtomSelection.FromAtomPattern ( self.project.system, str_teste )
        pymolIndex	 = pymolIndex.Within ( radius_distance )
        

        if selection_type == "ByComponent":
            pymolIndex	  = pymolIndex.ByComponent()
            self.builder.get_object("selectionByAtomSelectionMode")
            pymolIndex	 = Selection ( pymolIndex )
            #project.system = PruneByAtom ( project.system, pymolIndex )

        
        if selection_type == "Complement":
            pymolIndex	 = pymolIndex.Complement()
            self.builder.get_object("")
            pymolIndex	 = Selection ( pymolIndex )
            #project.system.DefineFixedAtoms ( pymolIndex )

        if selection_type == "ByLinearPolymer":
            pymolIndex	 = pymolIndex.ByLinearPolymer()
            self.builder.get_object("selectionByAtomSelectionMode")
            pymolIndex	 = Selection ( pymolIndex )		
        
        #print pymolIndex
        try:
            cmd.delete('sele')
        except:
            pass
        index_list = list(pymolIndex)
        PymolPutTable (index_list, "sele")
        pymol_id  =  self.project.settings['PyMOL_Obj'] 
        string22  = 'select sele, ('+pymol_id+ ' and  sele )'

        
        cmd.do(string22)
        #cmd.disable("all")
        #cmd.enable("pymol_id")
        cmd.enable("sele")
        
        #if 	import_type2 == "Select in PyMOl":
        #    # export data to pymol 
        #    try:
        #        cmd.delete("sele")
        #    except:
        #        a = None
        #
        #    pymol_put_table (index_list, "sele")
        #    pymol_id  = project.settings['last_pymol_id'] 
        #    string22  = 'select sele, ('+pymol_id+ ' and  sele )'
        #    cmd.do(string22)				
        #
        ##if 	import_type2 == "FIX atoms":
        #    project.system.DefineFixedAtoms ( pymolIndex )
        #    # export data to pymol 
        #    try:
        #        cmd.delete("FIX_atoms")
        #    except:
        #        a = None
        #    
        #    project.settings['fix_table'] = index_list
        #    
        #    pymol_put_table (index_list, "FIX_atoms")
        #    
        #    pymol_id  = project.settings['last_pymol_id'] 
        #    string22  = 'select FIX_atoms, ('+pymol_id+ ' and  FIX_atoms )'
        #    cmd.do(string22)
        #    string5  = 'color grey80, FIX_atoms'
        #    cmd.do(string5)			
        #    
        #if 	import_type2 == "PRUNE atoms":
        #    data_path      =  self.builder.get_object("01_main_window_filechooserbutton_datapath").get_filename()
        #    project.system = PruneByAtom ( project.system, pymolIndex )
        #    
        #    # exporting data to pymol 
        #    project.increment_step()                                               # step
        #    project.export_frames_to_pymol('prn', types_allowed , data_path)	# Loading the actual frame in pymol.		
        #    project.check_system(self.dualLog)                                     # Check System
        #
        #    # JOB HISTORY
        #    step       = project.step
        #    process    = "prune system"
        #    potencial  = project.settings["potencial"]
        #    energy     = " - "
        #    time       = " - " 
        #    #self.insert_JOB_HISTORY_DATA ( step, process, potencial, energy, time )

    
    
    
    
    def __init__(self, GTKDynamoSession):
        """ Class initialiser """
        self.radius_distance  = 16
        self.GTKDynamoSession = GTKDynamoSession
        #self.project          = GTKDynamoSession.project
        self.Visible          = False
        #print self.project.settings['data_path']

def main():
    dialog = ScanWindow()
    dialog.OpenWindow()
if __name__ == '__main__':
    main()
