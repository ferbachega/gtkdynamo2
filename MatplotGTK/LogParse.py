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

#
#
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
                print line
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


def ParseProcessLogFile(log_file):                              #  PROCESS  LOG  READER
    matrix_lines  =   []
    log = open( log_file , "r")

    parameters = {
                 'type'  : 'line'    ,   # line / matrix
                 'title' : ''        ,   #
                 'X'     : []        ,   # X 
                 'Y'     : []        ,   # Y 
                 'xlabel': 'x label' ,   # xlabel,
                 'ylabel': 'y label' ,   # ylabel,
                 }
    
    for line in log:
        linex = line.split()
        try:                                # Check if the Log is Molecular Dynamics
            if linex[0] == "Time":
                if linex[1] == "Total":
                    Time = []
                    Total_energy = []
                    Kinetic_Energy = []
                    Potential_Energy = []
                    Temperature = []
                                
                    for line in log:
                        line2 = line.split()
                        lengh = len(line2)

                        if lengh == 5:
                            tipo = line2[0].split(".")
                            lengh = len(tipo)
                            if lengh == 2:

                                try:
                                    Time.append(float(line2[0]))
                                    Total_energy.append(float(line2[1]))
                                    Kinetic_Energy.append(float(line2[2]))
                                    Potential_Energy.append(float(line2[3]))
                                    Temperature.append(float(line2[4]))

                                except:
                                    pass
            #print_graf2(Time,Total_energy,Kinetic_Energy,Potential_Energy,Temperature)
        except:
            a = None
        try:                                # Check if the Log is Molecular Dynamics
            if linex[0] == "Time":
                if linex[1] == "Total":
                    Time = []
                    Total_energy = []
                    Kinetic_Energy = []
                    Potential_Energy = []
                    Temperature = []
                                
                    for line in log:
                        line2 = line.split()
                        lengh = len(line2)
                        
                        if lengh == 5:
                            tipo = line2[0].split(".")
                            lengh = len(tipo)
                            if lengh == 2:
                                
                                try:
                                    Time.append(float(line2[0]))
                                    Total_energy.append(float(line2[1]))
                                    Kinetic_Energy.append(float(line2[2]))
                                    Potential_Energy.append(float(line2[3]))
                                    Temperature.append(float(line2[4]))
                
                                except:
                                    pass
            #print_graf2(Time,Total_energy,Kinetic_Energy,Potential_Energy,Temperature)
        except:
            a = None

        try:                                # Check if the Log is SAW process
            if linex[1] == "Self-Avoiding":
                if linex[2] == "Walk":
                    print "SAW log file"   
                    Structure = []
                    Energy = []
                    for line in log:
                        #print line
                        line2 = line.split()
                        lengh = len(line2)
                        
                        if lengh == 4:
                            tipo = line2[0].split(".")
                            lengh = len(tipo)
                            if lengh == 1:
                                
                                try:
                                    n = 0
                                    Structure.append(float(line2[0]))
                                    Energy.append(float(line2[1]))
                                except:
                                    pass
                        if lengh == 2:
                            tipo = line2[0].split(".")
                            lengh = len(tipo)
                            if lengh == 1:
                                
                                try:
                                    n = 0
                                    Structure.append(float(line2[0]))
                                    Energy.append(float(line2[1]))
                                except:
                                    pass						
                            
                parameters['type'  ] = 'line'
                parameters['title' ] = 'Self-Avoiding Walk'
                parameters['X'     ] = Structure
                parameters['Y'     ] = Energy
                parameters['xlabel'] = 'Frames'
                parameters['ylabel'] = 'Energy (KJ)'
                return parameters
                
                #return Structure,Energy
        except:
            a = None

        try:                                #check if Conjugate-Gradient
            if linex[1] == "Conjugate-Gradient":   # Check if the Log is a log of a minimization process
                interact = []
                Function = []
                RMS_Grad = []
                Mac_Grad = []
                RMS_disp = []
                MAS_Disp = []

                for line in log:
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
                
                
                parameters['type'  ] = 'line'
                parameters['title' ] = 'Energy minimization: Conjugate-Gradient'
                parameters['X'     ] = interact
                parameters['Y'     ] = Function
                parameters['xlabel'] = 'Frames'
                parameters['ylabel'] = 'Energy (KJ)'
                return parameters
                #return interact, Function
        except:
            a = None
            


        try:                                #check if Conjugate-Gradient
            if linex[1] == "Conjugate":     # Check if the Log is a log of a minimization process
                interact = []
                Function = []
                RMS_Grad = []
                Mac_Grad = []
                RMS_disp = []
                MAS_Disp = []

                for line in log:
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
                
                parameters['type'  ] = 'line'
                parameters['title' ] = 'Energy minimization: Conjugate-Gradient'
                parameters['X'     ] = interact
                parameters['Y'     ] = Function
                parameters['xlabel'] = 'Frames'
                parameters['ylabel'] = 'Energy (KJ)'
                return parameters
                #return interact, Function
        except:
            a = None






        try:
            if linex[1] == "Steepest-Descent":   # Check if the Log is a minimization log
                interact = []
                Function = []
                RMS_Grad = []
                Mac_Grad = []
                RMS_disp = []
                MAS_Disp = []

                for line in log:
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

                parameters['type'  ] = 'line'
                parameters['title' ] = 'Energy minimization: Steepest-Descent'
                parameters['X'     ] = interact
                parameters['Y'     ] = Function
                parameters['xlabel'] = 'Frames'
                parameters['ylabel'] = 'Energy (KJ)'
                return parameters
                #return interact, Function
        except:
            a = None






        #n = 0 
        try:                                # Check if the Log is a NEB process
            if linex[0] == "Growing":
                if linex[1] == "String":  
                    Structure = []
                    Energy = []
                    Energy_absolut = []
                    EnergyKcal = []
                    for line in log:
                        print line
                        line2 = line.split()
                        lengh = len(line2)
                        n = 0
                        
                        if lengh == 5:
                            tipo = line2[0].split(".")
                            tipo2= line2[1].split(".")
                            tipo3= line2[2].split(".")
                            
                            
                            lengh = len(tipo)
                            lengh2 = len(tipo2)
                            lengh3 = len(tipo3)
                            if lengh == 1:
                                if 	lengh2 == 2:
                                    if lengh3 == 2: 
                                        try:
                                            n = 0
                                            Energy_absolut.append(float(line2[1]))											
                                            
                                            Structure.append(float(line2[0]))
                                            Energy.append(float(line2[1]) - Energy_absolut[0])
                                            
                                            EnergyKcal.append((float(line2[1]) - Energy_absolut[0])*0.23923445  )

                                        except:
                                            pass	
                            n = 1

                parameters['type'  ] = 'line'
                parameters['title' ] = 'NEB'
                parameters['X'     ] = Structure
                parameters['Y'     ] = Energy
                parameters['xlabel'] = 'Frames'
                parameters['ylabel'] = 'Energy (KJ)'
                return parameters
                #return Structure,Energy
        except:
            a = None







        try:                                # Check if the Log is a log of a minimization process
            if linex[0] == "-------------------------------------":
                if linex[1] == "L-BFGS":   # Check if the Log is a log of a minimization process
                    interact = []
                    Function = []
                    RMS_Grad = []
                    Mac_Grad = []
                    RMS_disp = []
                    MAS_Disp = []

                    for line in log:
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
                    
                    parameters['type'  ] = 'line'
                    parameters['title' ] = 'Energy minimization: L-BFGS'
                    parameters['X'     ] = interact
                    parameters['Y'     ] = Function
                    parameters['xlabel'] = 'Frames'
                    parameters['ylabel'] = 'Energy (KJ)'
                    return parameters
                    #return interact, Function
        except:
            a = None		







        try:                                # Check if the Log is a Self-Diffusion Function process
            if linex[0] == "Self-Diffusion":
                if linex[1] == "Function":  
                    Structure = []
                    Energy = []
                    for line in log:
                        #print line
                        line2 = line.split()
                        lengh = len(line2)
                        if lengh == 2:
                            tipo = line2[0].split(".")
                            lengh = len(tipo)
                            if lengh == 1:
                                try:
                                    n = 0
                                    Structure.append(float(line2[0]))
                                    Energy.append(float(line2[1]))
                                except:
                                    pass
                parameters['type'  ] = 'line'
                parameters['title' ] = 'Self-Diffusion'
                parameters['X'     ] = Structure
                parameters['Y'     ] = Energy
                parameters['xlabel'] = 'Frames'
                parameters['ylabel'] = 'Energy (KJ)'
                return parameters
                #return Structure, Energy
        except:
            a = None

        '''
        try:                                      # Check if the Log is a UMBRELLA SAMPLING process
            if linex[0] == "Potential":
                if linex[1] == "of":
                    if linex[2] == "Mean": 
                        #print linex[0],linex[1],  linex[2]
                        #ReactionCoord = []
                        #PDF           = []
                        #PMF           = []
                        for line in log:
                            if len(line) == 60:
                                print line
                            
                            #line2 = line.split()
                            #lengh = len(line2)
                            #if lengh == 3:
                            #	tipo = line2[0].split(".")
                            #	lengh = len(tipo)
                            #	if lengh == 2:
                            #		try:
                            #			n = 0
                            #			ReactionCoord.append(float(line2[0]))
                            #			PDF.append(float(line2[1]))
                            #			PMF.append(float(line2[2]))
                            #		except:
                            #			print " "
                    #return ReactionCoord, PMF
        except:
            pass
        '''
        try:                                # Check if the Log is a UMBRELLA SAMPLING process  old function
            if linex[0] == "Potential":
                if linex[1] == "of":
                    if linex[2] == "Mean": 
                        print linex[0],linex[1],  linex[2]
                        ReactionCoord = []
                        PDF           = []
                        PMF           = []
                        for line in log:
                            line2 = line.split()
                            lengh = len(line2)
                            if lengh == 3:
                                tipo = line2[0].split(".")
                                lengh = len(tipo)
                                if lengh == 2:
                                    try:
                                        n = 0
                                        ReactionCoord.append(float(line2[0]))
                                        PDF.append(float(line2[1]))
                                        PMF.append(float(line2[2]))
                                    except:
                                        pass
                    
                    
                    parameters['type'  ] = 'line'
                    parameters['title' ] = 'Potential of mean force'
                    parameters['X'     ] = ReactionCoord
                    parameters['Y'     ] = PMF
                    parameters['xlabel'] = 'ReactionCoord'
                    parameters['ylabel'] = 'Energy (KJ)'
                    return parameters
                    #return ReactionCoord, PMF
        except:
            a = None




        #------------------------ GTKDynamo SCAN Multiple-Distance ----------------------
        #      [0]                  [1]      [2]        [3]                 [4]
        try:                                      # Check if the Log is a SCAN process of the GTKDYN
            if linex[1] == "GTKDynamo":
                if linex[2] == "SCAN":
                    if linex[3] == 'Multiple-Distance':
                        print linex[2],linex[3]
                        Frame      = []
                        PK1_PK2    = []
                        PK2_PK3    = []
                        Energy     = []
                        
                        for line in log:
                            line2 = line.split()
                            lengh = len(line2)
                            
                            if lengh == 4:
                                print line
                                try:
                                    Frame.append(float(line2[0]))
                                    Energy.append(float(line2[-1]))
                                except:
                                    a = None
                    
                    parameters['type'  ] = 'line'
                    parameters['title' ] = 'SCAN - Multiple-Distance'
                    parameters['X'     ] = Frame
                    parameters['Y'     ] = Energy
                    parameters['xlabel'] = 'Frames'
                    parameters['ylabel'] = 'Energy (KJ)'
                    return parameters
                    #return Frame, Energy
        except:
            a = None



        #------------------------ GTKDynamo SCAN  Simple-Distance -----------------------
        #      [0]                  [1]      [2]        [3]                 [4]
        try:                                      # Check if the Log is a SCAN process of the GTKDYN
            if linex[1] == "GTKDynamo":
                if linex[2] == "SCAN":
                    if linex[3] == 'Simple-Distance':
                        print linex[2],linex[3]
                        Frame      = []
                        PK1_PK2    = []
                        Energy     = []

                        for line in log:
                            line2 = line.split()
                            lengh = len(line2)
                            
                            if lengh == 3:
                                print line
                                try:
                                    Frame.append(float(line2[0]))
                                    Energy.append(float(line2[-1]))
                                except:
                                    a = None
                    
                    parameters['type'  ] = 'line'
                    parameters['title' ] = 'SCAN - Simple-Distance'
                    parameters['X'     ] = Frame
                    parameters['Y'     ] = Energy
                    parameters['xlabel'] = 'Frames'
                    parameters['ylabel'] = 'Energy (KJ)'
                    return parameters
                    #return Frame, Energy
        except:
            a = None		

                

        '''
        --------------------------------------------------------------------------------
        --                                                                            --
        --                          GTKDynamo SCAN  2D                                --
        [0]                            [1]    [2]  [3]                              [4]
        --                                                                            --
        --------------------------------------------------------------------------------

        ----------------------- Coordinate 1 - Simple-Distance -------------------------
        ATOM1                  =              1  ATOM NAME1             =             Br
        ATOM2                  =              2  ATOM NAME2             =              C
        NWINDOWS               =             20  FORCE CONSTANT         =     4000.00000
        DMINIMUM               =        1.94753  DINCREMENT             =        0.05000
        --------------------------------------------------------------------------------
        ----------------------- Coordinate 2 - Simple-Distance -------------------------
        ATOM1                  =              2  ATOM NAME1             =              C
        ATOM2                  =              0  ATOM NAME2             =             Cl
        NWINDOWS               =             25  FORCE CONSTANT         =     4000.00000
        DMINIMUM               =        2.86655  DINCREMENT             =       -0.05000
        --------------------------------------------------------------------------------

        MATRIX2         0.00000000          0.28827311          1.02210627          2.36403063  
        MATRIX2         0.09029504          0.36777736          1.07893998          2.37828860  
        MATRIX2         0.78146785          1.00737346          1.64857823          2.86669789  

        try:                                      # Check se o Log eh processo SCAN 2D do GTKDYN
            print line
            if line == "--                          GTKDynamo SCAN  2D                                --":
                return "matrix", "2d scan"
        except:
            a = None
        '''
        try:                                      # Check if the Log is a SCAN2D process of the GTKDYN
            i             =   0
            j             =   0
            
            #matrix_lines  =   []
             
            if linex[0] == "MATRIX2":
                #print linex
                i = len(linex) - 1
                j = j + 1
                
                
                for line in log:
                    lineX = line.split()
                    mline = []
                    if lineX[0] == "MATRIX2":
                        for a in lineX:
                            if a == "MATRIX2":
                                a = None
                            else:
                                mline.append(float(a))
                                
                        #print mline
                    matrix_lines.append(mline)
                
                #print matrix_lines
                
                
                
                import numpy as np
                X = np.array(matrix_lines)
                #print X
                parameters['type'  ] = 'matrix'
                parameters['title' ] = 'SCAN2D'
                parameters['matrix'] =  X
                parameters['xlabel'] = 'r1'
                parameters['ylabel'] = 'r2'
                return parameters
                
                
                #return "matrix", X
        except:
            a = None
        #print matrix_lines
        #print X


from pprint import pprint
def main():
    log_file ='/home/fernando/programs/pDynamo-1.9.0/scratch/.GTKDynamo/2_step_GeometryOptmization/2_step_GeometryOptmization.log'
    parameters = ParseProcessLogFile (log_file)
    pprint (parameters)
    return 0

if __name__ == '__main__':
	main()

