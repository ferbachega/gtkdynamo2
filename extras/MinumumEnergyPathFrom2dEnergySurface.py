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
		  'folder'   :folder    , 
		  'log_file' :log_file  ,
		  'output'   :output
		  }
    return input_parm

def minimum_path(X):
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
			print p3
			px = px + 1
			py = py + 1
			lista.append(p3)

			frame = str(px)+ "_" +str(py)
			frame_list.append(frame)
			
		if p2 < p1 and p2 < p3:
			print p2
			px = px + 0
			py = py + 1
			lista.append(p2)

			frame = str(px)+ "_" +str(py)
			frame_list.append(frame)
			
		if p1 < p2 and p1 < p3:
			print p1
			px = px + 1
			py = py + 0
			lista.append(p1)

			frame = str(px)+ "_" +str(py)
			frame_list.append(frame)
			
			
		if p1 == 1000000000000000 and p2 == 1000000000000000 and p3 == 1000000000000000:
			break
	return lista , frame_list

def outputLogBuilder (log_file     = None,
		      folder       = None,
		      outputfolder = None,
		      energy       = None,
		      frame_list   = None
		      ):
    """ Function doc """
    
    text   = ''''''
    string = ''
    
    
    
    
    
    
    

print sys.argv
args = sys.argv
inputs = parser_tags (args)



if '-h' in args or '-H' in args or inputs['folder'] == None or inputs['log_file'] == None or inputs['output'] == None:
    print text

else:
    data  = log_parser (inputs['log_file'])
    #pprint(data)
    data =  data[1]
    
    print 'energy model ', data['energy_model']
    z = data['matrix']
    lista , frame_list = minimum_path(z)
    print lista
    print frame_list

    Files    = os.listdir(inputs['folder']) 
    
    
    if not os.path.isdir(inputs['output']):
	os.mkdir(inputs['output'])
	#print "Temporary files directory:  %s" % EasyHybrid_TMP
    
    print  output_header
    print 'input logFile: ', inputs['log_file']
    print 'input folder: ', inputs['folder']
    print 'output folder: ', inputs['output']
    n = 0
    for i in frame_list:
	if 'frame_' + i + '.pkl' in Files:
	    frame  = 'frame_' + i + '.pkl'
	    frame2 = os.path.join(inputs['folder'],frame)
	    frameout = os.path.join(inputs['output'],'frame'+str(n)+'.pkl')
	    shutil.copy(frame2, frameout)
	    
	    
	    text = "%15i    %15s    %15s       %15.9f"   % (n, 'frame'+str(n)+'.pkl',  frame,   lista[n]     )
	    
	    print text
	    #'frame'+str(n)+'.pkl', frame , lista[n]
	    n += 1
	    #print 'frame_' + i + '.pkl'
    
    
    '''
    traj  = Trajectory()
    traj.import_frames_from_folder(InputTrajectory = inputs['log_file'],
				    trajectoryType = inputs['type'], 
				    fileType       = 'pkl')


    traj.Summary()
    traj.save_edited_trajectory(
				outputfolder =  inputs['out_file'], 
				i_offset     =  inputs['i_offset'], 
				j_offset     =  inputs['j_offset'], 
				fileType     = 'pkl')    


    EasyHybrid_TMP = os.path.join(PDYNAMO_SCRATCH, '.EasyHybrid')
    if not os.path.isdir(EasyHybrid_TMP):
	os.mkdir(EasyHybrid_TMP)
	print "Temporary files directory:  %s" % EasyHybrid_TMP
    '''


