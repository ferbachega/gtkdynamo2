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
	




    log     = DualTextLog(outpath,  "UmbrellaSampling.log")  #
    
    project.system.Summary(log=log)  
    arq = open(os.path.join(outpath, "UmbrellaSampling.log"), "a")


 
 
    text = "\n\n"
    text = text + "\n--------------------------------------------------------------------------------"
    text = text + "\n--                                                                            --"
    text = text + "\n--                           Umbrella-Samplig                                 --"
    text = text + "\n--                                                                            --"
    text = text + "\n--------------------------------------------------------------------------------"
    text = text + "\n"
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

    
    reaction_path_type  = REACTION_COORD1['REACTION_PATH_TYPE'] 
    trajectory          = REACTION_COORD1['FROM_TRAJECTORY'   ]    
    n_process           = REACTION_COORD1['N_PROCESS'         ]          

            #------------------------------------------------------------#
            #                    PARALLEL U.SAMPLING                     #
            #------------------------------------------------------------#
    #------------------------------------------------------------------------------#
    if reaction_path_type == 'from trajectory':                                    #
        
        text = text + "\n----------------------------------------------------------"
        text = text + "\n-          UMBRELLA SAMPLING FROM TRAJECTORY             -"
        text = text + "\n----------------------------------------------------------"

        Files    = os.listdir(trajectory)                                          #
        pklFiles = []                                                              #
        for File in Files:                                                         #
                                                                                   #
            File2 = File.split('.')                                                #
            #print File2                                                           #
            if File2[-1] ==  'pkl':                                                #
                pklFiles.append(File)                                              #
        print pklFiles                                                             #
        #--------------------------------------------------------------------------#
        inputs = []                                                                #
                                                                                   #
        for coordinate_file in pklFiles:                                           #
            input_system = [coordinate_file         ,                              #
                            outpath                 ,                              #
                            REACTION_COORD1         ,                              #
                            MINIMIZATION_PARAMETERS ,                              #
                            MDYNAMICS_PARAMETERS    ,                              #
                            project                 ]                              #
                                                                                   #
            inputs.append(input_system)                                            #
        #--------------------------------------------------------------------------#
        from multiprocessing import Pool                                           #
        p = Pool(n_process)                                                        #
        print(p.map(parallel_umbrella_sampling, inputs ))                          #
    #------------------------------------------------------------------------------#


            #------------------------------------------------------------#
            #                  SEQUENTIAL U.SAMPLING                     #
            #------------------------------------------------------------#
    #------------------------------------------------------------------------------#
    if reaction_path_type == 'sequential':                                         #
        text = text + "\n----------------------------------------------------------"
        text = text + "\n-             UMBRELLA SAMPLING SEQUENTIAL               -"
        text = text + "\n----------------------------------------------------------"
        sequential_umbrella_sampling(outpath                 ,                     #
                                     REACTION_COORD1         ,                     #
                                     MINIMIZATION_PARAMETERS ,                     #
                                     MDYNAMICS_PARAMETERS    ,                     #
                                     project                                       #
                                     )                                             #
                                                                                   #
    #------------------------------------------------------------------------------#   
    
 
 
                                        #-------------------------------------#
                                        #              LOG FILES              #
                                        #-------------------------------------#
    #-----------------------------------------------------------------------------------------------------------#
    MD_mode = MDYNAMICS_PARAMETERS['MD_mode']                                #

    if MD_mode == "Langevin Dynamics":                                                                          #
        text = text + "\n--------- Molecular-Dynamics-Langevin-Dynamics -----------"                            #
                                                                                                                #
    if MD_mode == "Velocity Verlet Dynamics":                                                                   #
        text = text + "\n---------- Molecular-Dynamics-Velocity-Verlet ------------"                            #
                                                                                                                #
    if MD_mode == "Leap Frog Dynamics":                                                                         #
        text = text + "\n------------- Molecular-Dynamics-Leap-Frog ---------------"	                        #
                                                                                                                #
    text = text + "\nNumber of steps(equilibrate)         =%20i" % (MDYNAMICS_PARAMETERS['nsteps_EQ'])          #
    text = text + "\nNumber of steps(data collection)     =%20i" % (MDYNAMICS_PARAMETERS['nsteps_DC'])          #
    text = text + "\ntemperature(K)                       =%20i" % (MDYNAMICS_PARAMETERS['temperature'])        #
    text = text + "\nstep size(ps)                        =%20f" % (MDYNAMICS_PARAMETERS['timestep'])           #
    if MD_mode ==  "Langevin Dynamics":                                                                         #
        text = text + "\ncollision frequency                  =%20i" % (MDYNAMICS_PARAMETERS['coll_freq'])      #
    text = text + "\n----------------------------------------------------------"                                #
    text = text + "\n"                                                                                          #
    #-----------------------------------------------------------------------------------------------------------#
    
    
    arq.writelines(text)
    arq.close()	     
    
    project.system.DefineSoftConstraints ( None )





def sequential_umbrella_sampling(outpath                 , 
					             REACTION_COORD1         ,
					             MINIMIZATION_PARAMETERS ,
					             MDYNAMICS_PARAMETERS    ,
					             project
					             ):

    #log     = DualTextLog(outpath,  "UmbrellaSampling.log")


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
        coord1_DINCREMENT1      = REACTION_COORD1['DINCREMENT']                                                                         #
        coord1_NWINDOWS1        = REACTION_COORD1['NWINDOWS'  ]                                                                         #
        coord1_FORCECONSTANT1   = REACTION_COORD1['FORCECONSTANT']                                                                      #
        coord1_DMINIMUM1        = REACTION_COORD1['DMINIMUM']                                                                           #
                                                                                                                                        #
    if mode1 == "multiple-distance":                                                                                                    #
        coord1_ATOM1            = REACTION_COORD1['ATOM1'     ]                                                                         #
        coord1_ATOM1_name       = REACTION_COORD1['ATOM1_name']                                                                         #
        coord1_ATOM2            = REACTION_COORD1['ATOM2'     ]                                                                         #
        coord1_ATOM2_name       = REACTION_COORD1['ATOM2_name']	                                                                        #
        coord1_ATOM3            = REACTION_COORD1['ATOM3'     ]                                                                         #
        coord1_ATOM3_name       = REACTION_COORD1['ATOM3_name']	                                                                        #
        coord1_DINCREMENT1      = REACTION_COORD1['DINCREMENT']                                                                         #
        coord1_NWINDOWS1        = REACTION_COORD1['NWINDOWS']                                                                           #
        coord1_FORCECONSTANT1   = REACTION_COORD1['FORCECONSTANT']                                                                      #
        coord1_DMINIMUM1        = REACTION_COORD1['DMINIMUM']                                                                           #
        coord1_sigma_pk1_pk3    = REACTION_COORD1['sigma_pk1_pk3']                                                                      #
        coord1_sigma_pk3_pk1    = REACTION_COORD1['sigma_pk3_pk1']                                                                      #
    #-----------------------------------------------------------------------------------------------------------------------------------#

    # . Define a constraint container and assign it to the system.
    constraints = SoftConstraintContainer ( )
    project.system.DefineSoftConstraints ( constraints )

                                      #--------------------------#
                                      #     SAMPLING DISTANCE    #
                                      #--------------------------#	
    #-------------------------------------------------------------------------------------------------------------------#
    for i in range ( coord1_NWINDOWS1 ):                                                                                #
                                                                                                                        #
        #-------------------------------------------------------#                                                       #
        trajname   = os.path.join (outpath, "frame" +  str(i))  #                                                       #
        #-------------------------------------------------------#                                                       #
                                                                                                                        #
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
            
        #------------------------------------------------------------------------#                                         
        if MINIMIZATION_PARAMETERS['do_minimizaton']:                            #
            Run_ConjugateGradientMinimize (system = project.system,              #
                          MINIMIZATION_PARAMETERS = MINIMIZATION_PARAMETERS)     #
            energy = project.system.Energy (log                 = None )         #
        #------------------------------------------------------------------------#                                         
                                      
                                      
                                      
                                      #--------------------------#
                                      #    MOLECULAR DYNAMICS    #
                                      #--------------------------#
        #------------------------------------------------------------------------#                                         
        #rng = Random ( )                                                        #
        #rng.seed ( 291731 + i )                                                 #
        # . Equilibration.                                                       #
        #MD_mode = MDYNAMICS_PARAMETERS['MD_mode']                               #                                                          
        #traj_name = 'window'                                                    #
                                                                                 #
                                                                                 #
        MD_mode = MDYNAMICS_PARAMETERS['MD_mode']                                #
                                                                                 #
        if MD_mode == "Velocity Verlet Dynamics":                                #
            energy = Run_VelocityVerletDynamics(system = project.system     ,    #
                                              trajname = trajname           ,    #
                                  MDYNAMICS_PARAMETERS = MDYNAMICS_PARAMETERS)   #
                                                                                 #
        if MD_mode == "Leap Frog Dynamics":	                                     #
            energy = Run_LeapFrogDynamics(system = project.system     ,          #
                                        trajname = trajname           ,          #
                            MDYNAMICS_PARAMETERS = MDYNAMICS_PARAMETERS)         #
                                                                                 #
        if MD_mode ==  "Langevin Dynamics":                                      #
            energy = Run_LangevinDynamics(system = project.system     ,          #
                                        trajname = trajname           ,          #
                            MDYNAMICS_PARAMETERS = MDYNAMICS_PARAMETERS)         #
        #------------------------------------------------------------------------#   
                                              
        #------------------------------------------------------------------------------------------------------#
        try:                                                                                                   #
            XMLPickle ( os.path.join ( outpath,"frame" +  str(i) +  ".pkl"), project.system.coordinates3 )     #
        except:                                                                                                #
            Pickle    ( os.path.join ( outpath,"frame" +  str(i) +  ".pkl"), project.system.coordinates3 )	   #
        #------------------------------------------------------------------------------------------------------#



    


def parallel_umbrella_sampling (input_system):
    """ Function doc """
    coordinate_file         = input_system[0]
    outpath                 = input_system[1]
    REACTION_COORD1         = input_system[2]
    MINIMIZATION_PARAMETERS = input_system[3]
    MDYNAMICS_PARAMETERS    = input_system[4]
    project                 = input_system[5]
    
    
    
    #----------------------------------------------#
    trajname   = coordinate_file.split('.')        #
    trajname   = trajname[0]                       #
    trajname   = os.path.join (outpath, trajname)  #
    #----------------------------------------------#
    
    
    #----------------------------------------------------------------------------------#
    trajectory = REACTION_COORD1['FROM_TRAJECTORY'   ]                                 #
    project.system.coordinates3 = Unpickle( os.path.join (trajectory, coordinate_file))#
    #----------------------------------------------------------------------------------#

    
    '''                Define a constraint container                  '''
    # . Define a constraint container and assign it to the system-------#
    constraints = SoftConstraintContainer ( )                           #
    project.system.DefineSoftConstraints ( constraints )                #
    #-------------------------------------------------------------------#

    
    
    mode1 = REACTION_COORD1['MODE']

    #--------------------------------------------------------------------------------
    if mode1 == 'simple-distance':                                        
        coord1_ATOM1            = REACTION_COORD1['ATOM1'     ]           
        coord1_ATOM1_name       = REACTION_COORD1['ATOM1_name']           
        coord1_ATOM2            = REACTION_COORD1['ATOM2'     ]           
        coord1_ATOM2_name       = REACTION_COORD1['ATOM2_name']           
                                                                          
                                                                          
        coord1_DINCREMENT1      = REACTION_COORD1['DINCREMENT']           
        coord1_NWINDOWS1        = REACTION_COORD1['NWINDOWS']             
        coord1_FORCECONSTANT1   = REACTION_COORD1['FORCECONSTANT']        
        coord1_DMINIMUM1        = REACTION_COORD1['DMINIMUM']             
                                                                          
        dist = project.system.coordinates3.Distance ( coord1_ATOM1, coord1_ATOM2)
    
        #--------------------------------------------------------------------------------------#
        rxncoord     = float(dist)                                                             #
        #print rxncoord                                                                         #
        scModel      = SoftConstraintEnergyModelHarmonic ( rxncoord, coord1_FORCECONSTANT1 )   #
        constraint   = SoftConstraintDistance         ( coord1_ATOM1, coord1_ATOM2, scModel )  #
        constraints["ReactionCoord"] = constraint                                              #
        #--------------------------------------------------------------------------------------#
                                                                                  
    if mode1 == "multiple-distance":                                      
        coord1_ATOM1            = REACTION_COORD1['ATOM1'     ]           
        coord1_ATOM1_name       = REACTION_COORD1['ATOM1_name']           
        coord1_ATOM2            = REACTION_COORD1['ATOM2'     ]           
        coord1_ATOM2_name       = REACTION_COORD1['ATOM2_name']	          
        coord1_ATOM3            = REACTION_COORD1['ATOM3'     ]           
        coord1_ATOM3_name       = REACTION_COORD1['ATOM3_name']	          
                                                                          
        coord1_DINCREMENT1      = REACTION_COORD1['DINCREMENT']           
        coord1_NWINDOWS1        = REACTION_COORD1['NWINDOWS']             
        coord1_FORCECONSTANT1   = REACTION_COORD1['FORCECONSTANT']        
        coord1_DMINIMUM1        = REACTION_COORD1['DMINIMUM']             
                                                                          
        coord1_sigma_pk1_pk3    = REACTION_COORD1['sigma_pk1_pk3']        
        coord1_sigma_pk3_pk1    = REACTION_COORD1['sigma_pk3_pk1']        
                                                                          
        dist12  = project.system.coordinates3.Distance ( coord1_ATOM1, coord1_ATOM2)
        dist23  = project.system.coordinates3.Distance ( coord1_ATOM2, coord1_ATOM3)
        dist    = dist12 - dist23

        #------------------------------------------------------------------------------------------------------#                  
        rxncoord     = float(dist) #coord1_DMINIMUM1 + coord1_DINCREMENT1 * float ( i )                        #
        scmodel      = SoftConstraintEnergyModelHarmonic ( rxncoord, coord1_FORCECONSTANT1 )                   #
        constraint   = SoftConstraintMultipleDistance ( [[coord1_ATOM2, coord1_ATOM1,                          #
                                                          coord1_sigma_pk1_pk3],                               #
                                                          [coord1_ATOM2, coord1_ATOM3, coord1_sigma_pk3_pk1]], #
                                                          scmodel )                                            #
        constraints["ReactionCoord"] = constraint			                                                   #
        #------------------------------------------------------------------------------------------------------#

    if MINIMIZATION_PARAMETERS['do_minimizaton']:
        Run_ConjugateGradientMinimize (system = project.system, 
                      MINIMIZATION_PARAMETERS = MINIMIZATION_PARAMETERS)
        energy = project.system.Energy (log                 = None )
        print dist, energy
        


    MD_mode = MDYNAMICS_PARAMETERS['MD_mode']
    
    if MD_mode == "Velocity Verlet Dynamics":
        energy = Run_VelocityVerletDynamics(system = project.system     , 
                                          trajname = trajname           ,  
                              MDYNAMICS_PARAMETERS = MDYNAMICS_PARAMETERS)
                              
    if MD_mode == "Leap Frog Dynamics":	
        energy = Run_LeapFrogDynamics(system = project.system     , 
                                    trajname = trajname           ,  
                        MDYNAMICS_PARAMETERS = MDYNAMICS_PARAMETERS)

    if MD_mode ==  "Langevin Dynamics":
        energy = Run_LangevinDynamics(system = project.system     , 
                                    trajname = trajname           ,  
                        MDYNAMICS_PARAMETERS = MDYNAMICS_PARAMETERS)
    
    return energy
    
  
  





def Run_ConjugateGradientMinimize (system = None, MINIMIZATION_PARAMETERS =  {} ):
    """ Function doc """
    max_int      = MINIMIZATION_PARAMETERS['max_int'   ]       
    log_freq     = MINIMIZATION_PARAMETERS['log_freq'  ]       
    rms_grad     = MINIMIZATION_PARAMETERS['rms_grad'  ]       
    mim_method   = MINIMIZATION_PARAMETERS['mim_method']       

    ConjugateGradientMinimize_SystemGeometry (system                          , 
                                              log                  =      None, 
                                              logFrequency         = 1        , 
                                              maximumIterations    = max_int  , 
                                              rmsGradientTolerance = rms_grad ) 
    #---------------------------------------------------------------------------

def Run_LangevinDynamics (system = None, trajname = None,  MDYNAMICS_PARAMETERS = {}):
    #----------------------------------------------------------------
    logFrequency        = MDYNAMICS_PARAMETERS['log_freq'   ]           
    steps               = MDYNAMICS_PARAMETERS['nsteps_EQ'  ]          
    temperature         = MDYNAMICS_PARAMETERS['temperature']        
    timeStep            = MDYNAMICS_PARAMETERS['timestep'   ]           
    coll_freq           = MDYNAMICS_PARAMETERS['coll_freq'  ]          
    # . Equilibration.                                               
    LangevinDynamics_SystemGeometry (system,                 
                    logFrequency        =   logFrequency,      
                    #log                 =   dualLog,          
                    #rng                 =   rng,              
                    steps               =   steps,             
                    timeStep            =  timeStep,             
                    collisionFrequency  = coll_freq,           
                    temperature         = temperature)         
    #----------------------------------------------------------------


                              #--------------------------#
                              #      DATA COLLECTION     #
                              #--------------------------#
    #-----------------------------------------------------------------------
    steps               = MDYNAMICS_PARAMETERS['nsteps_DC']                 
    trajectory = SystemSoftConstraintTrajectory ( trajname, system, mode = "w" )  
                                                                            
    LangevinDynamics_SystemGeometry (system,                        
                    trajectories        =[ ( trajectory, 1) ],        
                    logFrequency        =   logFrequency,             
                    #log                 =   dualLog,                 
                    #rng                 =   rng,                     
                    steps               =   steps,                    
                    timeStep            =  timeStep,                    
                    collisionFrequency  = coll_freq,                  
                    temperature         = temperature)                
    #-----------------------------------------------------------------------
    energy = system.Energy (log                 = None )
    ##print energy
    return energy


def Run_VelocityVerletDynamics (system = None, trajname = None,  MDYNAMICS_PARAMETERS = {}):
    """ Function doc """

                                  #--------------------------#
                                  #       EQUILIBRATION      #
                                  #--------------------------#
    #----------------------------------------------------------------------------------------#
                                                                                             #
    logFrequency        = MDYNAMICS_PARAMETERS['log_freq']                                   #
    steps               = MDYNAMICS_PARAMETERS['nsteps_EQ']                                  #
    temperature         = MDYNAMICS_PARAMETERS['temperature']                                #
    timeStep            = MDYNAMICS_PARAMETERS['timestep']                                   #
    temp_scale_freq     = MDYNAMICS_PARAMETERS['temp_scale_freq']                            #
                                                                                             #
    # . Equilibration.                                                                       #
    VelocityVerletDynamics_SystemGeometry(system,                                            #
                                        #rng                      =   rng,                   #
                                        log                       =   None,                  #
                                        logFrequency              =   logFrequency,          #
                                        steps                     =   steps,                 #
                                        timeStep                  =   timeStep,              #
                                        temperatureScaleFrequency =   temp_scale_freq,       #
                                        temperatureScaleOption    =   "constant",            #
                                        temperatureStart          =   temperature )          #
    #----------------------------------------------------------------------------------------#                    


                              #--------------------------#
                              #      DATA COLLECTION     #
                              #--------------------------#
    #----------------------------------------------------------------------------------------#
    steps               = MDYNAMICS_PARAMETERS['nsteps_DC']                                  #
    trajectory = SystemSoftConstraintTrajectory ( trajname, system, mode = "w" )             #
    VelocityVerletDynamics_SystemGeometry(system,                                            #
                                        trajectories              =   [ ( trajectory, 1) ],  #
                                        log                       =   None,                  #
                                        #rng                      =   rng,                   #
                                        logFrequency              =   logFrequency,          #
                                        steps                     =   steps,                 #
                                        timeStep                  =   timeStep,              #
                                        temperatureScaleFrequency =   temp_scale_freq,       #
                                        temperatureScaleOption    =   "constant",            #
                                        temperatureStart          =   temperature )          #
    #----------------------------------------------------------------------------------------#
    energy = system.Energy (log                 = None )
    ##print energy
    return energy

    
def Run_LeapFrogDynamics (system = None, trajname = None,  MDYNAMICS_PARAMETERS = {}):
    """ Function doc """
    
                              #---------------------------#
                              #       EQUILIBRATION       #
                              #---------------------------#
    #-------------------------------------------------------------------------------#
    logFrequency        = MDYNAMICS_PARAMETERS['log_freq']                          #
    steps               = MDYNAMICS_PARAMETERS['nsteps_EQ']                         #
    temperature         = MDYNAMICS_PARAMETERS['temperature']                       #
    temperatureCoupling = MDYNAMICS_PARAMETERS['temperatureCoupling']               #
    timeStep            = MDYNAMICS_PARAMETERS['timestep']                          #
                                                                                    #
    # . Equilibration.                                                              #
    LeapFrogDynamics_SystemGeometry ( system                  ,                     #
                                      log                 = None,                   #
                                      logFrequency        = logFrequency,           #
                                      #rng                 = rng,                   #
                                      steps               = steps,                  #
                                      temperature         = temperature,            #
                                      temperatureCoupling = temperatureCoupling,    #
                                      timeStep            = timeStep  )             #
    #-------------------------------------------------------------------------------#

                              #--------------------------#
                              #      DATA COLLECTION     #
                              #--------------------------#
    #--------------------------------------------------------------------------------#                  
                                                                                     #
    # . Data-collection.                                                             #
    trajectory = SystemSoftConstraintTrajectory ( trajname, system, mode = "w" )     #
                                                                                     #
                                                                                     #
    steps               = MDYNAMICS_PARAMETERS['nsteps_DC']                          #
    LeapFrogDynamics_SystemGeometry ( system,                                        #
                                      logFrequency        = logFrequency,            #
                                      log                 = None,                    #
                                      steps               = steps,                   #
                                      temperature         = temperature,             #
                                      temperatureCoupling = temperatureCoupling,     #
                                      timeStep            = timeStep,                #
                                      trajectories        = [ ( trajectory, 1 ) ] )  #
    #--------------------------------------------------------------------------------#



    energy = system.Energy (log                 = None )
    ##print energy
    return energy










def run_WHAM (PARAMETERS):
    """ Function doc """
    
    
                                   # Local time  -  LogFileName 
    #----------------------------------------------------------------------------------------
    localtime = time.asctime(time.localtime(time.time()))                                    
    localtime = localtime.split()                                                            
    #  0     1    2       3         4                                                        
    #[Sun] [Sep] [28] [02:32:04] [2014]                                                      
    LogFile = 'Potential_of_Mean_Force' + localtime[1] +'_' + localtime[2] + '_'+localtime[3]+'_' + localtime[4]+'.log'       #
    #----------------------------------------------------------------------------------------
    log     = DualTextLog(PARAMETERS['output'],  LogFile)
    
    # . Calculate the PMF.

    Bins                  = int(PARAMETERS['Bins'                ])   
    LogFrequency          = int(PARAMETERS['LogFrequency'        ])
    MaximumIterations     = int(PARAMETERS['MaximumIterations'   ])
    RMSGradientTolerance  = float(PARAMETERS['RMSGradientTolerance'])
    Temperature           = float(PARAMETERS['Temperature'         ])
    trajectory_blocks     = (PARAMETERS['trajectory_blocks'   ])
    
    state = WHAM_ConjugateGradientMinimize (trajectory_blocks                          ,
                                            log                  = log                 ,
                                            bins                 = [ Bins ]            ,
                                            logFrequency         =  LogFrequency       ,
                                            maximumIterations    =  MaximumIterations  ,
                                            rmsGradientTolerance = RMSGradientTolerance,
                                            temperature          = Temperature ) 
    
    print 'saving WHAM logfile: ',os.path.join (PARAMETERS['output'], LogFile )
    return os.path.join (PARAMETERS['output'], LogFile )
    
    #state = WHAM_ConjugateGradientMinimize (fileNames                      ,
    #                                        bins                 = [ 100 ] ,
    #                                        logFrequency         =      1  ,
    #                                        maximumIterations    =   1000  ,
    #                                        rmsGradientTolerance = 1.0e-3  ,
    #                                        temperature          = 300.0   )
    
    # . Write the PMF to a file.
    #histogram = state["Histogram"]
    #pmf       = state["PMF"      ]
    #histogram.ToTextFileWithData ( os.path.join (PARAMETERS['output'], LogFile ), [ pmf ], format = "{:20.3f} {:20.3f}\n" )

