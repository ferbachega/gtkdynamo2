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
from LogParse               import *

GTKDYNAMO_ROOT = os.getcwd()
PDYNAMO_SCRATCH = os.environ.get('PDYNAMO_SCRATCH')


GTKDYNAMO_TMP = os.path.join(PDYNAMO_SCRATCH, '.GTKDynamo')
if not os.path.isdir(GTKDYNAMO_TMP):
    os.mkdir(GTKDYNAMO_TMP)
    print "Temporary files directory:  %s" % GTKDYNAMO_TMP



texto_d1   = "\n\n                       -- simple-distance --\n\nFor simple-distance, select two atoms in pymol using the editing mode\nfollowing the diagram:\n\n   R                    R\n    \                  /\n     A1--A2  . . . . A3\n    /                  \ \n   R                    R\n         ^            ^\n         |            |\n        pk1  . . . . pk2\n                d1\n"
texto_d2d1 = "\n                       -- multiple-distance --\n\nFor multiple-distance, select three atoms in pymol using the editing mode\nfollowing the diagram:\n\n   R                    R\n    \                  /\n     A1--A2  . . . . A3\n    /                  \ \n   R                    R\n     ^   ^            ^\n     |   |            |\n    pk1-pk2  . . . . pk3\n       d1       d2\n"


    
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
    logFile = (outpath, "ScanLog-SimpleDistance.log")
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

    logFile = (outpath, "ScanLog-SimpleDistance.log")
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
