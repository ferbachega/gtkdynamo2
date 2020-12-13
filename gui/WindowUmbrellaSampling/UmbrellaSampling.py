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
from pDynamoMethods.pDynamoUmbrellaSampling import *
from MatplotGTK.LogParse    import *

#EasyHybrid_ROOT = os.getcwd()
EasyHybrid_ROOT = ''
EasyHybrid_GUI  = ''

texto_d1   = "\n\n                       -- simple-distance --\n\nFor simple-distance, select two atoms in pymol using the editing mode\nfollowing the diagram:\n\n   R                    R\n    \                  /\n     A1--A2  . . . . A3\n    /                  \ \n   R                    R\n         ^            ^\n         |            |\n        pk1  . . . . pk2\n                d1\n"
texto_d2d1 = "\n                       -- multiple-distance --\n\nFor multiple-distance, select three atoms in pymol using the editing mode\nfollowing the diagram:\n\n   R                    R\n    \                  /\n     A1--A2  . . . . A3\n    /                  \ \n   R                    R\n     ^   ^            ^\n     |   |            |\n    pk1-pk2  . . . . pk3\n       d1       d2\n"


def get_frames_from_directory (directory =None, _type = 'pkl'):
    """ Function doc """
    Files    = os.listdir(directory)
    
    file_list = []
    x_max = 0
    y_max = 0
    for File in Files:
	File2 = File.split('.')
	if File2[-1] == _type:
	    file_list.append(File)
	    file3 = File2[0].split('_')
	    x = int(file3[-1])
	    y = int(file3[-2])
	    
	    if x > x_max:
		x_max = x
	    
	    if y > y_max:
		y_max = y

    print file_list
    print 'x_max =', x_max 
    print 'y_max =', y_max
    return file_list, x_max+1, y_max+1


class Umbrella2DSamplingWindow():
    """ Class doc """
    def  on_Window_destroy(self, widget):
        """ Function doc """
        self.Visible  =  False
    
    def ComboxChange(self, combobox):
        """ Function doc """                    
        if combobox == self.builder.get_object('combobox_reaction_coordiante_type1'):
            mode = self.builder.get_object('combobox_reaction_coordiante_type1').get_active_text()
            if mode == 'simple-distance':
                self.builder.get_object('label_coord1_atom3'      ).set_sensitive(False)
                self.builder.get_object('entry_coord1_ATOM3'      ).set_sensitive(False)
                self.builder.get_object('label_coord1_ATOM3_name' ).set_sensitive(False)
                self.builder.get_object('entry_coord1_ATOM3_name' ).set_sensitive(False)
                self.builder.get_object('checkbutton_mass_weight1').set_sensitive(False)
            if mode == 'multiple-distance':
                self.builder.get_object('label_coord1_atom3'      ).set_sensitive(True)
                self.builder.get_object('entry_coord1_ATOM3'      ).set_sensitive(True)
                self.builder.get_object('label_coord1_ATOM3_name' ).set_sensitive(True)
                self.builder.get_object('entry_coord1_ATOM3_name' ).set_sensitive(True)
                self.builder.get_object('checkbutton_mass_weight1').set_sensitive(True)
        
        if combobox == self.builder.get_object('combobox_reaction_coordiante_type2'):
            mode = self.builder.get_object('combobox_reaction_coordiante_type2').get_active_text()
            if mode == 'simple-distance':
                self.builder.get_object('label_coord2_atom3'      ).set_sensitive(False)
                self.builder.get_object('entry_coord2_ATOM3'       ).set_sensitive(False)
                self.builder.get_object('label_coord2_ATOM3_name' ).set_sensitive(False)
                self.builder.get_object('entry_coord2_ATOM3_name' ).set_sensitive(False)
                self.builder.get_object('checkbutton_mass_weight2').set_sensitive(False)
            if mode == 'multiple-distance':
                self.builder.get_object('label_coord2_atom3'      ).set_sensitive(True)
                self.builder.get_object('entry_coord2_ATOM3'       ).set_sensitive(True)
                self.builder.get_object('label_coord2_ATOM3_name' ).set_sensitive(True)
                self.builder.get_object('entry_coord2_ATOM3_name' ).set_sensitive(True)
                self.builder.get_object('checkbutton_mass_weight2').set_sensitive(True)

        if combobox == self.builder.get_object('combobox1'):
            mode = self.builder.get_object('combobox1').get_active_text()
            
            if mode == 'sequential':
                self.builder.get_object('scan2d_label_step_size1'                      ).show()
                self.builder.get_object('entry_STEP_size1'                             ).show()
                self.builder.get_object('13_window_scan2d_scam_label_step_Nwindows2'   ).show()
                self.builder.get_object('entry_NWINDOWS1'                              ).show()
                self.builder.get_object('13_window_scan2d_scam_label_step_trajectory3' ).show()
                self.builder.get_object('entry_param_DMINIMUM1'                        ).show()
                
                #self.builder.get_object('table3').show()
                self.builder.get_object('table1').hide()

            if mode == 'from trajectory':
                #self.builder.get_object('table3').hide()
                self.builder.get_object('scan2d_label_step_size1'                      ).hide()
                self.builder.get_object('entry_STEP_size1'                             ).hide()
                self.builder.get_object('13_window_scan2d_scam_label_step_Nwindows2'   ).hide()
                self.builder.get_object('entry_NWINDOWS1'                              ).hide()
                self.builder.get_object('13_window_scan2d_scam_label_step_trajectory3' ).hide()
                self.builder.get_object('entry_param_DMINIMUM1'                        ).hide()
                
                self.builder.get_object('table1').show()

    def fileChooser_logFile (self, widget):
	""" Function doc 
	parameters = {
		      1: {
			 'type'          : 'line'    ,   # line / matrix
			 'title'         : ''        ,   #
			 'X'             : []        ,   # X 
			 'Y'             : []        ,   # Y 
			 'xlabel'        : 'x label' ,   # xlabel,
			 'ylabel'        : 'y label' ,   # ylabel,
			 'energy_model'  : 'UNK'     ,
			 
			 
			 'c1_ATOM1_id'   : None      ,
			 'c1_ATOM2_id'   : None      ,
			 'c1_ATOM3_id'   : None      ,
					 
			 'c1_ATOM1_name' : None      ,
			 'c1_ATOM2_name' : None      ,
			 'c1_ATOM3_name' : None      ,
					 
			 'c2_ATOM1_id'   : None      ,
			 'c2_ATOM2_id'   : None      ,
			 'c2_ATOM3_id'   : None      ,
					 
			 'c2_ATOM1_name' : None      ,
			 'c2_ATOM2_name' : None      ,
			 'c2_ATOM3_name' : None      ,
			 
			 }

	
	REACTION_COORD1 = {'MODE'         : mode,                                                    
			   'ATOM1'        : int(self.builder.get_object("entry_coord1_ATOM1"     ).get_text()),                                                  
			   'ATOM1_name'   : self.builder.get_object    ("entry_coord1_ATOM1_name").get_text() ,                                           
			   'ATOM2'        : int(self.builder.get_object("entry_coord1_ATOM2"     ).get_text()),
			   'ATOM2_name'   : self.builder.get_object    ("entry_coord1_ATOM2_name").get_text() ,
			   'ATOM3'        : int(self.builder.get_object("entry_coord1_ATOM3"     ).get_text()),
			   'ATOM3_name'   : self.builder.get_object    ("entry_coord1_ATOM3_name").get_text() ,


	"""
	FileName = self.builder.get_object("filechooserbutton4").get_filename()
	parameters = ParseProcessLogFile(FileName)
	#print parameters

	if parameters[1]['c1_ATOM1_id']:
	    self.builder.get_object("entry_coord1_ATOM1").set_text(parameters[1]['c1_ATOM1_id'])
	    self.builder.get_object("entry_coord1_ATOM1_name").set_text(parameters[1]['c1_ATOM1_name'])



	if parameters[1]['c1_ATOM2_id']:
	    self.builder.get_object("entry_coord1_ATOM2").set_text(parameters[1]['c1_ATOM2_id'])
	    self.builder.get_object ("entry_coord1_ATOM2_name").set_text(parameters[1]['c1_ATOM2_name'])


	if parameters[1]['c1_ATOM3_id']:
	    self.builder.get_object("entry_coord1_ATOM3").set_text(parameters[1]['c1_ATOM3_id'])
	    self.builder.get_object ("entry_coord1_ATOM3_name").set_text(parameters[1]['c1_ATOM3_name'])
	    self.builder.get_object('combobox_reaction_coordiante_type1').set_active(1)
	else:                       #combobox_SCAN_reaction_coordiante_type
	    self.builder.get_object('combobox_reaction_coordiante_type1').set_active(0)


	if parameters[1]['c2_ATOM1_id']:
	    self.builder.get_object("entry_coord2_ATOM1").set_text(parameters[1]['c2_ATOM1_id'])
	    self.builder.get_object ("entry_coord2_ATOM1_name").set_text(parameters[1]['c2_ATOM1_name'])

	
	
	if parameters[1]['c2_ATOM2_id']:
	    self.builder.get_object("entry_coord2_ATOM2").set_text(parameters[1]['c2_ATOM2_id'])
	    self.builder.get_object ("entry_coord2_ATOM2_name").set_text(parameters[1]['c2_ATOM2_name'])

	
	
	if parameters[1]['c2_ATOM3_id']:
	    self.builder.get_object("entry_coord2_ATOM3").set_text(parameters[1]['c2_ATOM3_id'])
	    self.builder.get_object ("entry_coord2_ATOM3_name").set_text(parameters[1]['c2_ATOM3_name'])
	    self.builder.get_object('combobox_reaction_coordiante_type2').set_active(1)
	else:
	    self.builder.get_object('combobox_reaction_coordiante_type2').set_active(0)

    def checkbutton_Minimization (self, checkbutton):
        if self.builder.get_object("checkbutton_minimization").get_active():
            self.builder.get_object('table17').set_sensitive(True)
        else:
            self.builder.get_object('table17').set_sensitive(False)

    def RunUmbrellaSampling(self, button):
	print 'run!'
        trajectory          = self.builder.get_object("filechooserbutton1").get_filename()        #
        files, x_max, y_max = get_frames_from_directory( directory = trajectory)
	N_process           = self.builder.get_object("spinbutton1"       ).get_value_as_int()    #

        #---------------------------------- importing parameters COORD-1 ---------------------------#
	FORCECONSTANT_1 = float(self.builder.get_object('entry_FORCE1'         ).get_text())        
        mode            = self.builder.get_object('combobox_reaction_coordiante_type1').get_active_text()

	ATOM1      = int(self.builder.get_object("entry_coord1_ATOM1"     ).get_text())            
	ATOM1_name = self.builder.get_object    ("entry_coord1_ATOM1_name").get_text()             
	ATOM2      = int(self.builder.get_object("entry_coord1_ATOM2"     ).get_text())            
	ATOM2_name = self.builder.get_object    ("entry_coord1_ATOM2_name").get_text()             
	
        if mode == "multiple-distance":                                                            
            ATOM3      = int(self.builder.get_object("entry_coord1_ATOM3"     ).get_text())        
            ATOM3_name = self.builder.get_object    ("entry_coord1_ATOM3_name").get_text()         



	    if self.builder.get_object("checkbutton_mass_weight1").get_active():
		sigma_pk1_pk3, sigma_pk3_pk1 = compute_sigma_a1_a3 (name1, name3)
		
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
	    else:
		sigma_pk1_pk3 =  1.0
		sigma_pk3_pk1 = -1.0


            mass_weight = self.builder.get_object    ("checkbutton_mass_weight1").get_active()    

            print "  "+ATOM1_name+"   ->-  "+ATOM2_name+"  -->-- "+ATOM3_name+"  "               
            print " pk1 --- pk2 ---- pk3 \n"                                                     
            print "\n\n"						                         
            print                                                                                


	    #sigma_pk1_pk3 = self.sigma_pk1_pk3                                                   
            #sigma_pk3_pk1 = self.sigma_pk3_pk1                                                   
            print sigma_pk3_pk1                                                                  
            print sigma_pk1_pk3                                                                  
                                                                                                 
            REACTION_COORD1 = {'MODE'         : mode,                                            
                               'ATOM1'        : ATOM1,                                           
                               'ATOM1_name'   : ATOM1_name,                                      
                               'ATOM2'        : ATOM2,                                           
                               'ATOM2_name'   : ATOM2_name,		                         
                               'ATOM3'        : ATOM3,                                           
                               'ATOM3_name'   : ATOM3_name,                                      
                               'DINCREMENT'   : 0,                                      
                               'NWINDOWS'     : y_max,                                        
                               'FORCECONSTANT': FORCECONSTANT_1,                                   
                               'DMINIMUM'     : 0,                                        
                               'mass_weight'  : mass_weight,                                     
                               'sigma_pk1_pk3': sigma_pk1_pk3,                                   
                               'sigma_pk3_pk1': sigma_pk3_pk1}                                   


	    
	else:
	    REACTION_COORD1 = {'MODE'         : mode,                                              
                               'ATOM1'        : ATOM1,                                             
                               'ATOM1_name'   : ATOM1_name,                                        
                               'ATOM2'        : ATOM2,                                             
                               'ATOM2_name'   : ATOM2_name,		                           
                               'DINCREMENT'   : 0,                                        
                               'NWINDOWS'     : y_max,                                          
                               'FORCECONSTANT': FORCECONSTANT_1,                                     
                               'DMINIMUM'     : 0}                                          
	
	
	
	
	
	
	
	
	
	
	
	
	
        #---------------------------------- importing parameters COORD-2 ---------------------------#
	FORCECONSTANT_2 = float(self.builder.get_object('entry_FORCE2'         ).get_text())        
        mode            = self.builder.get_object('combobox_reaction_coordiante_type2').get_active_text()
	
	ATOM1      = int(self.builder.get_object("entry_coord2_ATOM1"     ).get_text())            
	ATOM1_name = self.builder.get_object    ("entry_coord2_ATOM1_name").get_text()             
	ATOM2      = int(self.builder.get_object("entry_coord2_ATOM2"     ).get_text())            
	ATOM2_name = self.builder.get_object    ("entry_coord2_ATOM2_name").get_text()             
	
        if mode == "multiple-distance":                                                            
            ATOM3      = int(self.builder.get_object("entry_coord2_ATOM3"     ).get_text())        
            ATOM3_name = self.builder.get_object    ("entry_coord2_ATOM3_name").get_text()         


            mass_weight = self.builder.get_object    ("checkbutton_mass_weight2").get_active()    
	    if self.builder.get_object("checkbutton_mass_weight2").get_active():
		sigma_pk1_pk3, sigma_pk3_pk1 = compute_sigma_a1_a3 (name1, name3)
		
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
	    else:
		sigma_pk1_pk3 =  1.0
		sigma_pk3_pk1 = -1.0
		
            print "  "+ATOM1_name+"   ->-  "+ATOM2_name+"  -->-- "+ATOM3_name+"  "               
            print " pk1 --- pk2 ---- pk3 \n"                                                     
            print "\n\n"						                         
            print                                                                                
            
            print sigma_pk3_pk1                                                                  
            print sigma_pk1_pk3                                                                  
                                                                                                 
            REACTION_COORD2 = {'MODE'         : mode,                                            
                               'ATOM1'        : ATOM1,                                           
                               'ATOM1_name'   : ATOM1_name,                                      
                               'ATOM2'        : ATOM2,                                           
                               'ATOM2_name'   : ATOM2_name,		                         
                               'ATOM3'        : ATOM3,                                           
                               'ATOM3_name'   : ATOM3_name,                                      
                               'DINCREMENT'   : 0,                                      
                               'NWINDOWS'     : x_max,                                        
                               'FORCECONSTANT': FORCECONSTANT_2,                                   
                               'DMINIMUM'     : 0,                                        
                               'mass_weight'  : mass_weight,                                     
                               'sigma_pk1_pk3': sigma_pk1_pk3,                                   
                               'sigma_pk3_pk1': sigma_pk3_pk1}                                   

	else:
	    REACTION_COORD2 = {'MODE'         : mode,                                              
                               'ATOM1'        : ATOM1,                                             
                               'ATOM1_name'   : ATOM1_name,                                        
                               'ATOM2'        : ATOM2,                                             
                               'ATOM2_name'   : ATOM2_name,		                           
                               'DINCREMENT'   : 0,                                        
                               'NWINDOWS'     : x_max,                                          
                               'FORCECONSTANT': FORCECONSTANT_2,                                     
                               'DMINIMUM'     : 0}       
	



	

	



        #-----------------------------------import trajectory parameters--------------------------------#
        max_int       = int(self.builder.get_object  ("SCAN_MIN_entry_max_int").get_text())             #
        rms_grad      = float(self.builder.get_object("SCAN_MIN_entry_rmsd_grad").get_text())           #
        mim_method    = self.builder.get_object      ('combobox_optimization_method').get_active_text() #
        log_freq      = None                                                                            #
        #-----------------------------------------------------------------------------------------------#


        #-----------------------------------------------------------------------------------------------#
        data_path     = self.EasyHybridSession.project.settings['data_path']                                              #
        traj          = self.builder.get_object('umbrella_entry_TRAJECTORY').get_text()                 #
        if not os.path.exists (os.path.join(data_path, traj)): os.mkdir (os.path.join(data_path, traj)) #
        outpath = os.path.join(data_path, traj)                                                         #
        #-----------------------------------------------------------------------------------------------#
        
        if self.builder.get_object("checkbutton_minimization").get_active():
            outpath_opt     = os.path.join (outpath, 'GeometryOptimization')
            if not os.path.isdir(outpath_opt):
                os.mkdir(outpath_opt)
            #----------------------------------------------#
            MINIMIZATION_PARAMETERS={
                                    'do_minimizaton': True      ,
                                    'max_int'       : max_int   ,
                                    'log_freq'      : log_freq  ,
                                    'rms_grad'      : rms_grad  ,
                                    'mim_method'    : mim_method,
                                    'outpath'       : outpath_opt
                                    }
        else:
            MINIMIZATION_PARAMETERS = {'do_minimizaton': False }	




        MDYNAMICS_PARAMETERS  = {}
        MD_mode               =  self.builder.get_object('combobox_molecular_dynamics_method').get_active_text()
        

        
        if MD_mode == "Velocity Verlet Dynamics":
            nsteps_EQ         = int(self.builder.get_object  ('steps_eq').get_text())
            nsteps_DC         = int(self.builder.get_object  ('steps_dc').get_text())
            temperature       = int(self.builder.get_object  ('temperature').get_text())
            temp_scale_freq   = int(self.builder.get_object  ('temp_scale_freq').get_text())
            timestep          = float(self.builder.get_object('timestep').get_text())
            trajectory_freq   = int(self.builder.get_object  ("traj_freq_dy").get_text())
            log_freq          = int(self.builder.get_object  ("log_freq_dy").get_text())
            seed              = int(self.builder.get_object  ('entry_seed_dy').get_text())
            coll_freq         = int(self.builder.get_object  ('collision_frequency').get_text())
            
            MDYNAMICS_PARAMETERS   =   {'MD_mode'         : MD_mode,
                                        'nsteps_EQ'       : nsteps_EQ,
                                        'nsteps_DC'       : nsteps_DC,
                                        'temperature'     : temperature,
                                        'temp_scale_freq' : temp_scale_freq,
                                        'timestep'        : timestep,
                                        'trajectory_freq' : trajectory_freq,
                                        'log_freq'        : log_freq,
                                        'seed'            : seed,
                                        'coll_freq'       : coll_freq}
            
        if MD_mode == "Leap Frog Dynamics":
            nsteps_EQ         = int(self.builder.get_object  ('steps_eq').get_text())
            nsteps_DC         = int(self.builder.get_object  ('steps_dc').get_text())
            temperature       = int(self.builder.get_object  ('temperature').get_text())
            temp_scale_freq   = int(self.builder.get_object  ('temp_scale_freq').get_text())
            timestep          = float(self.builder.get_object('timestep').get_text())
            trajectory_freq   = int(self.builder.get_object  ("traj_freq_dy").get_text())
            log_freq          = int(self.builder.get_object  ("log_freq_dy").get_text())
            seed              = int(self.builder.get_object  ('entry_seed_dy').get_text())
            coll_freq         = int(self.builder.get_object  ('collision_frequency').get_text())
            
            MDYNAMICS_PARAMETERS   =   {'MD_mode'             : MD_mode,
                                        'nsteps_EQ'           : nsteps_EQ,
                                        'nsteps_DC'           : nsteps_DC,
                                        'temperature'         : temperature,
                                        'temp_scale_freq'     : temp_scale_freq,
                                        'timestep'            : timestep,
                                        'trajectory_freq'     : trajectory_freq,
                                        'log_freq'            : log_freq,
                                        'seed'                : seed,
                                        'coll_freq'           : coll_freq,
                                        'temperatureCoupling' : 0.1 }	
                
        if MD_mode == "Langevin Dynamics":
            nsteps_EQ         = int(self.builder.get_object  ('steps_eq').get_text())
            nsteps_DC         = int(self.builder.get_object  ('steps_dc').get_text())
            temperature       = int(self.builder.get_object  ('temperature').get_text())
            temp_scale_freq   = int(self.builder.get_object  ('temp_scale_freq').get_text())
            timestep          = float(self.builder.get_object('timestep').get_text())
            trajectory_freq   = int(self.builder.get_object  ("traj_freq_dy").get_text())
            log_freq          = int(self.builder.get_object  ("log_freq_dy").get_text())
            seed              = int(self.builder.get_object  ('entry_seed_dy').get_text())
            coll_freq         = int(self.builder.get_object  ('collision_frequency').get_text())
            MDYNAMICS_PARAMETERS   =   {'MD_mode'             : MD_mode,
                                        'nsteps_EQ'           : nsteps_EQ,
                                        'nsteps_DC'           : nsteps_DC,
                                        'temperature'         : temperature,
                                        'timestep'            : timestep,
                                        'trajectory_freq'     : trajectory_freq,
                                        'log_freq'            : log_freq,
                                        'seed'                : seed,
                                        'coll_freq'           : coll_freq}



        outpath_eq      = os.path.join (outpath, 'Equilibration')
        if not os.path.isdir(outpath_eq):
            os.mkdir(outpath_eq)
        outpath_collect = os.path.join (outpath, 'DataCollection')    
        if not os.path.isdir(outpath_collect):
            os.mkdir(outpath_collect)
        
        MDYNAMICS_PARAMETERS['outpath_collect'] = outpath_collect
        MDYNAMICS_PARAMETERS['outpath_eq']      = outpath_eq





	#print REACTION_COORD1
	#print REACTION_COORD2
	#print 'data_path :' ,  data_path
	#print 'traj      :' ,  traj     
        #print 'outpath   :' ,  outpath 
	#print MINIMIZATION_PARAMETERS
	#print MDYNAMICS_PARAMETERS
	'''
	print '\nREACTION_COORD1: \n'
        pprint(REACTION_COORD1)
	
	print '\n\nREACTION_COORD2: \n'
	pprint(REACTION_COORD2)
	
	print '\n\nMINIMIZATION_PARAMETERS: \n'
        pprint(MINIMIZATION_PARAMETERS)
        
	print '\n\nMDYNAMICS_PARAMETERS: \n'
	pprint(MDYNAMICS_PARAMETERS)
	'''

	trajectorypath =  trajectory 
        logFile = umbrella_sampling2D(outpath                 , 
                                      REACTION_COORD1         ,
                                      REACTION_COORD2         ,
				      trajectorypath          , 
				      files                   ,
				      N_process               ,
				      MINIMIZATION_PARAMETERS ,
                                      MDYNAMICS_PARAMETERS    ,
                                      self.EasyHybridSession.project
                                      )
        
        self.EasyHybridSession.project.From_PDYNAMO_to_EasyHybrid(type_='ubs', log =  logFile)
        self.Visible  =  False
        self.window.destroy()













	
    def OpenWindow (self, text):
        if self.Visible  ==  False:
            self.project    = self.EasyHybridSession.project
            EasyHybrid_ROOT = self.EasyHybridSession.EasyHybrid_ROOT
            EasyHybrid_GUI  = self.EasyHybridSession.EasyHybrid_GUI 


            self.builder = gtk.Builder()
            self.builder.add_from_file(
                os.path.join(EasyHybrid_GUI,'WindowUmbrellaSampling', 'UmbrellaSampling2D.glade'))

            self.builder.connect_signals(self)
            self.window = self.builder.get_object('window1')
            self.sigma_pk1_pk3 = None
            self.sigma_pk3_pk1 = None
            self.builder.get_object("umbrella_entry_TRAJECTORY").set_text(text)



            '''
            --------------------------------------------------
            -                                                -
            -	              WindowControl                  -
            -                                                -
            --------------------------------------------------
            '''        
            self.window_control = WindowControl(self.builder)

            #--------------------- Setup ComboBoxes -------------------------
            combobox  = 'combobox_reaction_coordiante_type1'                     
            combolist = ['simple-distance', 'multiple-distance']
            self.window_control.SETUP_COMBOBOXES(combobox, combolist, 0)     

            combobox  = 'combobox_reaction_coordiante_type2'                     
            combolist = ['simple-distance', 'multiple-distance']
            self.window_control.SETUP_COMBOBOXES(combobox, combolist, 0) 
            
	    #combobox  = 'combobox1'                     
            #combolist = ['sequential', 'from trajectory']
            #self.window_control.SETUP_COMBOBOXES(combobox, combolist, 0)  
            
            
            combobox  = 'combobox_optimization_method'                     
            combolist = ['Conjugate Gradient']#, 'Steepest Descent','LBFGS']
            self.window_control.SETUP_COMBOBOXES(combobox, combolist, 0)     
                                                                                                     
            combobox = 'combobox_molecular_dynamics_method'         #
            combolist = ["Velocity Verlet Dynamics", "Leap Frog Dynamics"]#,"Langevin Dynamics"]
            self.window_control.SETUP_COMBOBOXES(combobox, combolist, 0)
            #------------------------------------------------------------#

            # QC SPIN MULTIPLICITY
            spinbutton = 'spinbutton1'
            config     = [0.0, 1.0,    500.0, 1.0, 0.0, 0.0]
            self.window_control.SETUP_SPINBUTTON(spinbutton, config)


            self.window.show()                                               
            #                                                                
            self.builder.connect_signals(self)                                   

            self.Visible  =  True
            gtk.main()
            #----------------------------------------------------------------
    def CloseWindow (self, button):
        """ Function doc """
        #print "Bacheguissimo"
        self.window.destroy()

    def __init__(self, EasyHybridSession = None):
        """ Class initialiser """
        if EasyHybridSession != None:
            self.project          = EasyHybridSession.project
            self.main_builder     = EasyHybridSession.builder
            self.EasyHybridSession = EasyHybridSession        
            self.window_control   = EasyHybridSession.window_control

        self.Visible    =  False
















                
class UmbrellaSamplingWindow():
    """ Class doc """
    def  on_Window_destroy(self, widget):
        """ Function doc """
        self.Visible  =  False

    def RunUmbrellaSampling(self, button):
                             #---------------------------------------------------#
                             #                                                   #
                             #                  Reaction COORD-1                 #
                             #                                                   #
                             #---------------------------------------------------#
        #---------------------------------- importing parameters COORD-1 ---------------------------#
        DINCREMENT    = float(self.builder.get_object('entry_STEP_size1'     ).get_text())          #
        NWINDOWS      = int  (self.builder.get_object('entry_NWINDOWS1'      ).get_text())          #
        DMINIMUM      = float(self.builder.get_object('entry_param_DMINIMUM1').get_text())          #
        FORCECONSTANT = float(self.builder.get_object('entry_FORCE1'         ).get_text())          #
        #-------------------------------------------------------------------------------------------#

        mode  = self.builder.get_object('combobox_SCAN_reaction_coordiante_type').get_active_text()
        print "\n\n"
        print mode 
        self.EasyHybridSession.project.ActiveModeCheck()
        #-------------------------------------------------------------------------------------------------#
        #                                       simple-distance                                           #
        #-------------------------------------------------------------------------------------------------#
        if mode == "simple-distance":                                                                     #
            ATOM1      = int(self.builder.get_object("entry_coord1_ATOM1"     ).get_text())               #
            ATOM1_name = self.builder.get_object    ("entry_coord1_ATOM1_name").get_text()                #
            ATOM2      = int(self.builder.get_object("entry_coord1_ATOM2"     ).get_text())               #
            ATOM2_name = self.builder.get_object    ("entry_coord1_ATOM2_name").get_text()                #
                                                                                                          #
            REACTION_COORD1 = {'MODE'         : mode,                                                     #
                               'ATOM1'        : ATOM1,                                                    #
                               'ATOM1_name'   : ATOM1_name,                                               #
                               'ATOM2'        : ATOM2,                                                    #
                               'ATOM2_name'   : ATOM2_name,		                                          #
                               'DINCREMENT'   : DINCREMENT,                                               #
                               'NWINDOWS'     : NWINDOWS,                                                 #
                               'FORCECONSTANT': FORCECONSTANT,                                            #
                               'DMINIMUM'     : DMINIMUM}                                                 #
        #-------------------------------------------------------------------------------------------------#


        #-------------------------------------------------------------------------------------------------#
        #                                      multiple-distance                                          #
        #-------------------------------------------------------------------------------------------------#
        if mode == "multiple-distance":                                                                   #
            ATOM1      = int(self.builder.get_object("entry_coord1_ATOM1"     ).get_text())               #
            ATOM1_name = self.builder.get_object    ("entry_coord1_ATOM1_name").get_text()                #
            ATOM2      = int(self.builder.get_object("entry_coord1_ATOM2"     ).get_text())               #
            ATOM2_name = self.builder.get_object    ("entry_coord1_ATOM2_name").get_text()                #
            ATOM3      = int(self.builder.get_object("entry_coord1_ATOM3"     ).get_text())               #
            ATOM3_name = self.builder.get_object    ("entry_coord1_ATOM3_name").get_text()                #
                                                                                                          #
            mass_weight= self.builder.get_object    ("checkbutton_mass_weight1").get_active()             #
                                                                                                          #
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
            REACTION_COORD1 = {'MODE'         : mode,                                                     #
                               'ATOM1'        : ATOM1,                                                    #
                               'ATOM1_name'   : ATOM1_name,                                               #
                               'ATOM2'        : ATOM2,                                                    #
                               'ATOM2_name'   : ATOM2_name,		                                          #
                               'ATOM3'        : ATOM3,                                                    #
                               'ATOM3_name'   : ATOM3_name,                                               #
                               'DINCREMENT'   : DINCREMENT,                                               #
                               'NWINDOWS'     : NWINDOWS,                                                 #
                               'FORCECONSTANT': FORCECONSTANT,                                            #
                               'DMINIMUM'     : DMINIMUM,                                                 #
                               'mass_weight'  : mass_weight,                                              #
                               'sigma_pk1_pk3': sigma_pk1_pk3,                                            #
                               'sigma_pk3_pk1': sigma_pk3_pk1}                                            #
        #-------------------------------------------------------------------------------------------------#

        
        
        #----------------------------------------------------------------------------------------#
        #                      Reacion path type  sequential / from trajectory                   #
        #----------------------------------------------------------------------------------------#
        reaction_path_type = self.builder.get_object("combobox1"         ).get_active_text()     #
        trajectory         = self.builder.get_object("filechooserbutton1").get_filename()        #
        N_process          = self.builder.get_object("spinbutton1"       ).get_value_as_int()    #
                                                                                                 #
        REACTION_COORD1['REACTION_PATH_TYPE'] = reaction_path_type                               #
        REACTION_COORD1['FROM_TRAJECTORY']    = trajectory                                       #
        REACTION_COORD1['N_PROCESS']          = N_process                                        #
        '''
        REACTION_PATH_TYPE  = sequential or from trajectory
        FROM_TRAJECTORY     = a trajectory obtained by SCANS 
        N_PROCESS           = number of CPUs used 
        '''
        #----------------------------------------------------------------------------------------#

    
        
        #-----------------------------------import trajectory parameters--------------------------------#
        max_int       = int(self.builder.get_object  ("SCAN_MIN_entry_max_int").get_text())             #
        rms_grad      = float(self.builder.get_object("SCAN_MIN_entry_rmsd_grad").get_text())           #
        mim_method	  = self.builder.get_object      ('combobox_optimization_method').get_active_text() #
        log_freq      = None                                                                            #
        #-----------------------------------------------------------------------------------------------#


        #-----------------------------------------------------------------------------------------------#
        data_path     = self.EasyHybridSession.project.settings['data_path']                                              #
        traj          = self.builder.get_object('umbrella_entry_TRAJECTORY').get_text()                 #
        if not os.path.exists (os.path.join(data_path, traj)): os.mkdir (os.path.join(data_path, traj)) #
        outpath = os.path.join(data_path, traj)                                                         #
        #-----------------------------------------------------------------------------------------------#
        
        if self.builder.get_object("checkbutton_minimization").get_active():
            outpath_opt     = os.path.join (outpath, 'GeometryOptimization')
            if not os.path.isdir(outpath_opt):
                os.mkdir(outpath_opt)
            #----------------------------------------------#
            MINIMIZATION_PARAMETERS={
                                    'do_minimizaton': True      ,
                                    'max_int'       : max_int   ,
                                    'log_freq'      : log_freq  ,
                                    'rms_grad'      : rms_grad  ,
                                    'mim_method'    : mim_method,
                                    'outpath'       : outpath_opt
                                    }
        else:
            MINIMIZATION_PARAMETERS = {'do_minimizaton': False }	
        
        
        
        
        
        
        
        MDYNAMICS_PARAMETERS  = {}
        MD_mode               =  self.builder.get_object('combobox_molecular_dynamics_method').get_active_text()
        

        
        if MD_mode == "Velocity Verlet Dynamics":
            nsteps_EQ         = int(self.builder.get_object  ('steps_eq').get_text())
            nsteps_DC         = int(self.builder.get_object  ('steps_dc').get_text())
            temperature       = int(self.builder.get_object  ('temperature').get_text())
            temp_scale_freq   = int(self.builder.get_object  ('temp_scale_freq').get_text())
            timestep          = float(self.builder.get_object('timestep').get_text())
            trajectory_freq   = int(self.builder.get_object  ("traj_freq_dy").get_text())
            log_freq          = int(self.builder.get_object  ("log_freq_dy").get_text())
            seed              = int(self.builder.get_object  ('entry_seed_dy').get_text())
            coll_freq         = int(self.builder.get_object  ('collision_frequency').get_text())
            
            MDYNAMICS_PARAMETERS   =   {'MD_mode'         : MD_mode,
                                        'nsteps_EQ'       : nsteps_EQ,
                                        'nsteps_DC'       : nsteps_DC,
                                        'temperature'     : temperature,
                                        'temp_scale_freq' : temp_scale_freq,
                                        'timestep'        : timestep,
                                        'trajectory_freq' : trajectory_freq,
                                        'log_freq'        : log_freq,
                                        'seed'            : seed,
                                        'coll_freq'       : coll_freq}
            
        if MD_mode == "Leap Frog Dynamics":
            nsteps_EQ         = int(self.builder.get_object  ('steps_eq').get_text())
            nsteps_DC         = int(self.builder.get_object  ('steps_dc').get_text())
            temperature       = int(self.builder.get_object  ('temperature').get_text())
            temp_scale_freq   = int(self.builder.get_object  ('temp_scale_freq').get_text())
            timestep          = float(self.builder.get_object('timestep').get_text())
            trajectory_freq   = int(self.builder.get_object  ("traj_freq_dy").get_text())
            log_freq          = int(self.builder.get_object  ("log_freq_dy").get_text())
            seed              = int(self.builder.get_object  ('entry_seed_dy').get_text())
            coll_freq         = int(self.builder.get_object  ('collision_frequency').get_text())
            
            MDYNAMICS_PARAMETERS   =   {'MD_mode'             : MD_mode,
                                        'nsteps_EQ'           : nsteps_EQ,
                                        'nsteps_DC'           : nsteps_DC,
                                        'temperature'         : temperature,
                                        'temp_scale_freq'     : temp_scale_freq,
                                        'timestep'            : timestep,
                                        'trajectory_freq'     : trajectory_freq,
                                        'log_freq'            : log_freq,
                                        'seed'                : seed,
                                        'coll_freq'           : coll_freq,
                                        'temperatureCoupling' : 0.1 }	
                
        if MD_mode == "Langevin Dynamics":
            nsteps_EQ         = int(self.builder.get_object  ('steps_eq').get_text())
            nsteps_DC         = int(self.builder.get_object  ('steps_dc').get_text())
            temperature       = int(self.builder.get_object  ('temperature').get_text())
            temp_scale_freq   = int(self.builder.get_object  ('temp_scale_freq').get_text())
            timestep          = float(self.builder.get_object('timestep').get_text())
            trajectory_freq   = int(self.builder.get_object  ("traj_freq_dy").get_text())
            log_freq          = int(self.builder.get_object  ("log_freq_dy").get_text())
            seed              = int(self.builder.get_object  ('entry_seed_dy').get_text())
            coll_freq         = int(self.builder.get_object  ('collision_frequency').get_text())
            MDYNAMICS_PARAMETERS   =   {'MD_mode'             : MD_mode,
                                        'nsteps_EQ'           : nsteps_EQ,
                                        'nsteps_DC'           : nsteps_DC,
                                        'temperature'         : temperature,
                                        'timestep'            : timestep,
                                        'trajectory_freq'     : trajectory_freq,
                                        'log_freq'            : log_freq,
                                        'seed'                : seed,
                                        'coll_freq'           : coll_freq}

        outpath_eq      = os.path.join (outpath, 'Equilibration')
        if not os.path.isdir(outpath_eq):
            os.mkdir(outpath_eq)
        outpath_collect = os.path.join (outpath, 'DataCollection')    
        if not os.path.isdir(outpath_collect):
            os.mkdir(outpath_collect)
        
        MDYNAMICS_PARAMETERS['outpath_collect'] = outpath_collect
        MDYNAMICS_PARAMETERS['outpath_eq']      = outpath_eq

        pprint(REACTION_COORD1)
        pprint(MINIMIZATION_PARAMETERS)
        pprint(MDYNAMICS_PARAMETERS)

        logFile = umbrella_sampling (outpath                 , 
                                     REACTION_COORD1         ,
                                     MINIMIZATION_PARAMETERS ,
                                     MDYNAMICS_PARAMETERS    ,
                                     self.EasyHybridSession.project
                                     )
        
        self.EasyHybridSession.project.From_PDYNAMO_to_EasyHybrid(type_='ubs', log =  logFile)
        self.Visible  =  False
        self.window.destroy()

    def Button_import_PyMOL_index(self, button):
        '''
        ----------------------------------------------------
                        REACTION COORDINATE 1 
        ----------------------------------------------------
        '''
        if button == self.builder.get_object('Button_import_PyMOL_index1'):
            mode  =  self.builder.get_object('combobox_SCAN_reaction_coordiante_type').get_active_text()
            if mode == "simple-distance":
                try:
                    name1, atom1_index, name2, atom2_index, distance_a1_a2 = import_ATOM1_ATOM2("pk1", "pk2")
                    distance_a1_a2 = str(distance_a1_a2)
                    
                    self.builder.get_object('entry_param_DMINIMUM1'  ).set_text(distance_a1_a2)
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

                    print "distance between atom 1 and atom 2: ",distance_a1_a2
                    print "distance between atom 2 and atom 3: ",distance_a2_a3
                    
                    if self.builder.get_object("checkbutton_mass_weight1").get_active():
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
                        self.builder.get_object('entry_param_DMINIMUM1').set_text(str(DMINIMUM))
                        print "\n\nUsing mass weighted restraints"
                        print "Sigma pk1_pk3", self.sigma_pk1_pk3
                        print "Sigma pk3_pk1", self.sigma_pk3_pk1
                        print "Estimated minimum distance",  DMINIMUM
                        
                    else:
                        self.sigma_pk1_pk3 =  1.0
                        self.sigma_pk3_pk1 = -1.0
                        DMINIMUM = distance_a1_a2 - distance_a2_a3
                        self.builder.get_object('entry_param_DMINIMUM1').set_text(str(DMINIMUM))
                        
                        print "\n\nSigma pk1_pk3 ", self.sigma_pk1_pk3
                        print "Sigma pk3_pk1", self.sigma_pk3_pk1
                        print "Estimated minimum distance",  DMINIMUM			
                except:
                    cmd.edit_mode()
                    print "pk1, pk2 and pk3 selections not found"	
                    print texto_d2d1	
                    return			
                print name3, name2, name1
                self.builder.get_object("entry_coord1_ATOM1"     ).set_text(str(atom1_index))
                self.builder.get_object("entry_coord1_ATOM1_name").set_text(name1)
                self.builder.get_object("entry_coord1_ATOM2"     ).set_text(str(atom2_index))
                self.builder.get_object("entry_coord1_ATOM2_name").set_text(name2)
                self.builder.get_object("entry_coord1_ATOM3"     ).set_text(str(atom3_index))
                self.builder.get_object("entry_coord1_ATOM3_name").set_text(name3)


        
        '''
        ----------------------------------------------------
                        REACTION COORDINATE 2 
        ----------------------------------------------------
        '''
        if button == self.builder.get_object('Button_import_PyMOL_index2'):
            
            mode  =  self.builder.get_object('combobox_SCAN_reaction_coordiante2_type').get_active_text()
            if mode == "simple-distance":
                try:
                    name1, atom1_index, name2, atom2_index, distance_a1_a2 = import_ATOM1_ATOM2("pk1", "pk2")
                    distance_a1_a2 = str(distance_a1_a2)
                    
                    self.builder.get_object('entry_param_DMINIMUM2'  ).set_text(distance_a1_a2)
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

                    print "distance between atom 1 and atom 2: ",distance_a1_a2
                    print "distance between atom 2 and atom 3: ",distance_a2_a3
                    
                    if self.builder.get_object("checkbutton_mass_weight2").get_active():
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
                        self.builder.get_object('entry_param_DMINIMUM2').set_text(str(DMINIMUM))
                        print "\n\nUsing mass weighted restraints"
                        print "Sigma pk1_pk3", self.sigma_pk1_pk3
                        print "Sigma pk3_pk1", self.sigma_pk3_pk1
                        print "Estimated minimum distance",  DMINIMUM
                        
                    else:
                        self.sigma_pk1_pk3 =  1.0
                        self.sigma_pk3_pk1 = -1.0
                        DMINIMUM = distance_a1_a2 - distance_a2_a3
                        self.builder.get_object('entry_param_DMINIMUM2').set_text(str(DMINIMUM))
                        
                        print "\n\nSigma pk1_pk3 ", self.sigma_pk1_pk3
                        print "Sigma pk3_pk1", self.sigma_pk3_pk1
                        print "Estimated minimum distance",  DMINIMUM			
                except:
                    cmd.edit_mode()
                    print "pk1, pk2 and pk3 selections not found"	
                    print texto_d2d1	
                    return			
                print name3, name2, name1
                self.builder.get_object("entry_coord2_ATOM1"     ).set_text(str(atom1_index))
                self.builder.get_object("entry_coord2_ATOM1_name").set_text(name1)
                self.builder.get_object("entry_coord2_ATOM2"     ).set_text(str(atom2_index))
                self.builder.get_object("entry_coord2_ATOM2_name").set_text(name2)
                self.builder.get_object("entry_coord2_ATOM3"     ).set_text(str(atom3_index))
                self.builder.get_object("entry_coord2_ATOM3_name").set_text(name3)

    def on_ScanDialog_button_CANCEL_SCAN_clicked (self, button):
        """ Function doc """
        self.window.destroy()
    
    def Mass_weight_check(self, checkbutton):
        
        '''
        ----------------------------------------------------
                        REACTION COORDINATE 1 
        ----------------------------------------------------
        '''
        if checkbutton == self.builder.get_object('checkbutton_mass_weight1'):
            try:
                name1, atom1_index, name2, atom2_index, distance_a1_a2 = import_ATOM1_ATOM2("pk1", "pk2")
                name2, atom2_index, name3, atom3_index, distance_a2_a3 = import_ATOM1_ATOM2("pk2", "pk3")
            except:
                print texto_d2d1
                return
                
            if self.builder.get_object("checkbutton_mass_weight1").get_active():
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
                self.builder.get_object('entry_param_DMINIMUM1').set_text(str(DMINIMUM))
                print "\n\nUsing mass weighted restraints"
                print "Sigma pk1_pk3", self.sigma_pk1_pk3
                print "Sigma pk3_pk1", self.sigma_pk3_pk1
                print "Estimated minimum distance",  DMINIMUM
                
            else:
                self.sigma_pk1_pk3 =  1.0
                self.sigma_pk3_pk1 = -1.0
                DMINIMUM = distance_a1_a2 - distance_a2_a3
                self.builder.get_object('entry_param_DMINIMUM1').set_text(str(DMINIMUM))
                print "\n\nSigma pk1_pk3 ", self.sigma_pk1_pk3
                print "Sigma pk3_pk1", self.sigma_pk3_pk1
                print "Estimated minimum distance",  DMINIMUM	
        
        
        

        '''
        ----------------------------------------------------
                        REACTION COORDINATE 2 
        ----------------------------------------------------
        '''
        if checkbutton == self.builder.get_object('checkbutton_mass_weight2'):
            try:
                name1, atom1_index, name2, atom2_index, distance_a1_a2 = import_ATOM1_ATOM2("pk1", "pk2")
                name2, atom2_index, name3, atom3_index, distance_a2_a3 = import_ATOM1_ATOM2("pk2", "pk3")
            except:
                print texto_d2d1
                return
                
            if self.builder.get_object("checkbutton_mass_weight2").get_active():
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
                self.builder.get_object('entry_param_DMINIMUM2').set_text(str(DMINIMUM))
                print "\n\nUsing mass weighted restraints"
                print "Sigma pk1_pk3", self.sigma_pk1_pk3
                print "Sigma pk3_pk1", self.sigma_pk3_pk1
                print "Estimated minimum distance",  DMINIMUM
                
            else:
                self.sigma_pk1_pk3 =  1.0
                self.sigma_pk3_pk1 = -1.0
                DMINIMUM = distance_a1_a2 - distance_a2_a3
                self.builder.get_object('entry_param_DMINIMUM2').set_text(str(DMINIMUM))
                print "\n\nSigma pk1_pk3 ", self.sigma_pk1_pk3
                print "Sigma pk3_pk1", self.sigma_pk3_pk1
                print "Estimated minimum distance",  DMINIMUM

    def checkbutton_MassWeight (self, checkbutton):
        """ Function doc """
        print 'checkbutton_MassWeight'
        self.Mass_weight_check(checkbutton)
         
    def ComboxChange(self, combobox):
        """ Function doc """
        if combobox == self.builder.get_object('combobox_SCAN_reaction_coordiante_type'):
            mode = self.builder.get_object('combobox_SCAN_reaction_coordiante_type').get_active_text()
            if mode == 'simple-distance':
                self.builder.get_object('label_coord1_atom3'      ).set_sensitive(False)
                self.builder.get_object('entry_coord1_ATOM3'      ).set_sensitive(False)
                self.builder.get_object('label_coord1_ATOM3_name' ).set_sensitive(False)
                self.builder.get_object('entry_coord1_ATOM3_name' ).set_sensitive(False)
                self.builder.get_object('checkbutton_mass_weight1').set_sensitive(False)
            if mode == 'multiple-distance':
                self.builder.get_object('label_coord1_atom3'      ).set_sensitive(True)
                self.builder.get_object('entry_coord1_ATOM3'      ).set_sensitive(True)
                self.builder.get_object('label_coord1_ATOM3_name' ).set_sensitive(True)
                self.builder.get_object('entry_coord1_ATOM3_name' ).set_sensitive(True)
                self.builder.get_object('checkbutton_mass_weight1').set_sensitive(True)
        
        if combobox == self.builder.get_object('combobox_SCAN_reaction_coordiante2_type'):
            mode = self.builder.get_object('combobox_SCAN_reaction_coordiante2_type').get_active_text()
            if mode == 'simple-distance':
                self.builder.get_object('label_coord2_atom3'      ).set_sensitive(False)
                self.builder.get_object('entry_coord2_ATOM3'       ).set_sensitive(False)
                self.builder.get_object('label_coord2_ATOM3_name' ).set_sensitive(False)
                self.builder.get_object('entry_coord2_ATOM3_name' ).set_sensitive(False)
                self.builder.get_object('checkbutton_mass_weight2').set_sensitive(False)
            if mode == 'multiple-distance':
                self.builder.get_object('label_coord2_atom3'      ).set_sensitive(True)
                self.builder.get_object('entry_coord2_ATOM3'       ).set_sensitive(True)
                self.builder.get_object('label_coord2_ATOM3_name' ).set_sensitive(True)
                self.builder.get_object('entry_coord2_ATOM3_name' ).set_sensitive(True)
                self.builder.get_object('checkbutton_mass_weight2').set_sensitive(True)

        if combobox == self.builder.get_object('combobox1'):
            mode = self.builder.get_object('combobox1').get_active_text()
            
            if mode == 'sequential':
                self.builder.get_object('scan2d_label_step_size1'                      ).show()
                self.builder.get_object('entry_STEP_size1'                             ).show()
                self.builder.get_object('13_window_scan2d_scam_label_step_Nwindows2'   ).show()
                self.builder.get_object('entry_NWINDOWS1'                              ).show()
                self.builder.get_object('13_window_scan2d_scam_label_step_trajectory3' ).show()
                self.builder.get_object('entry_param_DMINIMUM1'                        ).show()
                
                #self.builder.get_object('table3').show()
                self.builder.get_object('table1').hide()

            if mode == 'from trajectory':
                #self.builder.get_object('table3').hide()
                self.builder.get_object('scan2d_label_step_size1'                      ).hide()
                self.builder.get_object('entry_STEP_size1'                             ).hide()
                self.builder.get_object('13_window_scan2d_scam_label_step_Nwindows2'   ).hide()
                self.builder.get_object('entry_NWINDOWS1'                              ).hide()
                self.builder.get_object('13_window_scan2d_scam_label_step_trajectory3' ).hide()
                self.builder.get_object('entry_param_DMINIMUM1'                        ).hide()
                
                self.builder.get_object('table1').show()



    def checkbutton_Minimization (self, checkbutton):
        if self.builder.get_object("checkbutton_minimization").get_active():
            self.builder.get_object('table17').set_sensitive(True)
        else:
            self.builder.get_object('table17').set_sensitive(False)

    def OpenWindow (self, text):
        if self.Visible  ==  False:
            self.project          = self.EasyHybridSession.project
            EasyHybrid_ROOT = self.EasyHybridSession.EasyHybrid_ROOT
            EasyHybrid_GUI  = self.EasyHybridSession.EasyHybrid_GUI 


            self.builder = gtk.Builder()
            self.builder.add_from_file(
                os.path.join(EasyHybrid_GUI,'WindowUmbrellaSampling', 'UmbrellaSampling.glade'))

            self.builder.connect_signals(self)
            self.window = self.builder.get_object('window1')
            self.sigma_pk1_pk3 = None
            self.sigma_pk3_pk1 = None
            self.builder.get_object("umbrella_entry_TRAJECTORY").set_text(text)



            '''
            --------------------------------------------------
            -                                                -
            -	              WindowControl                  -
            -                                                -
            --------------------------------------------------
            '''        
            self.window_control = WindowControl(self.builder)

            #--------------------- Setup ComboBoxes -------------------------
            combobox  = 'combobox_SCAN_reaction_coordiante_type'                     
            combolist = ['simple-distance', 'multiple-distance']
            self.window_control.SETUP_COMBOBOXES(combobox, combolist, 0)     

            
            combobox  = 'combobox1'                     
            combolist = ['sequential', 'from trajectory']
            self.window_control.SETUP_COMBOBOXES(combobox, combolist, 0)  
            
            
            combobox  = 'combobox_optimization_method'                     
            combolist = ['Conjugate Gradient']#, 'Steepest Descent','LBFGS']
            self.window_control.SETUP_COMBOBOXES(combobox, combolist, 0)     
                                                                                                     
            combobox = 'combobox_molecular_dynamics_method'         #
            combolist = ["Velocity Verlet Dynamics", "Leap Frog Dynamics"]#,"Langevin Dynamics"]
            self.window_control.SETUP_COMBOBOXES(combobox, combolist, 0)
            #------------------------------------------------------------#

            # QC SPIN MULTIPLICITY
            spinbutton = 'spinbutton1'
            config     = [0.0, 1.0,    500.0, 1.0, 0.0, 0.0]
            self.window_control.SETUP_SPINBUTTON(spinbutton, config)


            self.window.show()                                               
            #                                                                
            self.builder.connect_signals(self)                                   

            self.Visible  =  True
            gtk.main()
            #----------------------------------------------------------------
    def CloseWindow (self, button):
        """ Function doc """
        #print "Bacheguissimo"
        self.window.destroy()

    def __init__(self, EasyHybridSession = None):
        """ Class initialiser """
        if EasyHybridSession != None:
            self.project          = EasyHybridSession.project
            self.main_builder     = EasyHybridSession.builder
            self.EasyHybridSession = EasyHybridSession        
            self.window_control   = EasyHybridSession.window_control

        self.Visible    =  False


def main():
    dialog = ScanWindow()
    #dialog.OpenWindow()
if __name__ == '__main__':
    main()
