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

GTKDYNAMO_ROOT  = os.environ.get('GTKDYNAMO_ROOT')
PDYNAMO_SCRATCH = os.environ.get('PDYNAMO_SCRATCH')


GTKDYNAMO_TMP = os.path.join(PDYNAMO_SCRATCH, '.GTKDynamo')
if not os.path.isdir(GTKDYNAMO_TMP):
    os.mkdir(GTKDYNAMO_TMP)
    print "Temporary files directory:  %s" % GTKDYNAMO_TMP



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
    #----------------------------------------------#
    
    
    
    
    
    text = ""
    text = text + "\n--------------------------------------------------------------------------------"
    text = text + "\n                              GTKDynamo SCAN2D"
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
    
    
    
                       #-----------------#
                       #     S C A N     #
                       #-----------------#
    #---------------------------------------------------------#
    import numpy as np                                        #
    X = 0*np.random.rand (coord1_NWINDOWS1, coord2_NWINDOWS2) #
    #---------------------------------------------------------#

    
    
    # . Define a constraint container and assign it to the system.
    constraints  = SoftConstraintContainer ( )
    project.system.DefineSoftConstraints (constraints)
    
         
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
                                                              scmodel )                                                 #
                                                                                                                        #
            constraints["ReactionCoord"] = constraint			                                                        #
                                                                                                                        #
        text = text + "\nMATRIX1 "                                                                                      #
                                                                                                                        #
        for j in range (coord2_NWINDOWS2):                                                                              #
            if mode2 == 'simple-distance':                                                                              #
                rxncoord2    = coord2_DMINIMUM2 + coord2_DINCREMENT2 * float ( j )                                      #
                scModel2     = SoftConstraintEnergyModelHarmonic ( rxncoord2, coord2_FORCECONSTANT2 )                   #
                constraint2  = SoftConstraintDistance          (coord2_ATOM1, coord2_ATOM2, scModel2)                   #
                constraints["ReactionCoord2"] = constraint2				                                                #
                                                                                                                        #
            if mode2 == "multiple-distance":                                                                            #
                rxncoord2     = coord2_DMINIMUM2 + coord2_DINCREMENT2 * float ( j )                                     #
                scmodel2      = SoftConstraintEnergyModelHarmonic ( rxncoord2, coord2_FORCECONSTANT2 )                  #
                constraint2   = SoftConstraintMultipleDistance ([[coord2_ATOM2, coord2_ATOM1,                           #
                                                                  coord2_sigma_pk1_pk3],                                #
                                                                  [coord2_ATOM2, coord2_ATOM3, coord2_sigma_pk3_pk1]],  #
                                                                  scmodel2 )                                            #
                constraints["ReactionCoord2"] = constraint2                                                             #
    #-------------------------------------------------------------------------------------------------------------------#

            print 'Step : ',i,j
            
            
            #----------   LOG files   --------------#
            tmp  = DualTextLog(outpath,  "tmp.log") #
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
                try:                                                                                                              #
                    XMLPickle ( os.path.join ( outpath,"frame_" + str(i) + "_" + str(j) + ".pkl"), project.system.coordinates3 )  #
                except:                                                                                                           #
                    Pickle    ( os.path.join ( outpath,"frame_" + str(i) + "_" + str(j) + ".pkl"), project.system.coordinates3 )  #
                                                                                                                                  #
                distance_a3_a4 = project.system.coordinates3.Distance (coord2_ATOM1, coord2_ATOM2)                                #
                                                                                                                                  #
                try:                                                                                                              #
                    parameters = ParseProcessLogFile (outpath+ "/"+"tmp.log")                                                     #
                    x = parameters[1]['X']
                    y = parameters[1]['Y']
                    X[i][j] = y[-1]                                                                                               #
                    text = text + "%18.8f  " % (X[i][j])                                                                          #
                    #print text                                                                                                   #
                except:                                                                                                           #
                    print 'nothing'                                                                                               #
            #---------------------------------------------------------------------------------------------------------------------#


    
    X_norm = X - np.min(X)
    n1     = coord1_NWINDOWS1
    n2     = coord2_NWINDOWS2

    text = text + "\n\n"
    
    
    for i in range(n1):
        text = text + "\nMATRIX2 "
        for j in range(n2):
            text = text + "%18.8f  " % (X_norm[i][j])

    #print text  
    #print X
    #print X_norm
    #print text
    text = str(text)
    
    
    arq = open(os.path.join(outpath, "Scan2D.log"), 'a') 
    arq.writelines(text)
    arq.close()
    project.system.DefineSoftConstraints ( None )
    logFile = os.path.join(outpath, "Scan2D.log")
    return X, X_norm, logFile

    
        
        
        
        
        
        
        
        





















'''

def ScanSimpleDistance(parameters = None, project = None):                 
    if parameters != None:
        method          = parameters['method'      ]
        outpath         = parameters['outpath'      ]
        ATOM1           = parameters['ATOM1'        ]
        ATOM1_name      = parameters['ATOM1_name'   ]
        ATOM2           = parameters['ATOM2'        ]
        ATOM2_name      = parameters['ATOM2_name'   ]
        DINCREMENT      = parameters['DINCREMENT'   ]
        NWINDOWS        = parameters['NWINDOWS'     ]
        FORCECONSTANT   = parameters['FORCECONSTANT']
        DMINIMUM        = parameters['DMINIMUM'     ]
        max_int         = parameters['max_int'      ]
        log_freq        = parameters['log_freq'     ]
        rms_grad        = parameters['rms_grad'     ]
        mim_method      = parameters['mim_method'   ]
        data_path       = parameters['data_path'    ]
        OutputPath      =  outpath
    else:
        pass
    logFile = os.path.join(outpath, "ScanLog-SimpleDistance.log")
    log     = DualTextLog(outpath, "ScanLog-SimpleDistance.log")
    project.system.Summary(log=log)
    LogFileName  = 'ScanLog-SimpleDistance.log'
    
    arq = open(os.path.join(outpath, LogFileName), "a") # entra aqui o log do scan		
    text = ""
    text = text + "\n------------------------ GTKDynamo SCAN  Simple-Distance -----------------------"
    text = text + "\nATOM1                  =%15i  ATOM NAME1             =%15s"     % ( ATOM1,      ATOM1_name    )
    text = text + "\nATOM2                  =%15i  ATOM NAME2             =%15s"     % ( ATOM2,      ATOM2_name    )			
    text = text + "\nNWINDOWS               =%15i  FORCE CONSTANT         =%15i"     % ( NWINDOWS,   FORCECONSTANT )            
    text = text + "\nDMINIMUM               =%15.5f  MAX INTERACTIONS       =%15i"   % ( DMINIMUM,   max_int       )
    text = text + "\nSTEP SIZE              =%15.7f  RMS GRAD               =%15.7f" % ( DINCREMENT, rms_grad      )
    text = text + "\n--------------------------------------------------------------------------------"
    text = text + "\n\n------------------------------------------------------"
    text = text + "\n       Frame    distance pK1 - pK2         Energy     "
    text = text + "\n------------------------------------------------------"



    #print "\n\n         SCAN  MODE: ", mode       
    #print "\n"
    #print "  "+ATOM1_name+"   ->-  "+ATOM2_name
    #print " pk1 --- pk2 "
    #print "\n\n"			
    ##print "distance between atom 1 and atom 2: ",distance_a1_a2
    #print "DMINIMUM  : ",DMINIMUM




    # recording data
    X_general = []
    Y_general = []

    # . Define a constraint container and assign it to the system.
    constraints = SoftConstraintContainer ( )
    project.system.DefineSoftConstraints ( constraints )


    for i in range ( NWINDOWS ):
        distance = DINCREMENT * float ( i ) + DMINIMUM
        scModel    = SoftConstraintEnergyModelHarmonic ( distance, FORCECONSTANT )
        constraint = SoftConstraintDistance ( int(ATOM1), int(ATOM2), scModel )
        constraints["ReactionCoord"] = constraint			


        # Optmization

        TmpLog = DualTextLog(outpath, "_scan_step"+str(i)+".log")
        print 'Step : ',i 

        if method == 'Conjugate Gradient':
            ConjugateGradientMinimize_SystemGeometry (project.system,
                                                      log                  = TmpLog,
                                                      logFrequency         = 1, \
                                                      maximumIterations    = max_int, \
                                                      rmsGradientTolerance = rms_grad )

        if method == 'Steepest Descent':
            SteepestDescentMinimize_SystemGeometry ( project.system,
                                                     log = TmpLog,
                                                     logFrequency         = 1, \
                                                     maximumIterations    = max_int, \
                                                     rmsGradientTolerance = rms_grad )

        if method == 'LBFGS':
            try:
                LBFGSMinimize_SystemGeometry       (project.system,
                                                    log=TmpLog,
                                                    logFrequency          = 1,
                                                    maximumIterations     = max_int,
                                                    rmsGradientTolerance  = rms_grad)
            except:
                print 'LBFGS has failed (LBFGS is only available in pDynamo ver 1.8.2 or newer).'

        x,y = ParseProcessLogFile(outpath + '/' + "_scan_step"+str(i)+".log")

        X_general.append(i)
        Y_general.append(y[-1])

        real_distance = project.system.coordinates3.Distance (int(ATOM1), int(ATOM2),)

        text = text + "\n%9i       %13.12f       %13.12f"% (int(i), float(real_distance), float(y[-1]))

        try:
            XMLPickle ( os.path.join (outpath,"frame" +  str(i) +  ".pkl"), project.system.coordinates3 )
        except:
            Pickle    ( os.path.join (outpath,"frame" +  str(i) +  ".pkl"), project.system.coordinates3 )

        #output_path  = outpath
        #step         = self.step + i
        #backup orca
        #back_orca_output(output_path, step)	

    project.system.DefineSoftConstraints ( None )
    #print text
    text = str(text)
    arq.writelines(text)
    arq.close()
    for i in X_general:
        print i, Y_general[i]
    return X_general, Y_general , logFile
    
    

def ScanMultipleDistances(parameters = None, project = None):
    method          = parameters['method'       ]
    outpath         = parameters['outpath'      ]
    ATOM1           = parameters['ATOM1'        ]
    ATOM1_name      = parameters['ATOM1_name'   ]
    ATOM2           = parameters['ATOM2'        ]
    ATOM2_name      = parameters['ATOM2_name'   ]
    ATOM3           = parameters['ATOM3'        ]
    ATOM3_name      = parameters['ATOM3_name'   ]
    DINCREMENT      = parameters['DINCREMENT'   ]
    NWINDOWS        = parameters['NWINDOWS'     ]
    FORCECONSTANT   = parameters['FORCECONSTANT']
    DMINIMUM        = parameters['DMINIMUM'     ]
    sigma_pk1_pk3   = parameters['sigma_pk1_pk3']
    sigma_pk3_pk1   = parameters['sigma_pk3_pk1']
    max_int         = parameters['max_int'      ]
    log_freq        = parameters['log_freq'     ]
    rms_grad        = parameters['rms_grad'     ]
    mim_method      = parameters['mim_method'   ]
    data_path       = parameters['data_path'    ]

    logFile = os.path.join(outpath, "ScanLog-SimpleDistance.log")
    log = DualTextLog(outpath, "ScanLog-MultipleDistance.log")
    project.system.Summary(log=log)
    LogFileName  = 'ScanLog-MultipleDistance.log'
    arq = open(os.path.join(outpath, LogFileName), "a") # entra aqui o log do scan			
    text = ""
    text = text + "\n------------------------ GTKDynamo SCAN Multiple-Distance ----------------------"	
    text = text + "\nATOM1                  =%15i  ATOM NAME1             =%15s"     % ( ATOM1,         ATOM1_name    )
    text = text + "\nATOM2*                 =%15i  ATOM NAME2             =%15s"     % ( ATOM2,         ATOM2_name    )
    text = text + "\nATOM3                  =%15i  ATOM NAME3             =%15s"     % ( ATOM3,         ATOM3_name    )		
    text = text + "\nNWINDOWS               =%15i  FORCE CONSTANT         =%15i"     % ( NWINDOWS,      FORCECONSTANT )            
    text = text + "\nDMINIMUM               =%15.5f  MAX INTERACTIONS       =%15i"   % ( DMINIMUM,      max_int       )
    text = text + "\nSTEP SIZE              =%15.7f  RMS GRAD               =%15.7f" % ( DINCREMENT,    rms_grad      )
    text = text + "\nSigma atom1 - atom3    =%15.5f  Sigma atom3 - atom1    =%15.5f" % ( sigma_pk1_pk3, sigma_pk3_pk1 )		
    text = text + "\n--------------------------------------------------------------------------------"
    text = text + "\n\n---------------------------------------------------------------------------"
    text = text + "\n      Frame    distance pK1 - pK2    distance pK2 - pK3         Energy     "
    text = text + "\n---------------------------------------------------------------------------"
    



    # recording data
    X_general = []
    Y_general = []

            
    # . Define a constraint container and assign it to the system.
    constraints = SoftConstraintContainer ( )
    project.system.DefineSoftConstraints ( constraints )
    for i in range ( NWINDOWS ):

        # Calculate the new reaction coordinate restraint
        rxncoord   = DMINIMUM + DINCREMENT * float ( i )
        scmodel    = SoftConstraintEnergyModelHarmonic ( rxncoord, FORCECONSTANT )
        constraint = SoftConstraintMultipleDistance ( [[ATOM2, ATOM1, sigma_pk1_pk3], [ATOM2, ATOM3, sigma_pk3_pk1]], scmodel )
        constraints["ReactionCoord"] = constraint
            
        TmpLog = DualTextLog(outpath, "_scan_step"+str(i)+".log")
        print 'Step : ',i 



        if method == 'Conjugate Gradient':
            ConjugateGradientMinimize_SystemGeometry (project.system,
                                                      log                  = TmpLog,
                                                      logFrequency         = 1, \
                                                      maximumIterations    = max_int, \
                                                      rmsGradientTolerance = rms_grad )

        if method == 'Steepest Descent':
            SteepestDescentMinimize_SystemGeometry ( project.system,
                                                     log = TmpLog,
                                                     logFrequency         = 1, \
                                                     maximumIterations    = max_int, \
                                                     rmsGradientTolerance = rms_grad )

        if method == 'LBFGS':
            try:
                LBFGSMinimize_SystemGeometry       (project.system,
                                                    log=TmpLog,
                                                    logFrequency          = 1,
                                                    maximumIterations     = max_int,
                                                    rmsGradientTolerance  = rms_grad)
            except:
                print 'LBFGS has failed (LBFGS is only available in pDynamo ver 1.8.2 or newer).'

        x,y = ParseProcessLogFile(outpath + '/' + "_scan_step"+str(i)+".log")

        X_general.append(i)
        Y_general.append(y[-1])


        real_distance1 = project.system.coordinates3.Distance (ATOM1, ATOM2,)
        real_distance2 = project.system.coordinates3.Distance (ATOM2, ATOM3,)


        text = text + "\n%9i       %13.12f        %13.12f      %13.12f"% (int(i), float(real_distance1), float(real_distance2), float(y[-1]))

        try:
            XMLPickle ( os.path.join ( outpath,"frame" +  str(i) +  ".pkl"), project.system.coordinates3 )
        except:                                                              
            Pickle    ( os.path.join ( outpath,"frame" +  str(i) +  ".pkl"), project.system.coordinates3 )

    text = str(text)
    arq.writelines(text)
    arq.close()
    project.system.DefineSoftConstraints ( None )
    return X_general, Y_general	, logFile  
    
'''

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
    system = Unpickle(GTKDYNAMO_ROOT + '/test/test.pkl')
    pDynamoScan = pDynamoScan()
    return 0

if __name__ == '__main__':
    main()
