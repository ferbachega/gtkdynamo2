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
from PyMOLScripts.PyMOLScripts import *
from WindowControl import *
from pDynamoMethods.pDynamoScan   import *

#EasyHybrid_ROOT = os.getcwd()
EasyHybrid_ROOT = os.environ.get('EasyHybrid_ROOT')

EasyHybrid_GUI = os.path.join(EasyHybrid_ROOT, "gui")

texto_d1   = "\n\n                       -- simple-distance --\n\nFor simple-distance, select two atoms in pymol using the editing mode\nfollowing the diagram:\n\n   R                    R\n    \                  /\n     A1--A2  . . . . A3\n    /                  \ \n   R                    R\n         ^            ^\n         |            |\n        pk1  . . . . pk2\n                d1\n"
texto_d2d1 = "\n                       -- multiple-distance --\n\nFor multiple-distance, select three atoms in pymol using the editing mode\nfollowing the diagram:\n\n   R                    R\n    \                  /\n     A1--A2  . . . . A3\n    /                  \ \n   R                    R\n     ^   ^            ^\n     |   |            |\n    pk1-pk2  . . . . pk3\n       d1       d2\n"




                
class ScanWindow():
    """ Class doc """
    def  on_ScanWindow_destroy(self, widget):
        """ Function doc """
        self.Visible  =  False


    def RunScan(self, button):
        #------------------------------------- importing parameters -----------------------------------------------#
        DINCREMENT    = float(self.builder.get_object('ScanDialog_SCAN_entry_STEP_SIZE4').get_text())              #
        NWINDOWS      = int  (self.builder.get_object('ScanDialog_SCAN_entry_NWINDOWS4').get_text())               #
        DMINIMUM      = float(self.builder.get_object('ScanDialog_SCAN_entry_param_DMINIMUM').get_text())          #
        FORCECONSTANT = float(self.builder.get_object('ScanDialog_SCAN_entry_FORCE4').get_text())                  #
                                                                                                                   #
        max_int       = int(self.builder.get_object  ("ScanDialog_SCAN_mim_param_entry_max_int1").get_text())      #
        rms_grad      = float(self.builder.get_object("ScanDialog_SCAN_mim_param_entry_rmsd_grad1").get_text())    #
        mim_method	  = self.builder.get_object      ('ScanDialog_combobox_optimization_method').get_active_text() #
        log_freq      = None                                                                                       #
        data_path     = self.EasyHybridSession.project.settings['data_path']                                        #
        #----------------------------------------------------------------------------------------------------------#



        #-----------------------------------import trajectory parameters--------------------------------------------#
        traj            = self.builder.get_object('ScanDialog_SCAN_entry_trajectory_name').get_text()               #
        if not os.path.exists (os.path.join(data_path, traj)): os.mkdir (os.path.join(data_path, traj))             #
        outpath = os.path.join(data_path, traj)                                                                     #
        #-----------------------------------------------------------------------------------------------------------#



        mode        = self.builder.get_object('ScanDialog_combobox_SCAN_reaction_coordiante_type').get_active_text()
        print "\n\n"
        print mode 

        self.EasyHybridSession.project.ActiveModeCheck()
        #-------------------------------------------------------------------------------------------------#
        #                                       simple-distance                                           #
        #-------------------------------------------------------------------------------------------------#
        if mode == "simple-distance":                                                                     #
            ATOM1      = int(self.builder.get_object('ScanDialog_SCAN_entry_cood1_ATOM1').get_text())     #
            ATOM1_name = self.builder.get_object    ('ScanDialog_SCAN_entry_cood1_ATOM1_name').get_text() #
            ATOM2      = int(self.builder.get_object('ScanDialog_SCAN_entry_cood1_ATOM2').get_text())     #
            ATOM2_name = self.builder.get_object    ('ScanDialog_SCAN_entry_cood1_ATOM2_name').get_text() #
                                                                                                          #
            parameters = {'method'       : mim_method,
                          'outpath'      : outpath,                                                       #
                          'ATOM1'        : ATOM1,                                                         #
                          'ATOM1_name'   : ATOM1_name,                                                    #
                          'ATOM2'        : ATOM2,                                                         #
                          'ATOM2_name'   : ATOM2_name,		                                              #
                          'DINCREMENT'   : DINCREMENT,                                                    #
                          'NWINDOWS'     : NWINDOWS,                                                      #
                          'FORCECONSTANT': FORCECONSTANT,                                                 #
                          'DMINIMUM'     : DMINIMUM,                                                      #
                          'max_int'      : max_int,                                                       #
                          'log_freq'     : log_freq,                                                      #
                          'rms_grad'     : rms_grad,                                                      #
                          'mim_method'   : mim_method,                                                    #
                          'data_path'    : data_path  }                                                   #
            x, y, logFile = ScanSimpleDistance(parameters, self.EasyHybridSession.project)                 #
        #-------------------------------------------------------------------------------------------------#



        #-------------------------------------------------------------------------------------------------#
        #                                      multiple-distance                                          #
        #-------------------------------------------------------------------------------------------------#
        if mode == "multiple-distance":                                                                   #
            ATOM1      = int(self.builder.get_object('ScanDialog_SCAN_entry_cood1_ATOM1').get_text())     #
            ATOM1_name = self.builder.get_object    ('ScanDialog_SCAN_entry_cood1_ATOM1_name').get_text() #
            ATOM2      = int(self.builder.get_object('ScanDialog_SCAN_entry_cood1_ATOM2').get_text())     #
            ATOM2_name = self.builder.get_object    ('ScanDialog_SCAN_entry_cood1_ATOM2_name').get_text() #
            ATOM3      = int(self.builder.get_object('ScanDialog_SCAN_entry_cood1_ATOM3').get_text())     #
            ATOM3_name = self.builder.get_object    ('ScanDialog_SCAN_entry_cood1_ATOM3_name').get_text() #
                                                                                                          #
            mass_weight= self.builder.get_object("ScanDialog_scan_checkbutton_mass_weight").get_active() 
                        
            print "  "+ATOM1_name+"   ->-  "+ATOM2_name+"  -->-- "+ATOM3_name+"  "                        #
            print " pk1 --- pk2 ---- pk3 \n"                                                              #
            print "DMINIMUM  : ",DMINIMUM                                                                 #
            print "\n\n"						                                                          #
            print                                                                                         #
            sigma_pk1_pk3 = self.sigma_pk1_pk3                                                            #
            sigma_pk3_pk1 = self.sigma_pk3_pk1                                                            #
            print sigma_pk3_pk1                                                                           #
            print sigma_pk1_pk3                                                                           #
                                                                                                          #
            parameters = {'method'       : mim_method,                                                    #
                          'outpath'      : outpath,                                                       #
                          'ATOM1'        : ATOM1,                                                         #
                          'ATOM1_name'   : ATOM1_name,                                                    #
                          'ATOM2'        : ATOM2,                                                         #
                          'ATOM2_name'   : ATOM2_name,		                                              #
                          'ATOM3'        : ATOM3,                                                         #
                          'ATOM3_name'   : ATOM3_name,                                                    #
                          'DINCREMENT'   : DINCREMENT,                                                    #
                          'NWINDOWS'     : NWINDOWS,                                                      #
                          'FORCECONSTANT': FORCECONSTANT,                                                 #
                          'DMINIMUM'     : DMINIMUM,                                                      #
                          'sigma_pk1_pk3': sigma_pk1_pk3,                                                 #
                          'sigma_pk3_pk1': sigma_pk3_pk1,                                                 #
                          'max_int'      : max_int,                                                       #
                          'log_freq'     : log_freq,                                                      #
                          'rms_grad'     : rms_grad,                                                      #
                          'mim_method'   : mim_method,                                                    #
                          'mass_weight'  : mass_weight,                                                   #
                          'data_path'    : data_path  }                                                   #
                                                                                                          #
                                                                                                          #
            x, y, logFile = ScanMultipleDistances(parameters, self.EasyHybridSession.project)              #
        #-------------------------------------------------------------------------------------------------#
        self.EasyHybridSession.project.From_PDYNAMO_to_EasyHybrid(type_='scn', log =  logFile)
        
        self.BackUpWindowData()
        self.Visible  =  False
        self.window.destroy()
        return x, y, 

    def ScanDialog_ImportFromPyMOL(self, button):
        mode        =  self.builder.get_object('ScanDialog_combobox_SCAN_reaction_coordiante_type').get_active_text()
        
        if mode == "simple-distance":
            try:
                name1, atom1_index, name2, atom2_index, distance_a1_a2 = import_ATOM1_ATOM2("pk1", "pk2")
                distance_a1_a2 = str(distance_a1_a2)
                self.builder.get_object('ScanDialog_SCAN_entry_param_DMINIMUM').set_text(distance_a1_a2)

                self.builder.get_object("ScanDialog_SCAN_entry_cood1_ATOM1").set_text(str(atom1_index))
                self.builder.get_object("ScanDialog_SCAN_entry_cood1_ATOM1_name").set_text(name1)
                self.builder.get_object("ScanDialog_SCAN_entry_cood1_ATOM2").set_text(str(atom2_index))
                self.builder.get_object("ScanDialog_SCAN_entry_cood1_ATOM2_name").set_text(name2)
            
                self.atom1_index = atom1_index
                self.name1       = name1      
                self.atom2_index = atom2_index
                self.name2       = name2      
            
            
            except:
                cmd.edit_mode()
                print "pk1 and pk2 selections not found"					
                print texto_d1
                return	
		
        if mode == "multiple-distance":			
            try:
                name1, atom1_index, name2, atom2_index, distance_a1_a2 = import_ATOM1_ATOM2("pk1", "pk2")
                name2, atom2_index, name3, atom3_index, distance_a2_a3 = import_ATOM1_ATOM2("pk2", "pk3")

                print "distance between atom 1 and atom 2: ",distance_a1_a2
                print "distance between atom 2 and atom 3: ",distance_a2_a3
                
                if self.builder.get_object("ScanDialog_scan_checkbutton_mass_weight").get_active():
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
                    
                    DMINIMUM =  (self.sigma_pk1_pk3 * distance_a1_a2) -(self.sigma_pk3_pk1 * distance_a2_a3*-1)
                    self.builder.get_object('ScanDialog_SCAN_entry_param_DMINIMUM').set_text(str(DMINIMUM))
                    print "\n\nUsing mass weighted restraints"
                    print "Sigma pk1_pk3", self.sigma_pk1_pk3
                    print "Sigma pk3_pk1", self.sigma_pk3_pk1
                    print "Estimated minimum distance",  DMINIMUM
                    
                else:
                    self.sigma_pk1_pk3 =  1.0
                    self.sigma_pk3_pk1 = -1.0
                    DMINIMUM = distance_a1_a2 - distance_a2_a3
                    self.builder.get_object('ScanDialog_SCAN_entry_param_DMINIMUM').set_text(str(DMINIMUM))
                    
                    print "\n\nSigma pk1_pk3 ", self.sigma_pk1_pk3
                    print "Sigma pk3_pk1", self.sigma_pk3_pk1
                    print "Estimated minimum distance",  DMINIMUM			
            except:
                cmd.edit_mode()
                print "pk1, pk2 and pk3 selections not found"	
                print texto_d2d1	
                return			
            print name3, name2, name1
            self.builder.get_object("ScanDialog_SCAN_entry_cood1_ATOM1").set_text(str(atom1_index))
            self.builder.get_object("ScanDialog_SCAN_entry_cood1_ATOM1_name").set_text(name1)
            self.builder.get_object("ScanDialog_SCAN_entry_cood1_ATOM2").set_text(str(atom2_index))
            self.builder.get_object("ScanDialog_SCAN_entry_cood1_ATOM2_name").set_text(name2)
            self.builder.get_object("ScanDialog_SCAN_entry_cood1_ATOM3").set_text(str(atom3_index))
            self.builder.get_object("ScanDialog_SCAN_entry_cood1_ATOM3_name").set_text(name3)
                    
    def Mass_weight_check(self):
        try:
            name1, atom1_index, name2, atom2_index, distance_a1_a2 = import_ATOM1_ATOM2("pk1", "pk2")
            name2, atom2_index, name3, atom3_index, distance_a2_a3 = import_ATOM1_ATOM2("pk2", "pk3")
        except:
            print texto_d2d1
            return
            
        if self.builder.get_object("ScanDialog_scan_checkbutton_mass_weight").get_active():
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
            DMINIMUM =  (self.sigma_pk1_pk3 * distance_a1_a2) -(self.sigma_pk3_pk1 * distance_a2_a3*-1)
            self.builder.get_object('ScanDialog_SCAN_entry_param_DMINIMUM').set_text(str(DMINIMUM))
            print "\n\nUsing mass weighted restraints"
            print "Sigma pk1_pk3", self.sigma_pk1_pk3
            print "Sigma pk3_pk1", self.sigma_pk3_pk1
            print "Estimated minimum distance",  DMINIMUM
            
        else:
            self.sigma_pk1_pk3 =  1.0
            self.sigma_pk3_pk1 = -1.0
            DMINIMUM = distance_a1_a2 - distance_a2_a3
            self.builder.get_object('ScanDialog_SCAN_entry_param_DMINIMUM').set_text(str(DMINIMUM))
            print "\n\nSigma pk1_pk3 ", self.sigma_pk1_pk3
            print "Sigma pk3_pk1", self.sigma_pk3_pk1
            print "Estimated minimum distance",  DMINIMUM	

    def on_ScanDialog_checkbutton_MassWeight (self, checkbutton):
        """ Function doc """
        print 'checkbutton_MassWeight'
        self.Mass_weight_check()
        
    def ScanComboxChange(self, combobox):
        """ Function doc """
        mode = self.builder.get_object('ScanDialog_combobox_SCAN_reaction_coordiante_type').get_active_text()
        if mode == 'simple-distance':
            self.builder.get_object('ScanDialog_SCAN_label_coord1_atom3').set_sensitive(False)
            self.builder.get_object('ScanDialog_SCAN_entry_cood1_ATOM3').set_sensitive(False)
            self.builder.get_object('ScanDialog_SCAN_label_cood1_ATOM3_name').set_sensitive(False)
            self.builder.get_object('ScanDialog_SCAN_entry_cood1_ATOM3_name').set_sensitive(False)
            self.builder.get_object('ScanDialog_scan_checkbutton_mass_weight').set_sensitive(False)
            self.distanceType = 0
        if mode == 'multiple-distance':
            self.builder.get_object('ScanDialog_SCAN_label_coord1_atom3').set_sensitive(True)
            self.builder.get_object('ScanDialog_SCAN_entry_cood1_ATOM3').set_sensitive(True)
            self.builder.get_object('ScanDialog_SCAN_label_cood1_ATOM3_name').set_sensitive(True)
            self.builder.get_object('ScanDialog_SCAN_entry_cood1_ATOM3_name').set_sensitive(True)
            self.builder.get_object('ScanDialog_scan_checkbutton_mass_weight').set_sensitive(True)
            self.distanceType = 1
    
    def BackUpWindowData (self):
        """ Function doc """
        
        mode = self.builder.get_object('ScanDialog_combobox_SCAN_reaction_coordiante_type').get_active_text()
        if mode == 'simple-distance':
            self.distanceType = 0
        if mode == 'multiple-distance':
            self.distanceType = 1
        #---------------------------------------------------------------------------------------------------------#
        self.atom1_index = self.builder.get_object('ScanDialog_SCAN_entry_cood1_ATOM1')     .get_text()           #
        self.name1       = self.builder.get_object('ScanDialog_SCAN_entry_cood1_ATOM1_name').get_text()           #
        self.atom2_index = self.builder.get_object('ScanDialog_SCAN_entry_cood1_ATOM2')     .get_text()           #
        self.name2       = self.builder.get_object('ScanDialog_SCAN_entry_cood1_ATOM2_name').get_text()           #
        self.atom3_index = self.builder.get_object('ScanDialog_SCAN_entry_cood1_ATOM3')     .get_text()           #
        self.name3       = self.builder.get_object('ScanDialog_SCAN_entry_cood1_ATOM3_name').get_text()           #
        #---------------------------------------------------------------------------------------------------------#

        #---------------------------------------------------------------------------------------------------------#
        self._mass_weight_check = self.builder.get_object("ScanDialog_scan_checkbutton_mass_weight").get_active() #
        #---------------------------------------------------------------------------------------------------------#


        #------------------------------------- importing parameters ----------------------------------------------#
        self.DINCREMENT    = self.builder.get_object('ScanDialog_SCAN_entry_STEP_SIZE4')    .get_text()           #
        self.NWINDOWS      = self.builder.get_object('ScanDialog_SCAN_entry_NWINDOWS4')     .get_text()           #
        self.FORCECONSTANT = self.builder.get_object('ScanDialog_SCAN_entry_FORCE4')        .get_text()           #
        self.DMINIMUM      = self.builder.get_object('ScanDialog_SCAN_entry_param_DMINIMUM').get_text()           #
        #---------------------------------------------------------------------------------------------------------#



        #---------------------------------------------------------------------------------------------------------#
        mim_method	       = self.builder.get_object('ScanDialog_combobox_optimization_method').get_active_text() #
        self.minitype      = 0                                                                                    #
                                                                                                                  #
        self.max_int       = self.builder.get_object("ScanDialog_SCAN_mim_param_entry_max_int1")  .get_text()     #
        self.rms_grad      = self.builder.get_object("ScanDialog_SCAN_mim_param_entry_rmsd_grad1").get_text()     #

    def PutBackUpWindowData (self):
        
        
        #""" Function doc """
        #mode = self.builder.get_object('ScanDialog_combobox_SCAN_reaction_coordiante_type').get_active_text()
        #if mode == 'simple-distance':
        #    self.distanceType = 0
        #if mode == 'multiple-distance':
        #    self.distanceType = 1
        #---------------------------------------------------------------------------------------------------------#
        self.builder.get_object('ScanDialog_SCAN_entry_cood1_ATOM1')     .set_text(str(self.atom1_index))         #
        self.builder.get_object('ScanDialog_SCAN_entry_cood1_ATOM1_name').set_text(str(self.name1      ))         #
        self.builder.get_object('ScanDialog_SCAN_entry_cood1_ATOM2')     .set_text(str(self.atom2_index))         #
        self.builder.get_object('ScanDialog_SCAN_entry_cood1_ATOM2_name').set_text(str(self.name2      ))         #
        self.builder.get_object('ScanDialog_SCAN_entry_cood1_ATOM3')     .set_text(str(self.atom3_index))         #
        self.builder.get_object('ScanDialog_SCAN_entry_cood1_ATOM3_name').set_text(str(self.name3      ))         #
        #---------------------------------------------------------------------------------------------------------#
        
        #---------------------------------------------------------------------------------------------------------#
        if self._mass_weight_check:                                                                               #
            self.builder.get_object("ScanDialog_scan_checkbutton_mass_weight").set_active(True)                   #
        #---------------------------------------------------------------------------------------------------------#


        #------------------------------------- importing parameters ----------------------------------------------#
        self.builder.get_object('ScanDialog_SCAN_entry_STEP_SIZE4')    .set_text(str(self.DINCREMENT   ))         #
        self.builder.get_object('ScanDialog_SCAN_entry_NWINDOWS4')     .set_text(str(self.NWINDOWS     ))         #
        self.builder.get_object('ScanDialog_SCAN_entry_FORCE4')        .set_text(str(self.FORCECONSTANT))         #
        self.builder.get_object('ScanDialog_SCAN_entry_param_DMINIMUM').set_text(str(self.DMINIMUM     ))         #
        #---------------------------------------------------------------------------------------------------------#
        
        #---------------------------------------------------------------------------------------------------------#
        #mim_method	       = self.builder.get_object('ScanDialog_combobox_optimization_method').get_active_text() #
        #self.minitype      = 0                                                                                   #
                                                                                                                  #
        self.builder.get_object("ScanDialog_SCAN_mim_param_entry_max_int1")  .set_text(str(self.max_int ))        #
        self.builder.get_object("ScanDialog_SCAN_mim_param_entry_rmsd_grad1").set_text(str(self.rms_grad))        #
        #---------------------------------------------------------------------------------------------------------#   
  
    def OpenWindow (self, text):
        """ Function doc """
        if self.Visible  ==  False:
            self.project          = self.EasyHybridSession.project
            self.builder = gtk.Builder()
            self.builder.add_from_file(
                os.path.join(EasyHybrid_GUI,'WindowScan1D', 'ScanWindow.glade'))
            
            self.builder.connect_signals(self)
            self.window = self.builder.get_object('ScanWindow')
            self.sigma_pk1_pk3 = None
            self.sigma_pk3_pk1 = None
            self.builder.get_object("ScanDialog_SCAN_entry_trajectory_name").set_text(text)
            
            
            '''
            --------------------------------------------------
            -                                                -
            -	              WindowControl                  -
            -                                                -
            --------------------------------------------------
            '''        
            self.window_control = WindowControl(self.builder)
           
            #--------------------- Setup ComboBoxes -------------------------
            combobox  = 'ScanDialog_combobox_SCAN_reaction_coordiante_type'                     
            combolist = ['simple-distance', 'multiple-distance']
            self.window_control.SETUP_COMBOBOXES(combobox, combolist, self.distanceType)     

            combobox  = 'ScanDialog_combobox_optimization_method'                     
            combolist = ['Conjugate Gradient', 'Steepest Descent','LBFGS']
            self.window_control.SETUP_COMBOBOXES(combobox, combolist, self.minitype )     
                                                                                                             
            
            self.window.show()                                               
            #                                                                
            self.builder.connect_signals(self)                                   
            
            self.Visible  =  True
            self.PutBackUpWindowData()
            gtk.main()
            #----------------------------------------------------------------

    def CloseWindow (self, button):
        """ Function doc """
        self.BackUpWindowData()
        self.window.destroy()

    def __init__(self, EasyHybridSession = None):
        """ Class initialiser """
        if EasyHybridSession != None:
            self.project          = EasyHybridSession.project
            self.main_builder     = EasyHybridSession.builder
            self.EasyHybridSession = EasyHybridSession        
            self.window_control   = EasyHybridSession.window_control
        
        self.atom1_index = ''
        self.name1       = ''
        self.atom2_index = ''
        self.name2       = ''
        self.atom3_index = ''
        self.name3       = ''


        self.distanceType  = 0
        self.DMINIMUM      = ''
        self.minitype      = 0

        self.DINCREMENT    = '0.1'
        self.NWINDOWS      = '10'
        self.FORCECONSTANT = '4000'
        self.max_int       = '500'
        self.rms_grad      = '0.1'
        
        self._mass_weight_check = False


        #self.project   =  project
        self.Visible    =  False

def main():
    dialog = ScanWindow()
    dialog.OpenWindow()
if __name__ == '__main__':
    main()
