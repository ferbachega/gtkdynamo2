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



def set_charges_to_zero (project, selection):
    """ Function doc """
    pass


def compute_selection_total_charge (system, selection = None):
    """ Function doc """
    #-------------------------------------------------------------------#
    if selection == None:                                               #
        index_table = PymolGetTable('sele')                             #
    else:                                                               #
        index_table = selection                                         #
    
    charges         = system.energyModel.mmAtoms.AtomicCharges()        #
    charge_table    = []                                                #
    #-------------------------------------------------------------------#
    
    for i in index_table:
        charge_table.append(charges[i])
        
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
        charge_table.append(charges[i])
        
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
    
    charges.Print()
    n = 0
    
    # adding the new charges to system
    for i in index_table:
        charges[i]=charges_new[n]
        n = n+1
    charges.Print()
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
    system = Unpickle(GTKDYNAMO_ROOT + '/test/test.pkl')
    pDynamoScan = pDynamoScan()
    return 0

if __name__ == '__main__':
    main()
