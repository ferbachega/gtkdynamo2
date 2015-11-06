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
from pBabel import *
from pCore import *
from pMolecule import *
from pMoleculeScripts import *

from DualTextLogFileWriter3 import *


EasyHybrid_ROOT = os.getcwd()
PDYNAMO_SCRATCH = os.environ.get('PDYNAMO_SCRATCH')


EasyHybrid_TMP = os.path.join(PDYNAMO_SCRATCH, '.EasyHybrid')
if not os.path.isdir(EasyHybrid_TMP):
    os.mkdir(EasyHybrid_TMP)
    print "Temporary files directory:  %s" % EasyHybrid_TMP



def  pDynamoMinimization(  system = None                , 
                           method = 'Conjugate Gradient', 
                       parameters = None                , 
                        data_path = None                , 
                   TrajectoryFlag = True                ):
    
    """ Function doc """
    if data_path == None:
        data_path = EasyHybrid_TMP

    if parameters == None:
        logFrequency         = 1
        trajectory_name      = "test_mini"
        trajectory_freq      = 1
        maximumIterations    = 20
        rmsGradientTolerance = 0.1
        AmberTrajectoryFlag  = False
    else:
        logFrequency         = parameters['logFrequency']
        trajectory_name      = parameters['trajectory']
        trajectory_freq      = parameters['trajectory_freq']
        maximumIterations    = parameters['maximumIterations']
        rmsGradientTolerance = parameters['rmsGradientTolerance']
        AmberTrajectoryFlag  = parameters['AmberTrajectoryFlag']
        TrajectoryFlag       = parameters['TrajectoryFlag']
    # self.system.Summary()

    #---------------------------------------------------------------------------#
    #                    Removing the temp file: log.gui.txt                    #
    #---------------------------------------------------------------------------#
    #
    try:
        os.rename(
            EasyHybrid_TMP + '/log.gui.txt', EasyHybrid_TMP + '/log.gui.old')
    #
    except:
        a = None		                                                        #
    #---------------------------------------------------------------------------#




    TrajectoryOutputPath = os.path.join(data_path, trajectory_name)
    #---------------------------------------------------------------------------#
    #                           TrajectoryOutputPath                            #
    #---------------------------------------------------------------------------#
    if TrajectoryFlag:
     
        if AmberTrajectoryFlag:
            if not os.path.isdir(TrajectoryOutputPath):
                os.mkdir(TrajectoryOutputPath)
            print "Log files will be saved in:  %s" % TrajectoryOutputPath   
            trajectory = AmberTrajectoryFileWriter(TrajectoryOutputPath+'/'+trajectory_name, system)
        
        else:
            trajectory = SystemGeometryTrajectory(TrajectoryOutputPath, system, mode="w")
        
        logFile      = os.path.join(TrajectoryOutputPath, trajectory_name + ".log")
        log          = DualTextLog(TrajectoryOutputPath, trajectory_name + ".log")  # LOG
        trajectories = [(trajectory, trajectory_freq)]

    else:
        # even without the trajectory flag = False,
        # the directory will be created but only
        # containing the logfile.
        if not os.path.isdir(TrajectoryOutputPath):
            os.mkdir(TrajectoryOutputPath)
            print "Log files will be saved in:  %s" % TrajectoryOutputPath
        
        logFile      = os.path.join(TrajectoryOutputPath, trajectory_name + ".log")
        log = DualTextLog(TrajectoryOutputPath, trajectory_name + ".log")  # LOG
        trajectories = None
    #---------------------------------------------------------------------------#

    print 'log                 ', log
    print 'logFrequency        ', logFrequency
    print 'trajectory          ', trajectory_name
    print 'trajectory_freq     ', trajectory_freq
    print 'maximumIterations   ', maximumIterations
    print 'rmsGradientTolerance', rmsGradientTolerance

    #--------------------#
    #    Initial time    #
    #--------------------#
    t_initial = time.time()

    #---------------------------------#
    #             SUMMARY             #
    #---------------------------------#
    system.Summary(log=log)

    #----------------------------------------------#
    #             GEOMETRY OPTIMIZATION             #
    #----------------------------------------------#
    if method == 'Conjugate Gradient':
        try:
            if trajectories == None:
                ConjugateGradientMinimize_SystemGeometry(system                                     ,
                                                         log                  = log                 ,
                                                         logFrequency         = logFrequency        ,
                                                         maximumIterations    = maximumIterations   ,
                                                         rmsGradientTolerance = rmsGradientTolerance)
            else:                                                               
                ConjugateGradientMinimize_SystemGeometry(system                                     ,                
                                                         log                  = log                 ,
                                                         logFrequency         = logFrequency        ,
                                                         trajectories         = trajectories        ,
                                                         maximumIterations    = maximumIterations   ,
                                                         rmsGradientTolerance = rmsGradientTolerance)
            
        except:
            print 'Conjugate Gradient has failed'

    if method == 'Steepest Descent':
        # self.SteepestDescent(self.parameters)
        try:
            if trajectories == None:
                SteepestDescentMinimize_SystemGeometry(system,
                                                       log                  = log,
                                                       logFrequency         = logFrequency,
                                                       maximumIterations    = maximumIterations,
                                                       rmsGradientTolerance = rmsGradientTolerance)
            else:                                                             
                SteepestDescentMinimize_SystemGeometry(system,                
                                                       log                  = log,
                                                       logFrequency         = logFrequency,
                                                       trajectories         = trajectories,
                                                       maximumIterations    = maximumIterations,
                                                       rmsGradientTolerance = rmsGradientTolerance)
        except:
            print 'Steepest Descent has failed'

    if method == 'LBFGS':
        try:
            if trajectories == None:
                LBFGSMinimize_SystemGeometry(system,
                                             log                  = log,
                                             logFrequency         = logFrequency,
                                             maximumIterations    = maximumIterations,
                                             rmsGradientTolerance = rmsGradientTolerance)
            else:                                                   
                LBFGSMinimize_SystemGeometry(system,                
                                             log                  = log,
                                             logFrequency         = logFrequency,
                                             trajectories         = trajectories,
                                             maximumIterations    = maximumIterations,
                                             rmsGradientTolerance = rmsGradientTolerance)
        except:
            print 'LBFGS has failed (LBFGS is only available in pDynamo ver 1.8.2 or newer).'

    #------------------- Printing  time/data information -------------------#
    t_final = time.time()                                                 #
    #
    TotalTime = t_final - t_initial
    #
    print "Total time consumed:", TotalTime, 'seconds'
    #
    localtime = time.asctime(time.localtime(time.time()))                 #
    #
    print "Generated in:", localtime
    #-----------------------------------------------------------------------#
    return logFile

#class pDynamoMinimization():
#
#    """ Class doc """
#
#    def __init__(self, system=None, method='Conjugate Gradient', parameters=None, data_path=None, TrajectoryFlag=True):
#        """ Class initialiser """
#        self.system = system
#
#        if data_path == None:
#            data_path = EasyHybrid_TMP
#
#        if parameters == None:
#            logFrequency         = 1
#            trajectory_name      = "test_mini"
#            trajectory_freq      = 1
#            maximumIterations    = 20
#            rmsGradientTolerance = 0.1
#            AmberTrajectoryFlag  = False
#        else:
#            logFrequency         = parameters['logFrequency']
#            trajectory_name      = parameters['trajectory']
#            trajectory_freq      = parameters['trajectory_freq']
#            maximumIterations    = parameters['maximumIterations']
#            rmsGradientTolerance = parameters['rmsGradientTolerance']
#            AmberTrajectoryFlag  = parameters['AmberTrajectoryFlag']
#            TrajectoryFlag       = parameters['TrajectoryFlag']
#        # self.system.Summary()
#
#        #---------------------------------------------------------------------------#
#        #                    Removing the temp file: log.gui.txt                    #
#        #---------------------------------------------------------------------------#
#        #
#        try:
#            os.rename(
#                EasyHybrid_TMP + '/log.gui.txt', EasyHybrid_TMP + '/log.gui.old')
#        #
#        except:
#            a = None		                                                        #
#        #---------------------------------------------------------------------------#
#
#        
#        
#        
#        TrajectoryOutputPath = os.path.join(data_path, trajectory_name)
#        #---------------------------------------------------------------------------#
#        #                           TrajectoryOutputPath                            #
#        #---------------------------------------------------------------------------#
#        if TrajectoryFlag:
#         
#            if AmberTrajectoryFlag:
#                if not os.path.isdir(TrajectoryOutputPath):
#                    os.mkdir(TrajectoryOutputPath)
#                print "Log files will be saved in:  %s" % TrajectoryOutputPath   
#                trajectory = AmberTrajectoryFileWriter(TrajectoryOutputPath+'/'+trajectory_name, self.system)
#            
#            else:
#                trajectory = SystemGeometryTrajectory(TrajectoryOutputPath, self.system, mode="w")
#
#            log = DualTextLog(TrajectoryOutputPath, trajectory_name + ".log")  # LOG
#            trajectories = [(trajectory, trajectory_freq)]
#
#        else:
#            # even without the trajectory flag = False,
#            # the directory will be created but only
#            # containing the logfile.
#            if not os.path.isdir(TrajectoryOutputPath):
#                os.mkdir(TrajectoryOutputPath)
#                print "Log files will be saved in:  %s" % TrajectoryOutputPath
#            log = DualTextLog(TrajectoryOutputPath, trajectory_name + ".log")  # LOG
#            trajectories = None
#        #---------------------------------------------------------------------------#
#
#        print 'log                 ', log
#        print 'logFrequency        ', logFrequency
#        print 'trajectory          ', trajectory_name
#        print 'trajectory_freq     ', trajectory_freq
#        print 'maximumIterations   ', maximumIterations
#        print 'rmsGradientTolerance', rmsGradientTolerance
#
#        #--------------------#
#        #    Initial time    #
#        #--------------------#
#        t_initial = time.time()
#
#        #---------------------------------#
#        #             SUMMARY             #
#        #---------------------------------#
#        self.system.Summary(log=log)
#
#    #----------------------------------------------#
#    #             GEOMETRY OPTIMIZATION             #
#    #----------------------------------------------#
#        if method == 'Conjugate Gradient':
#            try:
#                ConjugateGradientMinimize_SystemGeometry(self.system,
#                                                         log=log,
#                                                         logFrequency=logFrequency,
#                                                         trajectories=trajectories,
#                                                         maximumIterations=maximumIterations,
#                                                         rmsGradientTolerance=rmsGradientTolerance)
#            except:
#                print 'Conjugate Gradient has failed'
#
#        if method == 'Steepest Descent':
#            # self.SteepestDescent(self.parameters)
#            try:
#                SteepestDescentMinimize_SystemGeometry(self.system,
#                                                       log=log,
#                                                       logFrequency=logFrequency,
#                                                       trajectories=trajectories,
#                                                       maximumIterations=maximumIterations,
#                                                       rmsGradientTolerance=rmsGradientTolerance)
#            except:
#                print 'Steepest Descent has failed'
#
#        if method == 'LBFGS':
#            try:
#                LBFGSMinimize_SystemGeometry(self.system,
#                                             log=log,
#                                             logFrequency=logFrequency,
#                                             trajectories=trajectories,
#                                             maximumIterations=maximumIterations,
#                                             rmsGradientTolerance=rmsGradientTolerance)
#            except:
#                print 'LBFGS has failed (LBFGS is only available in pDynamo ver 1.8.2 or newer).'
#
#        #------------------- Printing  time/data information -------------------#
#        t_final = time.time()                                                 #
#        #
#        TotalTime = t_final - t_initial
#        #
#        print "Total time consumed:", TotalTime, 'seconds'
#        #
#        localtime = time.asctime(time.localtime(time.time()))                 #
#        #
#        print "Generated in:", localtime
#        #-----------------------------------------------------------------------#
#
#
def main():
    system = Unpickle(EasyHybrid_ROOT + '/test/test.pkl')
    _min_ = pDynamoMinimization(system)
    #_min_    = pDynamoMinimization(system,'Steepest Descent')
    #_min_    = pDynamoMinimization(system,'LBFGS')
    return 0

if __name__ == '__main__':
    main()
