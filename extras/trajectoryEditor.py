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

Welcome to EasyHybrid PES logfile file processor.

Usage: python trajectoryEditor.py  -i inputfolder <options>  -o outfolder



Options:
	-i          =  input (folder)  
	-type       = 1D / 2D  
	-i_offset   =  <int>  eg:2      
	-j_offset   =  <int>  eg:2     
	-invert     =  false
	-o          =  output (folder)
	
	-h          =  help
'''




class Trajectory:
    """ Class doc """
    
    def __init__ (self):
        """ Class initialiser """
	self.Files    = None
        self.basename = 'frame'
	self.i_table = []
	self.j_table = []
	self.i_max   = 0
	self.j_max   = 0
	self.InputTrajectory = ''
	self.energy_matrix   = None
	#self.REACTION_COORD1 = None
	#self.REACTION_COORD2 = None

    def import_frames_from_folder(self, InputTrajectory = '', trajectoryType = '1D', fileType = 'pkl', invert = False):
        
	self.InputTrajectory = InputTrajectory

	self.Files = os.listdir(InputTrajectory)             
	self.trajectoryType = trajectoryType
	if trajectoryType == '1D':
	    for File in self.Files:                            
		name  = File.replace('frame', '')
		name  = name.split('.')               
		
		if name[-1] ==  fileType:               
		    name = name[0].split('_')
		    i    = int(name[-1])
		    self.i_table.append(i)                                                                  
	    #---------------------------------------------------------#
	    self.i_table  = np.array(self.i_table)
	    self.i_max = self.i_table.max()
	    #---------------------------------------------------------#
	
	
	
	if trajectoryType == '2D':
	    for File in self.Files:                            
		name  = File.replace('frame', '')
		name  = name.split('.')  	    
    
		if name[-1] ==  fileType:              
		    name = name[0].split('_')
		    j     = int(name[-1])
		    i     = int(name[-2])
		    self.i_table.append(i)                                                                  
		    self.j_table.append(j)  
	    
	    #---------------------------------------------------------#
	    self.i_table  = np.array(self.i_table)
	    self.j_table  = np.array(self.j_table)

	    self.i_max = self.i_table.max()
	    self.j_max = self.j_table.max()
	    #---------------------------------------------------------#
    
    def save_edited_trajectory(self                 , 
			       outputfolder = ''    , 
			       i_offset     = 2     , 
			       j_offset     = 2     , 
			       fileType    = 'pkl'):
	
	
	if not os.path.isdir(outputfolder):
	    os.mkdir(outputfolder)
	    print "Creating a new folder:  %s" % outputfolder
	
	
	if self.trajectoryType == '1D':
	    new_i = 0
	    
	    for i in range(0, self.i_max, i_offset):
		
		filein  = 'frame'+str(i)     +'.pkl'
		fileout = 'frame'+str(new_i) +'.pkl'  		
		
		_filein  = os.path.join(self.InputTrajectory, filein )
		_fileout = os.path.join(outputfolder        , fileout)

		shutil.copy(_filein, _fileout)
		
		new_i += 1
	
	if self.trajectoryType == '2D':
	    new_i = 0
	    new_j = 0

	    
	    for i in range(0, self.i_max, i_offset):
		
		new_j = 0

		for j in range(0, self.j_max, j_offset):
		    filein  = 'frame_'+str(i)     +'_'+ str(j)     +'.pkl'
		    fileout = 'frame_'+str(new_i) +'_'+ str(new_j) +'.pkl'  		
		    
		    _filein  = os.path.join(self.InputTrajectory, filein )
		    _fileout = os.path.join(outputfolder        , fileout)

		    shutil.copy(_filein, _fileout)
		    new_j += 1
		new_i += 1
		
		
		    
    def Summary (self):
	""" Function doc """
	print 'InputTrajectory',self.InputTrajectory
	print 'Files  '        ,  self.Files  
	print 'i_table'        ,  self.i_table
	print 'j_table'        ,  self.j_table
	print 'i_max  '        ,  self.i_max  
	print 'j_max  '        ,  self.j_max  
	print 'basename'       ,  self.basename
	
	
print sys.argv
args = sys.argv
	
def parser_tags (args):
    """ Function doc """
    if '-i' in args:
	index = args.index('-i')
	log_file  = args[index+1]
    else:
	log_file  = None

   
    if '-o' in args:
	index = args.index('-o')
	out_file  = args[index+1]
    else:
	out_file  = None

    
    if '-type' in args:
	index = args.index('-type')
	_type = args[index+1]
    else:
	_type = '2D'

    
    
    if '-i_offset' in args:
	index    = args.index('-i_offset')
	i_offset = int(args[index+1])
    else:
	i_offset = 2



    if '-j_offset' in args:
	index = args.index('-j_offset')
	j_offset  = int(args[index+1])
    else:
	j_offset  = 2


    
    if '-invert' in args:
	index = args.index('-invert')
	invert  = args[index+1]
    else:
	invert  = False



    input_parm = {'type'     :_type     , 
		  'i_offset' :i_offset  , 
		  'j_offset' :j_offset  , 
		  'invert'   :invert    , 
		  'log_file' :log_file  ,
		  'out_file' :out_file
		  } 
   
    return input_parm


inputs = parser_tags (args)

if '-h' in args or '-H' in args or inputs['log_file'] == None or inputs['out_file'] == None:
    print text

else:
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



	
'''
traj  = Trajectory()
traj.import_frames_from_folder(InputTrajectory = '/home/fernando/pDynamoWorkSpace/SN2_CL_CH3Br/12_step_Scan', 
				trajectoryType = '1D', 
				      fileType = 'pkl')

traj.Summary()
traj.save_edited_trajectory(
			    outputfolder = '/home/fernando/Desktop/teste1D', 
			    i_offset     = 2    , 
			    fileType     = 'pkl')
'''

'''
traj  = Trajectory()
traj.import_frames_from_folder(InputTrajectory = '/home/fernando/pDynamoWorkSpace/SN2_CL_CH3Br/14_step_Scan2D', 
				trajectoryType = '2D', 
				     fileType = 'pkl')

traj.Summary()
traj.save_edited_trajectory(
			    outputfolder = '/home/fernando/Desktop/teste2D', 
			    i_offset     = 2     , 
			    j_offset     = 2     , 
			    fileType    = 'pkl')
'''

'''
traj  = Trajectory()
traj.import_frames_from_folder(InputTrajectory = '/home/fernando/pDynamoWorkSpace/AKmm_Oct_01_2017/32_step_Scan2D', 
				trajectoryType = '2D', 
				     fileType = 'pkl')

traj.Summary()
traj.save_edited_trajectory(
			    outputfolder = '/home/fernando/pDynamoWorkSpace/MtDS_29_Nov_2017/19_edited', 
			    i_offset     = 3     , 
			    j_offset     = 3     , 
			    fileType    = 'pkl')
#'''


'''
traj  = Trajectory()
traj.import_frames_from_folder(InputTrajectory = '/home/farminfo/pDynamoWorkSpace/MtSK_QMMM_Artigo/18_step_Scan2D_edited',
				trajectoryType = '2D', 
				     fileType = 'pkl')






traj.Summary()
traj.save_edited_trajectory(
			    outputfolder = '/home/farminfo/pDynamoWorkSpace/MtSK_QMMM_Artigo/18_step_Scan2D_edited_02', 
			    i_offset     = 2     , 
			    j_offset     = 2     , 
			    fileType    = 'pkl')

#'''

##'''
#traj  = Trajectory()
#traj.import_frames_from_folder(InputTrajectory = '/home/rafa/pDynamoWorkSpace/AK/6_step_Scan2D',
#				trajectoryType = '2D', 
#				     fileType = 'pkl')
#
#
#traj.Summary()
#traj.save_edited_trajectory(
#			    outputfolder = '/home/rafa/pDynamoWorkSpace/AK/6_step_Scan2D_edited', 
#			    i_offset     = 3     , 
#			    j_offset     = 2     , 
#			    fileType    = 'pkl')
#
#'''
