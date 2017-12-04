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


def get_normal_deviate_generator(seed):
    """Create a normal deviate generator to set the random seed.

    :param seed: The random seed.
    """
    randomNumberGenerator = RandomNumberGenerator( )
    normalDeviateGenerator = NormalDeviateGenerator.WithRandomNumberGenerator(
            randomNumberGenerator)
    randomNumberGenerator.SetSeed(seed)
    return normalDeviateGenerator


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
        coord1_MASS_WEIGHT      = REACTION_COORD1['mass_weight']                                                                        #
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
					   frame  = "frame" +  str(i),           #
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
        if MD_mode == "Leap Frog Dynamics":	                                 #
            energy = Run_LeapFrogDynamics(system = project.system     ,          #
                                        trajname = trajname           ,          #
                            MDYNAMICS_PARAMETERS = MDYNAMICS_PARAMETERS)         #
                                                                                 #
        if MD_mode ==  "Langevin Dynamics":                                      #
            energy = Run_LangevinDynamics(system = project.system     ,          #
                                        trajname = trajname           ,          #
                            MDYNAMICS_PARAMETERS = MDYNAMICS_PARAMETERS)         #
        #------------------------------------------------------------------------#   
                                              
        ##------------------------------------------------------------------------------------------------------#
        #try:                                                                                                   #
        #    XMLPickle ( os.path.join ( outpath,"frame" +  str(i) +  ".pkl"), project.system.coordinates3 )     #
        #except:                                                                                                #
        #    Pickle    ( os.path.join ( outpath,"frame" +  str(i) +  ".pkl"), project.system.coordinates3 )	   #
        ##------------------------------------------------------------------------------------------------------#



    


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
    #trajname   = os.path.join (outpath, trajname)  #
    
    outpath_opt     = os.path.join (outpath, 'GeometryOptimization')
    if not os.path.isdir(outpath_opt):
        os.mkdir(outpath_opt)
    trajname_opt   = os.path.join (outpath_opt, trajname)
    
    
    outpath_eq      = os.path.join (outpath, 'Equilibration')
    if not os.path.isdir(outpath_eq):
        os.mkdir(outpath_eq)
    trajname_eq    = os.path.join (outpath_eq, trajname)

    outpath_collect = os.path.join (outpath, 'DataCollection')    
    if not os.path.isdir(outpath_collect):
        os.mkdir(outpath_collect)
    trajname_collect  = os.path.join (outpath_collect, trajname)

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
        coord1_MASS_WEIGHT      = REACTION_COORD1['mass_weight']                                                                  
        coord1_sigma_pk1_pk3    = REACTION_COORD1['sigma_pk1_pk3']        
        coord1_sigma_pk3_pk1    = REACTION_COORD1['sigma_pk3_pk1']        
                                                                          
        distance_a1_a2  = project.system.coordinates3.Distance ( coord1_ATOM1, coord1_ATOM2)
        distance_a2_a3  = project.system.coordinates3.Distance ( coord1_ATOM2, coord1_ATOM3)
        
        
        #-------------------------------#
        #           MASS_WEIGHT         #
        #-------------------------------#
        if coord1_MASS_WEIGHT:
            DMINIMUM =  (coord1_sigma_pk1_pk3 * distance_a1_a2) - (coord1_sigma_pk3_pk1 * distance_a2_a3*-1)
        
      
        #-------------------------------#
        #             NORMAL            #
        #-------------------------------#
        else:
            #self.sigma_pk1_pk3 =  1.0
            #self.sigma_pk3_pk1 = -1.0
            DMINIMUM = distance_a1_a2 - distance_a2_a3        
        #dist    = dist12 - dist23

        #------------------------------------------------------------------------------------------------------#                  
        rxncoord     = DMINIMUM #float(dist) #coord1_DMINIMUM1 + coord1_DINCREMENT1 * float ( i )                        #
        scmodel      = SoftConstraintEnergyModelHarmonic ( rxncoord, coord1_FORCECONSTANT1 )                   #
        constraint   = SoftConstraintMultipleDistance ( [[coord1_ATOM2, coord1_ATOM1,                          #
                                                          coord1_sigma_pk1_pk3],                               #
                                                          [coord1_ATOM2, coord1_ATOM3, coord1_sigma_pk3_pk1]], #
                                                          scmodel )                                            #
        constraints["ReactionCoord"] = constraint			                                                   #
        #------------------------------------------------------------------------------------------------------#

    if MINIMIZATION_PARAMETERS['do_minimizaton']:       
        Run_ConjugateGradientMinimize (system = project.system,
                                       frame  = trajname      ,
                      MINIMIZATION_PARAMETERS = MINIMIZATION_PARAMETERS)
        energy = project.system.Energy (log                 = None )
        #print dist, energy
        


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
    
  
  





def Run_ConjugateGradientMinimize (system = None, frame = None, MINIMIZATION_PARAMETERS =  {} ):
    """ Function doc """
    max_int      = MINIMIZATION_PARAMETERS['max_int'   ]       
    log_freq     = MINIMIZATION_PARAMETERS['log_freq'  ]       
    rms_grad     = MINIMIZATION_PARAMETERS['rms_grad'  ]       
    mim_method   = MINIMIZATION_PARAMETERS['mim_method']       
    outpath      = MINIMIZATION_PARAMETERS['outpath'   ]
    #index        = MINIMIZATION_PARAMETERS['index'     ]
    
    ConjugateGradientMinimize_SystemGeometry (system                          , 
                                              log                  =      None, 
                                              logFrequency         = 1        , 
                                              maximumIterations    = max_int  , 
                                              rmsGradientTolerance = rms_grad ) 
    
    try:
        XMLPickle ( os.path.join ( outpath ,frame+'.pkl'),system.coordinates3 )
    except:                                                              
        Pickle    ( os.path.join ( outpath ,frame+'.pkl'),system.coordinates3 )
    
    #---------------------------------------------------------------------------

def Run_LangevinDynamics (system = None, trajname = None,  MDYNAMICS_PARAMETERS = {}):
    
    outpath_collect = MDYNAMICS_PARAMETERS['outpath_collect']
    outpath_eq      = MDYNAMICS_PARAMETERS['outpath_eq']     
                                  
                                  #--------------------------#
                                  #       EQUILIBRATION      #
                                  #--------------------------#
    
    #------------------------------------------------------------------------------------------------------#
    #trajectory = SystemSoftConstraintTrajectory ( trajname, system, mode = "w" )                          #
    outpath_eq = os.path.join(outpath_eq, trajname)                                                        #
    trajectory = SystemGeometryTrajectory(outpath_eq, system, mode="w")                                    #    
                                                                                                           #
    #----------------------------------------------------------------                                      #
    trajectory_freq     = MDYNAMICS_PARAMETERS['trajectory_freq']                                          #
    logFrequency        = MDYNAMICS_PARAMETERS['log_freq'   ]                                              #
    steps               = MDYNAMICS_PARAMETERS['nsteps_EQ'  ]                                              #
    temperature         = MDYNAMICS_PARAMETERS['temperature']                                              #
    timeStep            = MDYNAMICS_PARAMETERS['timestep'   ]                                              #
    coll_freq           = MDYNAMICS_PARAMETERS['coll_freq'  ]                                              #
    seed                = MDYNAMICS_PARAMETERS['seed'       ]                                              #
                                                                                                           #
    normalDeviateGenerator = get_normal_deviate_generator(seed)                                            #
                                                                                                           #
    # . Equilibration.                                                                                     #
    LangevinDynamics_SystemGeometry (system,                                                               #
                    normalDeviateGenerator   =   normalDeviateGenerator,                                   #
		    trajectories             =[ ( trajectory, trajectory_freq) ],                          #
                    logFrequency             =   logFrequency,                                             #
                    #log                     =   dualLog,                                                  #
                    steps                    =   steps,                                                    #
                    timeStep                 =  timeStep,                                                  #
                    collisionFrequency       = coll_freq,                                                  #
                    temperature              = temperature)                                                #
    #------------------------------------------------------------------------------------------------------#


                              #--------------------------#
                              #      DATA COLLECTION     #
                              #--------------------------#
    #------------------------------------------------------------------------------------------------------#
    steps               = MDYNAMICS_PARAMETERS['nsteps_DC']                                                #
    outpath_collect     = os.path.join(outpath_collect, trajname)                                          #
    LangevinDynamics_SystemGeometry (system,                                                               #
                    normalDeviateGenerator = normalDeviateGenerator,                                       #
                    trajectories        =[ ( trajectory, 1) ],                                             #
                    logFrequency        =   logFrequency,                                                  #
                    #log                 =   dualLog,                                                      #
                    steps               =   steps,                                                         #
                    timeStep            =  timeStep,                                                       #
                    collisionFrequency  = coll_freq,                                                       #
                    temperature         = temperature)                                                     #
    #------------------------------------------------------------------------------------------------------#
    energy = system.Energy (log                 = None )
    ##print energy
    return energy


def Run_VelocityVerletDynamics (system = None, trajname = None,  MDYNAMICS_PARAMETERS = {}):
    """ Function doc """
    outpath_collect = MDYNAMICS_PARAMETERS['outpath_collect']
    outpath_eq      = MDYNAMICS_PARAMETERS['outpath_eq']     
                                  
                                  #--------------------------#
                                  #       EQUILIBRATION      #
                                  #--------------------------#
    
    #------------------------------------------------------------------------------------------------------#
    #trajectory = SystemSoftConstraintTrajectory ( trajname, system, mode = "w" )                          #
    outpath_eq = os.path.join(outpath_eq, trajname)                                                        #
    trajectory = SystemGeometryTrajectory(outpath_eq, system, mode="w")                                    #
    trajectory_freq     = MDYNAMICS_PARAMETERS['trajectory_freq']                                          #
    logFrequency        = MDYNAMICS_PARAMETERS['log_freq']                                                 #
    steps               = MDYNAMICS_PARAMETERS['nsteps_EQ']                                                #
    temperature         = MDYNAMICS_PARAMETERS['temperature']                                              #
    timeStep            = MDYNAMICS_PARAMETERS['timestep']                                                 #
    temp_scale_freq     = MDYNAMICS_PARAMETERS['temp_scale_freq']                                          #
    seed                = MDYNAMICS_PARAMETERS['seed'       ]                                              #
                                                                                                           #
    normalDeviateGenerator = get_normal_deviate_generator(seed)                                            #
                                                                                                           #
    # . Equilibration.                                                                                     #
    VelocityVerletDynamics_SystemGeometry(system,                                                          #
                                        normalDeviateGenerator    =   normalDeviateGenerator,              #
                                        trajectories              =[ ( trajectory, trajectory_freq) ],     #
                                        log                       =   None,                                #
                                        logFrequency              =   logFrequency,                        #
                                        steps                     =   steps,                               #
                                        timeStep                  =   timeStep,                            #
                                        temperatureScaleFrequency =   temp_scale_freq,                     #
                                        temperatureScaleOption    =   "constant",                          #
                                        temperatureStart          =   temperature )                        #
    #------------------------------------------------------------------------------------------------------#                    


                              #--------------------------#
                              #      DATA COLLECTION     #
                              #--------------------------#
    #----------------------------------------------------------------------------------------#
    steps               = MDYNAMICS_PARAMETERS['nsteps_DC']                                  #
    outpath_collect     = os.path.join(outpath_collect, trajname)
    
    trajectory = SystemSoftConstraintTrajectory ( outpath_collect, system, mode = "w" )      #
    VelocityVerletDynamics_SystemGeometry(system,                                            #
                                        normalDeviateGenerator    =   normalDeviateGenerator,#
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
    
    outpath_collect = MDYNAMICS_PARAMETERS['outpath_collect']
    outpath_eq      = MDYNAMICS_PARAMETERS['outpath_eq']     
                                  
                                  #--------------------------#
                                  #       EQUILIBRATION      #
                                  #--------------------------#
    
    #------------------------------------------------------------------------------------------------------#
    #trajectory = SystemSoftConstraintTrajectory ( trajname, system, mode = "w" ) 
    outpath_eq = os.path.join(outpath_eq, trajname)                               
    trajectory = SystemGeometryTrajectory(outpath_eq, system, mode="w")           

    trajectory_freq     = MDYNAMICS_PARAMETERS['trajectory_freq']                 
    logFrequency        = MDYNAMICS_PARAMETERS['log_freq']                        
    steps               = MDYNAMICS_PARAMETERS['nsteps_EQ']                       
    temperature         = MDYNAMICS_PARAMETERS['temperature']                     
    temperatureCoupling = MDYNAMICS_PARAMETERS['temperatureCoupling']             
    timeStep            = MDYNAMICS_PARAMETERS['timestep']                        
    seed                = MDYNAMICS_PARAMETERS['seed'       ]

    normalDeviateGenerator = get_normal_deviate_generator(seed)
                                                                                  
    # . Equilibration.                                                            
    LeapFrogDynamics_SystemGeometry ( system                  ,                   
                                      normalDeviateGenerator     = normalDeviateGenerator,
				      trajectories               =[ ( trajectory, trajectory_freq) ],    
                                      log                        = None,                   
                                      logFrequency               = logFrequency,           
                                      #rng                        = rng,                   
                                      steps                      = steps,                  
                                      temperature                = temperature,            
                                      temperatureCoupling        = temperatureCoupling,    
                                      timeStep                   = timeStep  )             
    #------------------------------------------------------------------------------------------------------#

                              #--------------------------#
                              #      DATA COLLECTION     #
                              #--------------------------#
    #-------------------------------------------------------------------------------------------------#                  
                                                                                    
    # . Data-collection.                                                            
    #trajectory = SystemSoftConstraintTrajectory ( trajname, system, mode = "w" )   
                                                                                    
                                                                                    
    steps               = MDYNAMICS_PARAMETERS['nsteps_DC']                         
    outpath_collect     = os.path.join(outpath_collect, trajname)
    trajectory = SystemSoftConstraintTrajectory ( outpath_collect, system, mode = "w" )     
    LeapFrogDynamics_SystemGeometry ( system,                                       
                                      normalDeviateGenerator = normalDeviateGenerator,
                                      logFrequency        = logFrequency,            
                                      log                 = None,                    
                                      steps               = steps,                   
                                      temperature         = temperature,             
                                      temperatureCoupling = temperatureCoupling,     
                                      timeStep            = timeStep,                
                                      trajectories        = [ ( trajectory, 1 ) ] )  
    #--------------------------------------------------------------------------------------------------#



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

