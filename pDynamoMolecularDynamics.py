#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  pDynamoMolecularDynamics.py
#  
#  Copyright 2014 Fernando Bachega <fernando@bachega>
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
from random                 import *

def RunMolecularDynamics( system, data_path, parameters):
    if parameters != None:
        
        #outpath              = project.data_path      
        trajectory_name      = parameters['trajectory_name'    ]
        nsteps               = parameters['nsteps'             ]                  
        log_freq             = parameters['log_freq'           ]              
        trajectory_freq      = parameters['trajectory_freq'    ]
        timestep             = parameters['timestep'           ]              
        method               = parameters['method'             ]                  
        seed                 = parameters['seed'               ]                      
        temperature          = parameters['temperature'        ]        
        temp_scale_freq      = parameters['temp_scale_freq'    ]
        coll_freq            = parameters['coll_freq'          ]            
        TrajectoryFlag       = parameters['TrajectoryFlag'     ]
        AmberTrajectoryFlag  = parameters['AmberTrajectoryFlag']
        rng = Random()
        rng.seed(seed)


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

            log = DualTextLog(TrajectoryOutputPath, trajectory_name + ".log")  # LOG
            trajectories = [(trajectory, trajectory_freq)]

        else:
            # even without the trajectory flag = False,
            # the directory will be created but only
            # containing the logfile.
            if not os.path.isdir(TrajectoryOutputPath):
                os.mkdir(TrajectoryOutputPath)
                print "Log files will be saved in:  %s" % TrajectoryOutputPath
            log = DualTextLog(TrajectoryOutputPath, trajectory_name + ".log")  # LOG
            trajectories = None
        #---------------------------------------------------------------------------#
    
    system.Summary(log=log)

    # . Define a random number generator in a given state.
    #normalDeviateGenerator = NormalDeviateGenerator.WithRandomNumberGenerator ( RandomNumberGenerator.WithSeed ( 175189 ) )
    
    if method == "Velocity Verlet Dynamics":
        VelocityVerletDynamics_SystemGeometry(system,
                            trajectories              =[ ( trajectory, trajectory_freq) ],
                            #rng                      =   rng,
                            log                       =   log, 
                            #normalDeviateGenerator   =   normalDeviateGenerator ,  # soh vale para a versao 1.8
                            logFrequency              =   log_freq,
                            steps                     =   nsteps,
                            timeStep                  =   timestep,
                            temperatureScaleFrequency =   temp_scale_freq,
                            temperatureScaleOption    =   "constant",
                            temperatureStart          =   temperature )
    
    elif method == "Leap Frog Dynamics":
        LeapFrogDynamics_SystemGeometry(system,
                            trajectories        =[ ( trajectory, trajectory_freq) ],
                            log                 = log,
                            logFrequency        = log_freq,
                            #rng                = rng, 
                            pressure            = 1.0,
                            pressureCoupling    = 2000.0,
                            steps               = nsteps,
                            timeStep            = timestep,
                            temperature         = temperature, 
                            temperatureCoupling = 0.1 
                            )
    
    elif method == "Langevin Dynamics":
        LangevinDynamics_SystemGeometry(system, 
                            trajectories        =[ ( trajectory, trajectory_freq) ],
                            collisionFrequency  = coll_freq, 
                            log                 = log, 
                            logFrequency        = log_freq, 
                            steps               = nsteps, 
                            temperature         = temperature, 
                            #rng                = rng, 
                            timeStep            = timestep )
    else:
        print "Select a method"


def main():
	
	return 0

if __name__ == '__main__':
	main()

