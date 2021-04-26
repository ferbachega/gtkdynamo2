#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  MinumumEnergyPathFrom2dEnergySurface.py
#  
#  Copyright 2019 Rafa <rafa@Frost>
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

from logParser import log_parser
import sys
import os
import shutil 
from pprint import pprint
text = '''
#-----------------------------------------------------------------------------#
#                                                                             #
#                                EasyHybrid                                   #
#                   - A pDynamo graphical user interface -                    #
#                                                                             #
#-----------------------------------------------------------------------------#
#     Developed by Jose Fernando R Bachega and Luis Fernando S M Timmers      #
#                            <ferbachega@gmail.com>                           #
#             visit: https://sites.google.com/site/EasyHybrid/                #
#-----------------------------------------------------------------------------#

Welcome to Minumum Energy Path From 2d Energy Surface.

Usage: python MinumumEnergyPathFrom2dEnergySurface.py  -i inputfile -if inputfolder <options>  -o outfolder



Options:
	-i          =  input log file
	-if         =  input 2d PES folder (scan 2D)
	-kf         =  force constant (default is 4.0)
		
	-o          =  output (folder)
	-h          =  help
'''




output_header = '''

#-----------------------------------------------------------------------------#
#                                                                             #
#                                EasyHybrid                                   #
#                   - A pDynamo graphical user interface -                    #
#                                                                             #
#-----------------------------------------------------------------------------#
#     Developed by Jose Fernando R Bachega and Luis Fernando S M Timmers      #
#                            <ferbachega@gmail.com>                           #
#             visit: https://sites.google.com/site/EasyHybrid/                #
#-----------------------------------------------------------------------------#

Welcome to Minumum Energy Path From 2d Energy Surface.

'''


def parser_tags (args):
    """ Function doc """
    if '-i' in args:
	index = args.index('-i')
	log_file  = args[index+1]
    else:
	log_file  = None



    if '-kf' in args:
	index = args.index('-kf')
	kf  = float(args[index+1])
    else:
	kf  = 4.0


    if '-if' in args:
	index = args.index('-if')
	folder  = args[index+1]
    else:
	folder  = None


    if '-o' in args:
	index = args.index('-o')
	output  = args[index+1]
    else:
	output  = None

    input_parm = {  		  
		  'folder'   : folder  , 
		  'log_file' : log_file,
		  'kf'       : kf      ,
		  'output'   : output
		  }
    return input_parm



def find_the_midpoint (coord1 , coord2):
	""" Function doc """
	#print (coord1, coord2)
	
	x = float(coord2[0] - coord1[0])
	x = (x/2)
	#print ('x', x)
	x = coord1[0] + x


	y = float(coord2[1] - coord1[1])
	y = (y/2)
	#print ('y', y)

	y = coord1[1] + y

	#print (x, y)
	return [int(x), int(round(y))]


def check_distance (coord1 , coord2):
	""" Function doc """
	x = float(coord2[0] - coord1[0])
	#x = (x/2)
	y = float(coord2[1] - coord1[1])

	d =  (x**2 + y**2)**0.5
	#print ('x=', x, 'y=', y, 'd=', d)

	if d < 1.42:
		#print 'too close, stop!'
		return False
	
	else:
		#print 'not too close'
		return True






def build_chain_of_states(matrix, input_coord):
	X = matrix
	
	#print (input_coord)
	inset_point = True


	while inset_point == True:
		
		a = 0
		counter = 0
		
		while a == 0:

			try:
				coord1 =  input_coord[ counter  ]
				coord2 =  input_coord[ counter+1]

				inset_point = check_distance (coord1 , coord2)
				
				if inset_point == False:
					counter += 1
					#print ('inset_point == False')
				else:
					midpoint = find_the_midpoint (coord1 , coord2)
					#print counter, counter+1, midpoint, input_coord
					input_coord.insert(counter+1, 0 )
					input_coord[counter+1] = midpoint
			except:
				a = True
	#print input_coord
	return input_coord
	
	'''
	lista = []
	px = 0
	py = 0

	# rminimum path energy frames
	frame_list = []
	frame = str(px)+ "_" +str(py)
	frame_list.append(frame)


	print X[px][py]
	lista.append(X[px][py])
	while 1 != 0:
		try:
			p1 = X[px+1][py+0]
		except:
			p1 = 1000000000000000
		try:
			p2 = X[px+0][py+1]
		except:
			p2 = 1000000000000000
		try:	
			p3 = X[px+1][py+1]
		except:
			p3 = 1000000000000000		
		
		
		if p3 < p2 and p3 < p1:
			#print p3
			px = px + 1
			py = py + 1
			lista.append(p3)

			frame = str(px)+ "_" +str(py)
			frame_list.append(frame)
			
		if p2 < p1 and p2 < p3:
			#print p2
			px = px + 0
			py = py + 1
			lista.append(p2)

			frame = str(px)+ "_" +str(py)
			frame_list.append(frame)
			
		if p1 < p2 and p1 < p3:
			#print p1
			px = px + 1
			py = py + 0
			lista.append(p1)

			frame = str(px)+ "_" +str(py)
			frame_list.append(frame)
			
			
		if p1 == 1000000000000000 and p2 == 1000000000000000 and p3 == 1000000000000000:
			break
	return lista , frame_list
	'''



def get_gradient_from_matrix_line (matrix_line, position):
    """ Function doc """
    d1 =  matrix_line[position-1] - matrix_line[position]
    #print position,'d1' , d1
    if d1 <= 0: 
	return -1 
    
    d2 =  matrix_line[position+1] - matrix_line[position]
    #print position, 'd2' , d2
    if d2 <= 0:
	return 1 

    return 0


def outputLogBuilder (log_file     = None,
		      folder       = None,
		      outputfolder = None,
		      energy       = None,
		      frame_list   = None
		      ):
    """ Function doc """
    
    text   = ''''''
    string = ''
    
    
    
    
    
    
    


args = sys.argv
inputs = parser_tags (args)



if '-h' in args or '-H' in args or inputs['folder'] == None or inputs['log_file'] == None or inputs['output'] == None:
    print text

else:
    data = log_parser (inputs['log_file'])
    data = data[1]
    k    = inputs['kf']
    z    = data['matrix']

    reac = [0,0]
    #ts   = [15,30]
    prod = [20,20]
    
    
    #
    Initial_positions = [reac, [4,10], prod]
    #Initial_positions = [reac, ts,  prod]
    
    
    
    print 'Matrix size:', len(z), len(z[0])

    initial_size = len(Initial_positions)
    xy_surface_positions   = build_chain_of_states(z, Initial_positions)
    final_size   = len(xy_surface_positions)
    
    #print xy_surface_positions
    print "\n\nOriginal chain of states: \n"
    for xy_coord in xy_surface_positions:
	#                    X     Y
	x = xy_coord[0]
	y = xy_coord[1]
	#print xy_coord, len(z), len(z[0])
	#try:
	print x, y, z[y][x]
	#except:
	    #print z[y]
    #'''
    
    counter                 = None
    total_sum_grad_ateriror = 0
    delta                   = None
    
    chain_of_states_convergence = False
    

    chain_of_states_convergence_max_interactions = 100
    chain_of_states_convergence_counter = 0
    
    while  chain_of_states_convergence != True:
	'''
	Optmizing the chain of states 
	----------------------------------------------------------------------------------------
	'''
	
	chain_of_states_perturbation_max_interactions = 100
	chain_of_states_perturbation_counter = 0
	
	while delta != 0:
	    total_sum_grad = 0
	    for xy_coord in xy_surface_positions:
		#                    X     Y
		index       = xy_surface_positions.index(xy_coord)
		final_index = len(xy_surface_positions)
		
		
		if index == 0 or index  == final_index-1:
		    pass
		
		else:
		    xy_coord_before = xy_surface_positions[index-1]
		    xy_coord_after  = xy_surface_positions[index+1]
		    
		    x_before   = xy_coord_before[0]
		    y_before   = xy_coord_before[1]
		    
		    
		    x_midpoint = xy_coord[0]
		    y_midpoint = xy_coord[1]
		
		    
		    x_after    = xy_coord_after[0]
		    y_after    = xy_coord_after[1]
		
		    #----------------------- X   perturbations  ---------------------------------------
		    energy_left  = k*( (x_midpoint-1) - x_before )**2 + k*( x_after - (x_midpoint-1) )**2
		    energy_midle = k*(  x_midpoint    - x_before )**2 + k*( x_after -  x_midpoint    )**2
		    energy_right = k*( (x_midpoint+1) - x_before )**2 + k*( x_after - (x_midpoint+1) )**2
		
		    
		    energy_left__from_matrix = z[y_midpoint][x_midpoint-1]
		    energy_midle_from_matrix = z[y_midpoint][x_midpoint]
		    energy_right_from_matrix = z[y_midpoint][x_midpoint+1]
		    
		    sum_l = energy_left  + energy_left__from_matrix
		    sum_m = energy_midle + energy_midle_from_matrix
		    sum_r = energy_right + energy_right_from_matrix
		    
		    
		    d1 = sum_l - sum_m
		    d2 = sum_r - sum_m  

		    if d2 < 0:
			asn = 1 
			total_sum_grad += d1

		    if d1 < 0: 
			asn = -1 	
			total_sum_grad += d2

		    if d1  > 0  and d2 > 0:
			asn = 0
		    
		    xy_surface_positions[index][0] += asn
		    #-------------------------------------------------------------------------------------
		    
		    
		    
		    #-----------------------   Y    perturbations  ---------------------------------------
		    energy_left  = k*( (y_midpoint-1) - y_before )**2 + k*( y_after - (y_midpoint-1) )**2
		    energy_midle = k*(  y_midpoint    - y_before )**2 + k*( y_after -  y_midpoint    )**2
		    energy_right = k*( (y_midpoint+1) - y_before )**2 + k*( y_after - (y_midpoint+1) )**2
		
		    
		    energy_left__from_matrix = z[y_midpoint-1][x_midpoint]
		    energy_midle_from_matrix = z[y_midpoint  ][x_midpoint]
		    energy_right_from_matrix = z[y_midpoint+1][x_midpoint]
		    
		    sum_l = energy_left  + energy_left__from_matrix
		    sum_m = energy_midle + energy_midle_from_matrix
		    sum_r = energy_right + energy_right_from_matrix
		    
		    
		    d1 = sum_l - sum_m
		    d2 = sum_r - sum_m  

		    if d2 < 0:
			asn = 1 
			total_sum_grad += d1

		    if d1 < 0: 
			asn = -1 	
			total_sum_grad += d2

		    if d1  > 0  and d2 > 0:
			asn = 0
		    
		    xy_surface_positions[index][1] += asn
	    
	    delta = total_sum_grad_ateriror - total_sum_grad
	    #print total_sum_grad, delta
	    total_sum_grad_ateriror = total_sum_grad


	    old = None
	    for xy_coord in xy_surface_positions:
		#                    X     Y
		index  = xy_surface_positions.index(xy_coord)
		if xy_coord == old:
		    #print 'pop item:', xy_coord, index
		    xy_surface_positions.pop(index)
		else:
		    
		    x = xy_coord[0]
		    y = xy_coord[1]
		    #print x, y, z[y][x]
		old = xy_coord
	    
	    chain_of_states_perturbation_counter += 1
	    
	    
	    if chain_of_states_perturbation_counter == chain_of_states_convergence_max_interactions:
		delta =  0
	    
	    
	'''
	----------------------------------------------------------------------------------------
	'''
	
	
	chain_of_states_convergence_counter += 1

	old = xy_surface_positions
	xy_surface_positions = build_chain_of_states(z, xy_surface_positions)
    
	if old == xy_surface_positions:
	    chain_of_states_convergence = True
	else:
	    pass
	
	
	if chain_of_states_convergence_counter == chain_of_states_convergence_max_interactions:
	    chain_of_states_convergence = True
	else:
	    pass
    
    #print xy_surface_positions
    print "\n\nOptimized chain of states: \n"
    for xy_coord in xy_surface_positions:
	#                    X     Y
	x = xy_coord[0]
	y = xy_coord[1]
	print x, y, z[y][x]
    
    
    #------------------------------------------------------------------------------------------
    #     exporting frames
    #------------------------------------------------------------------------------------------
    
    #'''
    Files    = os.listdir(inputs['folder']) 

	
    if not os.path.isdir(inputs['output']):
	os.mkdir(inputs['output'])
	#print "Temporary files directory:  %s" % EasyHybrid_TMP

    print  output_header
    print 'input logFile: ', inputs['log_file']
    print 'input folder:  ', inputs['folder']
    print 'output folder: ', inputs['output']
    #print '\n{:15s} {:<15s}  {:<15s}  {:15s}\n'.format('Frame num.', 'New Frame',  'Original Frame',   "Energy" )
    
    n = 0
    for i in xy_surface_positions:
	if 'frame_'+ str(i[1])+'_'+str(i[0])+'.pkl' in Files:
	    
	    
	    frame  = 'frame_' + str(i[1])+'_'+str(i[0])+'.pkl'
	    frame2 = os.path.join(inputs['folder'],frame)
	    frameout = os.path.join(inputs['output'],'frame'+str(n)+'.pkl')
	    shutil.copy(frame2, frameout)
	    
	    
	    #text = "%15i    %15s    %15s       %15.9f"   % (n, 'frame'+str(n)+'.pkl',  frame,   z[i[0]][i[1]]     )
	    #text = "%15i    %15s    %15s       %15.9f"   % (n, 'frame'+str(n)+'.pkl',  frame,   lista[n]     )
	    text = "{:5d}     {:<15s}    {:<15s}    {:15.9f}".format(n, 'frame'+str(n)+'.pkl',  frame,    z[i[1]][i[0]] )
	    
	    #"{:<6s}{:5d} {:<4s}{:1s}{:3s} {:1s}{:4s}{:1s}   {:8.3f}{:8.3f}{:8.3f}{:6.2f}{:6.2f}      {:<4s}{:2s}{:2s}\n"
	    
	    print text
	    #'frame'+str(n)+'.pkl', frame , lista[n]
	    n += 1
	else:
	    
	    print 'frame_.pkl'
    #'''

