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


GTKDYNAMO_ROOT = os.getcwd()
PDYNAMO_SCRATCH = os.environ.get('PDYNAMO_SCRATCH')


GTKDYNAMO_TMP = os.path.join(PDYNAMO_SCRATCH, '.GTKDynamo')
if not os.path.isdir(GTKDYNAMO_TMP):
    os.mkdir(GTKDYNAMO_TMP)
    print "Temporary files directory:  %s" % GTKDYNAMO_TMP


class pDynamoMinimization():

    """ Class doc """

    def __init__(self, system=None, method='Conjugate Gradient', parameters=None, data_path=None):
        """ Class initialiser """

        self.system = system

        if data_path == None:
            data_path = GTKDYNAMO_TMP

        if parameters == None:
            log = DualTextLog(data_path)
            logFrequency = 1
            trajectory_name = "test_mini"
            trajectory_freq = 1
            maximumIterations = 20
            rmsGradientTolerance = 0.1
            AmberTrajectoryFlag = False
        else:
            log = DualTextLog(data_path)
            logFrequency = parameters['logFrequency']
            trajectory_name = parameters['trajectory']
            trajectory_freq = parameters['trajectory_freq']
            maximumIterations = parameters['maximumIterations']
            rmsGradientTolerance = parameters['rmsGradientTolerance']
            AmberTrajectoryFlag = parameters['AmberTrajectoryFlag']

        # self.system.Summary()

        print 'log                 ', log
        print 'logFrequency        ', logFrequency
        print 'trajectory          ', trajectory_name
        print 'trajectory_freq     ', trajectory_freq
        print 'maximumIterations   ', maximumIterations
        print 'rmsGradientTolerance', rmsGradientTolerance

        #---------------------------------------------------------------------------#
        #                    Removing the temp file: log.gui.txt                    #
        #---------------------------------------------------------------------------#
        #
        try:
            os.rename(
                GTKDYNAMO_TMP + '/log.gui.txt', GTKDYNAMO_TMP + '/log.gui.old')
        #
        except:
            a = None		                                                        #
        #---------------------------------------------------------------------------#

        TrajectoryOutputPath = os.path.join(data_path, trajectory_name)

        if AmberTrajectoryFlag:
            trajectory = AmberTrajectoryFileWriter(
                TrajectoryOutputPath, self.system)
        else:
            trajectory = SystemGeometryTrajectory(
                TrajectoryOutputPath, self.system, mode="w")

        #--------------------#
        #    Initial time    #
        #--------------------#
        t_initial = time.time()

        #---------------------------------#
        #             SUMMARY             #
        #---------------------------------#
        self.system.Summary(log=log)

    #----------------------------------------------#
    #             GEOMETRY OPTMIZATION             #
    #----------------------------------------------#
        if method == 'Conjugate Gradient':
            try:
                ConjugateGradientMinimize_SystemGeometry(self.system,
                                                         log=log,
                                                         logFrequency=logFrequency,
                                                         trajectories=[
                                                             (trajectory, trajectory_freq)],
                                                         maximumIterations=maximumIterations,
                                                         rmsGradientTolerance=rmsGradientTolerance)
            except:
                print 'Conjugate Gradient has failed'

        if method == 'Steepest Descent':
            # self.SteepestDescent(self.parameters)
            try:
                SteepestDescentMinimize_SystemGeometry(self.system,
                                                       log=log,
                                                       logFrequency=logFrequency,
                                                       trajectories=[
                                                           (trajectory, trajectory_freq)],
                                                       maximumIterations=maximumIterations,
                                                       rmsGradientTolerance=rmsGradientTolerance)
            except:
                print 'Steepest Descent has failed'

        if method == 'LBFGS':
            try:
                LBFGSMinimize_SystemGeometry(self.system,
                                             log=log,
                                             logFrequency=logFrequency,
                                             trajectories=[
                                                 (trajectory, trajectory_freq)],
                                             maximumIterations=maximumIterations,
                                             rmsGradientTolerance=rmsGradientTolerance)
            except:
                print 'LBFGS has failed (LBFGS is only available in pDynamo ver 1.8.2 or newer).'

        #------------------- Recording time/data information -------------------#
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

        #------------------------------------------------------------#
        #             Renaming the temp file: log.gui.txt            #
        #------------------------------------------------------------#

        log_filename = TrajectoryOutputPath + '/process.log'
        try:
            os.rename(GTKDYNAMO_TMP + '/log.gui.txt', log_filename)
        except:
            a = None


def main():
    system = Unpickle(GTKDYNAMO_ROOT + '/test/test.pkl')
    _min_ = pDynamoMinimization(system)
    #_min_    = pDynamoMinimization(system,'Steepest Descent')
    #_min_    = pDynamoMinimization(system,'LBFGS')
    return 0

if __name__ == '__main__':
    main()
