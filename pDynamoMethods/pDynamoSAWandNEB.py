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
#from PyMOLScripts.PyMOLScripts import PymolGetTable

from pBabel           import *
from pCore            import * 
from pMolecule        import * 
from pMoleculeScripts import *
from DualTextLogFileWriter3 import *



def pDynamoNEB(
            project    = None, 
            parameters = None
            #reactants_file = None, 
            #products_file  = None, 
            #data_path, 
            #NEB_number_of_structures, 
            #NEB_maximum_interations, 
            #NEB_grad_tol, 
            #trajectory_name, 
            #plot_flag
            ):

    if parameters == None:
        parameters = {}
        parameters['reactants_file'           ] = "/home/farminf/Programas/pDynamo-1.9.0/book/data/mol/bala_c7eq.mol"
        parameters['products_file'            ] = "/home/farminf/Programas/pDynamo-1.9.0/book/data/xyz/bala_c5.xyz"
        parameters['data_path'                ] = ''
        parameters['NEB_number_of_structures' ] = 20
        parameters['NEB_maximum_interations'  ] = 2000
        parameters['NEB_grad_tol'             ] = 0.1
        parameters['trajectory_name'          ] = 'NEBtest.trj'
        parameters['plot_flag'                ] = False
    
    
    #parameters['data_path'                ] = ''
    #parameters['NEB_number_of_structures' ] = 20
    #parameters['NEB_maximum_interations'  ] = 2000
    #parameters['NEB_grad_tol'             ] = 0.1
    #parameters['trajectory_name'          ] = 'NEBtest.trj'
    #parameters['plot_flag'                ] = False
    
    reactants_file           = parameters['reactants_file'           ]
    products_file            = parameters['products_file'            ]
    data_path                = parameters['data_path'                ]
    NEB_number_of_structures = parameters['NEB_number_of_structures' ]
    NEB_maximum_interations  = parameters['NEB_maximum_interations'  ]
    NEB_grad_tol             = parameters['NEB_grad_tol'             ]
    trajectory_name          = parameters['trajectory_name'          ]
    plot_flag                = parameters['plot_flag'                ]
    #print parameters





    if project == None:
        # . Define the energy models.
        mmModel = MMModelOPLS ( "bookSmallExamples" )
        nbModel = NBModelFull ( )

        # . Generate the molecule.
        system = MOLFile_ToSystem ("/home/farminf/Programas/pDynamo-1.9.0/book/data/mol/bala_c7eq.mol")
        system.DefineMMModel ( mmModel )
        system.DefineNBModel ( nbModel )

        system.Summary ( )
        
        # Reactants
        reactants=Clone(system.coordinates3)
        # Products
        system.coordinates3 = XYZFile_ToCoordinates3("/home/farminf/Programas/pDynamo-1.9.0/book/data/xyz/bala_c5.xyz")
        products = Clone(system.coordinates3)

    
    else:
        system  = project.system
        
        # Reactants
        project.load_coordinate_file_to_system(reactants_file)
        reactants = Clone(project.system.coordinates3)
        # Products
        project.load_coordinate_file_to_system(products_file)
        products = Clone(project.system.coordinates3)
    
    
    t_initial = time.time()
    
    # Create initial trajectory
    
    trajectoryPath=(os.path.join(data_path, trajectory_name))
    
    if not os.path.isdir(trajectoryPath):
        os.mkdir(trajectoryPath)
        print "Log files will be saved in:  %s" % trajectoryPath
    log = DualTextLog(trajectoryPath, trajectory_name + ".log")  # LOG
    logFile = os.path.join(trajectoryPath, trajectory_name + ".log")
        

    
    system.Summary(log=log)
    
    
    
    GrowingStringInitialPath ( system, 
                               NEB_number_of_structures, 
                               reactants, 
                               products, 
                               trajectoryPath, 
                               maximumIterations    = NEB_maximum_interations, 
                               rmsGradientTolerance = NEB_grad_tol, 
                               log = log)

    
    # Optimize it
    trajectory = SystemGeometryTrajectory ( trajectoryPath, system, mode="a+" ) 
    ChainOfStatesOptimizePath_SystemGeometry (system                                       , 
                                             trajectory                                    ,\
                                             rmsGradientTolerance = NEB_grad_tol           , 
                                             maximumIterations    = NEB_maximum_interations,
                                             logFrequency         = 1                      , 
                                             log = log)
    
    #print trajectoryPath
    #AmberTrajectory_FromSystemGeometryTrajectory( trajectoryPath[:-4]+'.mdcrd', trajectoryPath, system)
    
    t_final = time.time()
    return logFile



def pDynamoSAW(
            project    = None, 
            parameters = None
            ):

    if parameters == None:
        parameters = {}
        parameters['reactants_file'           ] = "/home/farminf/Programas/pDynamo-1.9.0/book/data/mol/bala_c7eq.mol"
        parameters['products_file'            ] = "/home/farminf/Programas/pDynamo-1.9.0/book/data/xyz/bala_c5.xyz"
        parameters['data_path'                ] = ''
        parameters['SAW_number_of_structures' ] = 20
        parameters['SAW_maximum_interations'  ] = 2000
        parameters['SAW_grad_tol'             ] = 0.1
        parameters['trajectory_name'          ] = 'SAWtest.trj'
        parameters['plot_flag'                ] = False
    
    
    reactants_file           = parameters['reactants_file'           ]
    products_file            = parameters['products_file'            ]
    data_path                = parameters['data_path'                ]
    SAW_number_of_structures = parameters['SAW_number_of_structures' ]
    SAW_maximum_interations  = parameters['SAW_maximum_interations'  ]
    SAW_grad_tol             = parameters['SAW_grad_tol'             ]
    trajectory_name          = parameters['trajectory_name'          ]
    plot_flag                = parameters['plot_flag'                ]
    #print parameters

    if project == None:
        # . Define the energy models.
        mmModel = MMModelOPLS ( "bookSmallExamples" )
        nbModel = NBModelFull ( )

        # . Generate the molecule.
        system = MOLFile_ToSystem ("/home/farminf/Programas/pDynamo-1.9.0/book/data/mol/bala_c7eq.mol")
        system.DefineMMModel ( mmModel )
        system.DefineNBModel ( nbModel )

        system.Summary ( )
        
        # Reactants
        reactants=Clone(system.coordinates3)
        # Products
        system.coordinates3 = XYZFile_ToCoordinates3("/home/farminf/Programas/pDynamo-1.9.0/book/data/xyz/bala_c5.xyz")
        products = Clone(system.coordinates3)

    
    else:
        system  = project.system
        # Reactants
        project.load_coordinate_file_to_system(reactants_file)
        reactants = Clone(project.system.coordinates3)
        # Products
        project.load_coordinate_file_to_system(products_file)
        products = Clone(project.system.coordinates3)
    
    
    t_initial = time.time()
    
    #--------------------Create initial trajectory-----------------------------------------
    trajectoryPath=(os.path.join(data_path, trajectory_name))
    if not os.path.isdir(trajectoryPath):
        os.mkdir(trajectoryPath)
        print "Log files will be saved in:  %s" % trajectoryPath
    log = DualTextLog(trajectoryPath, trajectory_name + ".log")  # LOG
    logFile = os.path.join(trajectoryPath, trajectory_name + ".log")
    #--------------------Create initial trajectory-----------------------------------------
        
    system.Summary(log=log)
    
    # . Create a starting trajectory.
    trajectory = SystemGeometryTrajectory.LinearlyInterpolate ( os.path.join ( scratchPath, "cyclohexane_sawPath.trj" ), molecule, 11, reactants, products )

    # . Optimization.
    SAWOptimize_SystemGeometry ( system                    ,
                                 trajectory                  ,
                                 gamma             = 1000.0  ,
                                 maximumIterations = 200     )
    

    
    t_final = time.time()
    return logFile



#pDynamoNEB()

