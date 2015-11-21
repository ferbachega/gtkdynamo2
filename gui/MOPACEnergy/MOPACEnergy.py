#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  mydialog.py
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
#
import os
import gtk
import time
import gobject
from WindowControl import *

# pDynamo
from pBabel           import *
from pCore            import *
from pMolecule        import *
from pMoleculeScripts import *

import subprocess 
from pprint import pprint
from DualTextLogFileWriter3 import *
from MatplotGTK.LogParse    import *



class pDynamoToMOPAC:
    """ Class doc """
    def __init__ (self, system, QMMM = False):
        """ Class initialiser """
    
        self.system    = system
        self.QMMM      = QMMM
        self.MopacKeys = ''

    def DefineMopacKeys (self,
                         methods      = 'PM6',
                         charge       = '0'  ,
                         multiplicity = 'Singlet'  ,
                         AUX          = True ,
                         single_point = True ,
                         MOZYME       = False , 
                         BONDS        = False,
                         PDBOUT       = False,
                         QMMM         = False,
                         SOLV         = False,
                         ESP          = None ,
                         RSOLV        = None):
        
        """ Function doc """
        text = ''
        text += methods + ' '
        text += 'CHARGE='+charge + ' '
        text += multiplicity + ' '
        
        if AUX:
            text += 'AUX' + ' '
        if single_point:
            text += '1SCF' + ' '
        if MOZYME:
            text += 'MOZYME' + ' '
            text += 'GEO-OK' + ' '
        if BONDS:
            text += 'BONDS' + ' '
        if PDBOUT:
            text += 'PDBOUT' + ' '
        if SOLV:
            text += 'EPS='+ESP +' RSOLV='+RSOLV+' '
        if QMMM:
            text += 'GRAD QMMM'+ ' '
            self.QMMM = True
        self.MopacKeys = text
        return text
        
        
    def generate_atoms_dic (self):
        """ Function doc """
        #qc_table      = list(self.system.energyModel.qcAtoms.QCAtomSelection())
        #boundaryAtoms = list(self.system.energyModel.qcAtoms.BoundaryAtomSelection())
        #print  'boundaryAtoms', boundaryAtoms
        charges   = self.system.energyModel.mmAtoms.AtomicCharges()
        atoms_dic = {
                    # index : [symbol,x,y,z,chg]
        
                    }
     
        for i in self.system.atoms.items:
            symbol = PeriodicTable.Symbol(i.atomicNumber)
            index  = i.index
            x      = self.system.coordinates3[i.index, 0]
            y      = self.system.coordinates3[i.index, 1]
            z      = self.system.coordinates3[i.index, 2]
            atoms_dic[index] = [symbol,x,y,z,charges[index]]
        
        return atoms_dic

    def generate_molin_file (self, qc_table = False):
        """ Function doc """
        
        #--------------------------------------------------------------------------------#
        if qc_table == False:                                                            #
            qc_table      = list(self.system.energyModel.qcAtoms.QCAtomSelection())      #
            boundaryAtoms = list(self.system.energyModel.qcAtoms.BoundaryAtomSelection())#
        #--------------------------------------------------------------------------------#

        #---------------- Q M M M --------------------------#
        atoms_dic = self.generate_atoms_dic()               #
        #---------------------------------------------------#
        
        #phi = 0
        #print len (atoms_dic)
        #print len (qc_table)
        #print qc_table
        #print atoms_dic[1187]
        
        text  = ''
        text += '\n'+str(len(qc_table))+'    0     # of qmmm atoms, # of link atoms in Region I'
        
        
        
        for i in qc_table:
            phi = 0
            #print atoms_dic[i]
            for j in atoms_dic:
                #print j
                #print  atoms_dic[j]
                #if i in atoms_dic:
                if i == j:
                    #print atoms_dic[j]
                    pass
                else:
                    chrg = atoms_dic[j][4]
                    dist = self.system.coordinates3.Distance(i, j)
                    chrg_over_dist = chrg / dist
                    
                    phi += chrg_over_dist
                    #print chrg, dist, chrg_over_dist 
                    
            #print atoms_dic[i][0], atoms_dic[i][1] , atoms_dic[i][2], atoms_dic[i][3], phi, phi*332
            text += '\n{:2s} {:<15s} {:<15s} {:<15s} {:<15s}'.format (str(atoms_dic[i][0]), 
                                                                      str(atoms_dic[i][1]), 
                                                                      str(atoms_dic[i][2]), 
                                                                      str(atoms_dic[i][3]), 
                                                                      str(phi))
        #print text
        arq = open('mol.in', 'w') 
        arq.writelines(text)
        arq.close()

    def generate_MOPAC_file(self,
                             mopacKeys   = ''           ,
                             fileout     = 'system.mop' ):
        """ Function doc """
        
        #----------------------------------#
        #             Q M M M              #
        #----------------------------------#
        if self.QMMM == True:# False
            self.generate_molin_file(self.system)
        else:
            pass
        #----------------------------------#
        
        
        
        
        text = ''
        text += '* ===============================\n'       
        text += '* Input file for Mopac\n'
        text += '* ===============================\n'
        #text += 'PM6 1SCF    CHARGE=0 Singlet  BONDS AUX \n'
        text += self.MopacKeys
        text += '\n\n'
        
        text += 'Mopac file generated by EasyHybrid'
        
        qc_table      = list(self.system.energyModel.qcAtoms.QCAtomSelection())
        boundaryAtoms = list(self.system.energyModel.qcAtoms.BoundaryAtomSelection())
        #print  'boundaryAtoms', boundaryAtoms
        
        for i in self.system.atoms.items:
            if i.index in qc_table:
                symbol = PeriodicTable.Symbol (i.atomicNumber)
                index  = i.index
                x      = self.system.coordinates3[i.index, 0]
                y      = self.system.coordinates3[i.index, 1]
                z      = self.system.coordinates3[i.index, 2]
                if i.index in boundaryAtoms:
                    text += '\n{:2s} {:<15s} 1 {:<15s} 1 {:<15s} 1'.format('H',
                                                                           str(self.system.coordinates3[i.index, 0]), 
                                                                           str(self.system.coordinates3[i.index, 1]),  
                                                                           str(self.system.coordinates3[i.index, 2]))
                    #print   '\n{:2s} {:<15s}  1 {:<15s} 1 {:<15s} 1'.format('H',str(self.system.coordinates3[i.index, 0]), str(self.system.coordinates3[i.index, 1]),  str(self.system.coordinates3[i.index, 2]))
                else:
                    text += '\n{:2s} {:<15s} 1 {:<15s} 1 {:<15s} 1'.format(symbol,
                                                                           str(self.system.coordinates3[i.index, 0]), 
                                                                           str(self.system.coordinates3[i.index, 1]),  
                                                                           str(self.system.coordinates3[i.index, 2]))
                    #print   '\n{:2s} {:<15s} 1 {:<15s} 1 {:<15s} 1'.format(symbol,str(self.system.coordinates3[i.index, 0]), str(self.system.coordinates3[i.index, 1]),  str(self.system.coordinates3[i.index, 2]))
        
        arq = open(fileout, 'w') 
        arq.writelines(text)
        arq.close()
        return fileout

    def Energy (self, fileout = 'system.mop'):
        """ Function doc """
        #print fileout
        mopfile = self.generate_MOPAC_file(fileout= fileout)
        
        command   = '/opt/mopac/MOPAC2012.exe '+ mopfile 
        
        null_file = open(os.devnull, 'w' )
        
        subprocess.call(command.split(), stdout = null_file, stderr = null_file )
        
        energy    = self.ParseLogFile(mopfile[:-3]+'arc')
        
        return  energy
                
    def ParseLogFile(self, mopfile):
        """ Function doc """
        log = open(mopfile, 'r' )
        log2= log.readlines()
        
        for line in log2:
            #print line 
            line2 = line.split()
            if 'HEAT' in line2:
                #print 'HEAT OF FORMATION:' , line2[4]
                energy = line2[4]
        if energy:
            return energy
        else:
            return False




                
class MOPACSEnergyDialog():

    def runMOPACEnergy (self, button):
        """ Function doc """
        
        parameters = {}
        parameters['methods']           = None           
        parameters['trajectory']        = None           
        parameters['charge'      ]      = 0            #charge       = charge      ,  
        parameters['multiplicity']      = 1            #multiplicity = multiplicity,  
        parameters['mopac_AUX'   ]      = True         #AUX          = True        ,  
        parameters['mopac_1SCF'  ]      = True         #single_point = True        ,  
        parameters['mopac_MOZYME']      = True         #MOZYME       = MOZYME      ,  
        parameters['mopac_BONDS' ]      = False        #BONDS        = False       ,  
        parameters['mopac_PDBOUT']      = False        #PDBOUT       = False       ,  
        parameters['mopac_SOLV'  ]      = False        #SOLV         = SOLV        ,  
        parameters['mopac_ESP'   ]      = None         #ESP          = ESP         ,  
        parameters['mopac_RSOLV' ]      = None         #RSOLV        = RSOLV       ,  
        parameters['mopac_QMMM'  ]      = False         #QMMM         = QMMM        )
        parameters['tmpfile_outpath']   = None
        parameters['logfile_outpath']   = None
        parameters['log_file_name']     = None
        parameters['trajectory_type']   = "SCAN"
        
        
        #---------------------------------------------------------------------------------------------------------------#
        #                                              Time and log file                                                #
        #---------------------------------------------------------------------------------------------------------------#
        localtime = time.asctime(time.localtime(time.time()))                                                           #
        localtime = localtime.split()                                                                                   #
        #  0     1    2       3         4                                                                               #
        #[Sun] [Sep] [28] [02:32:04] [2014]                                                                             #
        log_file_name = 'MOPAC_Energy_' + localtime[1] +'_' + localtime[2] + '_'+localtime[3]+'_' + localtime[4]+'.log' #
        parameters['log_file_name'] = log_file_name                                                                     #
        #---------------------------------------------------------------------------------------------------------------#
        
        
        #-----------------------------------------------------------------------------------------------#
        #                                      folder and datapath                                      #
        #-----------------------------------------------------------------------------------------------#
        data_path     = self.EasyHybridSession.project.settings['data_path']                            #
                                                                                                        #
        #traj          = self.builder.get_object('umbrella_entry_TRAJECTORY').get_text()                #
        if not os.path.exists (os.path.join(data_path, 'MOPAC_files')):                                 #
            os.mkdir (os.path.join(data_path,'MOPAC_files'))                                            #
        logfile_outpath = os.path.join(data_path, 'MOPAC_files')                                        #
                                                                                                        #
                                                                                                        #
        if not os.path.exists (os.path.join(logfile_outpath, 'tmp')):                                   #
            os.mkdir (os.path.join(logfile_outpath,'tmp'))                                              #
        tmpfile_outpath = os.path.join(logfile_outpath, 'tmp')                                          #
        parameters['tmpfile_outpath'] = tmpfile_outpath                                                 #
        parameters['logfile_outpath'] = logfile_outpath                                                 #
        #-----------------------------------------------------------------------------------------------#       
        
        
        #-----------------------------------------------------------------------------------------------#
        #                                      LOG file - optional                                      #
        #-----------------------------------------------------------------------------------------------#
        scanLogFile  = self.builder.get_object('filechooserbutton3').get_filename()                     #
                                                                                                        #
        if scanLogFile == None:                                                                         #
            #parameters   = False                                                                       #
            #summary      = False                                                                       #
            parameters['original_system_summary'] =  False                                              #
            parameters['original_scan_log']       =  False                                              #
        else:                                                                                           #
            parameters['original_scan_log']       = ParseProcessLogFile(scanLogFile)                    #
            parameters['original_system_summary'] = ParseSummaryLogFile(scanLogFile)                    #
        #-----------------------------------------------------------------------------------------------#
    
        
        
        #-----------------------------------------------------------------------------------------------#
        charge          = self.builder.get_object('spinbutton_charge').get_value_as_int()               #
        charge          = str(charge)                                                                   #
        multiplicity    = self.builder.get_object('spinbutton_multiplicity').get_value_as_int()         #
        multiplicity    = 'Singlet'                                                                     #
                                                                                                        #
        parameters['charge'      ]    = charge                                                          #
        parameters['multiplicity']    = multiplicity                                                    #
        #-----------------------------------------------------------------------------------------------#
        
        
        
        
        
        if self.builder.get_object('checkbutton1').get_active() == True:                                
            SOLV    =  True                                                                             
            ESP     =  self.builder.get_object('entry2').get_text()                                     
            RSOLV   =  self.builder.get_object('entry3').get_text()                                     
            parameters['mopac_SOLV'  ]    = True
            parameters['mopac_ESP'   ]    = ESP
            parameters['mopac_RSOLV' ]    = RSOLV
            
        
        else:                                                                                           
            parameters['mopac_SOLV'  ]    = False                                                       
            parameters['mopac_ESP'   ]    = None                                                        
            parameters['mopac_RSOLV' ]    = None                                                        
                                                                                                        
        if self.builder.get_object('checkbutton2').get_active() == True:
            MOZYME                     =  True   
            parameters['mopac_MOZYME'] = MOZYME
        
        else:                                                                                           
            MOZYME    = False                                                                           
            parameters['mopac_MOZYME'] = MOZYME

        
        
        if self.builder.get_object('checkbutton3').get_active() == True:                                
            QMMM    =  True
            parameters['mopac_QMMM'  ]    =   QMMM                                                                         
        else:                                                                                           
            QMMM    = False 
            parameters['mopac_QMMM'  ]    =   QMMM                                                                         
        #-----------------------------------------------------------------------------------------------
        
        
        
        trajectory_type = self.builder.get_object('combobox2').get_active_text()
        # SCAN
        # SCAN-2D
        parameters['trajectory_type'] = trajectory_type
        
        
        
        #---------------------------------------------------------------------------#
        system = self.project.system                                                #
        parameters['system']  = system                                              #
        trajectory = self.builder.get_object('filechooserbutton1').get_filename()   #
        parameters['trajectory']  = trajectory                                      #
                                                                                    #
        methods = self.builder.get_object('entry1').get_text()                      #
        methods = methods.split()                                                   #
        parameters['methods'] = methods                                             #
        system.Summary()                                                            #
        #---------------------------------------------------------------------------#
        
        print charge, multiplicity, methods#, trajectory        
        
        
        
        if trajectory_type == 'SCAN':
            self.run_MOPAC_SCAN_refine  (parameters = parameters)
        
        if trajectory_type == 'SCAN-2D':
            self.run_MOPAC_SCAN2D_refine(parameters = parameters)
            
            


    def run_MOPAC_SCAN_refine(self, parameters = None):
        """ Function doc """
        '''
        parameters['methods']
        parameters['trajectory']
        parameters['charge'      ]
        parameters['multiplicity']
        parameters['mopac_AUX'   ]
        parameters['mopac_1SCF'  ]
        parameters['mopac_MOZYME']
        parameters['mopac_BONDS' ]
        parameters['mopac_PDBOUT']
        parameters['mopac_SOLV'  ]
        parameters['mopac_ESP'   ]
        parameters['mopac_RSOLV' ]
        parameters['mopac_QMMM'  ]
        parameters['tmpfile_outpath']
        parameters['logfile_outpath']
        parameters['log_file_name']
        '''
        logs = {
                }
        for method in parameters['methods']:
            
            logs[method] = {
                            'energy'     : [],
                            'energyNorm' : [],
                            }                                                          
            
            trajectory    = SystemGeometryTrajectory (parameters['trajectory'], parameters['system'], mode = "r" )                          
            n = 0                                                                                                
            
            while trajectory.RestoreOwnerData ( ):                                                               
                MOPAC_system = pDynamoToMOPAC(system = parameters['system'])                                                   
                                                                                                                 
                keywords = MOPAC_system.DefineMopacKeys (methods      = method                    ,                            
                                                         charge       = parameters['charge'      ],                            
                                                         multiplicity = parameters['multiplicity'],                            
                                                         AUX          = parameters['mopac_AUX'   ],                            
                                                         single_point = parameters['mopac_1SCF'  ],                            
                                                         MOZYME       = parameters['mopac_MOZYME'],                             
                                                         BONDS        = parameters['mopac_BONDS' ],    # False                          
                                                         PDBOUT       = parameters['mopac_PDBOUT'],   # False                          
                                                         SOLV         = parameters['mopac_SOLV'  ],                            
                                                         ESP          = parameters['mopac_ESP'   ],                            
                                                         RSOLV        = parameters['mopac_RSOLV' ],                            
                                                         QMMM         = parameters['mopac_QMMM'  ])                            
                                                                                                                 
                energy = MOPAC_system.Energy(fileout =  os.path.join(parameters['tmpfile_outpath'], 
                                                                     'system'+str(n)+'.mop'))   
                
                logs[method]['energy'].append(float(energy))                                                     
                logs[method]['energyNorm'].append(float(energy) - logs[method]['energy'][0])                                                                                                            
                n  += 1                                                                                          
                                                                                                                 
            #-------------------------------------------------------#                                            
            #                   LOG FILE SUMMARY                    #                                            
            #-------------------------------------------------------#                                            
            trajetoryFile = parameters['trajectory']
            string = ''                                                                                          
            string += 'trajectoy:    ' + trajetoryFile + '\n'                                                    
            string += 'keywords:     ' + keywords      + '\n'                                                    
            string += '\n'                                                                                       
                                                                                                                 
            for method in logs:                                                                                  
                string += " %15s "     % (method)                                                                
            string += '\n'                                                                                       
                                                                                                                 
            for i in range( 0, n): #len(logs['AM1']['energyNorm'])):                                             
                for method in logs:                                                                              
                    string += " %15.5f "  % (logs[method]['energyNorm'][i])                                      
                                                                                                                 
                string += '\n'                                                                                   
                                                                                                                 
            print string                                                                                         
            arq = open(os.path.join(parameters['logfile_outpath'], parameters['log_file_name']), 'w')                                        
            arq.writelines(string)                                                                               
            arq.close()                                                                                          



    def run_MOPAC_SCAN2D_refine(self, parameters):
        """ Function doc """
        #--------------------------------------------------------------#
        pass                                                           #
        trajectory_files   = os.listdir(parameters['trajectory'])      #
        trajectory_files2  = []                                        #
        #--------------------------------------------------------------#
        for File in trajectory_files:                                  #
            File2 = File.split('.')                                    #
                                                                       #
            if File2[-1] == 'pkl':                                     #
                trajectory_files2.append(File)                         #
        #--------------------------------------------------------------#
                
        for method in parameters['methods']:
            i_table      = []
            j_table      = []
            n = 1
            energy_table = {(0,0): 0.0}
            
            print method
            #--------------------------------------------------------------------------------------------------------------------------------#
            for File in trajectory_files2:                                                                                                   #
                File2 = File.split('.')                                                                                                      #
                File2 = File2[0].split('_')                                                                                                  #
                i = int(File2[1])                                                                                                            #
                j = int(File2[2])                                                                                                            #
                                                                                                                                             #
                system  = parameters['system']                                                                                               #
                system.coordinates3 = Unpickle(os.path.join(parameters['trajectory'],File))                                                  #
                MOPAC_system = pDynamoToMOPAC(system = system)                                                                               #
                                                                                                                                             #
                keywords = MOPAC_system.DefineMopacKeys (methods      = method                    ,                                          #
                                                         charge       = parameters['charge'      ],                                          #
                                                         multiplicity = parameters['multiplicity'],                                          #
                                                         AUX          = parameters['mopac_AUX'   ],                                          #
                                                         single_point = parameters['mopac_1SCF'  ],                                          #
                                                         MOZYME       = parameters['mopac_MOZYME'],                                          #
                                                         BONDS        = parameters['mopac_BONDS' ],   # False                                #
                                                         PDBOUT       = parameters['mopac_PDBOUT'],   # False                                #
                                                         SOLV         = parameters['mopac_SOLV'  ],                                          #
                                                         ESP          = parameters['mopac_ESP'   ],                                          #
                                                         RSOLV        = parameters['mopac_RSOLV' ],                                          #
                                                         QMMM         = parameters['mopac_QMMM'  ])                                          #
                                                                                                                                             #
                                                                                                                                             #
                energy = MOPAC_system.Energy(fileout =  os.path.join(parameters['tmpfile_outpath'], 'system_'+method+'_'+str(i)+'_'+str(j)+'.mop'))     #                
                energy_table[(i,j)] = float(energy)                                                                                          #
                i_table.append(i)                                                                                                            #
                j_table.append(j)                                                                                                            #
                print n, i, j, energy                                                                                                        #
                n = n+1                                                                                                                      #
            #--------------------------------------------------------------------------------------------------------------------------------#
            
            
            #---------------------------------------------------------#
            import numpy as np                                        #
            i_table  = np.array(i_table)
            j_table  = np.array(j_table)
            
            i_max = i_table.max()
            j_max = j_table.max()
            
            X = 0*np.random.rand (i_max+1, j_max+1)   
            #---------------------------------------------------------#
            
            
            #print X
            text    = ''
            
            for i in range(0,i_max+1):
                text    = text    + "\nMATRIX1 "
                for j in range(0,j_max+1):
                    X[i][j] = energy_table[(i,j)]
                    #text = text + "%18.8f  " % (X[i][j])
                    
            X_norm = X - np.min(X)
            
            parameters['energy_matrix'     ] = X
            parameters['energy_matrix_norm'] = X_norm
            parameters['actual_method'     ] = method
            
            parameters['matrix_i'     ] = i_max
            parameters['matrix_j'     ] = j_max
        
            
            self.build_SCAN2D_log(parameters)
       
    
    def build_SCAN2D_log (self, parameters ):

        """ Function doc """
        header  = '----------------------------- EasyHybrid - MOPAC Energy Refine ---------------------------------'
        header += "\nMETHOD                 =%20s  "     % (parameters['actual_method'] ) 
        header += "\nTOTAL CHARGE           =%20s  "     % (str(parameters['charge']) ) 
        header += "\nMULTIPLICITYE          =%20s  "     % (str(parameters['multiplicity']) ) 
        
        
        if parameters['mopac_MOZYME']:
            header += "\nMOZYME                 =%20s  "     % ("True")
        else:
            header += "\nMOZYME                 =%20s  "     % ("False")
            
        if  parameters['mopac_SOLV'  ]:
            header += "\nSOLV                   =%20s  "     % ('True')        #
            header += "\nmopac_ESP              =%20s  "     % (str(parameters['mopac_ESP'  ]))
            header += "\nmopac_RSOLV            =%20s  "     % (str(parameters['mopac_RSOLV']))            
        else:
            header += "\nSOLV                   =%20s  "     % ('False')        #
        
        header += "\n------------------------------------------------------------------------------------------------"          
        header += "\nRCOORD1 size           =%20s  "     % (str(parameters['matrix_i']))
        header += "\nRCOORD2 size           =%20s  "     % (str(parameters['matrix_j']))        
        
        if parameters['original_scan_log']:
            header += "\nRCOORD1                =%20s  "     % (parameters['original_scan_log'][1]['xlabel'])
            header += "\nRCOORD2                =%20s  "     % (parameters['original_scan_log'][1]['ylabel'])
        
        header += "\nTRAJECTORY             =%20s  "     % (parameters['trajectory'])        
        #header += "\nORIGINAL LOG           =%20s  "     % ("True")
        header += "\n------------------------------------------------------------------------------------------------"          
        
        
        text_matrix1 = '\n\n'
        for i in range(0,parameters['matrix_i']+1):
            text_matrix1  += "\nMATRIX1 "
            for j in range(0,parameters['matrix_j']+1):
                text_matrix1 += "%18.8f  " % (parameters['energy_matrix'][i][j])
        
        text_matrix1 += '\n\n'
        for i in range(0,parameters['matrix_i']+1):
            text_matrix1  += "\nMATRIX2 "
            for j in range(0,parameters['matrix_j']+1):
                text_matrix1 += "%18.8f  " % (parameters['energy_matrix_norm'][i][j])
        
        #print parameters['original_scan_log']
        #print parameters['original_scan_log'][1]
        #print parameters['original_scan_log'][1]['R1'    ]
        
        if parameters['original_scan_log']:
            print parameters['original_scan_log'][1]['R1'    ]
            #parameters['original_scan_log']
            
            if parameters['original_scan_log']:
                R1 = parameters['original_scan_log'][1]['R1'    ]
                R2 = parameters['original_scan_log'][1]['R2'    ]
                
                try:
                    text_matrix1 += '\n\n'
                    for i in range(0,parameters['matrix_i']+1):
                        text_matrix1  += "\nRCOORD1  "
                        for j in range(0,parameters['matrix_j']+1):
                            print i, j 
                            text_matrix1 += "%18.8f  " % (R1[i][j])

                    text_matrix1 += '\n\n'
                    for i in range(0,parameters['matrix_i']+1):
                        text_matrix1  += "\nRCOORD2  "
                        for j in range(0,parameters['matrix_j']+1):
                            text_matrix1 += "%18.8f  " % (R2[i][j])
                except:
                    pass        

        #---------------------------------------------------------------------------------------------------------------
        #                                              Time and log file                                                
        #---------------------------------------------------------------------------------------------------------------
        localtime = time.asctime(time.localtime(time.time()))                                                           
        localtime = localtime.split()                                                                                   
        #  0     1    2       3         4                                                                               
        #[Sun] [Sep] [28] [02:32:04] [2014]                                                                             
        log_file_name = "Scan2D_"+parameters['actual_method'] +'_'+ localtime[1] +'_'+ localtime[2] +'_'+ localtime[3] +'_'+ localtime[4]+'.log' #
        #--------------------------------------------------------------------------------------------------------------
        arq = open(os.path.join(parameters['trajectory'], log_file_name), 'w')
        arq.writelines(header)
        arq.writelines(text_matrix1)
        arq.close()
        #---------------------------------------------------------------------------------------------------------------


                
    def on_checkbutton1_toggled(self, button):
        """ Function doc """
        if self.builder.get_object('checkbutton1').get_active():
            self.builder.get_object('entry2').set_sensitive(True)
            self.builder.get_object('entry3').set_sensitive(True)
        else:
            self.builder.get_object('entry2').set_sensitive(False)
            self.builder.get_object('entry3').set_sensitive(False)
        
    def on_combobox1_changed(self, button):
        _type        = self.builder.get_object('combobox1').get_active_text()
        """ Function doc """
        if _type == 'folder - pDynamo':
            self.builder.get_object('filechooserbutton2').hide()
            self.builder.get_object('filechooserbutton1').show()
        else:
            self.builder.get_object('filechooserbutton2').show()
            self.builder.get_object('filechooserbutton1').hide()





    def __init__(self, EasyHybridSession = None):

        self.builder = gtk.Builder()
        if EasyHybridSession != None:
            self.project          = EasyHybridSession.project
            self.main_builder     = EasyHybridSession.builder
            self.window_control   = EasyHybridSession.window_control
            self.EasyHybridSession = EasyHybridSession
            self.EasyHybrid_ROOT   = EasyHybridSession.EasyHybrid_ROOT
            self.EasyHybrid_GUI    = EasyHybridSession.EasyHybrid_GUI 
            
            
            #      - - - importing ORCA PATH from EasyHybridConfig file. - - -        
            #-----------------------------------------------------------------------#
            try:                                                                    #
                ORCA                = EasyHybridSession.EasyHybridConfig['ORCAPATH']#
            except:                                                                 #
                ORCA = ''                                                           #
            #-----------------------------------------------------------------------#

        self.builder.add_from_file(
            os.path.join(self.EasyHybrid_GUI, 'MOPACEnergy',  'MOPACEnergy.glade'))
                
        self.builder.connect_signals(self)
        self.dialog = self.builder.get_object('dialog1')
        
        
        self.window_control = WindowControl(self.builder)
        # QC SPIN CHARGE
        spinbutton = 'spinbutton_charge'
        config     = [0.0, -500.0, 500.0, 1.0, 0.0, 0.0]
        self.window_control.SETUP_SPINBUTTON(spinbutton, config)

        # QC SPIN MULTIPLICITY
        spinbutton = 'spinbutton_multiplicity'
        config     = [0.0, 1.0,    500.0, 1.0, 0.0, 0.0]
        self.window_control.SETUP_SPINBUTTON(spinbutton, config)

        self.builder.get_object('filechooserbutton2').hide()
        
        #----------------- Setup ComboBoxes ----------------------------------------------#
        combobox = 'combobox1'         #                                                  #
        combolist = ["folder - pDynamo"]#, "trj - AMBER", "dcd - CHARMM", 'xtc - GROMACS']#
        self.window_control.SETUP_COMBOBOXES(combobox, combolist, 0)                      #
        combobox = 'combobox2'         #                                                  #
        combolist = ["SCAN" , 'SCAN-2D']#, "trj - AMBER", "dcd - CHARMM", 'xtc - GROMACS']#
        #---------------------------------------------------------------------------------#
        self.window_control.SETUP_COMBOBOXES(combobox, combolist, 0)
        
        # Hide unfinished widgets
        self.builder.get_object('checkbutton3').set_sensitive(False)



def main():
    dialog = MOPACSEnergyDialog()
    dialog.dialog.run()
    dialog.dialog.hide()
if __name__ == '__main__':
    main()
