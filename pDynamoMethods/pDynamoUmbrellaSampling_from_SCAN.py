#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  pDynamoMinimization.py
#
#  Copyright 2014 Labio <labio@labio-XPS-8300>
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
import os
import time
#import sys
from random import Random
from math import *
import glob



# pDynamo
from pBabel                 import *
from pCore                  import *
from pMolecule              import *
from pMoleculeScripts       import *

from DualTextLogFileWriter3 import *
from MatplotGTK.LogParse    import *

def umbrella_sampling(outpath                 , 
					  REACTION_COORD1         ,
					  MINIMIZATION_PARAMETERS ,
					  MDYNAMICS_PARAMETERS    ,
					  project
					  ):
                        #
	
	text = "\n\n"
	text = text + "\n--------------------------------------------------------------------------------"
	text = text + "\n--                                                                            --"
	text = text + "\n--                           Umbrella-Samplig                                 --"
	text = text + "\n--                                                                            --"
	text = text + "\n--------------------------------------------------------------------------------"
	text = text + "\n"



	log     = DualTextLog(outpath,  "UmbrellaSampling.log")  #
	project.system.Summary(log=log)  
	minimization =  False
	mdynamics    =  True
	
															#-----------------#
															#   REAC COORD 1  #
															#-----------------#
	#-----------------------------------------------------------------------------------------------------------------------------------#
	mode1 = REACTION_COORD1['MODE']                                                                                                     #
	if mode1 == 'simple-distance':                                                                                                      #
		coord1_ATOM1            = REACTION_COORD1['ATOM1'     ]                                                                         #
		coord1_ATOM1_name       = REACTION_COORD1['ATOM1_name']                                                                         #
		coord1_ATOM2            = REACTION_COORD1['ATOM2'     ]                                                                         #
		coord1_ATOM2_name       = REACTION_COORD1['ATOM2_name']                                                                         #
																																		#
																																		#
		coord1_DINCREMENT1      = REACTION_COORD1['DINCREMENT']                                                                         #
		coord1_NWINDOWS1        = REACTION_COORD1['NWINDOWS']                                                                           #
		coord1_FORCECONSTANT1   = REACTION_COORD1['FORCECONSTANT']                                                                      #
		coord1_DMINIMUM1        = REACTION_COORD1['DMINIMUM']                                                                           #
																																		#
		text = text + "\n----------------------- Coordinate1  - Simple-Distance -------------------------"								#				
		text = text + "\nATOM1                  =%15i  ATOM NAME1             =%15s"     % (coord1_ATOM1,     coord1_ATOM1_name)        #
		text = text + "\nATOM2                  =%15i  ATOM NAME2             =%15s"     % (coord1_ATOM2,     coord1_ATOM2_name)        #
		text = text + "\nNWINDOWS               =%15i  FORCE CONSTANT         =%15.3f"  % (coord1_NWINDOWS1, coord1_FORCECONSTANT1)    	#		
		text = text + "\nDMINIMUM               =%15.5f  DINCREMENT             =%15.5f" % (coord1_DMINIMUM1, coord1_DINCREMENT1)    	#		
		text = text + "\n--------------------------------------------------------------------------------"                              #
																																		#
	if mode1 == "multiple-distance":                                                                                                    #
		coord1_ATOM1            = REACTION_COORD1['ATOM1'     ]                                                                         #
		coord1_ATOM1_name       = REACTION_COORD1['ATOM1_name']                                                                         #
		coord1_ATOM2            = REACTION_COORD1['ATOM2'     ]                                                                         #
		coord1_ATOM2_name       = REACTION_COORD1['ATOM2_name']	                                                                        #
		coord1_ATOM3            = REACTION_COORD1['ATOM3'     ]                                                                         #
		coord1_ATOM3_name       = REACTION_COORD1['ATOM3_name']	                                                                        #
																																		#
		coord1_DINCREMENT1      = REACTION_COORD1['DINCREMENT']                                                                         #
		coord1_NWINDOWS1        = REACTION_COORD1['NWINDOWS']                                                                           #
		coord1_FORCECONSTANT1   = REACTION_COORD1['FORCECONSTANT']                                                                      #
		coord1_DMINIMUM1        = REACTION_COORD1['DMINIMUM']                                                                           #
																																		#
		coord1_sigma_pk1_pk3    = REACTION_COORD1['sigma_pk1_pk3']                                                                      #
		coord1_sigma_pk3_pk1    = REACTION_COORD1['sigma_pk3_pk1']                                                                      #
																																		#
		text = text + "\n--------------------- Coordinate1  - Multiple-Distance -------------------------"								#				
		text = text + "\nATOM1                  =%15i  ATOM NAME1             =%15s"     % (coord1_ATOM1,     coord1_ATOM1_name)        #
		text = text + "\nATOM2*                 =%15i  ATOM NAME2             =%15s"     % (coord1_ATOM2,     coord1_ATOM2_name)        #
		text = text + "\nATOM3                  =%15i  ATOM NAME3             =%15s"     % (coord1_ATOM3,     coord1_ATOM3_name)        #
		text = text + "\nSIGMA ATOM1/ATOM3      =%15.5f  SIGMA ATOM3/ATOM1      =%15.5f" % (coord1_sigma_pk1_pk3, coord1_sigma_pk3_pk1) #
		text = text + "\nNWINDOWS               =%15i  FORCE CONSTANT         =%15.3f"  % (coord1_NWINDOWS1, coord1_FORCECONSTANT1)    	#		
		text = text + "\nDMINIMUM               =%15.5f  DINCREMENT             =%15.5f" % (coord1_DMINIMUM1, coord1_DINCREMENT1)    	#		
		text = text + "\n--------------------------------------------------------------------------------"                              #
	#-----------------------------------------------------------------------------------------------------------------------------------#
    
    
				    
				    
				     
	                 #  MINIMIZATION_PARAMETERS  #
	#---------------------------------------------------------------#
	if MINIMIZATION_PARAMETERS == {}:                               #
		minimization =  False                                       #
	else:                                                           #
		max_int      = MINIMIZATION_PARAMETERS['max_int'   ]        #
		log_freq     = MINIMIZATION_PARAMETERS['log_freq'  ]        #
		rms_grad     = MINIMIZATION_PARAMETERS['rms_grad'  ]        #
		mim_method   = MINIMIZATION_PARAMETERS['mim_method']        #
		minimization = True                                         #
	#---------------------------------------------------------------#
	

	# . Define a constraint container and assign it to the system.
	constraints = SoftConstraintContainer ( )
	project.system.DefineSoftConstraints ( constraints )
	
	
									  #--------------------------#
									  #     SAMPLING DISTANCE    #
									  #--------------------------#	
	#-------------------------------------------------------------------------------------------------------------------#
	for i in range ( coord1_NWINDOWS1 ):                                                                                #
		if mode1 == 'simple-distance':                                                                                  #
			rxncoord     = coord1_DMINIMUM1 + coord1_DINCREMENT1 * float   ( i )                                        #
			scModel      = SoftConstraintEnergyModelHarmonic ( rxncoord, coord1_FORCECONSTANT1 )                        #
			constraint   = SoftConstraintDistance         ( coord1_ATOM1, coord1_ATOM2, scModel )                       #
			constraints["ReactionCoord"] = constraint                                                                   #
																														#
		if mode1 == "multiple-distance":                                                                                #
			rxncoord     = coord1_DMINIMUM1 + coord1_DINCREMENT1 * float ( i )                                          #
			scmodel      = SoftConstraintEnergyModelHarmonic ( rxncoord, coord1_FORCECONSTANT1 )                        #
			constraint   = SoftConstraintMultipleDistance ( [[coord1_ATOM2, coord1_ATOM1,                               #
															  coord1_sigma_pk1_pk3],                                    #
															  [coord1_ATOM2, coord1_ATOM3, coord1_sigma_pk3_pk1]],      #
															  scmodel )                                                 #                                                               #
			constraints["ReactionCoord"] = constraint			                                                        #
	#-------------------------------------------------------------------------------------------------------------------#
			
		##----------   LOG files   --------------#
		#tmp  = DualTextLog(outpath,  "tmp.log") #
		#project.system.Summary(log=tmp)         #
		##---------------------------------------#
			
			
			
			
			
			
			
									  #--------------------------#
									  #    ENERGY MINIMIZATION   #
									  #--------------------------#
		#------------------------------------------------------------------------------------------#                                         
		if minimization == True:                                                                   #
			if mim_method == 'Conjugate Gradient':                                                 #
				ConjugateGradientMinimize_SystemGeometry (project.system                  ,        #
														  logFrequency         = 1        ,        #
														  maximumIterations    = max_int  ,        #
														  rmsGradientTolerance = rms_grad )        #
		#------------------------------------------------------------------------------------------#                                         



		
									  
									  
									  
									  #--------------------------#
									  #    MOLECULAR DYNAMICS    #
									  #--------------------------#
		rng = Random ( )
		rng.seed ( 291731 + i )
		# . Equilibration.
		MD_mode = MDYNAMICS_PARAMETERS['MD_mode']                                                                                          
		traj_name = 'window'

		if MD_mode == "Leap Frog Dynamics":	
									  #--------------------------#
									  #       EQUILIBRATION      #
									  #--------------------------#
		#----------------------------------------------------------------------------------------------------------------------------------#                         
																																		   #
			logFrequency        = MDYNAMICS_PARAMETERS['log_freq']                                                                         #
			steps               = MDYNAMICS_PARAMETERS['nsteps_EQ']                                                                        #
			temperature         = MDYNAMICS_PARAMETERS['temperature']                                                                      #
			temperatureCoupling = MDYNAMICS_PARAMETERS['temperatureCoupling']                                                              #
			timeStep            = MDYNAMICS_PARAMETERS['timestep']                                                                         #
																																		   #
			# . Equilibration.                                                                                                             #
			LeapFrogDynamics_SystemGeometry ( project.system,                                                                              #
											  logFrequency        = logFrequency,                                                          #
											  #rng                 = rng,                                                                  #
											  steps               = steps,                                                                 #
											  temperature         = temperature,                                                           #
											  temperatureCoupling = temperatureCoupling,                                                   #
											  timeStep            = timeStep  )                                                            #
		#----------------------------------------------------------------------------------------------------------------------------------#                         
		
									  #--------------------------#
									  #      DATA COLLECTION     #
									  #--------------------------#
		#------------------------------------------------------------------------------------------------------------------------------------#                   
																																		     #
			# . Data-collection.                                                                                                             #
			trajectory = SystemSoftConstraintTrajectory ( os.path.join ( outpath, traj_name + str(i) + ".trj" ), project.system, mode = "w" )#
																																             #
			steps               = MDYNAMICS_PARAMETERS['nsteps_DC']                                                                          #
			LeapFrogDynamics_SystemGeometry ( project.system,                                                                                #
											  logFrequency        = logFrequency,                                                            #
											  #rng                 = rng,                                                                    #
											  steps               = steps,                                                                   #
											  temperature         = temperature,                                                             #
											  temperatureCoupling = temperatureCoupling,                                                     #
											  timeStep            = timeStep,                                                                #
											  trajectories        = [ ( trajectory, 1 ) ] )                                                  #
		#------------------------------------------------------------------------------------------------------------------------------------#

		if MD_mode == "Velocity Verlet Dynamics":
								  #--------------------------#
								  #       EQUILIBRATION      #
								  #--------------------------#
		#---------------------------------------------------------------------------------------------------------------------------------# 
																																		  #
			logFrequency        = MDYNAMICS_PARAMETERS['log_freq']                                                                        #
			steps               = MDYNAMICS_PARAMETERS['nsteps_EQ']                                                                       #
			temperature         = MDYNAMICS_PARAMETERS['temperature']                                                                     #
			timeStep            = MDYNAMICS_PARAMETERS['timestep']                                                                        #
			temp_scale_freq     = MDYNAMICS_PARAMETERS['temp_scale_freq']                                                                 #
																																		  #
			# . Equilibration.                                                                                                            #
			VelocityVerletDynamics_SystemGeometry(project.system,                                                                            #
												#rng                       =   rng,                                                       #
												logFrequency              =   logFrequency,                                               #
												steps                     =   steps,                                                      #
												timeStep                  =   0.001,                                                      #
												temperatureScaleFrequency =   temp_scale_freq,                                            #
												temperatureScaleOption    =   "constant",                                                 #
												temperatureStart          =   temperature )                                               #
		#---------------------------------------------------------------------------------------------------------------------------------#                         
			
			
									  #--------------------------#
									  #      DATA COLLECTION     #
									  #--------------------------#
		#---------------------------------------------------------------------------------------------------------------------------------#  
			steps               = MDYNAMICS_PARAMETERS['nsteps_DC']                                                                       #
			trajectory = SystemSoftConstraintTrajectory ( os.path.join ( outpath, traj_name + str(i) + ".trj" ), project.system, mode = "w" )#
			VelocityVerletDynamics_SystemGeometry(project.system,                                                                            #
												trajectories              =[ ( trajectory, 1) ],                                          #
												#rng                       =   rng,                                                       #
												logFrequency              =   logFrequency,                                               #
												steps                     =   steps,                                                      #
												timeStep                  =   0.001,                                                      #
												temperatureScaleFrequency =   temp_scale_freq,                                            #
												temperatureScaleOption    =   "constant",                                                 #
												temperatureStart          =   temperature )                                               #
		#---------------------------------------------------------------------------------------------------------------------------------#                        
		
		if MD_mode ==  "Langevin Dynamics":
								  #--------------------------#
								  #       EQUILIBRATION      #
								  #--------------------------#
		#---------------------------------------------------------------------------------------------------------------------------------#
			logFrequency        = MDYNAMICS_PARAMETERS['log_freq']                                                                        #
			steps               = MDYNAMICS_PARAMETERS['nsteps_EQ']                                                                       #
			temperature         = MDYNAMICS_PARAMETERS['temperature']                                                                     #
			timeStep            = MDYNAMICS_PARAMETERS['timestep']                                                                        #
			coll_freq           = MDYNAMICS_PARAMETERS['coll_freq']                                                                       #
			# . Equilibration.                                                                                                            #
			LangevinDynamics_SystemGeometry (project.system,                                                                                 #
							logFrequency              =   logFrequency,                                                                   #
							#log                       =   dualLog,                                                                        #
							#rng                       =   rng,                                                                           #
							steps                     =   steps,                                                                          #
							timeStep                  =   0.001,                                                                          #
							collisionFrequency        = coll_freq,                                                                        #
							temperature               = temperature)                                                                      #
		#---------------------------------------------------------------------------------------------------------------------------------#
			
			
									  #--------------------------#
									  #      DATA COLLECTION     #
									  #--------------------------#
		#---------------------------------------------------------------------------------------------------------------------------------#
			steps               = MDYNAMICS_PARAMETERS['nsteps_DC']                                                                       #
			trajectory = SystemSoftConstraintTrajectory ( os.path.join ( outpath, traj_name + str(i) + ".trj" ), project.system, mode = "w" )#
																																		  #
			LangevinDynamics_SystemGeometry (project.system,                                                                                 #
							trajectories              =[ ( trajectory, 1) ],                                                              #
							logFrequency              =   logFrequency,                                                                   #
							#log                       =   dualLog,                                                                        #
							#rng                       =   rng,                                                                           #
							steps                     =   steps,                                                                          #
							timeStep                  =   0.001,                                                                          #
							collisionFrequency        = coll_freq,                                                                        #
							temperature               = temperature)                                                                      #
		#---------------------------------------------------------------------------------------------------------------------------------#


		#------------------------------------------------------------------------------------------------------#
		try:                                                                                                   #
			XMLPickle ( os.path.join ( outpath,"frame" +  str(i) +  ".pkl"), project.system.coordinates3 )     #
		except:                                                                                                #
			Pickle    ( os.path.join ( outpath,"frame" +  str(i) +  ".pkl"), project.system.coordinates3 )	   #
		#------------------------------------------------------------------------------------------------------#








	                                 #-------------------------------------#
	                                 #              LOG FILES              #
	                                 #-------------------------------------#
	#----------------------------------------------------------------------------------------------------------------------#
	arq = open(os.path.join(outpath,  "UmbrellaSampling.log"), "a")                                                        #
	                                                                                                                       #
	if MD_mode == "Langevin Dynamics":                                                                                     #
		text = text + "\n--------- Molecular-Dynamics-Langevin-Dynamics -----------"                                       #
                                                                                                                           #
	if MD_mode == "Velocity Verlet Dynamics":                                                                              #
		text = text + "\n---------- Molecular-Dynamics-Velocity-Verlet ------------"                                       #
	                                                                                                                       #
	if MD_mode == "Leap Frog Dynamics":                                                                                    #
		text = text + "\n------------- Molecular-Dynamics-Leap-Frog ---------------"	                                   #
                                                                                                                           #
	text = text + "\nNumber of steps(equilibrate)         =%20i" % (MDYNAMICS_PARAMETERS['nsteps_EQ'])                     #
	text = text + "\nNumber of steps(data collection)     =%20i" % (MDYNAMICS_PARAMETERS['nsteps_DC'])                     #
	text = text + "\ntemperature(K)                       =%20i" % (MDYNAMICS_PARAMETERS['temperature'])                   #
	text = text + "\nstep size(ps)                        =%20f" % (MDYNAMICS_PARAMETERS['timestep'])                      #
	if MD_mode ==  "Langevin Dynamics":                                                                                    #
		text = text + "\ncollision frequency                  =%20i" % (MDYNAMICS_PARAMETERS['coll_freq'])                 #
	text = text + "\n----------------------------------------------------------"                                           #
	text = text + "\n"                                                                                                     #
	#----------------------------------------------------------------------------------------------------------------------#
	
	
	
	
	
	                                 #-------------------------------------#
	                                 #              PMF BLOCK              #
	                                 #-------------------------------------#
	#----------------------------------------------------------------------------------------------------------------------#
	text = text + "\n----------------------------------------------------------------------------------------------------" #
	text = text + "\n                                           PMF-BLOCK                                                " #
	text = text + "\n----------------------------------------------------------------------------------------------------" #
	text = text + "\n"                                                                                                     #
	text = str(text)                                                                                                       #
	                                                                                                                       #
	arq.writelines(text)                                                                                                   #
	arq.close()	                                                                                                           #
	                                                                                                                       #
	                                                                                                                       #
	                                                                                                                       #
	fileNames = glob.glob(os.path.join ( outpath, traj_name+"*.trj" ))                                                     #
	trajectories = []                                                                                                      #
	for fileName in fileNames:                                                                                             #
		trajectories.append (SystemSoftConstraintTrajectory (fileName, project.system, mode = "r" ) )                      #
	                                                                                                                       #
	#print trajectories                                                                                                     #
                                                                                                                           #
                                                                                                                           #
	# . Calculate the PMF.                                                                                                 #
	state = WHAM_ConjugateGradientMinimize ( fileNames                      ,                                              #
											 bins                 = [ 100 ] ,                                              #
											 log                  = log     ,                                              #
											 logFrequency         =      1  ,                                              #
											 maximumIterations    =   1000  ,                                              #
											 rmsGradientTolerance = 1.0e-3  ,                                              #
											 temperature          = temperature)                                           #
                                                                                                                           #
	# . Write the PMF to a file.                                                                                           #
	histogram = state["Histogram"]                                                                                         #
	pmf       = state["PMF"      ]                                                                                         #
	histogram.ToTextFileWithData ( os.path.join ( outpath, "system_pmf.dat" ), [ pmf ], format = "{:20.3f} {:20.3f}\n" )   #
	#----------------------------------------------------------------------------------------------------------------------#	

	project.system.DefineSoftConstraints ( None )
	
	logFile = os.path.join(outpath,  "UmbrellaSampling.log")
	return logFile















'''
"""Example 9."""

from Definitions import *

# . Define the MM, NB and QC models.
mmModel = MMModelOPLS ( "bookSmallExamples" )
nbModel = NBModelFull ( )
qcModel = QCModelMNDO ( )

# . Define the molecule.
molecule = MOLFile_ToSystem ( os.path.join ( molPath, "bala_c7eq.mol" ) )

# . Define the selection for the first molecule.
methylGroup = Selection.FromIterable ( [ 10, 11, 12, 13 ] )

# . Define the energy model.
molecule.DefineMMModel ( mmModel )
molecule.DefineQCModel ( qcModel, qcSelection = methylGroup )
molecule.DefineNBModel ( nbModel )
molecule.Summary ( )

# . Calculate an energy.



#xyzFiles = [ "bala_alpha.xyz", "bala_c5.xyz", "bala_c7ax.xyz", "bala_c7eq.xyz" ]
xyzFiles = [["bala_alpha.xyz",'traj1'], 
            ["bala_c5.xyz"   ,'traj2'], 
            ["bala_c7ax.xyz" ,'traj3'], 
            ["bala_c7eq.xyz" ,'traj4']]

from multiprocessing import Pool

def f(xyzFile):
    
    trajname = xyzFile[1]
    xyzFile  = xyzFile[0]
    
    print xyzFile, trajname
    
    molecule.coordinates3 = XYZFile_ToCoordinates3 ( os.path.join ( xyzPath, xyzFile ) )
    
    trajectory = SystemGeometryTrajectory ( trajname, molecule, mode = "w" )
    
    LeapFrogDynamics_SystemGeometry(molecule                    ,
                        trajectories        =[ (trajectory, 100) ],
                        log                 = None,
                        pressure            = 1.0,
                        pressureCoupling    = 2000.0,
                        steps               = 50000,
                        timeStep            = 0.001,
                        temperature         = 300, 
                        temperatureCoupling = 0.1 )
    
    energy = molecule.Energy ( )
    return energy






if __name__ == '__main__':
    p = Pool(4)
    print(p.map(f, xyzFiles ))
'''




