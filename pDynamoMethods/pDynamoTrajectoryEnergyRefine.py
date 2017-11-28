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
import numpy as np
# pDynamo
from pBabel import *
from pCore import *
from pMolecule import *
from pMoleculeScripts import *

from DualTextLogFileWriter3 import *
from pprint import pprint
import multiprocessing
EasyHybrid_ROOT = os.getcwd()
PDYNAMO_SCRATCH = os.environ.get('PDYNAMO_SCRATCH')


EasyHybrid_TMP = os.path.join(PDYNAMO_SCRATCH, '.EasyHybrid')
if not os.path.isdir(EasyHybrid_TMP):
    os.mkdir(EasyHybrid_TMP)
    print "Temporary files directory:  %s" % EasyHybrid_TMP



def parallel_energy_refine_1D (job):
    """ 
    job = [i, None, REACTION_COORD1, None, trajectory, system, File]
    """
    i                =  job[0]
    j                =  job[1]
    REACTION_COORD1  =  job[2] 
    REACTION_COORD2  =  job[3]
    trajectory       =  job[4]
    system           =  job[5]
    coordinate_file  =  job[6]


    system.coordinates3  = Unpickle(os.path.join(trajectory, coordinate_file))
    
    
    mode       = REACTION_COORD1['MODE'] 

    if mode == "simple-distance":    	    									
	coord1_ATOM1         = REACTION_COORD1['ATOM1'     ]           
	coord1_ATOM1_name    = REACTION_COORD1['ATOM1_name']           
	coord1_ATOM2         = REACTION_COORD1['ATOM2'     ]           
	coord1_ATOM2_name    = REACTION_COORD1['ATOM2_name']                
	dist                 = system.coordinates3.Distance ( coord1_ATOM1, coord1_ATOM2)
	rcoord = [dist]

    if mode == "multiple-distance":
	coord1_ATOM1         = REACTION_COORD1['ATOM1'     ]           
	coord1_ATOM1_name    = REACTION_COORD1['ATOM1_name']           
	coord1_ATOM2         = REACTION_COORD1['ATOM2'     ]           
	coord1_ATOM2_name    = REACTION_COORD1['ATOM2_name']	          
	coord1_ATOM3         = REACTION_COORD1['ATOM3'     ]           
	coord1_ATOM3_name    = REACTION_COORD1['ATOM3_name']	          
									    
	distance_a1_a2       =  system.coordinates3.Distance ( coord1_ATOM1, coord1_ATOM2)
	distance_a2_a3       =  system.coordinates3.Distance ( coord1_ATOM2, coord1_ATOM3)
	dist = distance_a1_a2 - distance_a2_a3  
	rcoord = [distance_a1_a2, distance_a2_a3, dist]


    energy              = system.Energy()
    dipole              = system.DipoleMoment ()    
    
    
    
    
    
    output_parameters = {
			 i : {
			      'energy': energy,
			      'dipole': dipole,
			      'coord1': rcoord,
			      'coord2': None
			     } 
			}     
    return output_parameters
    
    

def pDynamoTrajectoryEnergyRefine (system           = None     , 
				   data_path        = None     ,     
				   trajectory       = None     ,  
				   REACTION_COORD1  = None     ,
				   REACTION_COORD2  = None     ,
				   input_type       = 'pkl'    , 
				   _type            = 'Scan 1D',
				   nCPUs            = 1        ):

                               # Local time  -  LogFileName 
    #----------------------------------------------------------------------------------------
    localtime = time.asctime(time.localtime(time.time()))                                    
    localtime = localtime.split()                                                            
    #  0     1    2       3         4                                                        
    #[Sun] [Sep] [28] [02:32:04] [2014]                                                      
    LogFile = 'Energy_' + localtime[1] +'_' + localtime[2] + '_'+localtime[3]+'_' + localtime[4]+'.log'       #
    #----------------------------------------------------------------------------------------
    
    log = DualTextLog(data_path, LogFile)  # LOG
    system.Summary(log=log)
    
    #--------------------#
    #    Initial time    #
    #--------------------#
    t_initial = time.time()

    #---------------------------------#
    #             SUMMARY             #
    #---------------------------------#
    
    if _type == '1D':
	
	Files    = os.listdir(trajectory)             
	multjobs = []                                 
    
	for File in Files:                            
	    name  = File.replace('frame', '')
	    name  = name.split('.')               
	    
	    if name[-1] ==  input_type:               
		
		name = name[0].split('_')
		i    = int(name[-1])
		multjobs.append([i, None, REACTION_COORD1, None, trajectory, system, File])
	
	#--------------------------------------------------------------------------#
	p = multiprocessing.Pool(nCPUs)                                            #
	muiltdata = (p.map(parallel_energy_refine_1D, multjobs ))                  #
	#--------------------------------------------------------------------------#
	total = len(muiltdata)
	X = np.zeros( (total,1) )

	job_results  = [None]*total
	for data in muiltdata:
	    _key              = data.keys()
	    _key              = _key[0]
	    X[_key][0]        = data[_key]['energy']
	    #job_results[_key] = str(_key) +' '+str(data[_key]['coord1']) + str(data[_key]['energy'])
	    #                      0             1                 2                3      4
	    job_results[_key] = [ _key, data[_key]['coord1'], data[_key]['energy'] ]

	min_value = np.min(X)	
	
	
	text = ''
	if REACTION_COORD1['MODE'] == "simple-distance":
	    text = text + "\n"
	    text = text + "\n--------------------------------------------------------------------------------"
	    text = text + "\n                              EasyHybrid SCAN"
	    text = text + "\n--------------------------------------------------------------------------------"
	    text = text + "\n"
	    text = text + "\n------------------------- EasyHybrid SCAN Simple-Distance -----------------------"
	                                                                                         
	    text = text + "\nATOM1                  =%15i  ATOM NAME1             =%15s"     % ( REACTION_COORD1['ATOM1'], REACTION_COORD1['ATOM1_name'])
	    text = text + "\nATOM2                  =%15i  ATOM NAME2             =%15s"     % ( REACTION_COORD1['ATOM2'], REACTION_COORD1['ATOM2_name'])
	    text = text + "\nTYPE                   = ENERGY REFINAMENT"
	    text = text + "\n--------------------------------------------------------------------------------"
	    
	    text = text + "\n\n-------------------------------------------------------------------------------------------------------------------------"
	    text = text + "\n       Frame     distance-pK1-pK2         Energy(kJ/mol)       Energy_Norm(kJ/mol)         Energy(kCal/mol)"
	    text = text + "\n---------------------------------------------------------------------------------------------------------------------------"
	
	    for line in job_results:
		                #0             1            2                3         4            
		text = text + "\n%9i       %13.12f       %13.12f       %13.12f       %13.12f"% (int(line[0])                 , 
		                                                                              float(line[1][0])              , 
											            line[2]                  , 
												    line[2] - min_value      , 
												   (line[2] - min_value)/4.18)
	
	if REACTION_COORD1['MODE'] == "multiple-distance":
	    text = text + "\n"
	    text = text + "\n--------------------------------------------------------------------------------"
	    text = text + "\n                              EasyHybrid SCAN"
	    text = text + "\n--------------------------------------------------------------------------------"
	    text = text + "\n"
	    text = text + "\n------------------------ EasyHybrid SCAN Multiple-Distance ----------------------"	
	    text = text + "\nATOM1                  =%15i  ATOM NAME1             =%15s"     % ( REACTION_COORD1['ATOM1'], REACTION_COORD1['ATOM1_name'])
	    text = text + "\nATOM2*                 =%15i  ATOM NAME2             =%15s"     % ( REACTION_COORD1['ATOM2'], REACTION_COORD1['ATOM2_name'])
	    text = text + "\nATOM3                  =%15i  ATOM NAME3             =%15s"     % ( REACTION_COORD1['ATOM3'], REACTION_COORD1['ATOM3_name'])		
	    text = text + "\nTYPE                   = ENERGY REFINAMENT"
	    text = text + "\n--------------------------------------------------------------------------------"
	    text = text + "\n\n--------------------------------------------------------------------------------------------------------------------------------------------------------"
	    text = text + "\n      Frame     distance1-pK1-pK2      distance2-pK2-pK3      dis1-dis2         Energy(kJ/mol)       Energy_Norm(kJ/mol)         Energy(kCal/mol)"
	    text = text + "\n----------------------------------------------------------------------------------------------------------------------------------------------------------"

	    for line in job_results:                                                             # index           Dist           energy   energy norm           energy kcal
				#0             1            2                3         4             5              6
		text = text + "\n%9i       %13.12f       %13.12f       %13.12f       %13.12f       %13.12f       %13.12f"% (int(line[0])                      , # 0
															   float(line[1][0])                    , # 1
															   float(line[1][1])                    , # 2
															   float(line[1][0]) - float(line[1][1]), # 3
															         line[2]                        , # 4
															         line[2] - min_value            , # 5
															        (line[2] - min_value)/4.18)       # 6

	text = str(text)
	
	arq = open(os.path.join(data_path, LogFile), 'a')
	arq.writelines(text)
	arq.close()

	for line in job_results:
	    print line[0], line[1], line[2], line[2] - min_value, (line[2] - min_value)/4.18
	
	print '\n\nSaving results:'
	print os.path.join(data_path, LogFile)
  
    
    
    
    
    
    if _type == '2D':
	
	Files    = os.listdir(trajectory)             
	multjobs = []                                 
    
	for File in Files:                            
	    File2 = File.split('.')               
	    
	    if File2[-1] ==  'pkl':               
		
		File3 = File2[0].split('_')
		i     = int(File3[-1])
		j     = int(File3[-2])
		multjobs.append([i, j, trajectory, system, File])
    
    
    
    
    '''	system.coordinates3 = Unpickle(coordinatefile)

    if _type == '1D':
        system.Summary(log=log)
        energy_table  = []
        
        trajectory = SystemGeometryTrajectory (trajectory, system, mode = "r" )

        n = 0 
        while trajectory.RestoreOwnerData ( ):
            energy = system.Energy(log=log)
            dipolo = system.DipoleMoment ()
            energy_table.append(energy)
            n  += 1

        pprint (energy_table)
    '''
    '''
    if _type == '2D':

        #--------------------------------------------------------------#
        trajectory_files   = os.listdir(parameters['trajectory'])      #
        trajectory_files2  = []                                        #
        #--------------------------------------------------------------#
        for File in trajectory_files:                                  #
            File2 = File.split('.')                                    #
                                                                       #
            if File2[-1] == 'pkl':                                     #
                trajectory_files2.append(File)                         #
        #--------------------------------------------------------------#


        for File in  trajectory_files2:
            print File
    '''

        #system.Summary(log=log)
        #energy_table  = []
        #
        #trajectory = SystemGeometryTrajectory (trajectory, system, mode = "r" )
        #
        #n = 0 
        #while trajectory.RestoreOwnerData ( ):
        #    energy = system.Energy(log=log)
        #    dipolo = system.DipoleMoment ()
        #    energy_table.append(energy)
        #    n  += 1
        #
        #pprint (energy_table)




    #else: 
    #    print '_type =  UNK'
    
    #back_orca_output(output_path, step)

    #--------------------#
    #     final time     #
    #--------------------#      
    t_final = time.time()
    total_time  = t_final - t_initial
    #print "Total time = : ", t_final - t_initial
    #return energy


def pDynamoTrajectoryOptimizeEnergyRefine(outpath                 , 
					                      REACTION_COORD1         ,
					                      MINIMIZATION_PARAMETERS ,
					                      MDYNAMICS_PARAMETERS    ,
					                      project
					                      ):

    log     = DualTextLog  (outpath, "TrajectoryOptimizeEnergyRefine.log")  #
    project.system.Summary (log = log)  
    arq = open(os.path.join(outpath, "TrajectoryOptimizeEnergyRefine.log"), "a")

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
        #coord1_DINCREMENT1      = REACTION_COORD1['DINCREMENT']                                                                         #
        #coord1_NWINDOWS1        = REACTION_COORD1['NWINDOWS']                                                                           #
        coord1_FORCECONSTANT1   = REACTION_COORD1['FORCECONSTANT']                                                                      #
        #coord1_DMINIMUM1        = REACTION_COORD1['DMINIMUM']                                                                           #
                                                                                                                                        #
        text = text + "\n----------------------- Coordinate1  - Simple-Distance -------------------------"								#				
        text = text + "\nATOM1                  =%15i  ATOM NAME1             =%15s"     % (coord1_ATOM1,     coord1_ATOM1_name)        #
        text = text + "\nATOM2                  =%15i  ATOM NAME2             =%15s"     % (coord1_ATOM2,     coord1_ATOM2_name)        #
        #text = text + "\nNWINDOWS               =%15i  FORCE CONSTANT         =%15.3f"  % (coord1_NWINDOWS1, coord1_FORCECONSTANT1)    	#		
        #text = text + "\nDMINIMUM               =%15.5f  DINCREMENT             =%15.5f" % (coord1_DMINIMUM1, coord1_DINCREMENT1)    	#		
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
        #coord1_DINCREMENT1      = REACTION_COORD1['DINCREMENT']                                                                         #
        #coord1_NWINDOWS1        = REACTION_COORD1['NWINDOWS']                                                                           #
        coord1_FORCECONSTANT1   = REACTION_COORD1['FORCECONSTANT']                                                                      #
        #coord1_DMINIMUM1        = REACTION_COORD1['DMINIMUM']                                                                           #
        coord1_MASS_WEIGHT      = REACTION_COORD1['mass_weight']                                                                        #
        coord1_sigma_pk1_pk3    = REACTION_COORD1['sigma_pk1_pk3']                                                                      #
        coord1_sigma_pk3_pk1    = REACTION_COORD1['sigma_pk3_pk1']                                                                      #
                                                                                                                                        #
        text = text + "\n--------------------- Coordinate1  - Multiple-Distance -------------------------"								#				
        text = text + "\nATOM1                  =%15i  ATOM NAME1             =%15s"     % (coord1_ATOM1,     coord1_ATOM1_name)        #
        text = text + "\nATOM2*                 =%15i  ATOM NAME2             =%15s"     % (coord1_ATOM2,     coord1_ATOM2_name)        #
        text = text + "\nATOM3                  =%15i  ATOM NAME3             =%15s"     % (coord1_ATOM3,     coord1_ATOM3_name)        #
        text = text + "\nSIGMA ATOM1/ATOM3      =%15.5f  SIGMA ATOM3/ATOM1      =%15.5f" % (coord1_sigma_pk1_pk3, coord1_sigma_pk3_pk1) #
        #text = text + "\nNWINDOWS               =%15i  FORCE CONSTANT         =%15.3f"  % (coord1_NWINDOWS1, coord1_FORCECONSTANT1)    	#		
        #text = text + "\nDMINIMUM               =%15.5f  DINCREMENT             =%15.5f" % (coord1_DMINIMUM1, coord1_DINCREMENT1)    	#		
        text = text + "\n--------------------------------------------------------------------------------"                              #
        
        #if coord1_MASS_WEIGHT:
        #    text = text + '\n'
        #    text = text + '\n---------------------  Using mass weighted restraints  -------------------------'
        #    text = text + '\n                                                                                '
        #    text = text + '\n                           R                    R                               '
        #    text = text + '\n                            \                  /                                '
        #    text = text + '\n                             A1--A2  . . . . A3                                 '
        #    text = text + '\n                            /                  \                                '
        #    text = text + '\n                           R                    R                               '
        #    text = text + '\n                             ^   ^            ^                                 '
        #    text = text + '\n                             |   |            |                                 '
        #    text = text + '\n                            pk1-pk2  . . . . pk3                                '
        #    text = text + '\n                               d1       d2	                                     '
        #    text = text + '\n                                                                                '
        #    text = text + '\n d1 = distance ATOM1/ATOM2                                                      '
        #    text = text + '\n d2 = distance ATOM2/ATOM3                                                      '
        #    text = text + '\n                                                                                '
        #    text = text + '\n sigma_a1_a3 =  mass1/(mass1+mass3)                                             '
        #    text = text + '\n sigma_a3_a1 =  mass3/(mass1+mass3)*-1                                          '
        #    text = text + '\n                                                                                '
        #    text = text + '\n Reaction coordinate =  (sigma_a1_a3 * d1) -(sigma_a3_a1 * d2)                  '
        #    text = text + '\n                                                                                '
        #    text = text + '\n--------------------------------------------------------------------------------'
        #
        #
        #else:
        #    text = text + '\n'
        #    text = text + '\n---------------------  Using mass weighted restraints  -------------------------'
        #    text = text + '\n                                                                                '
        #    text = text + '\n                           R                    R                               '
        #    text = text + '\n                            \                  /                                '
        #    text = text + '\n                             A1--A2  . . . . A3                                 '
        #    text = text + '\n                            /                  \                                '
        #    text = text + '\n                           R                    R                               '
        #    text = text + '\n                             ^   ^            ^                                 '
        #    text = text + '\n                             |   |            |                                 '
        #    text = text + '\n                            pk1-pk2  . . . . pk3                                '
        #    text = text + '\n                               d1       d2	                                     '
        #    text = text + '\n                                                                                '
        #    text = text + '\n d1 = distance ATOM1/ATOM2                                                      '
        #    text = text + '\n d2 = distance ATOM2/ATOM3                                                      '
        #    text = text + '\n                                                                                '
        #    text = text + '\n sigma_a1_a3 =  mass1/(mass1+mass3)                                             '
        #    text = text + '\n sigma_a3_a1 =  mass3/(mass1+mass3)*-1                                          '
        #    text = text + '\n                                                                                '
        #    text = text + '\n Reaction coordinate =  (sigma_a1_a3 * d1) -(sigma_a3_a1 * d2)                  '
        #    text = text + '\n                                                                                '
        #    text = text + '\n--------------------------------------------------------------------------------'
    #-----------------------------------------------------------------------------------------------------------------------------------#

    reaction_path_type  = REACTION_COORD1['REACTION_PATH_TYPE'] 
    trajectory          = REACTION_COORD1['FROM_TRAJECTORY'   ]    
    n_process           = REACTION_COORD1['N_PROCESS'         ]          

            #------------------------------------------------------------#
            #                    GEOMETRY OPTIMIZATION                   #
            #------------------------------------------------------------#
    #------------------------------------------------------------------------------#
    if reaction_path_type == 'from trajectory':                                    #
        
        text = text + "\n----------------------------------------------------------"
        text = text + "\n-        GEOMETRY OPTIMIZATION FROM TRAJECTORY           -"
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
    arq.writelines(text)
    arq.close()	     
    
    project.system.DefineSoftConstraints ( None )





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
                      MINIMIZATION_PARAMETERS = MINIMIZATION_PARAMETERS)
        energy = project.system.Energy (log                 = None )
        print dist, energy
        
    return energy
    
  

def ParseLogFile (filein):
	""" Function doc """
	pass















def main():
    system = Unpickle(EasyHybrid_ROOT + '/test/test.pkl')
    _min_ = pDynamoEnergy(system)
    #_min_    = pDynamoMinimization(system,'Steepest Descent')
    #_min_    = pDynamoMinimization(system,'LBFGS')
    return 0

if __name__ == '__main__':
    main()
