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
from pBabel           import *
from pCore            import *
from pMolecule        import *
from pMoleculeScripts import *

from DualTextLogFileWriter3 import *


GTKDYNAMO_ROOT = os.getcwd()
PDYNAMO_SCRATCH = os.environ.get('PDYNAMO_SCRATCH')


GTKDYNAMO_TMP = os.path.join(PDYNAMO_SCRATCH, '.GTKDynamo')
if not os.path.isdir(GTKDYNAMO_TMP):
    os.mkdir(GTKDYNAMO_TMP)
    print "Temporary files directory:  %s" % GTKDYNAMO_TMP



texto_d1   = "\n\n                       -- simple-distance --\n\nFor simple-distance, select two atoms in pymol using the editing mode\nfollowing the diagram:\n\n   R                    R\n    \                  /\n     A1--A2  . . . . A3\n    /                  \ \n   R                    R\n         ^            ^\n         |            |\n        pk1  . . . . pk2\n                d1\n"
texto_d2d1 = "\n                       -- multiple-distance --\n\nFor multiple-distance, select three atoms in pymol using the editing mode\nfollowing the diagram:\n\n   R                    R\n    \                  /\n     A1--A2  . . . . A3\n    /                  \ \n   R                    R\n     ^   ^            ^\n     |   |            |\n    pk1-pk2  . . . . pk3\n       d1       d2\n"


class pDynamoScan():

    def ScanSimpleDistance(self, parameters = None, method = 'Conjugate Gradient'):                 
        outpath         = parameters['outpath'      ]
        ATOM1,          = parameters['ATOM1'        ]
        ATOM1_name,     = parameters['ATOM1_name'   ]
        ATOM2,          = parameters['ATOM2'        ]
        ATOM2_name,     = parameters['ATOM2_name'   ]
        DINCREMENT,     = parameters['DINCREMENT'   ]
        NWINDOWS,       = parameters['NWINDOWS'     ]
        FORCECONSTANT,  = parameters['FORCECONSTANT']
        DMINIMUM,       = parameters['DMINIMUM'     ]
        max_int,        = parameters['max_int'      ]
        log_freq,       = parameters['log_freq'     ]
        rms_grad,       = parameters['rms_grad'     ]
        mim_method,     = parameters['mim_method'   ]
        data_path       = parameters['data_path'    ]


        LogFileName  = 'ScanLog-SimpleDistance.lof'
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
        self.system.DefineSoftConstraints ( constraints )


        for i in range ( NWINDOWS ):
            distance = DINCREMENT * float ( i ) + DMINIMUM
            scModel    = SoftConstraintEnergyModelHarmonic ( distance, FORCECONSTANT )
            constraint = SoftConstraintDistance ( ATOM1, ATOM2, scModel )
            constraints["ReactionCoord"] = constraint			


            # Optmization

            TmpLog = DualTextLog(OutputPath, "_scan_step"+str(i)+".log")
            print 'Step : ',i 

            if method == 'Conjugate Gradient':
                ConjugateGradientMinimize_SystemGeometry (self.system,
                                                          log                  = TmpLog,
                                                          logFrequency         = 1, \
                                                          maximumIterations    = max_int, \
                                                          rmsGradientTolerance = rms_grad )

            if method == 'Steepest Descent':
                SteepestDescentMinimize_SystemGeometry ( self.system,
                                                         log = TmpLog,
                                                         logFrequency         = 1, \
                                                         maximumIterations    = max_int, \
                                                         rmsGradientTolerance = rms_grad )

            if method == 'LBFGS':
                try:
                    LBFGSMinimize_SystemGeometry       (self.system,
                                                        log=TmpLog,
                                                        logFrequency          = 1,
                                                        maximumIterations     = max_int,
                                                        rmsGradientTolerance  = rms_grad)
                except:
                    print 'LBFGS has failed (LBFGS is only available in pDynamo ver 1.8.2 or newer).'

            x,y = parse_log_file (OutputPath + '/' + "_scan_step"+str(i)+".log")

            X_general.append(i)
            Y_general.append(y[-1])

            real_distance = self.system.coordinates3.Distance (ATOM1, ATOM2,)

            text = text + "\n%9i       %13.12f       %13.12f"% (int(i), float(real_distance), float(y[-1]))

            try:
                XMLPickle ( os.path.join (OutputPath,"frame" +  str(i) +  ".pkl"), self.system.coordinates3 )
            except:
                Pickle    ( os.path.join (OutputPath,"frame" +  str(i) +  ".pkl"), self.system.coordinates3 )

            #output_path  = outpath
            #step         = self.step + i
            #backup orca
            #back_orca_output(output_path, step)	
            
        self.system.DefineSoftConstraints ( None )
        #print text
        text = str(text)
        arq.writelines(text)
        arq.close()
        return X_general, Y_general



    #def ScanMultipleDistances(self, parameters = None, method = 'Conjugate Gradient'): 
    #    outpath         = parameters['outpath'      ]
    #    ATOM1,          = parameters['ATOM1'        ]
    #    ATOM1_name,     = parameters['ATOM1_name'   ]
    #    ATOM2,          = parameters['ATOM2'        ]
    #    ATOM2_name,     = parameters['ATOM2_name'   ]
    #    ATOM3,          = parameters['ATOM3'        ]
    #    ATOM3_name,     = parameters['ATOM3_name'   ]
    #    DINCREMENT,     = parameters['DINCREMENT'   ]
    #    NWINDOWS,       = parameters['NWINDOWS'     ]
    #    FORCECONSTANT,  = parameters['FORCECONSTANT']
    #    DMINIMUM,       = parameters['DMINIMUM'     ]
    #    sigma_pk1_pk3   = parameters['sigma_pk1_pk3']
    #    sigma_pk3_pk1   = parameters['sigma_pk3_pk1']
    #    max_int,        = parameters['max_int'      ]
    #    log_freq,       = parameters['log_freq'     ]
    #    rms_grad,       = parameters['rms_grad'     ]
    #    mim_method,     = parameters['mim_method'   ]
    #    data_path       = parameters['data_path'    ]
    #
    #
    #
    #    arq = open(os.path.join(path, LogFileName), "a") # entra aqui o log do scan		
    #    text = ""
    #
    #    text = text + "\n------------------------ GTKDynamo SCAN Multiple-Distance ----------------------"	
    #    text = text + "\nATOM1                  =%15i  ATOM NAME1             =%15s"     % ( ATOM1,         ATOM1_name    )
    #    text = text + "\nATOM2*                 =%15i  ATOM NAME2             =%15s"     % ( ATOM2,         ATOM2_name    )
    #    text = text + "\nATOM3                  =%15i  ATOM NAME3             =%15s"     % ( ATOM3,         ATOM3_name    )		
    #    text = text + "\nNWINDOWS               =%15i  FORCE CONSTANT         =%15i"     % ( NWINDOWS,      FORCECONSTANT )            
    #    text = text + "\nDMINIMUM               =%15.5f  MAX INTERACTIONS       =%15i"   % ( DMINIMUM,      max_int       )
    #    text = text + "\nSTEP SIZE              =%15.7f  RMS GRAD               =%15.7f" % ( DINCREMENT,    rms_grad      )
    #    text = text + "\nSigma atom1 - atom3    =%15.5f  Sigma atom3 - atom1    =%15.5f" % ( sigma_pk1_pk3, sigma_pk3_pk1 )		
    #    text = text + "\n--------------------------------------------------------------------------------"
    #    text = text + "\n\n---------------------------------------------------------------------------"
    #    text = text + "\n      Frame    distance pK1 - pK2    distance pK2 - pK3         Energy     "
    #    text = text + "\n---------------------------------------------------------------------------"
    #    
    #
    #
    #
    #    # recording data
    #    X_general = []
    #    Y_general = []
    #
    #            
    #    # . Define a constraint container and assign it to the system.
    #    constraints = SoftConstraintContainer ( )
    #    self.system.DefineSoftConstraints ( constraints )
    #
    #    if mim_method == 'Conjugate Gradient':
    #
    #        for i in range ( NWINDOWS ):
    #
    #            # Calculate the new reaction coordinate restraint
    #            rxncoord   = DMINIMUM + DINCREMENT * float ( i )
    #            scmodel    = SoftConstraintEnergyModelHarmonic ( rxncoord, FORCECONSTANT )
    #            constraint = SoftConstraintMultipleDistance ( [[ATOM2, ATOM1, sigma_pk1_pk3], [ATOM2, ATOM3, sigma_pk3_pk1]], scmodel )
    #            constraints["ReactionCoord"] = constraint
    #                
    #            # . Optimization.
    #            try:
    #                os.remove(data_path +'/log.gui.txt')
    #            except:
    #                pass
    #            self.system.Summary ( dualLog )
    #            TmpLog = DualTextLog(OutputPath, "_scan_step"+str(i)+".log")
    #
    #            ConjugateGradientMinimize_SystemGeometry ( self.system,
    #                                                        log = TmpLog,
    #                                                        logFrequency         = 1, \
    #                                                        maximumIterations    = max_int, \
    #                                                        rmsGradientTolerance = rms_grad )
    #            
    #            os.rename(data_path +'/log.gui.txt',  outpath+ "/"+"tmp.log")
    #            
    #            x,y = parse_log_file (outpath+ "/"+"tmp.log")
    #
    #            
    #            X_general.append(i)
    #            Y_general.append(y[-1])
    #            real_distance1 = self.system.coordinates3.Distance (ATOM1, ATOM2,)
    #            real_distance2 = self.system.coordinates3.Distance (ATOM2, ATOM3,)
    #
    #
    #            text = text + "\n%9i       %13.12f        %13.12f      %13.12f"% (int(i), float(real_distance1), float(real_distance2), float(y[-1]))
    #
    #            try:
    #                XMLPickle ( os.path.join ( outpath,"frame" +  str(i) +  ".pkl"), self.system.coordinates3 )
    #            except:
    #                Pickle    ( os.path.join ( outpath,"frame" +  str(i) +  ".pkl"), self.system.coordinates3 )
    #        
    #        #print text
    #        text = str(text)
    #        arq.writelines(text)
    #        
    #        arq.close()
    #        
    #        self.system.DefineSoftConstraints ( None )
    #        return X_general, Y_general	
    #
    #    elif mim_method == 'Steepest Descent':
    #
    #        for i in range ( NWINDOWS ):
    #
    #        # Calculate the new reaction coordinate restraint
    #            
    #            rxncoord = DMINIMUM + DINCREMENT * float ( i )
    #            scmodel    = SoftConstraintEnergyModelHarmonic ( rxncoord, FORCECONSTANT )
    #            constraint = SoftConstraintMultipleDistance ( [[ATOM2, ATOM1, sigma_pk1_pk3], [ATOM2, ATOM3, sigma_pk3_pk1]], scmodel )
    #            constraints["ReactionCoord"] = constraint
    #                
    #            # . Optimization.
    #            try:
    #                os.remove(data_path +'/log.gui.txt')
    #            except:
    #                pass
    #            #self.system.Summary ( dualLog )	
    #            #os.rename('log.gui.txt', 'log.gui.old')
    #            
    #            self.system.Summary ( dualLog )
    #            
    #            SteepestDescentMinimize_SystemGeometry ( self.system,
    #                                                        log = dualLog,
    #                                                        logFrequency         = 1, \
    #                                                        maximumIterations    = max_int, \
    #                                                        rmsGradientTolerance = rms_grad )
    #            
    #            os.rename(data_path +'/log.gui.txt',  outpath+ "/"+"tmp.log")
    #            
    #            x,y = parse_log_file (outpath+ "/"+"tmp.log")
    #            
    #            #appending text
    #            #text = text + str(i) + "        "
    #            
    #            X_general.append(i)
    #            Y_general.append(y[-1])
    #            
    #            real_distance1 = self.system.coordinates3.Distance (ATOM1, ATOM2,)
    #            real_distance2 = self.system.coordinates3.Distance (ATOM2, ATOM3,)
    #            
    #            #appending text
    #            #text = text + str(real_distance) + "       "
    #            #appending text
    #            #text = text + str(y[-1]) + "\n"
    #            text = text + "\n%9i       %13.12f        %13.12f      %13.12f"% (int(i), float(real_distance1), float(real_distance2), float(y[-1]))
    #            
    #            try:
    #                XMLPickle ( os.path.join ( outpath,"frame" +  str(i) +  ".pkl"), self.system.coordinates3 )
    #            except:
    #                Pickle    ( os.path.join ( outpath,"frame" +  str(i) +  ".pkl"), self.system.coordinates3 )
    #        
    #        #print text
    #        text = str(text)
    #        arq.writelines(text)
    #        
    #        arq.close()
    #        
    #        self.system.DefineSoftConstraints ( None )
    #        return X_general, Y_general	
    #
    #    elif mim_method == 'LBFGS':
    #
    #        for i in range ( NWINDOWS ):
    #
    #        # Calculate the new reaction coordinate restraint
    #            
    #            rxncoord = DMINIMUM + DINCREMENT * float ( i )
    #            scmodel    = SoftConstraintEnergyModelHarmonic ( rxncoord, FORCECONSTANT )
    #            constraint = SoftConstraintMultipleDistance ( [[ATOM2, ATOM1, sigma_pk1_pk3], [ATOM2, ATOM3, sigma_pk3_pk1]], scmodel )
    #            constraints["ReactionCoord"] = constraint
    #                
    #            # . Optimization.
    #            try:
    #                os.remove(data_path +'/log.gui.txt')
    #            except:
    #                pass
    #            #self.system.Summary ( dualLog )	
    #            #os.rename('log.gui.txt', 'log.gui.old')
    #            
    #            self.system.Summary ( dualLog )
    #            
    #            LBFGSMinimize_SystemGeometry (self.system,
    #                                          log                  = dualLog,
    #                                          logFrequency         = 1,
    #                                          maximumIterations    = max_int,
    #                                          rmsGradientTolerance = rms_grad)
    #            
    #            os.rename(data_path +'/log.gui.txt',  outpath+ "/"+"tmp.log")
    #            
    #            x,y = parse_log_file (outpath+ "/"+"tmp.log")
    #            
    #            #appending text
    #            #text = text + str(i) + "        "
    #            
    #            X_general.append(i)
    #            Y_general.append(y[-1])
    #            
    #            real_distance1 = self.system.coordinates3.Distance (ATOM1, ATOM2,)
    #            real_distance2 = self.system.coordinates3.Distance (ATOM2, ATOM3,)
    #            
    #            #appending text
    #            #text = text + str(real_distance) + "       "
    #            #appending text
    #            #text = text + str(y[-1]) + "\n"
    #            text = text + "\n%9i       %13.12f        %13.12f      %13.12f"% (int(i), float(real_distance1), float(real_distance2), float(y[-1]))
    #            
    #            try:
    #                XMLPickle ( os.path.join ( outpath,"frame" +  str(i) +  ".pkl"), self.system.coordinates3 )
    #            except:
    #                Pickle    ( os.path.join ( outpath,"frame" +  str(i) +  ".pkl"), self.system.coordinates3 )
    #        
    #        #print text
    #        text = str(text)
    #        arq.writelines(text)
    #        
    #        arq.close()
    #        
    #        self.system.DefineSoftConstraints ( None )
    #        return X_general, Y_general	
    #
    #
    #
    def __init__(self, system = None, data_path= None, mode = 'multiple-distance'):
        """ Class initialiser """

        self.system = system
        if data_path == None:
            data_path = GTKDYNAMO_TMP

        # self.system.Summary()

        #---------------------------------------------------------------------------#
        #                    Removing the temp file: log.gui.txt                    #
        #---------------------------------------------------------------------------#
        #                                                                           #
        try:                                                                        #
            os.rename(                                                              #
                GTKDYNAMO_TMP + '/log.gui.txt', GTKDYNAMO_TMP + '/log.gui.old')     #
        #                                                                           #
        except:                                                                     #
            a = None		                                                        #
        #---------------------------------------------------------------------------#
        
        
                                   # Local time  -  LogFileName 
        #---------------------------------------------------------------------------------------------------#
        localtime = time.asctime(time.localtime(time.time()))                                               #
        localtime = localtime.split()                                                                       #
        #  0     1    2       3         4                                                                   #
        #[Sun] [Sep] [28] [02:32:04] [2014]                                                                 #
        LogFile = 'Energy_' + localtime[1] +'_' + localtime[2] + '_'+localtime[3]+'_' + localtime[4]+'.log' # 
        #---------------------------------------------------------------------------------------------------#
        

        log = DualTextLog(data_path, LogFile)  # LOG

        #--------------------#
        #    Initial time    #
        #--------------------#
        t_initial = time.time()

     
        
        #back_orca_output(output_path, step)
        
        #--------------------#
        #     final time     #
        #--------------------#      
        t_final = time.time()
        total_time  = t_final - t_initial
        print "Total time = : ", t_final - t_initial




    def back_orca_output(self, output_path, step):
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
    _min_ = pDynamoEnergy(system)
    return 0

if __name__ == '__main__':
    main()
