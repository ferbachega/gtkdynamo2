#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  MOPACEnergy.py
#  
#  Copyright 2015 farminf <farminf@farminf-3>
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


# pDynamo
from pBabel           import *
from pCore            import *
from pMolecule        import *
from pMoleculeScripts import *
import os
import subprocess 
from pprint import pprint

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
                         MOZYME       = True , 
                         BONDS        = False,
                         PDBOUT       = False,
                         SOLV         = False
                         ):
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
        if BONDS:
            text += 'BONDS' + ' '
        if PDBOUT:
            text += 'PDBOUT' + ' '
        if SOLV:
            text += 'EPS=78.39 RSOLV=1.3'+ ' '
        if self.QMMM:
            text += 'GRAD QMMM'+ ' '
        
        self.MopacKeys = text
        
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

        #---------------- Q M M M ---------------------#
        atoms_dic = generate_atoms_dic(self.system)    #
        #----------------------------------------------#
        
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
            generate_molin_file(self.system)
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
        
        text += 'Mopac file generated by GTKDynamo'
        
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
        return energy




system = Unpickle('TIM_sitio_grande_AM1.pkl')
trajectory = SystemGeometryTrajectory ('/home/farminf/pDynamoWorkSpace/TIM_sitio_grande_AM1/25_step_Scan', system, mode = "r" )
methods = ['AM1','PM3','RM1','PM6','PM6-DH','PM6-DH2','PM6-DH+','PM6-DH2X','PM6-D3H4','PM7'] 


system.Summary()
logs = {
        #method: {
                  #energy     : []
                  #energyNorm : []
                 # }
        }

for method in methods:
    logs[method] = {
                    'energy'     : [],
                    'energyNorm' : [],
                    }
    n = 0 
    while trajectory.RestoreOwnerData ( ):
        MOPAC_system = pDynamoToMOPAC(system = system)
        MOPAC_system.DefineMopacKeys (methods      = method   ,
                                      charge       = '-2'     ,
                                      multiplicity = 'Singlet',
                                      AUX          = True     ,
                                      single_point = True     ,
                                      MOZYME       = True     , 
                                      BONDS        = False    ,
                                      PDBOUT       = False    ,
                                      SOLV         = True    )
        
        energy = MOPAC_system.Energy(fileout = 'system'+str(n)+'.mop')
        
        logs[method]['energy'].append(float(energy))
        logs[method]['energyNorm'].append(float(energy) - logs[method]['energy'][0])
        
        #Energy.append(energy)
        #print n
        n  += 1
    #pprint (logs)


n= 0
string = ''

for method in logs:
    string += method + '  '
string += '\n'



for i in range( 0, len(logs['AM1']['energyNorm'])):  
    for method in logs:
        string += str(logs[method]['energyNorm'][i]) + '  '
    string += '\n'
    n += 1
#pprint (Energy)


pprint (logs)

print string
arq = open('output_sitio_grande_AM1_30steps_PM7_TS.log', 'w') 
arq.writelines(string)
arq.close()













































#pprint(logs)
