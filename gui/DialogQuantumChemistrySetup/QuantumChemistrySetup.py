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
#from PyMOLScripts.PyMOLScripts import *
from WindowControl import *

#EasyHybrid_ROOT = os.environ.get('EasyHybrid_ROOT')
#EasyHybrid_GUI = os.path.join(EasyHybrid_ROOT, "gui")


dialog_text = {
    'error_topologies/Parameters': "Error: the topology, parameters or coordinates do not match the system type: ",
    'error_coordiantes': "Error: the coordinates do not match the loaded system.",
    'error_trajectory': "Error: the trajectory does not match the loaded system.",
    'delete': "Delete memory system.",
    'prune': "Warning: this is an irreversible process. Do you want to continue?",
    'qc_region': "Warning: no quantum region has been defined. Would you like to put all atoms in the quantum region?",
    'delete2': "Warning: there is a system loaded in memory. Are you sure that you want to delete it?"
}



# MNDO list - pDynamo semi empirical methods
mndo_list = ["am1",
			 "am1dphot",
			 "pm3",
			 "pm6",
			 "rm1",
			 #"chops",
			 #"recal"
             ]

SMO_Methods=['AM1'     ,
             'AM1dPhoT',
             'PM3'     ,
             'PM6'     ,
             'RM1'     ,
             #'CHOPS'   ,
             #'RECAL'   
             ]
                
SMO_Methods_Dic = {'AM1'     : "am1",
                   'AM1dPhoT': "am1dphot",
                   'PM3'     : "pm3",
                   'PM6'     : "pm6",
                   'RM1'     : "rm1",
                   #'CHOPS'   : "chops",
                   #'RECAL'   : "recal"
                   }

# DFT list - pDynamo DFT methods
DFT_Methods = ["DFT - demon, lda, 321g",
			   "DFT - demon, blyp, 321g",
			   "DFT - ahlrichs, lda, 631gs",
			   "DFT - ahlrichs, blyp, 631gs",
			   "DFT - weigend, lda, svp",
			   "DFT - weigend, blyp, svp"]

DFT_Methods_Dic = {"DFT - demon, lda, 321g"     : ['demon'   ,'lda'  , "321g" ],  
			       "DFT - demon, blyp, 321g"    : ['demon'   ,'blyp' , "321g" ], 
			       "DFT - ahlrichs, lda, 631gs" : ['ahlrichs','lda'  , "631gs"],
			       "DFT - ahlrichs, blyp, 631gs": ['ahlrichs','blyp' , "631gs"],
			       "DFT - weigend, lda, svp"    : ['weigend' ,'lda'  , "svp"  ],
			       "DFT - weigend, blyp, svp"   : ['weigend' ,'blyp' , "svp"  ]}






# ORCA config - abinitio methods
ORCA_Method = ['ab initio using ORCA']

HF_list = ["HF - Hartree-Fock",
		   "MP2"]

KS_list = ["LDA    - Local density approximation"                     ,
		   "BLYP   - Becke '88 exchange and Lee-Yang-Parr correlation",
		   "mPWPW  - Modified PW exchange and PW correlation"         ,
		   "mPWLYP - Modified PW exchange and LYP correlation"        ,
		   
		   "TPSSh - The hybrid version of TPSS"                       ,
   
		   "B3LYP - The popular B3LYP functional (20% HF exchange"   ,
		   "B3PW - The three parameter hybrid version of PW91"       ,
		   "PW1PW - One parameter hybrid version of PW91"            ,
		   "mPW1PW - One parameter hybrid version of mPWPW"          ,
		   "mPW1LYP - One parameter hybrid version of mPWLYP"        ,
		   "PBE0 - One parameter hybrid version of PBE"]

BASIS_ORCA =["3-21G Pople 3-21G",
             "3-21GSP Buenker 3-21GSP",
             "4-22GSP Buenker 4-22GSP",
             "6-31G Pople 6-31G and its modifications",
             "6-311G Pople 6-311G and its modifications"]

POLARIZATION_ORCA = ["No",
                     "*",
                     "**",
                     "(2d)",
                     "(2d,2p)",
                     "(2df)",
                     "(2df,2pd)",
                     "(3df)",
                     "(3df,3pd)"]

DIFFUSE_ORCA = ["No",
                "+",
                "++"]
                
SCF_ORCA = ["NORMALSCF",
            "LOOSESCF",
            "SLOPPYSCF",
            "STRONGSCF",
            "TIGHTSCF",
            "VERYTIGHTSCF",
            "EXTREMESCF",
            "SCFCONV6",
            "SCFCONV7",
            "SCFCONV8",	
            "SCFCONV9",
            "SCFCONV10"]






                
class QuantumChemistrySetupDialog():

    """ Class doc """
    def SetQCParameters (self, button):
        """Function doc """
        self.project          = self.EasyHybridSession.project

        qc_table      = self.project.settings['qc_table']                                                     

        if self.project.system == None:
            return "system empty"


                                                 #  Message Dialog                   
        #-----------------------------------------------------------------------------------------------------#
        if qc_table == []:                                                                                    #
                                             #  -  I M P O R T A N T  -  #                                    #
                                #---------------------------------------------------------#                   #
                                #                                                         #                   #
                                #		 Message Dialog  -  when 2 buttons will be showed #                   #
                                #  1 -create the warning message                          #                   #
                                #  2 -hide the actual dialog - optional                   #                   #
                                #  3 -show the message dialog                             #                   #
                                #  4 -hide the message dialog                             #                   #
                                #  5 -check the returned valor by the message dialog      #                   #
                                #  6 -do something                                        #                   #
                                #  7 -restore the actual dialog - optional	              #                   #
                                #---------------------------------------------------------#                   #
            # 1 step                                                                                          #
            self.builder.get_object('MessageDialogQuestion').format_secondary_text(dialog_text['qc_region'])  #
            dialog = self.builder.get_object('MessageDialogQuestion')                                         #
                                                                                                              #
            a = dialog.run()  # possible "a" valors                                                           #
            # 4 step          #	-8  -  yes                                                                    #
            dialog.hide()     #	-9  -  no                                                                     #
                              #	-4  -  close                                                                  #
                              # -5  -  OK                                                                     #
                              # -6  -  Cancel                                                                 #
                                                                                                              #
            # 5 step                                                                                          #
            if a == -8:                                                                                       #
                # 6 step                                                                                      #
                pass                                                                                          #
            else:                                                                                             #
                return 0                                                                                      #
            # 7 step                                                                                          #
            #self.load_trj_windows.run()                                                                      #
        else:                                                                                                 #
            print qc_table                                                                                    #
        #-----------------------------------------------------------------------------------------------------#






        qc_method       = self.builder.get_object('combobox1').get_active_text()
        charge          = self.builder.get_object('spinbutton_charge').get_value_as_int()
        multiplicity    = self.builder.get_object('spinbutton_multiplicity').get_value_as_int()        

        if qc_method in SMO_Methods:
            print SMO_Methods_Dic[qc_method]
            self.project.set_qc_parameters_MNDO(SMO_Methods_Dic[qc_method], charge, multiplicity)
        
        if qc_method in DFT_Methods:
            print DFT_Methods_Dic[qc_method]
            density_tol     = self.builder.get_object('DFT_density_tolerance_entry').get_text()
            Maximum_SCF     = self.builder.get_object('DFT_Maximum_SCF_entry2').get_text()        
            densityBasis    = DFT_Methods_Dic[qc_method][0]
            functional      = DFT_Methods_Dic[qc_method][1]
            orbitalBasis    = DFT_Methods_Dic[qc_method][2] 
            self.project.set_qc_parameters_DFT (qc_method, charge,       multiplicity, density_tol, 
                                              Maximum_SCF, densityBasis, functional,   orbitalBasis)
        
        if qc_method in ORCA_Method:
            print ORCA_Method[0]
            ORCA_method       = self.builder.get_object('combobox1_ORCA_method'      ).get_active_text()
            ORCA_SCF          = self.builder.get_object('combobox2_ORCA_SCF'         ).get_active_text()
            ORCA_basis        = self.builder.get_object('combobox3_ORCA_basis'       ).get_active_text()
            ORCA_POLARIZATION = self.builder.get_object('combobox2_ORCA_POLARIZATION').get_active_text()
            ORCA_DIFFUSE      = self.builder.get_object('combobox2_ORCA_DIFFUSE'     ).get_active_text()
            ORCA_PATH         = self.builder.get_object('ORCA_entry_command'         ).get_text()
            
            if self.builder.get_object('ORCA_radiobutton_restrict'):
                print 'radiobutton_restrict = True'
            else:
                print 'radiobutton_restrict = False'
            
            PAL              = self.builder.get_object('SpinButton1_ORCA_pal').get_value_as_int()
            ORCA_String      = self.builder.get_object('ORCA_entry_keywords').get_text()
            
            
            
            self.project.set_qc_parameters_ORCA(charge = charge       , 
                                          multiplicity = multiplicity , 
                                              qc_table = qc_table     , 
                                           ORCA_String = ORCA_String  ,        
                                                   PAL = PAL          ,
                                             ORCA_PATH = ORCA_PATH)        
        
        self.project.settings['charge']        = charge
        self.project.settings['multiplicity']  = multiplicity	


    def QCcomboxChange(self, combobox):
        """ Function doc """
        mode = self.builder.get_object('combobox1').get_active_text()
        
        if mode == 'ab initio using ORCA':
            self.builder.get_object('06_window_alignment3_ORCA').show()
            self.builder.get_object('06_window_alignment3_ORCA2').show()
            self.builder.get_object('alignment3').show()
            self.builder.get_object('06_window_alignment3_ORCA1').hide()
        if mode in DFT_Methods:
            self.builder.get_object('06_window_alignment3_ORCA').hide()
            self.builder.get_object('alignment3').hide()
            self.builder.get_object('06_window_alignment3_ORCA2').hide()
            self.builder.get_object('06_window_alignment3_ORCA1').show() 
            self.builder.get_object('DFT_density_tolerance_entry').set_sensitive(True)
            self.builder.get_object('DFT_Maximum_SCF_entry2').set_sensitive(True)
            self.builder.get_object('06_window_label78_ORCA1').set_sensitive(True)
            self.builder.get_object('06_window_label75_ORCA1').set_sensitive(True)
        if mode in SMO_Methods:
            self.builder.get_object('06_window_alignment3_ORCA').hide()
            self.builder.get_object('06_window_alignment3_ORCA2').hide()
            self.builder.get_object('alignment3').hide()
            self.builder.get_object('06_window_alignment3_ORCA1').show() 
            self.builder.get_object('DFT_density_tolerance_entry').set_sensitive(False)
            self.builder.get_object('DFT_Maximum_SCF_entry2').set_sensitive(False) 
            self.builder.get_object('06_window_label78_ORCA1').set_sensitive(False)
            self.builder.get_object('06_window_label75_ORCA1').set_sensitive(False)
    
	
    def save_ORCAPATH(self, widget):
        """ Function doc """
        self.EasyHybridSession.EasyHybridConfig['ORCAPATH'] = self.builder.get_object('ORCA_entry_command').get_text()
        self.EasyHybridSession.Save_EasyHybrid_ConfigFile()
    
    def ORCA_check_parameters(self, widget):
        """ Function doc """
        orca_method = self.builder.get_object('combobox1_ORCA_method'      ).get_active_text()
        orca_scf    = self.builder.get_object('combobox2_ORCA_SCF'         ).get_active_text()
        orca_basis  = self.builder.get_object('combobox3_ORCA_basis'       ).get_active_text()
        orca_pol    = self.builder.get_object('combobox2_ORCA_POLARIZATION').get_active_text()
        orca_diff   = self.builder.get_object('combobox2_ORCA_DIFFUSE'     ).get_active_text()
        orca_restriciton = None

        if  self.builder.get_object("ORCA_radiobutton_restrict").get_active():
            if orca_method in KS_list:
                orca_restriciton = "RKS"
            if orca_method in HF_list:
                orca_restriciton = "RHF"

        if  self.builder.get_object("ORCA_radiobutton_unrestrict").get_active():
            if orca_method in KS_list:
                orca_restriciton = "UKS"
            if orca_method in HF_list:
                orca_restriciton = "UHF"

        orca_method2 = orca_method.split()
        orca_method2 = orca_method2[0]
            
        orca_basis2 = orca_basis.split()
        orca_basis2 = orca_basis2[0]

        if orca_diff != "No":
            orca_basis2 = orca_basis2.split("G")
            orca_basis2 = orca_basis2[0] + orca_diff + "G"
        if orca_pol != "No":
            orca_basis2 = orca_basis2 + orca_pol
            
        orca_string = orca_method2 +' '+ orca_basis2 +' '+ orca_scf +' '+ orca_restriciton +' CHELPG'

        self.builder.get_object("ORCA_entry_keywords").set_text(orca_string)


    def __init__(self, EasyHybridSession = None):
        ''''''

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
                ORCA                  = EasyHybridSession.EasyHybridConfig['ORCAPATH']#
            except:                                                                 #
                ORCA = ''                                                           #
            #-----------------------------------------------------------------------#


        self.builder.add_from_file(
            os.path.join(self.EasyHybrid_GUI, 'DialogQuantumChemistrySetup',  'QuantumChemistrySetupDialog.glade'))
        
        self.builder.add_from_file(
            os.path.join(self.EasyHybrid_GUI, 'MessageDialogQuestion.glade'))
                
        self.builder.connect_signals(self)
        self.dialog = self.builder.get_object('dialog1')
        
        
        #self.builder.get_object('06_window_alignment3_ORCA1').hide()
        self.builder.get_object('06_window_alignment3_ORCA').hide()
        self.builder.get_object('06_window_alignment3_ORCA2').hide()
        
        if ORCA == None:
			ORCA = ''
        
        self.builder.get_object('ORCA_entry_command').set_text(ORCA)
        
        '''
		--------------------------------------------------
		-                                                -
		-	              WindowControl                  -
		-                                                -
		--------------------------------------------------
		'''
        self.window_control = WindowControl(self.builder)
       
        #--------------------- Setup ComboBoxes -------------------------
        combobox  = 'combobox1'                                           
        combolist = SMO_Methods + DFT_Methods + ORCA_Method # = ORCA_Method = ['ab initio using ORCA'] 
        self.window_control.SETUP_COMBOBOXES(combobox, combolist, 0)     
                                                                         
        combobox  = 'combobox1_ORCA_method'                     
        combolist = HF_list + KS_list                                    
        self.window_control.SETUP_COMBOBOXES(combobox, combolist, 0)     
                                                                         
        combobox  = 'combobox2_ORCA_SCF'                        
        combolist = SCF_ORCA                                             
        self.window_control.SETUP_COMBOBOXES(combobox, combolist, 0)     
       
        combobox  = 'combobox3_ORCA_basis'                      
        combolist = BASIS_ORCA                                           
        self.window_control.SETUP_COMBOBOXES(combobox, combolist, 0)         
        
        combobox  = 'combobox2_ORCA_POLARIZATION'                        
        combolist = POLARIZATION_ORCA                                             
        self.window_control.SETUP_COMBOBOXES(combobox, combolist, 0)     

        combobox  = 'combobox2_ORCA_DIFFUSE'                        
        combolist = DIFFUSE_ORCA                                             
        self.window_control.SETUP_COMBOBOXES(combobox, combolist, 0)
        
        # QC SPIN CHARGE
        spinbutton = 'spinbutton_charge'
        config     = [0.0, -500.0, 500.0, 1.0, 0.0, 0.0]
        self.window_control.SETUP_SPINBUTTON(spinbutton, config)

        # QC SPIN MULTIPLICITY
        spinbutton = 'spinbutton_multiplicity'
        config     = [0.0, 1.0,    500.0, 1.0, 0.0, 0.0]
        self.window_control.SETUP_SPINBUTTON(spinbutton, config)
       
        # QC SPIN PAL - ORCA ONY
        spinbutton = 'SpinButton1_ORCA_pal'                        
        config     = [0.0, 1.0, 500.0, 1.0, 0.0, 0.0]       
        self.window_control.SETUP_SPINBUTTON(spinbutton, config)


        self.builder.get_object('combobox1_ORCA_method'      ).connect("changed", self.ORCA_check_parameters)
        self.builder.get_object('combobox2_ORCA_SCF'         ).connect("changed", self.ORCA_check_parameters)
        self.builder.get_object('combobox3_ORCA_basis'       ).connect("changed", self.ORCA_check_parameters)
        self.builder.get_object('combobox2_ORCA_POLARIZATION').connect("changed", self.ORCA_check_parameters)
        self.builder.get_object('combobox2_ORCA_DIFFUSE'     ).connect("changed", self.ORCA_check_parameters)
        self.builder.get_object("ORCA_radiobutton_restrict"  ).connect("toggled", self.ORCA_check_parameters)
        self.builder.get_object("ORCA_radiobutton_unrestrict").connect("toggled", self.ORCA_check_parameters)
        #----------------------------------------------------------------
        

def main():
    dialog = QuantumChemistrySetupDialog()
    dialog.dialog.run()
    dialog.dialog.hide()
if __name__ == '__main__':
    main()
