import os
import numpy as np
import shutil
import sys


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

Welcome to EasyHybrid merge trajectory script.

Usage: python mergeTrajectories.py  


The trajectory list must contain all trajectory directories that will 
be compiled into a single trajectory directory.

example:
trajectories = [
'~/pDynamoWorkSpace/some_project/2_step_UmbrellaSampling/Equilibration/frame0'  ,
'~/pDynamoWorkSpace/some_project/2_step_UmbrellaSampling/Equilibration/frame1'  ,
'~/pDynamoWorkSpace/some_project/2_step_UmbrellaSampling/Equilibration/frame2'  ,
'~/pDynamoWorkSpace/some_project/2_step_UmbrellaSampling/Equilibration/frame3'  ,
'~/pDynamoWorkSpace/some_project/2_step_UmbrellaSampling/Equilibration/frame4'  ,
]

the outputFolder should contain the full path for the new 
folder that will be create

example:
outputFolder = '~/pDynamoWorkSpace/some_project/2_step_UmbrellaSampling/FullTrajectory'



'''

trajectories = [
'/home/rafa/pDynamoWorkSpace/Chaine_AM1_dPhot_Oct_14_2019/2_step_UmbrellaSampling/Equilibration/frame0'  ,
'/home/rafa/pDynamoWorkSpace/Chaine_AM1_dPhot_Oct_14_2019/2_step_UmbrellaSampling/Equilibration/frame1'  ,
'/home/rafa/pDynamoWorkSpace/Chaine_AM1_dPhot_Oct_14_2019/2_step_UmbrellaSampling/Equilibration/frame2'  ,
'/home/rafa/pDynamoWorkSpace/Chaine_AM1_dPhot_Oct_14_2019/2_step_UmbrellaSampling/Equilibration/frame3'  ,
'/home/rafa/pDynamoWorkSpace/Chaine_AM1_dPhot_Oct_14_2019/2_step_UmbrellaSampling/Equilibration/frame4'  ,
'/home/rafa/pDynamoWorkSpace/Chaine_AM1_dPhot_Oct_14_2019/2_step_UmbrellaSampling/Equilibration/frame5'  ,
'/home/rafa/pDynamoWorkSpace/Chaine_AM1_dPhot_Oct_14_2019/2_step_UmbrellaSampling/Equilibration/frame6'  ,
'/home/rafa/pDynamoWorkSpace/Chaine_AM1_dPhot_Oct_14_2019/2_step_UmbrellaSampling/Equilibration/frame7'  ,
'/home/rafa/pDynamoWorkSpace/Chaine_AM1_dPhot_Oct_14_2019/2_step_UmbrellaSampling/Equilibration/frame8'  ,
'/home/rafa/pDynamoWorkSpace/Chaine_AM1_dPhot_Oct_14_2019/2_step_UmbrellaSampling/Equilibration/frame9'  ,
'/home/rafa/pDynamoWorkSpace/Chaine_AM1_dPhot_Oct_14_2019/2_step_UmbrellaSampling/Equilibration/frame10' ,
'/home/rafa/pDynamoWorkSpace/Chaine_AM1_dPhot_Oct_14_2019/2_step_UmbrellaSampling/Equilibration/frame11' ,
'/home/rafa/pDynamoWorkSpace/Chaine_AM1_dPhot_Oct_14_2019/2_step_UmbrellaSampling/Equilibration/frame12' ,
'/home/rafa/pDynamoWorkSpace/Chaine_AM1_dPhot_Oct_14_2019/2_step_UmbrellaSampling/Equilibration/frame13' ,
'/home/rafa/pDynamoWorkSpace/Chaine_AM1_dPhot_Oct_14_2019/2_step_UmbrellaSampling/Equilibration/frame14' ,
'/home/rafa/pDynamoWorkSpace/Chaine_AM1_dPhot_Oct_14_2019/2_step_UmbrellaSampling/Equilibration/frame15' ,
'/home/rafa/pDynamoWorkSpace/Chaine_AM1_dPhot_Oct_14_2019/2_step_UmbrellaSampling/Equilibration/frame16' ,
'/home/rafa/pDynamoWorkSpace/Chaine_AM1_dPhot_Oct_14_2019/2_step_UmbrellaSampling/Equilibration/frame17' ,
'/home/rafa/pDynamoWorkSpace/Chaine_AM1_dPhot_Oct_14_2019/2_step_UmbrellaSampling/Equilibration/frame18' ,
'/home/rafa/pDynamoWorkSpace/Chaine_AM1_dPhot_Oct_14_2019/2_step_UmbrellaSampling/Equilibration/frame19' ,
'/home/rafa/pDynamoWorkSpace/Chaine_AM1_dPhot_Oct_14_2019/2_step_UmbrellaSampling/Equilibration/frame20' ,
'/home/rafa/pDynamoWorkSpace/Chaine_AM1_dPhot_Oct_14_2019/2_step_UmbrellaSampling/Equilibration/frame21' ,
'/home/rafa/pDynamoWorkSpace/Chaine_AM1_dPhot_Oct_14_2019/2_step_UmbrellaSampling/Equilibration/frame22' ,
'/home/rafa/pDynamoWorkSpace/Chaine_AM1_dPhot_Oct_14_2019/2_step_UmbrellaSampling/Equilibration/frame23' ,
'/home/rafa/pDynamoWorkSpace/Chaine_AM1_dPhot_Oct_14_2019/2_step_UmbrellaSampling/Equilibration/frame24' ,
'/home/rafa/pDynamoWorkSpace/Chaine_AM1_dPhot_Oct_14_2019/2_step_UmbrellaSampling/Equilibration/frame25' ,
'/home/rafa/pDynamoWorkSpace/Chaine_AM1_dPhot_Oct_14_2019/2_step_UmbrellaSampling/Equilibration/frame26' ,
'/home/rafa/pDynamoWorkSpace/Chaine_AM1_dPhot_Oct_14_2019/2_step_UmbrellaSampling/Equilibration/frame27' ,
'/home/rafa/pDynamoWorkSpace/Chaine_AM1_dPhot_Oct_14_2019/2_step_UmbrellaSampling/Equilibration/frame28' ,
'/home/rafa/pDynamoWorkSpace/Chaine_AM1_dPhot_Oct_14_2019/2_step_UmbrellaSampling/Equilibration/frame29' ,
'/home/rafa/pDynamoWorkSpace/Chaine_AM1_dPhot_Oct_14_2019/2_step_UmbrellaSampling/Equilibration/frame30' ,
'/home/rafa/pDynamoWorkSpace/Chaine_AM1_dPhot_Oct_14_2019/2_step_UmbrellaSampling/Equilibration/frame31' ,
]



outputFolder = '/home/rafa/pDynamoWorkSpace/Chaine_AM1_dPhot_Oct_14_2019/2_step_UmbrellaSampling/FullTrajectory'
#EasyHybrid_TMP = os.path.join(PDYNAMO_SCRATCH, '.EasyHybrid')         #
if not os.path.isdir(outputFolder):                                #
    os.mkdir(outputFolder)                                         #
    print "Creating a new folder:  %s" % outputFolder          #


frame_counter = 0

for trajectory in trajectories:
	
	files = os.listdir(trajectory)
	
	
	
	n = 0
	for _file in files:
		_file2 = _file.split('.')
		
		if _file2[-1] == 'pkl':
			pass
		else:
			files.pop(n)
		n += 1




	size  = len (files)

	for index in range(0,size):
		
		_filein  = os.path.join(trajectory, 'frame'+str(index)+'.pkl')
		_fileout = os.path.join(outputFolder, 'frame'+str(frame_counter)+'.pkl')
		print 'coping frame ', str(index), 'to', frame_counter
		shutil.copy(_filein, _fileout)
		frame_counter += 1


