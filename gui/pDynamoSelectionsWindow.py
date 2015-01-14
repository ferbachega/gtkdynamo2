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
#from PyMOLScripts     import PymolPutTable

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
                os.path.join(GTKDYNAMO_GUI, 'pDynamoSelectionsWindow.glade'))
            
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
            self.build_treeview()
            self.window.show()                                               
            self.builder.connect_signals(self)                                   
            
            self.Visible  =  True
            gtk.main()

    def build_treeview(self):
        treeview = self.builder.get_object("selection_treeview1")		
        model    = self.builder.get_object("selection_liststore1") 
        model.clear()
        print self.project.settings['data_path']
        PDBFile_FromSystem (self.project.settings['data_path'] + "/my_system_full.pdb", self.project.system)
        AMBER_READ  = open (self.project.settings['data_path'] + "/my_system_full.pdb", "r")

        for line in AMBER_READ:						
            line2 = line.split()				
            line1 = line[0:6]					
            if line1 == "ATOM  " or line1 == "HETATM" :	
                index   = line[6:11]	
                A_name  = line[11:16]	
                resn    = line[16:20] 	
                chain   = line[20:22]	
                resi    = line[22:26]	
                gap     = line[26:30]	
                x       = line[30:38]	
                y       = line[38:46]	
                z       = line[46:54]	
                                        
                b       = line[54:60]	
                oc      = line[60:66]	
                gap2    = line[66:76]	
                atom    = line[76:78] 	
                
                index2  = index.split()
                index2  = int(index2[0])			

                        
                A_name2 = A_name.split()		
                A_name2 = A_name2[0]				


                resn2 = resn.split()
                resn2 = resn2[0]

                
                #chain2 = chain.split()
                #chain2 = chain2[0]

                
                resi2 = resi.split()
                resi2 = int(resi2[0])			

                
                atom2 = atom.split()
                atom2 = atom2[0]			
                if chain   == "  ":
                    chain2 = 'A' 
                else:
                    chain2 = chain.split()
                    chain2 = chain2[0]
                    
                lista  = ( index2, A_name2, resn2, chain2, resi2, atom2 )
                
                self.project.pdbInfo[index2] = [resn2, chain2, resi2, A_name2]
                model.append(lista)		

    def importResidueInformation(self, button):
        print 'button'
        try:
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
        except:
            cmd.edit_mode()
            print "pk1 selection not found"

    

    def apply_pdynamo_selection(self, button):    #pdynamo method
        """Fucntion that permits select atoms from pDynamo arguments"""
        
        #model       = self.builder.get_object("selection_liststore1") 
        #treeview    = self.builder.get_object("selection_treeview1")
        #selection   = treeview.get_selection()
        #model, iter = selection.get_selected()


        iter3 = self.builder.get_object('selection_entry1').get_text()
        iter2 = self.builder.get_object('selection_entry2').get_text()
        iter4 = self.builder.get_object('selection_entry3').get_text()
        iter1 = self.builder.get_object('selection_entry4').get_text()

        str_teste = "*:%s.%s:%s" %(iter2, iter4, iter1)
        
        import_type2    =       self.builder.get_object("combobox_select_as_prune_fix_pymol").get_active_text()
        import_type     =       self.builder.get_object("combobox_selection_type").get_active_text()
        selection_type  =       self.builder.get_object("combobox_selection_type").get_active_text()
        radius_distance = float(self.builder.get_object("selection_radius_distance_entry1").get_text())

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
        self.project = GTKDynamoSession.project
        self.Visible = False
        print self.project.settings['data_path']

def main():
    dialog = ScanWindow()
    dialog.OpenWindow()
if __name__ == '__main__':
    main()
