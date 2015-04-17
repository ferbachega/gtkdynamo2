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

#GTKDYNAMO_ROOT = os.getcwd()
GTKDYNAMO_ROOT = ''
GTKDYNAMO_GUI  = ''

texto_d1   = "\n\n                       -- simple-distance --\n\nFor simple-distance, select two atoms in pymol using the editing mode\nfollowing the diagram:\n\n   R                    R\n    \                  /\n     A1--A2  . . . . A3\n    /                  \ \n   R                    R\n         ^            ^\n         |            |\n        pk1  . . . . pk2\n                d1\n"
texto_d2d1 = "\n                       -- multiple-distance --\n\nFor multiple-distance, select three atoms in pymol using the editing mode\nfollowing the diagram:\n\n   R                    R\n    \                  /\n     A1--A2  . . . . A3\n    /                  \ \n   R                    R\n     ^   ^            ^\n     |   |            |\n    pk1-pk2  . . . . pk3\n       d1       d2\n"




                
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
		self.GTKDynamoSession.project.ActiveModeCheck()
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
							   'sigma_pk1_pk3': sigma_pk1_pk3,                                            #
							   'sigma_pk3_pk1': sigma_pk3_pk1}                                            #
		#-------------------------------------------------------------------------------------------------#

		#-----------------------------------import trajectory parameters--------------------------------#
		max_int       = int(self.builder.get_object  ("SCAN_MIN_entry_max_int").get_text())             #
		rms_grad      = float(self.builder.get_object("SCAN_MIN_entry_rmsd_grad").get_text())           #
		mim_method	  = self.builder.get_object      ('combobox_optimization_method').get_active_text() #
		log_freq      = None                                                                            #
		#-----------------------------------------------------------------------------------------------#


		#-----------------------------------------------------------------------------------------------#
		data_path     = self.GTKDynamoSession.project.settings['data_path']                                              #
		traj          = self.builder.get_object('umbrella_entry_TRAJECTORY').get_text()                 #
		if not os.path.exists (os.path.join(data_path, traj)): os.mkdir (os.path.join(data_path, traj)) #
		outpath = os.path.join(data_path, traj)                                                         #
		#-----------------------------------------------------------------------------------------------#
		
		if self.builder.get_object("checkbutton_minimization").get_active():
			MINIMIZATION_PARAMETERS={
									'max_int'   : max_int   ,
									'log_freq'  : log_freq  ,
									'rms_grad'  : rms_grad  ,
									'mim_method': mim_method,
									'outpath'   : outpath
									}
		else:
			MINIMIZATION_PARAMETERS = {}	
		
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

	

		
		pprint(REACTION_COORD1)
		pprint(MINIMIZATION_PARAMETERS)
		pprint(MDYNAMICS_PARAMETERS)

		logFile = umbrella_sampling (outpath                 , 
			                         REACTION_COORD1         ,
			                         MINIMIZATION_PARAMETERS ,
			                         MDYNAMICS_PARAMETERS    ,
			                         self.GTKDynamoSession.project
			                         )

		self.GTKDynamoSession.project.From_PDYNAMO_to_GTKDYNAMO(type_='ubs', log =  logFile)
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

	def checkbutton_Minimization (self, checkbutton):
		if self.builder.get_object("checkbutton_minimization").get_active():
			self.builder.get_object('table17').set_sensitive(True)
		else:
			self.builder.get_object('table17').set_sensitive(False)



















	def OpenWindow (self):
		""" Function doc """
		if self.Visible  ==  False:
			self.project          = self.GTKDynamoSession.project
			GTKDYNAMO_ROOT = self.GTKDynamoSession.GTKDYNAMO_ROOT
			GTKDYNAMO_GUI  = self.GTKDynamoSession.GTKDYNAMO_GUI 
			
			
			self.builder = gtk.Builder()
			self.builder.add_from_file(
				os.path.join(GTKDYNAMO_GUI,'WindowUmbrellaSampling', 'UmbrellaSampling2.glade'))
			
			self.builder.connect_signals(self)
			self.window = self.builder.get_object('window1')
			self.sigma_pk1_pk3 = None
			self.sigma_pk3_pk1 = None
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

			combobox  = 'combobox_optimization_method'                     
			combolist = ['Conjugate Gradient', 'Steepest Descent','LBFGS']
			self.window_control.SETUP_COMBOBOXES(combobox, combolist, 0)     
																											 
			combobox = 'combobox_molecular_dynamics_method'         #
			combolist = ["Velocity Verlet Dynamics", "Leap Frog Dynamics","Langevin Dynamics"]
			self.window_control.SETUP_COMBOBOXES(combobox, combolist, 0)
			#------------------------------------------------------------#
			
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

	def __init__(self, GTKDynamoSession = None):
		""" Class initialiser """
		if GTKDynamoSession != None:
			self.project          = GTKDynamoSession.project
			self.main_builder     = GTKDynamoSession.builder
			self.GTKDynamoSession = GTKDynamoSession        
			self.window_control   = GTKDynamoSession.window_control
		
		#self.project   =  project
		self.Visible    =  False
		#self.window_control = window_control
		#self.builder = gtk.Builder()
		#self.main_builder = main_builder

		#self.builder.add_from_file(
		#    os.path.join(GTKDYNAMO_GUI, 'UmbrellaSampling2.glade'))
		##
		#self.builder.connect_signals(self)
		#self.window = self.builder.get_object('window1')
		#
		#self.sigma_pk1_pk3 = None
		#self.sigma_pk3_pk1 = None
		
		'''
		--------------------------------------------------
		-                                                -
		-	              WindowControl                  -
		-                                                -
		--------------------------------------------------
		'''        
		#self.window_control = WindowControl(self.builder)
		#
		##--------------------- Setup ComboBoxes -------------------------
		#combobox  = 'ScanDialog_combobox_SCAN_reaction_coordiante_type'                     
		#combolist = ['simple-distance', 'multiple-distance']
		#self.window_control.SETUP_COMBOBOXES(combobox, combolist, 0)     
		#
		#combobox  = 'ScanDialog_combobox_optimization_method'                     
		#combolist = ['Conjugate Gradient', 'Steepest Descent','LBFGS']
		#self.window_control.SETUP_COMBOBOXES(combobox, combolist, 0)     
		#                                                                                                 
		#
		#self.window.show()                                               
		##                                                                
		#self.builder.connect_signals(self)                                   
		#gtk.main()
		##----------------------------------------------------------------
		

def main():
    dialog = ScanWindow()
    #dialog.OpenWindow()
if __name__ == '__main__':
    main()
