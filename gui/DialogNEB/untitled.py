#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  untitled.py
#  
#  Copyright 2015 Fernando Bachega <fernando@bahamuth>
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




def run_SAW(parameters = None, project = None):
	reactants_file           = parameters['reactants_file'           ]
	products_file            = parameters['products_file'            ]
	data_path                = parameters['data_path'                ]
	SAW_number_of_structures = parameters['SAW_number_of_structures' ]
	SAW_maximum_interations  = parameters['SAW_maximum_interations'  ]
	SAW_gamma                = parameters['SAW_gamma'                ]
	trajectory_name          = parameters['trajectory_name'          ]
	plot_flag                = parameters['plot_flag'                ]
	dualLog                  = parameters['dualLog'                  ]
	
	t_initial = time.time()
	
	
	
	#----------------------------------   Reactants   -----------------------------------------#    
																							   #
	type_ = get_file_type (reactants_file)                                                     #
	#reactants = XYZFile_ToCoordinates3(os.path.join ( reactants_file ), log = dualLog  )      #
	if type_ == "xyz":                                                                         #
		reactants = XYZFile_ToCoordinates3 ( os.path.join (reactants_file),  dualLog )         #
																							   #
	elif type_ == "pdb":                                                                       #      # When the coordinate file is a PDB
		reactants_file = gtkdin_PDBFile_ToCoordinates3(reactants_file)                         #      # Uses the gtkdin_PDBFile_ToCoordinates3 functions - converts a PDB to XYZ
		reactants = XYZFile_ToCoordinates3 ( os.path.join (reactants_file),  dualLog )         #      # imports the xyz file
		os.remove("tmp_out.xyz")                                                               #
																							   #
	elif type_ == "xpk":                                                                       #
		try:                                                                                   #
			reactants = Unpickle (reactants_file)                                              #
		except:                                                                                #
			reactants = XMLUnpickle (reactants_file)		                                   #
																							   #
	elif type_ == "pkl":                                                                       #
		try:                                                                                   #
			reactants = Unpickle (reactants_file)                                              #
		except:                                                                                #
			reactants = XMLUnpickle (reactants_file)                                           #
																							   #
	elif type_ == "yaml":                                                                      #
		reactants = YAMLUnpickle (reactants_file)                                              #
																							   #
	elif type_ == "chm":                                                                       #
		reactants = CHARMMCRDFile_ToCoordinates3 ( os.path.join ( reactants_file ),  dualLog ) #
																							   #
	elif type_ == "crd":                                                                       #
		reactants = AmberCrdFile_ToCoordinates3 ( os.path.join (reactants_file),  dualLog )    #
																							   #
	elif type_ == "mol":                                                                       #
		reactants = MOLFile_ToCoordinates3( os.path.join ( reactants_file),  log = dualLog )   #
	else:                                                                                      #
		return "ops!"	                                                                       #
																							   #
																							   #
	#------------------------------------------------------------------------------------------#





	#----------------------------------   Products   ------------------------------------------#
																							   #
	type_ = get_file_type (products_file)                                                      #
	#products = XYZFile_ToCoordinates3(os.path.join ( products_file ), log = dualLog  )        #
	if type_ == "xyz":                                                                         #
		products = XYZFile_ToCoordinates3 ( os.path.join (products_file),  dualLog )           #
																							   #
	elif type_ == "pdb":                                                                       #
		products_file = gtkdin_PDBFile_ToCoordinates3(products_file)                           #  
		products = XYZFile_ToCoordinates3 ( os.path.join (products_file),  dualLog )           #
		os.remove("tmp_out.xyz")                                                               #
																							   #
	elif type_ == "xpk":                                                                       #
		try:                                                                                   #
			products = Unpickle (products_file)                                                #
		except:                                                                                #
			products = XMLUnpickle (products_file)		                                       #
																							   #
	elif type_ == "pkl":                                                                       #
		try:                                                                                   #
			products = Unpickle (products_file)                                                #
		except:                                                                                #
			products = XMLUnpickle (products_file)                                             #
																							   #
	elif type_ == "yaml":                                                                      #
		products = YAMLUnpickle (products_file)                                                #
																							   #
	elif type_ == "chm":                                                                       #
		products = CHARMMCRDFile_ToCoordinates3 ( os.path.join ( products_file ),  dualLog )   #
																							   #
	elif type_ == "crd":                                                                       #
		products = AmberCrdFile_ToCoordinates3 ( os.path.join (products_file),  dualLog )      #
																							   #
	elif type_ == "mol":                                                                       #
		products = MOLFile_ToCoordinates3( os.path.join ( products_file),  log = dualLog )     #
	else:                                                                                      #
		return "ops!"	                                                                       #
																							   #
	#------------------------------------------------------------------------------------------#



	# . Create a starting trajectory.
	trajectory = SystemGeometryTrajectory.LinearlyInterpolate( 
											os.path.join ( data_path, 
											               trajectory_name), 
											self.system, 
											SAW_number_of_structures, 
											reactants, products 
											                  )


	# . Pathway.
	SAWOptimize_SystemGeometry ( self.system,                                    \
								 trajectory,                                     \
								 log = dualLog,                                  \
								 gamma             = SAW_gamma,                  \
								 maximumIterations = SAW_maximum_interations     )	

	#print NEB_data
	trajectory.Close ( )
	t_final = time.time()
	



def main():
	
	return 0

if __name__ == '__main__':
	main()
