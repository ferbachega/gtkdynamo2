#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  DynamicBondsTable.py
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
from pBabel           import *
from pCore            import *
from pMolecule        import *
from pMoleculeScripts import *
from PyMOLScripts     import *

system = Unpickle('/home/labio/Documents/gtkdynamo2/test/test.pkl')
lista  = [399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419]


BondTable       = {}
PyMOL_BondTable = {}

for i in lista:
    for j in lista: 
        if i != j:
            atom1    = system.atoms[i]
            atom2    = system.atoms[j]
            element1 = PeriodicTable.Symbol (atom1.atomicNumber ).upper ( )
            element2 = PeriodicTable.Symbol (atom2.atomicNumber ).upper ( )
            #BondTable[i,j] = [atomic_dic[element1][2] + atomic_dic[element2][2], True]
            
            
            
            Distance_i_j             = system.coordinates3.Distance (i,j)
            Rcov                     = (atomic_dic[element1][2] + atomic_dic[element2][2]) + (atomic_dic[element1][2] + atomic_dic[element2][2])/50
            Bond_Unbond              = None
            if Distance_i_j <= Rcov:
                Bond_Unbond  = True
            else:
                Bond_Unbond  = False

            #PyMOL_BondTable[i+1,j+1] = [atomic_dic[element1][2] + atomic_dic[element2][2], True]
            print i+1, element1, j+1,element2, "BOND: ", Rcov, Distance_i_j, Bond_Unbond
            PyMOL_BondTable[i+1,j+1] = [Rcov, Bond_Unbond]

#for i in PyMOL_BondTable:
#    print i, PyMOL_BondTable[i]
#
#dist = cmd.get_distance(PyMOL_Obj+ ' and index ' + str(lista[i]), PyMOL_Obj+ ' and index '+ str(lista[j]), int (valor) )

#print BondTable

#for index in lista:
#	atom = system.atoms[index]
#	element = PeriodicTable.Symbol (atom.atomicNumber ).upper ( )
#	print index, element, atomic_dic[element][0],atomic_dic[element][1]


def main():
	
	return 0

if __name__ == '__main__':
	main()

