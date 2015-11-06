#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  LogParse.py
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
from pprint import pprint
logList = [
        #'/home/fernando/programs/EasyHybrid2/MatplotGTK/logs/2_step_MolecularDynamics.log'   , 
        #'/home/fernando/programs/EasyHybrid2/MatplotGTK/logs/6_step_GeometryOptmization.log' , 
        #'/home/fernando/programs/EasyHybrid2/MatplotGTK/logs/9_step_GeometryOptmization.log' , 
        #'/home/fernando/programs/EasyHybrid2/MatplotGTK/logs/10_step_GeometryOptmization.log', 
        '/home/fernando/programs/EasyHybrid2/MatplotGTK/logs/Scan2D.log'                     , 
		'/home/fernando/programs/EasyHybrid2/MatplotGTK/logs/Scan2D_m.log',
		#'/home/fernando/programs/EasyHybrid2/MatplotGTK/logs/ScanLog-MultipleDistance.log',
		#'/home/fernando/programs/EasyHybrid2/MatplotGTK/logs/ScanLog-SimpleDistance.log',
        
        #'/home/fernando/programs/EasyHybrid2/MatplotGTK/logs/system_pmf.dat'                 , 
        #'/home/fernando/programs/EasyHybrid2/MatplotGTK/logs/UmbrellaSampling.log'           ,
		#'/home/fernando/programs/EasyHybrid2/MatplotGTK/logs/11_step_MolecularDynamics.log',
		#'/home/fernando/programs/EasyHybrid2/MatplotGTK/logs/12_step_MolecularDynamics.log',
		#'/home/fernando/programs/EasyHybrid2/MatplotGTK/logs/13_step_MolecularDynamics.log',
        ] 




             
def ParseSummaryLogFile (log_file):
    """ Reads a Summary log - Status Bar"""
    
    parameters = {}
    parameters['Energy Model']               = "UNK"
    parameters['Number of Atoms']            = "UNK"
    parameters['El. 1-4 Scaling']            = "UNK"
    parameters['Number of MM Atom Types']    = "UNK"
    parameters['Total MM Charge']            = "UNK"
    parameters['Harmonic Bond Terms']        = "UNK"
    parameters['Harmonic Bond Parameters']   = "UNK"
    parameters['Harmonic Angle Terms']       = "UNK"
    parameters['Harmonic Angle Parameters']  = "UNK"
    parameters['Fourier Dihedral Terms']     = "UNK"
    parameters['Fourier Dihedral Parameters']= "UNK"
    parameters['Fourier Improper Terms']     = "UNK"
    parameters['Number of QC Atoms']         = "0"
    parameters['Number of Fixed Atoms']      = "0"
    parameters['QC Parameter Centers']       = "UNK"
    parameters['Fourier Improper Parameters']= "UNK"
    parameters['Exclusions']                 = "UNK"
    parameters['Energy Base Line']           = "UNK"
    parameters['Crystal Class']              = "-"
    
    log = open( log_file , "r")
    for line in log:
        #print line
        linex = line.split()
        
        try:  # Number of Atoms
            if linex[0] == 'Number':
                if linex[1] == 'of':
                    if linex[2] == 'Atoms':
                        parameters['Number of Atoms'] = linex[4]  
        except:
            pass			
        
        
        try:  # Energy Model    -   Summary for Energy Model "AMBER/ABFS"
            if linex[0] == 'Summary':
                #print line
                if linex[1] == 'for':
                    if linex[2] == 'Energy':
                        if linex[3] == 'Model': 
                            parameters['Energy Model'] = linex[4]
        except:
            
            pass
        
        
        try:  # LJ 1-4 Scaling
            if linex[0] == 'LJ':
                if linex[1] == '1-4':
                    if linex[2] == 'Scaling':
                        parameters['LJ 1-4 Scaling']= linex[4]
            if linex[5] == 'El.':
                if linex[6] == '1-4':
                    if linex[7] == 'Scaling':
                        parameters['El. 1-4 Scaling'] = linex[9]
        except:
            pass

        
        try: # Number of MM Atoms
            if linex[0] == 'Number':
                if linex[1] == 'of':
                    if linex[2] == 'MM':
                        if linex[3] == 'Atoms':
                            if linex[4] == '=':
                                parameters['Number of MM Atoms']= linex[5]
            
            if linex[6] == 'Number':
                if linex[7] == 'of':
                    if linex[8] == 'MM':
                        if linex[9] == 'Atom':
                            if linex[10] == 'Types':
                                parameters['Number of MM Atom Types'] = linex[12]
        except:
            pass


        try: # Harmonic Bond Terms
            if linex[0] == 'Total':
                if linex[1] == 'MM':
                    if linex[2] == 'Charge':
                        parameters['Total MM Charge']= linex[4]
            if linex[5] == 'Harmonic':
                if linex[6] == 'Bond':
                    if linex[7] == 'Terms':
                        parameters['Harmonic Bond Terms'] = linex[9]
        except:

            pass	
        
        
        try: # Harmonic Angle Terms
            if linex[0] == 'Harmonic':
                if linex[1] == 'Bond':
                    if linex[2] == 'Parameters':
                        parameters['Harmonic Bond Parameters']= linex[4]
            if linex[5] == 'Harmonic':
                if linex[6] == 'Angle':
                    if linex[7] == 'Terms':
                        parameters['Harmonic Angle Terms'] = linex[9]
        except:
            pass


        try: # Fourier Dihedral Terms
            if linex[0] == 'Harmonic':
                if linex[1] == 'Angle':
                    if linex[2] == 'Parameters':
                        parameters['Harmonic Angle Parameters']= linex[4]
            if linex[5] == 'Fourier':
                if linex[6] == 'Dihedral':
                    if linex[7] == 'Terms':
                        parameters['Fourier Dihedral Terms'] = linex[9]
        except:
            pass


        try: # Fourier Improper Terms
            if linex[0] == 'Fourier':
                if linex[1] == 'Dihedral':
                    if linex[2] == 'Parameters':
                        parameters['Fourier Dihedral Parameters']= linex[4]
            if linex[5] == 'Fourier':
                if linex[6] == 'Improper':
                    if linex[7] == 'Terms':
                        parameters['Fourier Improper Terms'] = linex[9]
        except:
            pass


        try: # Fourier Improper Parameters and Exclusions
            if linex[0] == 'Fourier':
                if linex[1] == 'Improper':
                    if linex[2] == 'Parameters':
                        parameters['Fourier Improper Parameters']= linex[4]
            if linex[5] == 'Exclusions':
                parameters['Exclusions'] = linex[7]
        except:

            pass

        
        try: #
            if linex[0] == '1-4':
                if linex[1] == 'Interactions':
                    parameters['1-4 Interactions']= linex[3]
            if linex[4] == 'LJ':
                if linex[5] == 'Parameters':
                    if linex[6] == 'Form':
                        parameters['Fourier Improper Terms'] = linex[8]
        except:
            pass

        try:
            if linex[0] == 'LJ':
                if linex[1] == 'Parameters':
                    if linex[2] == 'Types':
                        parameters['LJ Parameters Types']= linex[4]
            if linex[5] == '1-4':
                if linex[6] == 'Lennard-Jones':
                    if linex[7] == 'Form':
                        parameters['1-4 Lennard-Jones Form'] = linex[9]
        except:
            pass


        try:
            if linex[0] == '1-4':
                if linex[1] == 'Lennard-Jones':
                    if linex[2] == 'Types':
                        parameters['1-4 Lennard-Jones Types']= linex[4]
        except:
            pass


        try:
            if linex[0] == 'Dielectric':
                if linex[1] == '=':
                    parameters['Dielectric']= linex[2]
            
            if linex[3] == 'El.':
                if linex[4] == '1-4':
                    if linex[5] == 'Scaling':
                        parameters['El. 1-4 Scaling'] = linex[7]
        except:
            pass


        try:
            if linex[0] == 'Inner':
                if linex[1] == 'Cutoff':
                    parameters['Inner Cutoff']= linex[3]
            
            if linex[4] == 'Outer':
                if linex[5] == 'Cutoff':
                    parameters['Outer Cutoff'] = linex[7]
        except:
            pass


        try:
            if linex[0] == 'List':
                if linex[1] == 'Cutoff':
                    parameters['List Cutoff']= linex[3]
            
            if linex[4] == 'QC/MM':
                if linex[5] == 'Coupling':
                    parameters['QC/MM Coupling'] = linex[7]+' '+linex[8]
        except:
            pass


        try:
            if linex[0] == 'Crystal':
                if linex[1] == 'Class':
                    parameters['Crystal Class']= linex[3]
        except:
            pass


        try:
            if linex[0] == 'Charge':
                if linex[1] == '=':
                    parameters['Charge']= linex[2]
            
            if linex[3] == 'Multiplicity':
                if linex[4] == '=':
                    parameters['Multiplicity'] = linex[5]
        except:
            parameters['Charge']       = "-"
            parameters['Multiplicity'] = '-'
            pass


        try:
            if linex[0] == 'Number':
                if linex[1] == 'of':
                    if linex[2] == 'QC':
                        if linex[3] == 'Atoms':
                            parameters['Number of QC Atoms']= linex[5]
            
            if linex[6] == 'Boundary':
                if linex[7] == 'Atoms':
                    if linex[8] == '=':
                        parameters['Boundary Atoms'] = linex[9]
        except:
            pass


        try:
            if linex[0] == 'Nuclear':
                if linex[1] == 'Charge':
                    if linex[2] == '=':
                        parameters['Nuclear Charge']= linex[3]
            
            if linex[4] == 'Orbital':
                if linex[5] == 'Functions':
                    if linex[6] == '=':
                        parameters['Orbital Functions'] = linex[7]
        except:
            pass


        try:
            if linex[0] == 'Fitting':
                if linex[1] == 'Functions':
                    if linex[2] == '=':
                        parameters['Fitting Functions']= linex[3]
            
            if linex[4] == 'Energy':
                if linex[5] == 'Base':
                    if linex[6] == 'Line':
                        parameters['Energy Base Line'] = linex[8]
        except:
            pass


        try:
            if linex[0] == 'QC':
                if linex[1] == 'Parameter':
                    if linex[2] == 'Centers':
                        parameters['QC Parameter Centers']= linex[4]
        except:
            pass


        try:
            if linex[0] == 'Number':
                if linex[1] == 'of':
                    if linex[2] == 'Fixed':
                        if linex[3] == 'Atoms':
                            parameters['Number of Fixed Atoms']= linex[5]
        except:
            pass
        
    return parameters

        
             
             
def ParseProcessLogFile(log_file):
    """ Function doc """
    parameters = {
                  1: {
                     'type'  : 'line'    ,   # line / matrix
                     'title' : ''        ,   #
                     'X'     : []        ,   # X 
                     'Y'     : []        ,   # Y 
                     'xlabel': 'x label' ,   # xlabel,
                     'ylabel': 'y label' ,   # ylabel,
                     }
                 }
    
    
    log = open( log_file , "r")
    #print log
    lines = log.readlines()
    #print lines

    interact = []
    Function = []
    RMS_Grad = []
    Mac_Grad = []
    RMS_disp = []
    MAS_Disp = []

    if '       Chain-Of-States Optimizer Statistics\n' in lines:
        
        index = lines.index('       Chain-Of-States Optimizer Statistics\n')
        
        for line in lines[index:]:
            line2 =  line.split()
            if len(line2) == 9:
                parameters[1]['X'     ].append(line2[0])
                parameters[1]['Y'     ].append(line2[2])
            
         
        parameters[1]['type'  ] = 'line'
        parameters[1]['title' ] = 'Chain-Of-States'
        parameters[1]['xlabel'] = 'Frames'
        parameters[1]['ylabel'] = 'Energy (KJ)'
        #pprint(parameters)
        return parameters
        
        
    if '                              EasyHybrid SCAN2D\n' in lines:
        index = lines.index('                              EasyHybrid SCAN2D\n')
        #print lines[index]
        #print index
        i             =   0
        j             =   0        
        matrix_lines  = []
        r1 = ''
        r2 = ''
        for line in lines[index: -1]:
            if line == '----------------------- Coordinate 1 - Simple-Distance -------------------------\n':
                index2 = lines.index('----------------------- Coordinate 1 - Simple-Distance -------------------------\n')
                for atomLine in lines[index2+1 :index2+4]:
                    atom = atomLine.split()
                    if atom[0][0:4] == 'ATOM':
                        
                        if atom[0][-1] == '2':
                            r1 = r1 +atom[2] + '(' +atom[6] + ')'
                        else:
                            r1 = r1 +atom[2] + '(' +atom[6] + ')' + " - "
                        #print r1


            if line == '--------------------- Coordinate 1 - Multiple-Distance -------------------------\n':
                index2 = lines.index('--------------------- Coordinate 1 - Multiple-Distance -------------------------\n')
                for atomLine in lines[index2+1 :index2+4]:
                    atom = atomLine.split()
                    if atom[0][0:4] == 'ATOM':
                        if atom[0][-1] == '*':
                            r1 = r1 + " - " + atom[2] + '(' +atom[6] + ')*' + " - "
                        else:
                            r1 = r1 +atom[2] + '(' +atom[6] + ')'
                        #print r1

            
            
            
            
            
            if line == '----------------------- Coordinate 2 - Simple-Distance -------------------------\n':
                index2 = lines.index('----------------------- Coordinate 2 - Simple-Distance -------------------------\n')
                for atomLine in lines[index2+1 :index2+4]:
                    atom = atomLine.split()
                    if atom[0][0:4] == 'ATOM':
                        if atom[0][-1] == '2':
                            r2 = r2 +atom[2] + '(' +atom[6] + ')'
                        else:
                            r2 = r2 +atom[2] + '(' +atom[6] + ')' + " - "
                        #print r2
            
            if line == '--------------------- Coordinate 2 - Multiple-Distance -------------------------\n':
                index2 = lines.index('--------------------- Coordinate 2 - Multiple-Distance -------------------------\n')
                for atomLine in lines[index2+1 :index2+4]:
                    atom = atomLine.split()
                    if atom[0][0:4] == 'ATOM':
                        if atom[0][-1] == '*':
                            r2 = r2 + " - " + atom[2] + '(' +atom[6] + ')*' + " - "
                        else:
                            r2 = r2 +atom[2] + '(' +atom[6] + ')'
                        #print r2

            
            
            
            #print line
            try:
                linex = line.split()
                if linex[0] == "MATRIX2":
                    #print linex
                    i = len(linex) - 1
                    j = j + 1
                    mline = []
                    
                    for item in linex[1:-1]:
                        #print item
                        mline.append(float(item))
                    #print mline
                    
                    matrix_lines.append(mline)
                    
            except:
                pass	
        import numpy as np
        X = np.array(matrix_lines)

                
        parameters[1]['type'  ] = 'matrix'
        parameters[1]['title' ] = 'SCAN2D'
        parameters[1]['matrix'] =  X
        parameters[1]['xlabel'] = r1
        parameters[1]['ylabel'] = r2
        #print parameters
        return parameters



    if '------------------------ EasyHybrid SCAN Multiple-Distance ----------------------\n' in lines:
        index = lines.index('------------------------ EasyHybrid SCAN Multiple-Distance ----------------------\n')
        #print lines[index]
        #print index
        Frame      = []
        PK1_PK2    = []
        PK2_PK3    = []
        ReactionCoord = []
        Energy     = []

        
        for line in lines[index: -1]:
            linex = line.split()
            #print linex
            
            if len(linex) == 4:
                #print linex
                
                try:
                    Frame.append(float(linex[0]))
                    
                    ReactionCoord.append(float(linex[1])-float(linex[2]))
                
                    Energy.append(float(linex[-1]))
                except:
                    a = None
        parameters[1]['type'  ] = 'line'
        parameters[1]['title' ] = 'SCAN Multiple-Distance'
        parameters[1]['X'     ] = Frame
        parameters[1]['Y'     ] = Energy
        parameters[1]['xlabel'] = 'Frames'
        parameters[1]['ylabel'] = 'Energy (KJ)'
        
        #parameters[2] = {}
        #parameters[2]['type'  ] = 'line'
        #parameters[2]['title' ] = 'SCAN Multiple-Distance'
        #parameters[2]['X'     ] = ReactionCoord
        #parameters[2]['Y'     ] = Energy
        #parameters[2]['xlabel'] = 'Reaction Coordinate(r1 -r2)'
        #parameters[2]['ylabel'] = 'Energy (KJ)'
        
        #print parameters
        return parameters



    if '------------------------- EasyHybrid SCAN Simple-Distance -----------------------\n' in lines:
        index = lines.index('------------------------- EasyHybrid SCAN Simple-Distance -----------------------\n')
        #print lines[index]
        #print index
        Frame      = []
        PK1_PK2    = []
        PK2_PK3    = []
        Energy     = []
        ReactionCoord = []
        
        for line in lines[index: -1]:
            linex = line.split()
            #print linex
            
            if len(linex) == 3:
                #print linex
                
                try:
                    Frame        .append(float(linex[0] ))
                    ReactionCoord.append(float(linex[1] ))
                    Energy       .append(float(linex[-1]))
                except:
                    a = None
        
        parameters[1]['type'  ] = 'line'
        parameters[1]['title' ] = 'SCAN Multiple-Distance'
        parameters[1]['X'     ] = Frame
        parameters[1]['Y'     ] = Energy
        parameters[1]['xlabel'] = 'Frames'
        parameters[1]['ylabel'] = 'Energy (KJ)'
        
        #parameters[2] = {}
        #parameters[2]['type'  ] = 'line'
        #parameters[2]['title' ] = 'SCAN Multiple-Distance'
        #parameters[2]['X'     ] = ReactionCoord
        #parameters[2]['Y'     ] = Energy
        #parameters[2]['xlabel'] = 'Reaction Coordinate(r1)'
        #parameters[2]['ylabel'] = 'Energy (KJ)'
        
        
        #print parameters
        return parameters	






    '''   
    ------------------------------------------------------------
                       Potential of Mean Force
    ------------------------------------------------------------
        ReactionCoord            PMF                 PDF
    ------------------------------------------------------------
                 1.58169                   0              158.96
                 1.58798        2.49434e+300                   0
                 1.59428        2.49434e+300                   0
    '''
    if '    ReactionCoord            PMF                 PDF\n' in lines:
        index = lines.index('    ReactionCoord            PMF                 PDF\n')
        #print lines[index]
        print index
        
        
        ReactionCoord = []
        PDF           = []
        PMF           = []
        
        for line in lines[index: -1]:
            #print line 
            line2 = line.split()
            if len(line2) == 3:
                try:
                    ReactionCoord.append(float(line2[0]))
                    PDF.append(float(line2[2]))
                    PMF.append(float(line2[1]))
                except:
                    pass
        
        
        parameters[1]['type'  ] = 'line'
        parameters[1]['title' ] = 'Potential of mean force'
        parameters[1]['X'     ] = ReactionCoord
        parameters[1]['Y'     ] = PMF
        parameters[1]['xlabel'] = 'ReactionCoord'
        parameters[1]['ylabel'] = 'Energy (KJ)'

        #parameters[2] = {}
        #parameters[2]['type'  ] = 'line'
        #parameters[2]['title' ] = 'Potential of mean force'
        #parameters[2]['X'     ] = ReactionCoord
        #parameters[2]['Y'     ] = PDF
        #parameters[2]['xlabel'] = 'Reaction Coordinate'
        #parameters[2]['ylabel'] = ' - '
        

        return parameters







    '''
    ------------------------------------- L-BFGS Minimizer Options -------------------------------------
    History                          =             10  Log Frequency                    =              5
    Maximum Iterations               =            200  Maximum Step                     =           0.01
    RMS Gradient Tolerance           =            0.1
    ----------------------------------------------------------------------------------------------------

    ----------------------------------------------------------------------------------------------------------------
      Iteration       Function          RMS Gradient        Max. |Grad.|          RMS Disp.         Max. |Disp.|
    ----------------------------------------------------------------------------------------------------------------
         0     I      -2861.47060058          0.16863474          2.57918121          0.00000000          0.00000000
    ----------------------------------------------------------------------------------------------------------------
    '''


    if '------------------------------------- L-BFGS Minimizer Options -------------------------------------\n' in lines:
        index = lines.index('------------------------------------- L-BFGS Minimizer Options -------------------------------------\n')
        #print lines[index]
        #print index
        interact = []
        Function = []
        RMS_Grad = []
        Mac_Grad = []
        RMS_disp = []
        MAS_Disp = []
        for line in lines[index: -1]:
            line2 = line.split()
            lengh = len(line2)
            if lengh == 7:
                try:
                    n = 0
                    interact.append(float(line2[0]))
                    Function.append(float(line2[2]))
                    RMS_Grad.append(float(line2[3]))
                    Mac_Grad.append(float(line2[4]))
                    RMS_disp.append(float(line2[5]))
                    MAS_Disp.append(float(line2[6]))
                except:
                    pass
        
        parameters[1]['type'  ] = 'line'
        parameters[1]['title' ] = 'Energy minimization: L-BFGS'
        parameters[1]['X'     ] = interact
        parameters[1]['Y'     ] = Function
        parameters[1]['xlabel'] = 'Frames'
        parameters[1]['ylabel'] = 'Energy (KJ)'
        
        
        #pprint(parameters)
        return parameters






    '''
    -------------------------------  Conjugate Gradient Minimizer Options ------------------------------
    Beta Type                        =              1  Initial Step                     =            0.1
    Line Searcher                    =           None  Log Frequency                    =              5
    Maximum Iterations               =            200  Maximum Theta                    =          1e+10
    Minimum Theta                    =          1e-10  RMS Gradient Tolerance           =            0.1
    Steepest Descent Tolerance       =          0.001  Use Spectral Theta               =           True
    ----------------------------------------------------------------------------------------------------

    ----------------------------------------------------------------------------------------------------------------
      Iteration       Function          RMS Gradient        Max. |Grad.|          RMS Disp.         Max. |Disp.|
    ----------------------------------------------------------------------------------------------------------------
         0     I      -1142.98230437        118.93269476       2669.91104143          0.00227862          0.05115256
    '''

    if '-------------------------------  Conjugate Gradient Minimizer Options ------------------------------\n' in lines:
        index = lines.index('-------------------------------  Conjugate Gradient Minimizer Options ------------------------------\n')
        #print lines[index]
        print index
        interact = []
        Function = []
        RMS_Grad = []
        Mac_Grad = []
        RMS_disp = []
        MAS_Disp = []
        
        for line in lines[index: -1]:
            line2 = line.split()
            lengh = len(line2)
            if lengh == 7:
                try:
                    n = 0
                    interact.append(float(line2[0]))
                    Function.append(float(line2[2]))
                    RMS_Grad.append(float(line2[3]))
                    Mac_Grad.append(float(line2[4]))
                    RMS_disp.append(float(line2[5]))
                    MAS_Disp.append(float(line2[6]))
                except:
                    pass
        
        parameters[1]['type'  ] = 'line'
        parameters[1]['title' ] = 'Energy minimization: Conjugate-Gradient'
        parameters[1]['X'     ] = interact
        parameters[1]['Y'     ] = Function
        parameters[1]['xlabel'] = 'Frames'
        parameters[1]['ylabel'] = 'Energy (KJ)'
        #pprint(parameters)
        return parameters









    '''
    -------------------------------- Steepest-Descent Minimizer Options --------------------------------
    Log Frequency                    =              1  Maximum Iterations               =             10
    Maximum Step Size                =              1  Minimum Step Size                =          1e-06
    RMS Gradient Tolerance           =            0.1  Scale Down                       =            0.5
    Scale Up                         =            1.2  Step Size                        =           0.01
    ----------------------------------------------------------------------------------------------------

    ----------------------------------------------------------------------------------------------------------------
      Iteration       Function          RMS Gradient        Max. |Grad.|          RMS Disp.         Max. |Disp.|
    ----------------------------------------------------------------------------------------------------------------
         0     I      -2814.85409217          0.47710045         12.37630814          0.00000000          0.00000000
    '''
    if '-------------------------------- Steepest-Descent Minimizer Options --------------------------------\n' in lines:
        index = lines.index('-------------------------------- Steepest-Descent Minimizer Options --------------------------------\n')
        #print lines[index]
        #print index
        for line in lines[index: -1]:
            line2 = line.split()
            lengh = len(line2)
            if lengh == 6:
                try:
                    n = 0
                    interact.append(float(line2[0]))
                    Function.append(float(line2[1]))
                    RMS_Grad.append(float(line2[2]))
                    Mac_Grad.append(float(line2[3]))
                    RMS_disp.append(float(line2[4]))
                    MAS_Disp.append(float(line2[5]))

                except:
                    pass

            if lengh == 7:
                try:
                    n = 0
                    interact.append(float(line2[0]))
                    Function.append(float(line2[2]))
                    RMS_Grad.append(float(line2[3]))
                    Mac_Grad.append(float(line2[4]))
                    RMS_disp.append(float(line2[5]))
                    MAS_Disp.append(float(line2[6]))

                except:
                    pass

        parameters[1]['type'  ] = 'line'
        parameters[1]['title' ] = 'Energy minimization: Steepest-Descent'
        parameters[1]['X'     ] = interact
        parameters[1]['Y'     ] = Function
        parameters[1]['xlabel'] = 'Frames'
        parameters[1]['ylabel'] = 'Energy (KJ)'
        #pprint(parameters)
        return parameters





            
            
            
    '''
    ----------------------------------------------------------------------------------------------------
                                 Velocity Verlet Integrator Results
    ----------------------------------------------------------------------------------------------------
        Time            Total Energy       Kinetic Energy     Potential Energy       Temperature
    ----------------------------------------------------------------------------------------------------
          0.00000000       -423.80962900       2394.56813435      -2818.37776335        300.00000000
    '''
    if '                                 Velocity Verlet Integrator Results\n' in lines:
        index = lines.index('                                 Velocity Verlet Integrator Results\n')
        #print lines[index]
        #print index
        Time             = []
        Total_energy     = []
        Kinetic_Energy   = []
        Potential_Energy = []
        Temperature      = []
        
        for line in lines[index: -1]:
            linex = line.split()
            
            if len(linex) == 5:
                tipo = linex[0].split(".")
                lengh = len(tipo)
                if lengh == 2:
                    try:
                        Time.append(float(linex[0]))
                        Total_energy.append(float(linex[1]))
                        Kinetic_Energy.append(float(linex[2]))
                        Potential_Energy.append(float(linex[3]))
                        Temperature.append(float(linex[4]))
                    except:
                        pass


        parameters[1]['type'  ] = 'line'
        parameters[1]['title' ] = 'Velocity Verlet Integrator'
        parameters[1]['X'     ] = Time
        parameters[1]['Y'     ] = Total_energy
        parameters[1]['xlabel'] = 'Time'
        parameters[1]['ylabel'] = 'Total_energy'
        
        
        
        #pprint(parameters)
        return parameters





    '''
    --------------------------------------------------------------------------------------------------------------------------------------------
                                                         Leapfrog Verlet Integrator Results
    --------------------------------------------------------------------------------------------------------------------------------------------
            Time            Total Energy       Kinetic Energy     Potential Energy       Temperature          Pressure             Volume
    --------------------------------------------------------------------------------------------------------------------------------------------
              0.00000000       1920.46434760       2394.56813435       -474.10378674        300.00000000          0.00000000          0.00000000
    '''
    if '                                                     Leapfrog Verlet Integrator Results\n' in lines:
        index = lines.index('                                                     Leapfrog Verlet Integrator Results\n')
        #print lines[index]
        print index
        Time             = []
        Total_energy     = []
        Kinetic_Energy   = []
        Potential_Energy = []
        Temperature      = []
        Pressure         = []    
        Volume           = []
        for line in lines[index: -1]:
            linex = line.split()
            
            if len(linex) == 7:
                tipo = linex[0].split(".")
                lengh = len(tipo)
                if lengh == 2:
                    try:
                        Time.append(float(linex[0]))
                        Total_energy.append(float(linex[1]))
                        Kinetic_Energy.append(float(linex[2]))
                        Potential_Energy.append(float(linex[3]))
                        Temperature.append(float(linex[4]))
                        Pressure.append(float(linex[5]))
                        Volume  .append(float(linex[6]))
                        
                    except:
                        pass


        parameters[1]['type'  ] = 'line'
        parameters[1]['title' ] = 'Leapfrog Verlet Integrator'
        parameters[1]['X'     ] = Time
        parameters[1]['Y'     ] = Total_energy
        parameters[1]['xlabel'] = 'Time'
        parameters[1]['ylabel'] = 'Total_energy'
        pprint(parameters)
        return parameters








    '''
    ----------------------------------------------------------------------------------------------------
                                 Langevin Velocity Verlet Integrator Results
    ----------------------------------------------------------------------------------------------------
            Time            Total Energy       Kinetic Energy     Potential Energy       Temperature
    ----------------------------------------------------------------------------------------------------
              0.00000000       2019.32202144       2394.56813435       -375.24611290        300.00000000
    '''
    if '                             Langevin Velocity Verlet Integrator Results\n' in lines:
        index = lines.index('                             Langevin Velocity Verlet Integrator Results\n')
        #print lines[index]
        #print index
        Time             = []
        Total_energy     = []
        Kinetic_Energy   = []
        Potential_Energy = []
        Temperature      = []
        Pressure         = []    
        Volume           = []
        for line in lines[index: -1]:
            linex = line.split()
            
            if len(linex) == 5:
                tipo = linex[0].split(".")
                lengh = len(tipo)
                if lengh == 2:
                    try:
                        Time.append(float(linex[0]))
                        Total_energy.append(float(linex[1]))
                        Kinetic_Energy.append(float(linex[2]))
                        Potential_Energy.append(float(linex[3]))
                        Temperature.append(float(linex[4]))
                        #Pressure.append(float(linex[5]))
                        #Volume  .append(float(linex[6]))
                        
                    except:
                        pass


        parameters[1]['type'  ] = 'line'
        parameters[1]['title' ] = 'Langevin Velocity Verlet Integrator'
        parameters[1]['X'     ] = Time
        parameters[1]['Y'     ] = Total_energy
        parameters[1]['xlabel'] = 'Time'
        parameters[1]['ylabel'] = 'Total_energy'
        #pprint(parameters)
        return parameters

















def main():  
    for log_file in logList:
        parameters = ParseProcessLogFile (log_file)
    #pprint (parameters)
    return 0

if __name__ == '__main__':
	main()

