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

# pDynamo
from pBabel                 import *
from pCore                  import *
from pMolecule              import *
from pMoleculeScripts       import *

from DualTextLogFileWriter3 import *
from MatplotGTK.LogParse    import *

#---------------------------------------
from multiprocessing        import Pool
#---------------------------------------

import numpy as np                                        #
import multiprocessing
EasyHybrid_ROOT  = os.environ.get('EasyHybrid_ROOT')
PDYNAMO_SCRATCH = os.environ.get('PDYNAMO_SCRATCH')


EasyHybrid_TMP = os.path.join(PDYNAMO_SCRATCH, '.EasyHybrid')
if not os.path.isdir(EasyHybrid_TMP):
    os.mkdir(EasyHybrid_TMP)
    print "Temporary files directory:  %s" % EasyHybrid_TMP



texto_d1   = "\n\n                       -- simple-distance --\n\nFor simple-distance, select two atoms in pymol using the editing mode\nfollowing the diagram:\n\n   R                    R\n    \                  /\n     A1--A2  . . . . A3\n    /                  \ \n   R                    R\n         ^            ^\n         |            |\n        pk1  . . . . pk2\n                d1\n"
texto_d2d1 = "\n                       -- multiple-distance --\n\nFor multiple-distance, select three atoms in pymol using the editing mode\nfollowing the diagram:\n\n   R                    R\n    \                  /\n     A1--A2  . . . . A3\n    /                  \ \n   R                    R\n     ^   ^            ^\n     |   |            |\n    pk1-pk2  . . . . pk3\n       d1       d2\n"










def Scan2D(outpath            , 
           REACTION_COORD1    ,
           REACTION_COORD2    ,
           PARAMETERS         ,
           project
           ):
    
    #----------------------------------------------#
    #          Preparing the log files             #
    #----------------------------------------------#
    outpath = PARAMETERS['outpath']                #
    logFile = os.path.join(outpath, "Scan2D.log")  #
    log     = DualTextLog(outpath,  "Scan2D.log")  #
    project.system.Summary(log=log)                #
    LogFileName  = 'ScScan2D.log'                  #
    nCPUs = multiprocessing.cpu_count()
    #----------------------------------------------#

    
    
    
    
    text = ""
    text = text + "\n--------------------------------------------------------------------------------"
    text = text + "\n                              EasyHybrid SCAN2D"
    text = text + "\n--------------------------------------------------------------------------------"
    text = text + "\n"
    arq = open(os.path.join(outpath, "Scan2D.log"), 'a') 
    arq.writelines(text)
    text = ''




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
        text = text + "\n----------------------- Coordinate 1 - Simple-Distance -------------------------"								#				
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
        text = text + "\n--------------------- Coordinate 1 - Multiple-Distance -------------------------"								#				
        text = text + "\nATOM1                  =%15i  ATOM NAME1             =%15s"     % (coord1_ATOM1,     coord1_ATOM1_name)        #
        text = text + "\nATOM2*                 =%15i  ATOM NAME2             =%15s"     % (coord1_ATOM2,     coord1_ATOM2_name)        #
        text = text + "\nATOM3                  =%15i  ATOM NAME3             =%15s"     % (coord1_ATOM3,     coord1_ATOM3_name)        #
        text = text + "\nSIGMA ATOM1/ATOM3      =%15.5f  SIGMA ATOM3/ATOM1      =%15.5f" % (coord1_sigma_pk1_pk3, coord1_sigma_pk3_pk1) #
        text = text + "\nNWINDOWS               =%15i  FORCE CONSTANT         =%15.3f"  % (coord1_NWINDOWS1, coord1_FORCECONSTANT1)    	#		
        text = text + "\nDMINIMUM               =%15.5f  DINCREMENT             =%15.5f" % (coord1_DMINIMUM1, coord1_DINCREMENT1)    	#		
        text = text + "\n--------------------------------------------------------------------------------"                              #
    #-----------------------------------------------------------------------------------------------------------------------------------#


							#-----------------#
							#   REAC COORD 2  #
							#-----------------#
    #-----------------------------------------------------------------------------------------------------------------------------------#
    mode2 = REACTION_COORD2['MODE']                                                                                                     #
    if mode2 == 'simple-distance':                                                                                                      #
	    coord2_ATOM1            = REACTION_COORD2['ATOM1'     ]                                                                         #
	    coord2_ATOM1_name       = REACTION_COORD2['ATOM1_name']                                                                         #
	    coord2_ATOM2            = REACTION_COORD2['ATOM2'     ]                                                                         #
	    coord2_ATOM2_name       = REACTION_COORD2['ATOM2_name']                                                                         #
																																	    #
																																	    #
	    coord2_NWINDOWS2        = REACTION_COORD2['NWINDOWS']                                                                           #
	    coord2_DMINIMUM2        = REACTION_COORD2['DMINIMUM']                                                                           #
	    coord2_FORCECONSTANT2   = REACTION_COORD2['FORCECONSTANT']                                                                      #
	    coord2_DINCREMENT2      = REACTION_COORD2['DINCREMENT']                                                                         #
																																	    #
	    text = text + "\n----------------------- Coordinate 2 - Simple-Distance -------------------------"								#			
	    text = text + "\nATOM1                  =%15i  ATOM NAME1             =%15s"     % (coord2_ATOM1,     coord2_ATOM1_name)        #
	    text = text + "\nATOM2                  =%15i  ATOM NAME2             =%15s"     % (coord2_ATOM2,     coord2_ATOM2_name)        #
	    text = text + "\nNWINDOWS               =%15i  FORCE CONSTANT         =%15.3f"  % (coord2_NWINDOWS2, coord2_FORCECONSTANT2)    	#	
	    text = text + "\nDMINIMUM               =%15.5f  DINCREMENT             =%15.5f" % (coord2_DMINIMUM2, coord2_DINCREMENT2)    	#	
	    text = text + "\n--------------------------------------------------------------------------------"                              #
	    text = text + "\n"                                                                                                              #
																																	    #
    if mode2 == "multiple-distance":                                                                                                    #
	    coord2_ATOM1            = REACTION_COORD2['ATOM1'     ]                                                                         #
	    coord2_ATOM1_name       = REACTION_COORD2['ATOM1_name']                                                                         #
	    coord2_ATOM2            = REACTION_COORD2['ATOM2'     ]                                                                         #
	    coord2_ATOM2_name       = REACTION_COORD2['ATOM2_name']                                                                         #
	    coord2_ATOM3            = REACTION_COORD2['ATOM3'     ]                                                                         #
	    coord2_ATOM3_name       = REACTION_COORD2['ATOM3_name']                                                                         #
																																	    #
	    coord2_NWINDOWS2        = REACTION_COORD2['NWINDOWS']                                                                           #
	    coord2_DMINIMUM2        = REACTION_COORD2['DMINIMUM']                                                                           #
	    coord2_FORCECONSTANT2   = REACTION_COORD2['FORCECONSTANT']                                                                      #
	    coord2_DINCREMENT2      = REACTION_COORD2['DINCREMENT']                                                                         #
																																	    #
	    coord2_sigma_pk1_pk3    = REACTION_COORD2['sigma_pk1_pk3']                                                                      #
	    coord2_sigma_pk3_pk1    = REACTION_COORD2['sigma_pk3_pk1']			                                                            #
																																	    #
	    text = text + "\n--------------------- Coordinate 2 - Multiple-Distance -------------------------"								#			
	    text = text + "\nATOM1                  =%15i  ATOM NAME1             =%15s"     % (coord2_ATOM1,     coord2_ATOM1_name)        #
	    text = text + "\nATOM2*                 =%15i  ATOM NAME2             =%15s"     % (coord2_ATOM2,     coord2_ATOM2_name)        #
	    text = text + "\nATOM3                  =%15i  ATOM NAME3             =%15s"     % (coord2_ATOM3,     coord2_ATOM3_name)        #
	    text = text + "\nSIGMA ATOM1/ATOM3      =%15.5f  SIGMA ATOM3/ATOM1      =%15.5f" % (coord2_sigma_pk1_pk3, coord2_sigma_pk3_pk1) #
	    text = text + "\nNWINDOWS               =%15i  FORCE CONSTANT         =%15.3f"  % (coord2_NWINDOWS2, coord2_FORCECONSTANT2)    	#	
	    text = text + "\nDMINIMUM               =%15.5f  DINCREMENT             =%15.5f" % (coord2_DMINIMUM2, coord2_DINCREMENT2)    	#	
	    text = text + "\n--------------------------------------------------------------------------------"                              #
	    text = text + "\n"	                                                                                                            #
    #-----------------------------------------------------------------------------------------------------------------------------------#


			       #------------------#
			       #    PARAMETERS    #
			       #------------------#
    #-----------------------------------------------#
    max_int      = PARAMETERS['max_int']            #
    log_freq     = PARAMETERS['log_freq']           #
    rms_grad     = PARAMETERS['rms_grad']		    #
    mim_method   = PARAMETERS['mim_method']		    #
    #-----------------------------------------------#
    text = str(text)
    arq = open(os.path.join(outpath, "Scan2D.log"), 'a') 
    arq.writelines(text)

    text = ''
    
    X = np.zeros( (coord1_NWINDOWS1, coord2_NWINDOWS2) )





    # . Define a constraint container and assign it to the system.
    constraints  = SoftConstraintContainer ( )
    project.system.DefineSoftConstraints (constraints)
    RCOORD1 = ''
    RCOORD2 = ''


    #-------------------------------------------------------------------------------------------------------------
    text    = text    + "\n"                                                                              
    RCOORD1 = RCOORD1 + '\n'
    RCOORD2 = RCOORD2 + '\n' 
    
    multjobs = []
	
    
    
    #output_parameters = [i, [None]*coord2_NWINDOWS2, [None]*coord2_NWINDOWS2], [None]*coord2_NWINDOWS2]    
    

    #[i, [None]*coord2_NWINDOWS2, [None]*coord2_NWINDOWS2], [None]*coord2_NWINDOWS2]    

    '''#---------------------------------------------------------------------------------------------------------------------#'''

    for i in range ( coord1_NWINDOWS1 ):                                                                          
        
        output_parameters = {
                             i : {
                                  'energy': [],
                                  'coord1': [],
                                  'coord2': []
                                 } 
                            } 
        
        if mode1 == 'simple-distance':                                                                            
            rxncoord     = coord1_DMINIMUM1 + coord1_DINCREMENT1 * float   ( i )                                  
            scModel      = SoftConstraintEnergyModelHarmonic ( rxncoord, coord1_FORCECONSTANT1 )                  
            constraint   = SoftConstraintDistance         ( coord1_ATOM1, coord1_ATOM2, scModel )                 
            constraints["ReactionCoord"] = constraint                                                             
                                                                                                                  
        if mode1 == "multiple-distance":                                                                          
            rxncoord     = coord1_DMINIMUM1 + coord1_DINCREMENT1 * float ( i )                                    
            scmodel      = SoftConstraintEnergyModelHarmonic ( rxncoord, coord1_FORCECONSTANT1 )                  
            constraint   = SoftConstraintMultipleDistance ( [[coord1_ATOM2, coord1_ATOM1,                         
                                                              coord1_sigma_pk1_pk3],                              
                                                              [coord1_ATOM2, coord1_ATOM3, coord1_sigma_pk3_pk1]],
                                                              scmodel )                                           
                                                                                                                  
            constraints["ReactionCoord"] = constraint			                                                  

        j = 0
        if mode2 == 'simple-distance':                                                                            
            rxncoord2    = coord2_DMINIMUM2 + coord2_DINCREMENT2 * float ( j )                                    
            scModel2     = SoftConstraintEnergyModelHarmonic ( rxncoord2, coord2_FORCECONSTANT2 )                 
            constraint2  = SoftConstraintDistance          (coord2_ATOM1, coord2_ATOM2, scModel2)                 
            constraints["ReactionCoord2"] = constraint2				                                              
                                                                                                                
        if mode2 == "multiple-distance":                                                                          
            rxncoord2     = coord2_DMINIMUM2 + coord2_DINCREMENT2 * float ( j )                                   
            scmodel2      = SoftConstraintEnergyModelHarmonic ( rxncoord2, coord2_FORCECONSTANT2 )                
            constraint2   = SoftConstraintMultipleDistance ([[coord2_ATOM2, coord2_ATOM1,                         
                                                              coord2_sigma_pk1_pk3],                              
                                                              [coord2_ATOM2, coord2_ATOM3, coord2_sigma_pk3_pk1]],
                                                              scmodel2 )                                          
            constraints["ReactionCoord2"] = constraint2                                                           
        #-------------------------------------------------------------------------------------------------------------

        #----------   LOG files   --------------#
        _logfile  = outpath+ "/"+"frame_"+str(i)+'_'+str(j)+".log"
        tmp  = DualTextLog(outpath,  "frame_"+str(i)+'_'+str(j)+".log") #
        project.system.Summary(log=tmp)         #
        #---------------------------------------#
                                                 
                              #--------------------------#
                              #    ENERGY MINIMIZATION   #
                              #--------------------------#
        
        #---------------------------------------------------------------------------------------------------------------------#
        if mim_method == 'Conjugate Gradient':                                                                                #
            ConjugateGradientMinimize_SystemGeometry (project.system                  ,                                       #
                                                      log                  = tmp      ,                                       #
                                                      logFrequency         = 1        ,                                       #
                                                      maximumIterations    = max_int  ,                                       #
                                                      rmsGradientTolerance = rms_grad )                                       #
            fileout = os.path.join ( outpath,"frame_" + str(i) + "_" + str(j) + ".pkl")
            try:                                                                                                              #
                XMLPickle ( fileout, project.system.coordinates3 )  #
            except:                                                                                                           #
                Pickle    ( fileout, project.system.coordinates3 )  #
                                                                                                                              #
            distance_a3_a4 = project.system.coordinates3.Distance (coord2_ATOM1, coord2_ATOM2)                                #
            #-----------------------------------------------------------------------------------------------------------------#
	    
	    
	    
	    #-----------------------------------------------------------------------------------------------------------------#
	    #                                            Reaction Coords 1 and 2                                              #
	    #-----------------------------------------------------------------------------------------------------------------#
        if mode1 == 'simple-distance':                                                                    
            distance_a1_a2  = project.system.coordinates3.Distance ( coord1_ATOM1, coord1_ATOM2)
            #RCOORD1         = RCOORD1 + "%18.8f  " % (distance_a1_a2) #' ' + str(distance_a1_a2)
            output_parameters[i]['coord1'].append(distance_a1_a2)

        if mode1 == "multiple-distance":    
            distance_a1_a2  = project.system.coordinates3.Distance ( coord1_ATOM1, coord1_ATOM2)
            distance_a2_a3  = project.system.coordinates3.Distance ( coord1_ATOM2, coord1_ATOM3)
            #RCOORD1         = RCOORD1 + "%18.8f  " %(distance_a1_a2 -  distance_a2_a3)
            output_parameters[i]['coord1'].append(distance_a1_a2 -  distance_a2_a3)

        if mode2 == 'simple-distance':                                                                    
            distance_a1_a2  = project.system.coordinates3.Distance ( coord2_ATOM1, coord2_ATOM2)
            #RCOORD2         = RCOORD2 + "%18.8f  " %(distance_a1_a2)
            output_parameters[i]['coord2'].append(distance_a1_a2)

        if mode2 == "multiple-distance":    
            distance_a1_a2  = project.system.coordinates3.Distance ( coord2_ATOM1, coord2_ATOM2)
            distance_a2_a3  = project.system.coordinates3.Distance ( coord2_ATOM2, coord2_ATOM3)
            #RCOORD2         = RCOORD2 + "%18.8f  " %(distance_a1_a2 -  distance_a2_a3)
            output_parameters[i]['coord2'].append(distance_a1_a2 -  distance_a2_a3)

	    #------------------------------------------------------------------------------------------------------------------                

        try:                                                                                              
            parameters = ParseProcessLogFile (outpath+ "/"+"frame_"+str(i)+'_'+str(j)+".log")                                     
            y = parameters[1]['Y']
            output_parameters[i]['energy'].append(y[-1])
        except:                                                                                                            #
            #print 'nothing'                                                                                               #
            output_parameters[i]['energy'].append(None)

        
        multjobs.append([i, REACTION_COORD1, REACTION_COORD2, outpath, PARAMETERS, project.system, fileout, output_parameters])

    
    
    '''#---------------------------------------------------------------------------------------------------------------------#'''
    
    #--------------------------------------------------------------------------#
    p = multiprocessing.Pool(nCPUs)                                                #
    muiltdata = (p.map(run_Scan2D_in_parallel, multjobs ))                            #
    #--------------------------------------------------------------------------#

    print muiltdata
                       #-----------------#
                       #     S C A N     #
                       #-----------------#
    #---------------------------------------------------------#
    #X = 0*np.random.rand (coord1_NWINDOWS1, coord2_NWINDOWS2) #
    #---------------------------------------------------------#
    
    for data in muiltdata:
        key = data.keys()
        i = key[0]
        j = 0
        for energy  in data[i]['energy']:
            X[i][j] = energy
            j += 1
    
    for data in muiltdata:
        key = data.keys()
        i = key[0]
        j = 0
        RCOORD1 += '\nRCOORD1'
        for coord1  in data[i]['coord1']:
            RCOORD1 = RCOORD1 + "%18.8f  " %(coord1)
            j += 1
	
	
	
    for data in muiltdata:
        key = data.keys()
        i = key[0]
        j = 0
        RCOORD2 += '\nRCOORD2'
        for coord2  in data[i]['coord2']:
            RCOORD2 = RCOORD2 + "%18.8f  " %(coord2)
            j += 1
        
	




    X_norm = X - np.min(X)
    n1     = coord1_NWINDOWS1
    n2     = coord2_NWINDOWS2
    RCOORD1 = RCOORD1 + '\n\n'
    RCOORD2 = RCOORD2 + '\n\n'
    
    for i in range(n1):
        text = text + "\nMATRIX1 "
        for j in range(n2):
            text = text + "%18.8f  " % (X[i][j])
    
    text = text + "\n\n"

    for i in range(n1):
        text = text + "\nMATRIX2 "
        for j in range(n2):
            text = text + "%18.8f  " % (X_norm[i][j])
    
    text = str(text)
    arq.writelines(text)
    arq.writelines('\n\n')
    arq.writelines(RCOORD1)
    arq.writelines(RCOORD2)
    arq.close()
    project.system.DefineSoftConstraints ( None )
    logFile = os.path.join(outpath, "Scan2D.log")
    return X, X_norm, logFile
    

    

def run_Scan2D_in_parallel (Parameters):
    """ Function doc 
    Parameters = [i, REACTION_COORD1, REACTION_COORD2, outpath, PARAMETERS, project, "frame_" + str(i) + "_" + str(j) + ".pkl"]
    """
    i                 = Parameters[0]
    REACTION_COORD1   = Parameters[1]
    REACTION_COORD2   = Parameters[2]
    outpath           = Parameters[3]
    PARAMETERS        = Parameters[4]
    system            = Parameters[5]
    coordinatefile    = Parameters[6]
    output_parameters = Parameters[7]
    # . Define a constraint container and assign it to the system.
    constraints  = SoftConstraintContainer ( )
    system.DefineSoftConstraints (constraints)
    
    #text    = text    + "\nMATRIX1 "                                                                              
    #RCOORD1 = RCOORD1 + '\nRCOORD1'
    #RCOORD2 = RCOORD2 + '\nRCOORD2' 
    
    
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
    #-----------------------------------------------------------------------------------------------------------------------------------#


							#-----------------#
							#   REAC COORD 2  #
							#-----------------#
    #-----------------------------------------------------------------------------------------------------------------------------------#
    mode2 = REACTION_COORD2['MODE']                                                                                                     #
    if mode2 == 'simple-distance':                                                                                                      #
	    coord2_ATOM1            = REACTION_COORD2['ATOM1'     ]                                                                         #
	    coord2_ATOM1_name       = REACTION_COORD2['ATOM1_name']                                                                         #
	    coord2_ATOM2            = REACTION_COORD2['ATOM2'     ]                                                                         #
	    coord2_ATOM2_name       = REACTION_COORD2['ATOM2_name']                                                                         #
																																	    #
																																	    #
	    coord2_NWINDOWS2        = REACTION_COORD2['NWINDOWS']                                                                           #
	    coord2_DMINIMUM2        = REACTION_COORD2['DMINIMUM']                                                                           #
	    coord2_FORCECONSTANT2   = REACTION_COORD2['FORCECONSTANT']                                                                      #
	    coord2_DINCREMENT2      = REACTION_COORD2['DINCREMENT']                                                                         #
																																	    #
    if mode2 == "multiple-distance":                                                                                                    #
	    coord2_ATOM1            = REACTION_COORD2['ATOM1'     ]                                                                         #
	    coord2_ATOM1_name       = REACTION_COORD2['ATOM1_name']                                                                         #
	    coord2_ATOM2            = REACTION_COORD2['ATOM2'     ]                                                                         #
	    coord2_ATOM2_name       = REACTION_COORD2['ATOM2_name']                                                                         #
	    coord2_ATOM3            = REACTION_COORD2['ATOM3'     ]                                                                         #
	    coord2_ATOM3_name       = REACTION_COORD2['ATOM3_name']                                                                         #
																																	    #
	    coord2_NWINDOWS2        = REACTION_COORD2['NWINDOWS']                                                                           #
	    coord2_DMINIMUM2        = REACTION_COORD2['DMINIMUM']                                                                           #
	    coord2_FORCECONSTANT2   = REACTION_COORD2['FORCECONSTANT']                                                                      #
	    coord2_DINCREMENT2      = REACTION_COORD2['DINCREMENT']                                                                         #
																																	    #
	    coord2_sigma_pk1_pk3    = REACTION_COORD2['sigma_pk1_pk3']                                                                      #
	    coord2_sigma_pk3_pk1    = REACTION_COORD2['sigma_pk3_pk1']			                                                            #
    #-----------------------------------------------------------------------------------------------------------------------------------#

			       #------------------#
			       #    PARAMETERS    #
			       #------------------#
    #-----------------------------------------------#
    max_int      = PARAMETERS['max_int']            #
    log_freq     = PARAMETERS['log_freq']           #
    rms_grad     = PARAMETERS['rms_grad']		    #
    mim_method   = PARAMETERS['mim_method']		    #
    #-----------------------------------------------#

    
    #----------------------------------------------------------------------------------#
    #trajectory = REACTION_COORD1['FROM_TRAJECTORY'   ]                                 #
    system.coordinates3 = Unpickle(coordinatefile)#
    #----------------------------------------------------------------------------------#


    
    if mode1 == 'simple-distance':                                                                            
        rxncoord     = coord1_DMINIMUM1 + coord1_DINCREMENT1 * float   ( i )                                  
        scModel      = SoftConstraintEnergyModelHarmonic ( rxncoord, coord1_FORCECONSTANT1 )                  
        constraint   = SoftConstraintDistance         ( coord1_ATOM1, coord1_ATOM2, scModel )                 
        constraints["ReactionCoord"] = constraint                                                             
                                                                                                              
    if mode1 == "multiple-distance":                                                                          
        rxncoord     = coord1_DMINIMUM1 + coord1_DINCREMENT1 * float ( i )                                    
        scmodel      = SoftConstraintEnergyModelHarmonic ( rxncoord, coord1_FORCECONSTANT1 )                  
        constraint   = SoftConstraintMultipleDistance ( [[coord1_ATOM2, coord1_ATOM1,                         
                                                          coord1_sigma_pk1_pk3],                              
                                                          [coord1_ATOM2, coord1_ATOM3, coord1_sigma_pk3_pk1]],
                                                          scmodel )                                           
        constraints["ReactionCoord"] = constraint			                                                  
                                                                                                                  
    
    
    for j in range (1, coord2_NWINDOWS2 ):                                                                          
        if mode2 == 'simple-distance':                                                                            
            rxncoord2    = coord2_DMINIMUM2 + coord2_DINCREMENT2 * float ( j )                                    
            scModel2     = SoftConstraintEnergyModelHarmonic ( rxncoord2, coord2_FORCECONSTANT2 )                 
            constraint2  = SoftConstraintDistance          (coord2_ATOM1, coord2_ATOM2, scModel2)                 
            constraints["ReactionCoord2"] = constraint2				                                              
                                                                                                                
        if mode2 == "multiple-distance":                                                                          
            rxncoord2     = coord2_DMINIMUM2 + coord2_DINCREMENT2 * float ( j )                                   
            scmodel2      = SoftConstraintEnergyModelHarmonic ( rxncoord2, coord2_FORCECONSTANT2 )                
            constraint2   = SoftConstraintMultipleDistance ([[coord2_ATOM2, coord2_ATOM1,                         
                                                              coord2_sigma_pk1_pk3],                              
                                                              [coord2_ATOM2, coord2_ATOM3, coord2_sigma_pk3_pk1]],
                                                              scmodel2 )                                          
            constraints["ReactionCoord2"] = constraint2                                                           
        #-------------------------------------------------------------------------------------------------------------

        #----------   LOG files   --------------#
        tmp  = DualTextLog(outpath,  "frame_"+str(i)+'_'+str(j)+".log") #
        system.Summary(log=tmp)         #
        #---------------------------------------#
                                                 
                              #--------------------------#
                              #    ENERGY MINIMIZATION   #
                              #--------------------------#
        
        #---------------------------------------------------------------------------------------------------------------------#
        if mim_method == 'Conjugate Gradient':                                                                                #
            ConjugateGradientMinimize_SystemGeometry (system                          ,                                       #
                                                      log                  = tmp      ,                                       #
                                                      logFrequency         = 1        ,                                       #
                                                      maximumIterations    = max_int  ,                                       #
                                                      rmsGradientTolerance = rms_grad )                                       #
            try:                                                                                                              #
                XMLPickle ( os.path.join ( outpath,"frame_" + str(i) + "_" + str(j) + ".pkl"), system.coordinates3 )  #
            except:                                                                                                   #
                Pickle    ( os.path.join ( outpath,"frame_" + str(i) + "_" + str(j) + ".pkl"), system.coordinates3 )  #
                                                                                                                              #
            distance_a3_a4 = system.coordinates3.Distance (coord2_ATOM1, coord2_ATOM2)                                #
            #-----------------------------------------------------------------------------------------------------------------#
            #files.append[i, rxncoord, coord2_NWINDOWS2, rxncoord2, outpath,"frame_" + str(i) + "_" + str(j) + ".pkl"]
        
        
        
        #-----------------------------------------------------------------------------------------------------------------#
        #                                            Reaction Coords 1 and 2                                              #
        #-----------------------------------------------------------------------------------------------------------------#
        if mode1 == 'simple-distance':                                                                    
            distance_a1_a2  = system.coordinates3.Distance ( coord1_ATOM1, coord1_ATOM2)
            #RCOORD1         = RCOORD1 + "%18.8f  " % (distance_a1_a2) #' ' + str(distance_a1_a2)
            output_parameters[i]['coord1'].append(distance_a1_a2)

        if mode1 == "multiple-distance":    
            distance_a1_a2  = system.coordinates3.Distance ( coord1_ATOM1, coord1_ATOM2)
            distance_a2_a3  = system.coordinates3.Distance ( coord1_ATOM2, coord1_ATOM3)
            #RCOORD1         = RCOORD1 + "%18.8f  " %(distance_a1_a2 -  distance_a2_a3)
            output_parameters[i]['coord1'].append(distance_a1_a2 -  distance_a2_a3)

        if mode2 == 'simple-distance':                                                                    
            distance_a1_a2  = system.coordinates3.Distance ( coord2_ATOM1, coord2_ATOM2)
            #RCOORD2         = RCOORD2 + "%18.8f  " %(distance_a1_a2)
            output_parameters[i]['coord2'].append(distance_a1_a2)

        if mode2 == "multiple-distance":    
            distance_a1_a2  = system.coordinates3.Distance ( coord2_ATOM1, coord2_ATOM2)
            distance_a2_a3  = system.coordinates3.Distance ( coord2_ATOM2, coord2_ATOM3)
            #RCOORD2         = RCOORD2 + "%18.8f  " %(distance_a1_a2 -  distance_a2_a3)
            output_parameters[i]['coord2'].append(distance_a1_a2 -  distance_a2_a3)
        #------------------------------------------------------------------------------------------------------------------                

        try:                                                                                              
            parameters = ParseProcessLogFile (outpath+ "/"+"frame_"+str(i)+'_'+str(j)+".log")                                     
            y = parameters[1]['Y']
            
            output_parameters[i]['energy'].append(y[-1])

            #x = parameters[1]['X']
            #y = parameters[1]['Y']
            #X[i][j] = y[-1]                                                                                               #
            #text = text + "%18.8f  " % (X[i][j])                                                                          #
            #print text                                                                                                    #
        except:                                                                                                            #
            #print 'nothing'                                                                                               #
            output_parameters[i]['energy'].append(None)


        #multjobs.append([i, REACTION_COORD1, REACTION_COORD2, outpath, PARAMETERS, system, fileout, output_parameters])
        
        
    #---------------------------------------------------------------------------------------------------------------------#
    return output_parameters






def back_orca_output(output_path, step):
    try:
        SCRATCH = os.environ.get('PDYNAMO_SCRATCH')
        #os.rename(SCRATCH + "/job.out", output_path+'/orca_step' + str(step) + ".out" )
        #os.rename(SCRATCH + "/job.gbw", output_path+'/orca_step' + str(step) + ".gbw" )
        #print   "Saving orca output: ", output_path+'/orca_step' + str(step) + ".out"

        os.rename(SCRATCH + "/job.out", output_path+'/step_' + str(step) + "_orca_output.out" )
        os.rename(SCRATCH + "/job.gbw", output_path+'/step_' + str(step) + "_orca_output.gbw" )
        print   "Saving orca output log:", output_path+'/step_' + str(step)  + "_orca_output.out"
        print   "Saving orca output gbw:", output_path+'/step_' + str(step) + "_orca_output.gbw"

    except:
        a = None


def main():
    system = Unpickle(EasyHybrid_ROOT + '/test/test.pkl')
    pDynamoScan = pDynamoScan()
    return 0

if __name__ == '__main__':
    main()


