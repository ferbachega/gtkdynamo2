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
from PyMOLScripts.PyMOLScripts import PymolGetTable
from pymol import cmd 


def set_charges_to_zero (project, selection):
    """ Function doc """
    pass


def split_charges_in_selection (project = None, PyMOL_Obj = None):                            
    """ Function doc """
    print '--------------------------------------------------------------------'                                                                    
    system       = project.system                                                             
    
    obj          = cmd.get_model(PyMOL_Obj)                                                   
    model_split  = obj.atom	                                                                  
    residue_list = []                                                                         
    PyMOL_Obj    = project.settings['PyMOL_Obj']
    for i in model_split:                                                                     
        resi = i.resi                                                                         
        if resi in 	residue_list:                                                             
            pass                                                                              
        else:                                                                                 
            residue_list.append(resi)                                                         
    
    print PyMOL_Obj
    #print model_split
    print residue_list
    
    for resi in residue_list:                                                                 
        #command = 'select charge_split, (' + PyMOL_Obj + ' and  resi ' + str(resi) +' )'              
                                                                                              
        #select sele, Step1 and  resi 178 and  not name ca+C+O+OXT+N+H+HA+H1+H2+H3            
                                                                                              
        #cmd.do(command)                                                                      
        #                         N+HT1+HT2+HT3+CA+HA+HA2+C+O+HN+OT1+OT2   
        #                         #----- AMBER / OPLS atom names       |            CHARMM atom names---------|              
        commands = ['and not name CA+C+O+OXT+N+H+HA+HA2+HA3+H1+H2+H3',#+N+HT1+HT2+HT3+CA+HA+HA2+C+O+HN+OT1+OT2', # side chain               
                    'and name     CA+C+O+OXT+N+H+HA+HA2+HA3+H1+H2+H3']#+N+HT1+HT2+HT3+CA+HA+HA2+C+O+HN+OT1+OT2'] # main chain               
        
        
        print '\n\n--------------------------------------------------------------------', 
        print 'Residue: ' , resi
        
        command = 'select  chg , ' +PyMOL_Obj + ' and resi '+str(resi)+' and not name CA+C+O+OXT+N+H+HA+HA2+HA3+H1+H2+H3'
        cmd.do(command)
        _sum, _len = compute_selection_total_charge (system, selection = 'chg')
        charge = round(_sum)
        
        print  '-----------------------------------------------------------'
        print  'SIDE CHAIN sum of partial charges: ', _sum                                                      
        rescale_charges(project, 'chg', charge)                                                
        _sum, _len = compute_selection_total_charge (system, selection = 'chg')
        print  'SIDE CHAIN sum of partial charges after rescale: ', _sum                                                      
        print  '-----------------------------------------------------------'
        
        
        
        
        command = 'select  chg , ' +PyMOL_Obj + ' and resi '+str(resi)+' and name CA+C+O+OXT+N+H+HA+HA2+HA3+H1+H2+H3'
        cmd.do(command)
        _sum, _len = compute_selection_total_charge (system, selection = 'chg')            
        charge = round(_sum)                                                                                 

        if _sum >= 10e-10:
            print  '-----------------------------------------------------------'
            print  'MAIN CHAIN sum of partial charges: ', _sum
            print  'MAIN CHAIN sum of partial charges after rescale: ', _sum
            #print   _sum,     _len, charge                                                         
            print  '-----------------------------------------------------------'

            pass
        else:
            print  '-----------------------------------------------------------'
            print  'MAIN CHAIN sum of partial charges: ', _sum
            rescale_charges(project, 'chg', charge)    
            _sum, _len = compute_selection_total_charge (system, selection = 'chg')                                                  
            print  'MAIN CHAIN sum of partial charges after rescale: ', _sum
            #print   _sum,     _len, charge                                                         
            print  '-----------------------------------------------------------'

                    
                                                                                              
        #for command in commands:                                                              
        #    cmd.select ('charge_split',  PyMOL_Obj + ' and sele  and  resi ' + str(resi) + command)             
        #    
        #    _sum, _len = compute_selection_total_charge (system, selection = 'sele')          
        #    charge = round(_sum)                                                              
        #    #diference  = charge - _sum                                                       
        #    rescale_charges(project, 'charge_split', charge)                                          
                                                                                              
                                                                                              
                                                                                              
                                                                                              
                                                                                              
                                                                                              
def check_charges_by_residue (project = None, PyMOL_Obj = None):                              
    """ Function doc """                                                                      
    system       = project.system
    obj          = cmd.get_model(PyMOL_Obj)
    model_split  = obj.atom	
    residue_list = [] 

    for i in model_split:
        resi = i.resi
        if resi in 	residue_list:
            pass
        else:
            residue_list.append(resi)
    #print residue_list
    for resi in residue_list:
        command = 'select sele, (' + PyMOL_Obj + ' and  resi ' + str(resi) +' )'
        #cmd.do(command)
        cmd.select ('sele',  PyMOL_Obj + ' and  resi ' + str(resi) )
        _sum, _len = compute_selection_total_charge (system, selection = 'sele')
        charge = round(_sum)
        
        diference  = charge - _sum
        
        rescale_charges(project, 'sele', charge)

def compute_selection_total_charge (system, selection = None):
    """ Function doc """
    #-------------------------------------------------------------------#
    if selection == None:                                               #
        index_table = PymolGetTable('sele')                             #
    else:                                                               #
        index_table = PymolGetTable(selection)                          #
    
    charges         = system.energyModel.mmAtoms.AtomicCharges()        #
    charge_table    = []                                                #
    #-------------------------------------------------------------------#
    #print 'index_table:', index_table
    for i in index_table:
        charge_table.append(charges[int(i)])
        
    _sum = sum(charge_table) # the sum of partial charges of the atoms from selection list
    _len = len(charge_table)
    return _sum, _len
 
   

def rescale_charges(project, selection, total_charge):	
    #selection       = self.builder.get_object('04_window_entry_pymol_selection').get_text()
    #total_charge    = int(self.builder.get_object('04_window_entry_charge').get_text())
    #output_filename = "chrg_table.index"
    
    #selection indexes
    #-------------------------------------------------------------------#
    index_table     = PymolGetTable(selection)                          # selection indexes
    charges         = project.system.energyModel.mmAtoms.AtomicCharges()#
    charge_table    = []                                                #
    #-------------------------------------------------------------------#
    
    for i in index_table:
        try:
            charge_table.append(charges[i])
        except:
            print 'index_table', len(index_table)
            print 'charges', len(charges)
            print 'charge_table', len(charge_table)
            
            
    a = sum(charge_table) # the sum of partial charges of the atoms from selection list
    l = len(charge_table) # number of the atoms from selection list

    frac = (total_charge - a)/l 

    
    print "total charge = ", total_charge
    print "sum of total charges in the block = ", a
    print "fraction charges is = ", frac
    
    # rescaling the charges 
    charges_new = []
    for i in charge_table:
        i = i + frac
        charges_new.append(i)
        
    #print charges_new
    #print sum(charges_new)
    #
    
    #charges.Print()
    n = 0
    
    # adding the new charges to system
    for i in index_table:
        charges[i]=charges_new[n]
        n = n+1
    #charges.Print()
    project.system.energyModel.mmAtoms.SetAtomicCharges(charges)

	
    #def CHARGE_PRINT(self, project):
	#	#data_path       = self.builder.get_object("01_main_window_filechooserbutton_datapath").get_filename()
	#	#selection       = self.builder.get_object('04_window_entry_pymol_selection').get_text()
	#	#total_charge    = int(self.builder.get_object('04_window_entry_charge').get_text())
	#	#output_filename = "chrg_table.index"
	#	
	#	selection       = "sele"
	#	index_table     = pymol_get_table(selection)
	#	charges         = project.system.energyModel.mmAtoms.AtomicCharges()
	#	
	#	charge_table    = []
	#	   
	#	for i in index_table:
	#		charge_table.append(charges[i])
	#		
	#	a = sum(charge_table)
	#	l = len(charge_table)
	#	frac = (total_charge - a)/l
    #
	#	print "total charge = ", total_charge
	#	print "sum of total charges in the block = ", a
	#	print "fraction charges is = ", frac
    #
	#	#charges_new = []
	#	#for i in charge_table:
	#	#	i = i + frac
	#	#	charges_new.append(i)
	#	#	
	#	#print charges_new
	#	#print sum(charges_new)
	#	#
	#	#
	#	#charges.Print()
	#	#n = 0
	#	#for i in index_table:
	#	#	charges[i]=charges_new[n]
	#	#	n = n+1
	#	#charges.Print()
	#	#project.system.energyModel.mmAtoms.SetAtomicCharges(charges)

def main():
    system = Unpickle(EasyHybrid_ROOT + '/test/test.pkl')
    pDynamoScan = pDynamoScan()
    return 0

if __name__ == '__main__':
    main()
