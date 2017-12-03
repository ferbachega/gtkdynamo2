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
import time
import gobject
from WindowControl import *
import copy
# pDynamo
from pBabel           import *
from pCore            import *
from pMolecule        import *
from pMoleculeScripts import *

from pDynamoMethods.pDynamoScan   import *
from pDynamoMethods.pDynamoTrajectoryEnergyRefine import *
from PyMOLScripts.PyMOLScripts import *

from pprint import pprint
from DualTextLogFileWriter3 import *
from pprint import pprint

      
class TrajectoryEnergyRefineDialog():

    def runTrajectoryEnergyRefine (self, button):
        """ Function doc """
        
        trajectory = self.builder.get_object('filechooserbutton1').get_filename()
        data_path  = self.project.settings['data_path']
        logfile    = self.builder.get_object('filechooserbutton4').get_filename()
        input_type = self.builder.get_object('combobox4').get_active_text()
	nCPUs      = self.builder.get_object('spinbutton2').get_value_as_int()
	#nCPUs      = 8
        REACTION_COORD1 = None
	REACTION_COORD2 = None
	
	set_MM_chrgs_to_zero = False
	exclude_MM_atoms     = False
	system     = Clone(self.project.system)
	
	if self.builder.get_object("checkbutton_set_MM_charges_to_zero").get_active():
	    charges =  system.energyModel.mmAtoms.AtomicCharges()
	    natoms  = len(charges)
	    ZeroCharges = [0.0] * natoms
	    system.energyModel.mmAtoms.SetAtomicCharges(ZeroCharges)
        
	

	#if self.builder.get_object("checkbutton_exclude_MM_atoms").get_active():
	#    exclude_MM_atoms = True
	
	#_type = None
        
	#-------------------------------------------------------------------------------------------------#
	# 				Coordinate 1
	#-------------------------------------------------------------------------------------------------#
	mode       = self.builder.get_object('combobox_reaction_coordiante_type1').get_active_text() 
	if mode == "simple-distance":                                                                
	    REACTION_COORD1 = {'MODE'         : mode,                                                    
			       'ATOM1'        : int(self.builder.get_object("entry_coord1_ATOM1"     ).get_text()) ,                                            
			       'ATOM1_name'   : self.builder.get_object    ("entry_coord1_ATOM1_name").get_text()  ,                                            
			       'ATOM2'        : int(self.builder.get_object("entry_coord1_ATOM2"     ).get_text()) ,                                            
			       'ATOM2_name'   : self.builder.get_object    ("entry_coord1_ATOM2_name").get_text()  ,	                                     
			      }                                                                             
	                                                                                             
	if mode == "multiple-distance":                                                                           
	    REACTION_COORD1 = {'MODE'         : mode,                                                    
			       'ATOM1'        : int(self.builder.get_object("entry_coord1_ATOM1"     ).get_text()),                                                  
			       'ATOM1_name'   : self.builder.get_object    ("entry_coord1_ATOM1_name").get_text() ,                                           
			       'ATOM2'        : int(self.builder.get_object("entry_coord1_ATOM2"     ).get_text()),
			       'ATOM2_name'   : self.builder.get_object    ("entry_coord1_ATOM2_name").get_text() ,
			       'ATOM3'        : int(self.builder.get_object("entry_coord1_ATOM3"     ).get_text()),
			       'ATOM3_name'   : self.builder.get_object    ("entry_coord1_ATOM3_name").get_text() ,
			       }                                        
	#-------------------------------------------------------------------------------------------------#
	


	
	
	
	#-------------------------------------------------------------------------------------------------#
	# 				Coordinate 2
	#-------------------------------------------------------------------------------------------------#
	if self.refine_type == '2D':
	    mode       = self.builder.get_object('combobox_reaction_coordiante_type2').get_active_text() 
	    if mode == "simple-distance":    	    									
		REACTION_COORD2 = {'MODE'         : mode,                                        
				   'ATOM1'        : int(self.builder.get_object("entry_coord2_ATOM1"     ).get_text()),                                        
				   'ATOM1_name'   : self.builder.get_object    ("entry_coord2_ATOM1_name").get_text() ,                                        
				   'ATOM2'        : int(self.builder.get_object("entry_coord2_ATOM2"     ).get_text()),                                        
				   'ATOM2_name'   : self.builder.get_object    ("entry_coord2_ATOM2_name").get_text() ,  		                                                          
			       }                                                                 
	    
	    if mode == "multiple-distance":                                                              											 
		REACTION_COORD2 = {'MODE'         : mode,                                                    
				   'ATOM1'        : int(self.builder.get_object("entry_coord2_ATOM1"     ).get_text()),                                              
				   'ATOM1_name'   : self.builder.get_object    ("entry_coord2_ATOM1_name").get_text() ,                                              
				   'ATOM2'        : int(self.builder.get_object("entry_coord2_ATOM2"     ).get_text()),                                              
				   'ATOM2_name'   : self.builder.get_object    ("entry_coord2_ATOM2_name").get_text() ,		                                     
				   'ATOM3'        : int(self.builder.get_object("entry_coord2_ATOM3"     ).get_text()),                                              
				   'ATOM3_name'   : self.builder.get_object    ("entry_coord2_ATOM3_name").get_text() ,                                              
				   }  
	#-------------------------------------------------------------------------------------------------#

	'''
	if self.builder.get_object('checkbutton_minimization').get_active()  :

	    #---------------------------------- importing parameters COORD-1 ---------------------------#
            FORCECONSTANT = float(self.builder.get_object('entry_FORCE1').get_text())                   #
            #-------------------------------------------------------------------------------------------#
            self.EasyHybridSession.project.ActiveModeCheck()
            MINIMIZATION_PARAMETERS = None
            
            if self.builder.get_object("checkbutton_minimization").get_active():
                #---------------------------------------------------------------------------------------------------------#
                mim_method	   = self.builder.get_object('combobox_optimization_method').get_active_text()            #                                                                                                                         #
                max_int            = self.builder.get_object("entry_max_interactions")      .get_text()                   #
                rms_grad           = self.builder.get_object("entry_rmsd_grad")             .get_text()                   #
                log_freq           = 1
                #---------------------------------------------------------------------------------------------------------#
                
                MINIMIZATION_PARAMETERS={
                                        'do_minimizaton': True      ,
                                        'max_int'       : max_int   ,
                                        'log_freq'      : log_freq  ,
                                        'rms_grad'      : rms_grad  ,
                                        'mim_method'    : mim_method}

            pprint(REACTION_COORD1)
            pprint(MINIMIZATION_PARAMETERS)

        
	else:
	    pass
	'''
	
	_type = 'energy'
	
	
	
	pDynamoTrajectoryEnergyRefine (system               = system              , 
				       data_path            = data_path           ,     
				       trajectory           = trajectory          ,  
				       REACTION_COORD1      = REACTION_COORD1     ,
				       REACTION_COORD2      = REACTION_COORD2     ,
				       input_type           = input_type          , 
				       _type                = self.refine_type    ,
				       nCPUs                = nCPUs               ,
				       set_MM_chrgs_to_zero = set_MM_chrgs_to_zero,
				       exclude_MM_atoms     = exclude_MM_atoms    )   

	#if self.builder.get_object("checkbutton_set_MM_charges_to_zero").get_active():
	#    self.project.system.energyModel.mmAtoms.SetAtomicCharges(charges)
        #

    def Button_import_PyMOL_index(self, button):
        '''
        ----------------------------------------------------
                        REACTION COORDINATE 1 
        ----------------------------------------------------
        '''
        if button == self.builder.get_object('import_indexes_from_PyMOL1'):
            mode  =  self.builder.get_object('combobox_reaction_coordiante_type1').get_active_text()
            if mode == "simple-distance":
                try:
                    name1, atom1_index, name2, atom2_index, distance_a1_a2 = import_ATOM1_ATOM2("pk1", "pk2")
                    distance_a1_a2 = str(distance_a1_a2)
                    
                    #self.builder.get_object('entry_param_DMINIMUM1'  ).set_text(distance_a1_a2)
                    self.builder.get_object("entry_coord1_ATOM1"     ).set_text(str(atom1_index))
                    self.builder.get_object("entry_coord1_ATOM1_name").set_text(name1)
                    self.builder.get_object("entry_coord1_ATOM2"     ).set_text(str(atom2_index))
                    self.builder.get_object("entry_coord1_ATOM2_name").set_text(name2)
                except:
                    cmd.edit_mode()
                    print "pk1, pk2 selection not found"					
                    print texto_d1
                    return	
        
            if mode == "multiple-distance":			
                try:
                    name1, atom1_index, name2, atom2_index, distance_a1_a2 = import_ATOM1_ATOM2("pk1", "pk2")
                    name2, atom2_index, name3, atom3_index, distance_a2_a3 = import_ATOM1_ATOM2("pk2", "pk3")

                    #print "distance between atom 1 and atom 2: ",distance_a1_a2
                    #print "distance between atom 2 and atom 3: ",distance_a2_a3
                    
		    '''
                    if self.builder.get_object("checkbutton_mass_weight").get_active():
                        self.sigma_pk1_pk3, self.sigma_pk3_pk1 = compute_sigma_a1_a3 (name1, name3)
                        
                        """
                           R                    R
                            \                  /
                             A1--A2  . . . . A3
                            /                  \ 
                           R                    R
                             ^   ^            ^
                             |   |            |
                            pk1-pk2  . . . . pk3
                               d1       d2	
                        
                        q1 =  1 / (mpk1 + mpk3)  =  [ mpk1 * r (pk3_pk2)  -   mpk3 * r (pk1_pk2) ]
                        
                        """			
                        
                        #DMINIMUM =  (self.sigma_pk1_pk3 * distance_a1_a2) -(self.sigma_pk3_pk1 * distance_a2_a3*-1)
                        #self.builder.get_object('entry_param_DMINIMUM1').set_text(str(DMINIMUM))
                        print "\n\nUsing mass weighted restraints"
                        print "Sigma pk1_pk3", self.sigma_pk1_pk3
                        print "Sigma pk3_pk1", self.sigma_pk3_pk1
                        #print "Estimated minimum distance",  DMINIMUM
                        
                    else:
                        self.sigma_pk1_pk3 =  1.0
                        self.sigma_pk3_pk1 = -1.0
                        #DMINIMUM = distance_a1_a2 - distance_a2_a3
                        #self.builder.get_object('entry_param_DMINIMUM1').set_text(str(DMINIMUM))
                        
                        print "\n\nSigma pk1_pk3 ", self.sigma_pk1_pk3
                        print "Sigma pk3_pk1", self.sigma_pk3_pk1
                        #print "Estimated minimum distance",  DMINIMUM			
		    '''
		
		except:
                    cmd.edit_mode()
                    print "pk1, pk2 and pk3 selections not found"	
                    return			
                
		print name3, name2, name1
                self.builder.get_object("entry_coord1_ATOM1"     ).set_text(str(atom1_index))
                self.builder.get_object("entry_coord1_ATOM1_name").set_text(name1)
                self.builder.get_object("entry_coord1_ATOM2"     ).set_text(str(atom2_index))
                self.builder.get_object("entry_coord1_ATOM2_name").set_text(name2)
                self.builder.get_object("entry_coord1_ATOM3"     ).set_text(str(atom3_index))
                self.builder.get_object("entry_coord1_ATOM3_name").set_text(name3)

        if button == self.builder.get_object('import_indexes_from_PyMOL2'):
            mode  =  self.builder.get_object('combobox_reaction_coordiante_type2').get_active_text()
            if mode == "simple-distance":
                try:
                    name1, atom1_index, name2, atom2_index, distance_a1_a2 = import_ATOM1_ATOM2("pk1", "pk2")
                    distance_a1_a2 = str(distance_a1_a2)
                    
                    #self.builder.get_object('entry_param_DMINIMUM1'  ).set_text(distance_a1_a2)
                    self.builder.get_object("entry_coord2_ATOM1"     ).set_text(str(atom1_index))
                    self.builder.get_object("entry_coord2_ATOM1_name").set_text(name1)
                    self.builder.get_object("entry_coord2_ATOM2"     ).set_text(str(atom2_index))
                    self.builder.get_object("entry_coord2_ATOM2_name").set_text(name2)
                except:
                    cmd.edit_mode()
                    print "pk1, pk2 selection not found"					
                    print texto_d1
                    return	
        
            if mode == "multiple-distance":			
                try:
                    name1, atom1_index, name2, atom2_index, distance_a1_a2 = import_ATOM1_ATOM2("pk1", "pk2")
                    name2, atom2_index, name3, atom3_index, distance_a2_a3 = import_ATOM1_ATOM2("pk2", "pk3")
                    #print "distance between atom 1 and atom 2: ",distance_a1_a2
                    #print "distance between atom 2 and atom 3: ",distance_a2_a3
                    '''
                    if self.builder.get_object("checkbutton_mass_weight").get_active():
                        self.sigma_pk1_pk3, self.sigma_pk3_pk1 = compute_sigma_a1_a3 (name1, name3)
                        
                        """
                           R                    R
                            \                  /
                             A1--A2  . . . . A3
                            /                  \ 
                           R                    R
                             ^   ^            ^
                             |   |            |
                            pk1-pk2  . . . . pk3
                               d1       d2	
                        
                        q1 =  1 / (mpk1 + mpk3)  =  [ mpk1 * r (pk3_pk2)  -   mpk3 * r (pk1_pk2) ]
                        
                        """			
                        
                        #DMINIMUM =  (self.sigma_pk1_pk3 * distance_a1_a2) -(self.sigma_pk3_pk1 * distance_a2_a3*-1)
                        #self.builder.get_object('entry_param_DMINIMUM1').set_text(str(DMINIMUM))
                        print "\n\nUsing mass weighted restraints"
                        print "Sigma pk1_pk3", self.sigma_pk1_pk3
                        print "Sigma pk3_pk1", self.sigma_pk3_pk1
                        #print "Estimated minimum distance",  DMINIMUM
                        
                    else:
                        self.sigma_pk1_pk3 =  1.0
                        self.sigma_pk3_pk1 = -1.0
                        #DMINIMUM = distance_a1_a2 - distance_a2_a3
                        #self.builder.get_object('entry_param_DMINIMUM1').set_text(str(DMINIMUM))
                        
                        print "\n\nSigma pk1_pk3 ", self.sigma_pk1_pk3
                        print "Sigma pk3_pk1", self.sigma_pk3_pk1
                        #print "Estimated minimum distance",  DMINIMUM			
		    '''
		except:
                    cmd.edit_mode()
                    print "pk1, pk2 and pk3 selections not found"	
                    #print texto_d2d1	
                    return			
                print name3, name2, name1
                self.builder.get_object("entry_coord2_ATOM1"     ).set_text(str(atom1_index))
                self.builder.get_object("entry_coord2_ATOM1_name").set_text(name1)
                self.builder.get_object("entry_coord2_ATOM2"     ).set_text(str(atom2_index))
                self.builder.get_object("entry_coord2_ATOM2_name").set_text(name2)
                self.builder.get_object("entry_coord2_ATOM3"     ).set_text(str(atom3_index))
                self.builder.get_object("entry_coord2_ATOM3_name").set_text(name3)

    def ComboxChange(self, combobox):
        """ Function doc """
        #print combobox, combobox.get_active_text()
	if combobox == self.builder.get_object('combobox_reaction_coordiante_type1'):
            mode = self.builder.get_object('combobox_reaction_coordiante_type1').get_active_text()
            if mode == 'simple-distance':
                self.builder.get_object('label_coord1_atom3'      ).set_sensitive(False)
                self.builder.get_object('entry_coord1_ATOM3'      ).set_sensitive(False)
                self.builder.get_object('label_coord1_ATOM3_name' ).set_sensitive(False)
                self.builder.get_object('entry_coord1_ATOM3_name' ).set_sensitive(False)
            if mode == 'multiple-distance':
                self.builder.get_object('label_coord1_atom3'      ).set_sensitive(True)
                self.builder.get_object('entry_coord1_ATOM3'      ).set_sensitive(True)
                self.builder.get_object('label_coord1_ATOM3_name' ).set_sensitive(True)
                self.builder.get_object('entry_coord1_ATOM3_name' ).set_sensitive(True)

	if combobox == self.builder.get_object('combobox_reaction_coordiante_type2'):
            mode = self.builder.get_object('combobox_reaction_coordiante_type2').get_active_text()
            if mode == 'simple-distance':
                self.builder.get_object('label_coord2_atom3'      ).set_sensitive(False)
                self.builder.get_object('entry_coord2_ATOM3'      ).set_sensitive(False)
                self.builder.get_object('label_coord2_ATOM3_name' ).set_sensitive(False)
                self.builder.get_object('entry_coord2_ATOM3_name' ).set_sensitive(False)
            if mode == 'multiple-distance':
                self.builder.get_object('label_coord2_atom3'      ).set_sensitive(True)
                self.builder.get_object('entry_coord2_ATOM3'      ).set_sensitive(True)
                self.builder.get_object('label_coord2_ATOM3_name' ).set_sensitive(True)
                self.builder.get_object('entry_coord2_ATOM3_name' ).set_sensitive(True)

	if combobox == self.builder.get_object('combobox1'):
	    mode = combobox.get_active_text()
            
            if mode == 'Scan 1D':
		self.builder.get_object('vseparator1').hide()
		self.builder.get_object('vbox4').hide()
		self.refine_type = "1D"
            
            if mode == 'Scan 2D':
		self.builder.get_object('vseparator1').show()
		self.builder.get_object('vbox4').show()
		self.refine_type = '2D'

    def on_combobox1_changed(self, button):
        _type        = self.builder.get_object('combobox1').get_active_text()
        """ Function doc """
        if _type == 'folder - pDynamo':
            self.builder.get_object('filechooserbutton2').hide()
            self.builder.get_object('filechooserbutton1').show()
        else:
            self.builder.get_object('filechooserbutton2').show()
            self.builder.get_object('filechooserbutton1').hide()

    def geo_opt_change(self, widget):
        if self.builder.get_object('checkbutton_minimization').get_active():
            self.builder.get_object('vbox3').set_sensitive(True)
        
        else:
            self.builder.get_object('vbox3').set_sensitive(False)

    def __init__(self, EasyHybridSession = None):

        self.builder = gtk.Builder()
        if EasyHybridSession != None:
            self.project          = EasyHybridSession.project
            self.main_builder     = EasyHybridSession.builder
            self.window_control   = EasyHybridSession.window_control
            self.EasyHybridSession = EasyHybridSession
            self.EasyHybrid_ROOT   = EasyHybridSession.EasyHybrid_ROOT
            self.EasyHybrid_GUI    = EasyHybridSession.EasyHybrid_GUI 
            
            
            #      - - - importing ORCA PATH from EasyHybridConfig file. - - -        
            #-----------------------------------------------------------------------#
            try:                                                                    #
                ORCA                = EasyHybridSession.EasyHybridConfig['ORCAPATH']#
            except:                                                                 #
                ORCA = ''                                                           #
            #-----------------------------------------------------------------------#

        self.builder.add_from_file(
            os.path.join(self.EasyHybrid_GUI, 'DialogTrajectoryEnergyRefine','TrajectoryEnergyRefine.glade'))
                
        self.builder.connect_signals(self)
        self.dialog = self.builder.get_object('dialog1')

        self.window_control = WindowControl(self.builder)
        self.builder.get_object('filechooserbutton2').hide()
        
        self.builder.get_object('vseparator1').hide()
        self.builder.get_object('vbox4').hide()

        
        
        #----------------- Setup ComboBoxes -------------------------#
        combobox  = 'combobox1'         #
        
        combolist = ["Scan 1D", "Scan 2D"]#, "trj - AMBER", "dcd - CHARMM", 'xtc - GROMACS']
        self.window_control.SETUP_COMBOBOXES(combobox, combolist, 0)
        
        combobox  = 'combobox4'         #
        combolist = ["pkl", "xyz", 'pdb']#, "trj - AMBER", "dcd - CHARMM", 'xtc - GROMACS']
        self.window_control.SETUP_COMBOBOXES(combobox, combolist, 0)


        combobox = 'combobox_optimization_method'         #
        combolist = ['Conjugate Gradient', 'Steepest Descent','LBFGS']
        self.window_control.SETUP_COMBOBOXES(combobox, combolist,0)  
        
        combobox  = 'combobox_reaction_coordiante_type1'                     
        combolist = ['simple-distance', 'multiple-distance']
        self.window_control.SETUP_COMBOBOXES(combobox, combolist,0)  
        
	combobox  = 'combobox_reaction_coordiante_type2'                     
        combolist = ['simple-distance', 'multiple-distance']
        self.window_control.SETUP_COMBOBOXES(combobox, combolist,0)  
        
        self.refine_type = '1D'
        
        # QC SPIN MULTIPLICITY
        self.spinbutton = 'spinbutton2'
        config     = [0.0, 1.0,    500.0, 1.0, 0.0, 0.0]
        self.window_control.SETUP_SPINBUTTON(self.spinbutton, config)

        #if self.builder.get_object('check_opt_geometry'):
        self.builder.get_object('vbox3').set_sensitive(False)

        self.sigma_pk1_pk3 = None
        self.sigma_pk3_pk1 = None

    def Mass_weight_check(self, checkbutton):
        
        '''
        ----------------------------------------------------
                        REACTION COORDINATE 1 
        ----------------------------------------------------
        '''
        if checkbutton == self.builder.get_object('checkbutton_mass_weight'):
            try:
                name1, atom1_index, name2, atom2_index, distance_a1_a2 = import_ATOM1_ATOM2("pk1", "pk2")
                name2, atom2_index, name3, atom3_index, distance_a2_a3 = import_ATOM1_ATOM2("pk2", "pk3")
            except:
                print texto_d2d1
                return
                
            if self.builder.get_object("checkbutton_mass_weight").get_active():
                self.sigma_pk1_pk3, self.sigma_pk3_pk1 = compute_sigma_a1_a3 (name1, name3)
                
                """
                   R                    R
                    \                  /
                     A1--A2  . . . . A3
                    /                  \ 
                   R                    R
                     ^   ^            ^
                     |   |            |
                    pk1-pk2  . . . . pk3
                       d1       d2	
                
                q1 =  1 / (mpk1 + mpk3)  =  [ mpk1 * r (pk3_pk2)  -   mpk3 * r (pk1_pk2) ]
                
                """			
                #DMINIMUM =  (self.sigma_pk1_pk3 * distance_a1_a2) -(self.sigma_pk3_pk1 * distance_a2_a3*-1)
                #self.builder.get_object('entry_param_DMINIMUM1').set_text(str(DMINIMUM))
                print "\n\nUsing mass weighted restraints"
                print "Sigma pk1_pk3", self.sigma_pk1_pk3
                print "Sigma pk3_pk1", self.sigma_pk3_pk1
                #print "Estimated minimum distance",  DMINIMUM
                
            else:
                self.sigma_pk1_pk3 =  1.0
                self.sigma_pk3_pk1 = -1.0
                #DMINIMUM = distance_a1_a2 - distance_a2_a3
                #self.builder.get_object('entry_param_DMINIMUM1').set_text(str(DMINIMUM))
                print "\n\nSigma pk1_pk3 ", self.sigma_pk1_pk3
                print "Sigma pk3_pk1",      self.sigma_pk3_pk1
                #print "Estimated minimum distance",  DMINIMUM	
        

def main():
    dialog = TrajectoryEnergyRefineDialog()
    dialog.dialog.run()
    dialog.dialog.hide()
if __name__ == '__main__':
    main()
