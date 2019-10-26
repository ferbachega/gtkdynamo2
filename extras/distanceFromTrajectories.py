#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  distanceFromTrajectories.py
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
from pBabel           import *
from pCore            import *
from pMolecule        import *
from pMoleculeScripts import *
import os

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

Welcome to  

Usage: python script.py  -i inputfile -if inputfolder <options>  -o outfolder

Options:
	-i          =  
	-if         =  
	-o          =  
	-h          =  
'''


filename = '/home/rafa/programs/gtkdynamo2/extras/old/Chaine_AM1_dPhot_Oct_14_2019.pkl'


trajectories = [
#'/home/rafa/pDynamoWorkSpace/Chaine_AM1_dPhot_Oct_14_2019/2_step_UmbrellaSampling/Equilibration/frame0'  ,
#'/home/rafa/pDynamoWorkSpace/Chaine_AM1_dPhot_Oct_14_2019/2_step_UmbrellaSampling/Equilibration/frame1'  ,
#'/home/rafa/pDynamoWorkSpace/Chaine_AM1_dPhot_Oct_14_2019/2_step_UmbrellaSampling/Equilibration/frame2'  ,
#'/home/rafa/pDynamoWorkSpace/Chaine_AM1_dPhot_Oct_14_2019/2_step_UmbrellaSampling/Equilibration/frame3'  ,
#'/home/rafa/pDynamoWorkSpace/Chaine_AM1_dPhot_Oct_14_2019/2_step_UmbrellaSampling/Equilibration/frame4'  ,
#'/home/rafa/pDynamoWorkSpace/Chaine_AM1_dPhot_Oct_14_2019/2_step_UmbrellaSampling/Equilibration/frame5'  ,
#'/home/rafa/pDynamoWorkSpace/Chaine_AM1_dPhot_Oct_14_2019/2_step_UmbrellaSampling/Equilibration/frame6'  ,
#'/home/rafa/pDynamoWorkSpace/Chaine_AM1_dPhot_Oct_14_2019/2_step_UmbrellaSampling/Equilibration/frame7'  ,
#'/home/rafa/pDynamoWorkSpace/Chaine_AM1_dPhot_Oct_14_2019/2_step_UmbrellaSampling/Equilibration/frame8'  ,
#'/home/rafa/pDynamoWorkSpace/Chaine_AM1_dPhot_Oct_14_2019/2_step_UmbrellaSampling/Equilibration/frame9'  ,
#'/home/rafa/pDynamoWorkSpace/Chaine_AM1_dPhot_Oct_14_2019/2_step_UmbrellaSampling/Equilibration/frame10' ,
#'/home/rafa/pDynamoWorkSpace/Chaine_AM1_dPhot_Oct_14_2019/2_step_UmbrellaSampling/Equilibration/frame11' ,
#'/home/rafa/pDynamoWorkSpace/Chaine_AM1_dPhot_Oct_14_2019/2_step_UmbrellaSampling/Equilibration/frame12' ,
#'/home/rafa/pDynamoWorkSpace/Chaine_AM1_dPhot_Oct_14_2019/2_step_UmbrellaSampling/Equilibration/frame13' ,
#'/home/rafa/pDynamoWorkSpace/Chaine_AM1_dPhot_Oct_14_2019/2_step_UmbrellaSampling/Equilibration/frame14' ,
#'/home/rafa/pDynamoWorkSpace/Chaine_AM1_dPhot_Oct_14_2019/2_step_UmbrellaSampling/Equilibration/frame15' ,
#'/home/rafa/pDynamoWorkSpace/Chaine_AM1_dPhot_Oct_14_2019/2_step_UmbrellaSampling/Equilibration/frame16' ,
#'/home/rafa/pDynamoWorkSpace/Chaine_AM1_dPhot_Oct_14_2019/2_step_UmbrellaSampling/Equilibration/frame17' ,
#'/home/rafa/pDynamoWorkSpace/Chaine_AM1_dPhot_Oct_14_2019/2_step_UmbrellaSampling/Equilibration/frame18' ,
#'/home/rafa/pDynamoWorkSpace/Chaine_AM1_dPhot_Oct_14_2019/2_step_UmbrellaSampling/Equilibration/frame19' ,
#'/home/rafa/pDynamoWorkSpace/Chaine_AM1_dPhot_Oct_14_2019/2_step_UmbrellaSampling/Equilibration/frame20' ,
#'/home/rafa/pDynamoWorkSpace/Chaine_AM1_dPhot_Oct_14_2019/2_step_UmbrellaSampling/Equilibration/frame21' ,
#'/home/rafa/pDynamoWorkSpace/Chaine_AM1_dPhot_Oct_14_2019/2_step_UmbrellaSampling/Equilibration/frame22' ,
#'/home/rafa/pDynamoWorkSpace/Chaine_AM1_dPhot_Oct_14_2019/2_step_UmbrellaSampling/Equilibration/frame23' ,
#'/home/rafa/pDynamoWorkSpace/Chaine_AM1_dPhot_Oct_14_2019/2_step_UmbrellaSampling/Equilibration/frame24' ,
#'/home/rafa/pDynamoWorkSpace/Chaine_AM1_dPhot_Oct_14_2019/2_step_UmbrellaSampling/Equilibration/frame25' ,
#'/home/rafa/pDynamoWorkSpace/Chaine_AM1_dPhot_Oct_14_2019/2_step_UmbrellaSampling/Equilibration/frame26' ,
#'/home/rafa/pDynamoWorkSpace/Chaine_AM1_dPhot_Oct_14_2019/2_step_UmbrellaSampling/Equilibration/frame27' ,
#'/home/rafa/pDynamoWorkSpace/Chaine_AM1_dPhot_Oct_14_2019/2_step_UmbrellaSampling/Equilibration/frame28' ,
#'/home/rafa/pDynamoWorkSpace/Chaine_AM1_dPhot_Oct_14_2019/2_step_UmbrellaSampling/Equilibration/frame29' ,
#'/home/rafa/pDynamoWorkSpace/Chaine_AM1_dPhot_Oct_14_2019/2_step_UmbrellaSampling/Equilibration/frame30' ,
'/home/rafa/pDynamoWorkSpace/Chaine_AM1_dPhot_Oct_14_2019/2_step_UmbrellaSampling/Equilibration/frame31' ,
]
bonds  = [[4483,4484]]
system = Unpickle(filename)


trajectory_distance1 = []
trajectory_distance2 = []
trajectory_d1_minus_d2 = []



for trajectory  in trajectories:
	
	files = os.listdir(trajectory)
	
	n = 0
	for _file in files:
		_file2 = _file.split('.')
		
		if _file2[-1] == 'pkl':
			pass
		else:
			files.pop(n)
		n += 1
	
	
	frame_distance1 = []
	frame_distance2 = []
	frame_d1_minus_d2 = []
	for frame in files:
		

		
		system.coordinates3 = Unpickle(os.path.join(trajectory,frame))
		frame_name = frame.split('/')
			
		for bond in bonds:
			
			distance1 = system.coordinates3.Distance (4551, 4484,)
			distance2 = system.coordinates3.Distance (4484, 4483,)
			
			print trajectory, frame_name[-1], bond, distance1, distance2 , distance2 - distance1


			frame_distance1.append(distance1)
			frame_distance2.append(distance2)
			frame_d1_minus_d2.append(distance2 - distance1)


	trajectory_distance1.append(frame_distance1)
	trajectory_distance2.append(frame_distance2)
	trajectory_d1_minus_d2.append(frame_d1_minus_d2)





window_number = 0
for window in trajectory_distance1:

	mean_valor = 0.0
	size = len(window)
	
	for distance in window:
		mean_valor += distance

	
	print window_number, mean_valor/size, mean_valor
	window_number += 1




window_number = 0
for window in trajectory_distance2:

	mean_valor = 0.0
	size = len(window)
	
	for distance in window:
		mean_valor += distance

	
	print window_number, mean_valor/size, mean_valor
	window_number += 1





window_number = 0
for window in trajectory_d1_minus_d2:

	mean_valor = 0.0
	size = len(window)
	
	for distance in window:
		mean_valor += distance

	
	print window_number, mean_valor/size, mean_valor
	window_number += 1








