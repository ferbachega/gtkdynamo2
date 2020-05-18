#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  logParser.py
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
def log_parser (log_file):
    """ Function doc """
    parameters = {
                  1: {
                     'type'          : 'line'    ,   # line / matrix
                     'title'         : ''        ,   #
                     'X'             : []        ,   # X 
                     'Y'             : []        ,   # Y 
                     'xlabel'        : 'x label' ,   # xlabel,
                     'ylabel'        : 'y label' ,   # ylabel,
                     'energy_model'  : 'UNK'     ,
                     
                     
                     'c1_ATOM1_id'   : None      ,
                     'c1_ATOM2_id'   : None      ,
                     'c1_ATOM3_id'   : None      ,
                                     
                     'c1_ATOM1_name' : None      ,
                     'c1_ATOM2_name' : None      ,
                     'c1_ATOM3_name' : None      ,
                                     
                     'c2_ATOM1_id'   : None      ,
                     'c2_ATOM2_id'   : None      ,
                     'c2_ATOM3_id'   : None      ,
                                     
                     'c2_ATOM1_name' : None      ,
                     'c2_ATOM2_name' : None      ,
                     'c2_ATOM3_name' : None      ,
                     
                     
                     }
                 }
    
    parameters[1]['log_file'] = log_file
    
    #summary_arameters = ParseSummaryLogFile(log_file)
    #parameters[1]['energy_model'] = summary_arameters['Energy Model']
    
    log = open( log_file , "r")
    lines = log.readlines()

    for line in lines:
	if 'Summary for Energy Model' in line:
	    #print line
	    line2 = line.split('"')
	    parameters['energy_model'] = line2[1]

    interact = []
    Function = []
    RMS_Grad = []
    Mac_Grad = []
    RMS_disp = []
    MAS_Disp = []
    
    if '                              GTKDynamo SCAN2D\n' in lines:
        index = lines.index('                              GTKDynamo SCAN2D\n')
        #print lines[index]
        #print index
        i             =   0
        j             =   0        
        matrix_lines  = []
        r1 = ''
        r2 = ''
        for line in lines[index: -1]:
            if line == '----------------------- Coordinate 1 - Simple-Distance -------------------------\n':
                index2 = lines.index('----------------------- Coordinate 1 - Simple-Distance -------------------------\n')
                for atomLine in lines[index2+1 :index2+4]:
                    atom = atomLine.split()
                    if atom[0][0:4] == 'ATOM':
                        
                        if atom[0][-1] == '2':
                            r1 = r1 +atom[2] + '(' +atom[6] + ')'
                        else:
                            r1 = r1 +atom[2] + '(' +atom[6] + ')' + " - "
                        #print r1


            if line == '--------------------- Coordinate 1 - Multiple-Distance -------------------------\n':
                index2 = lines.index('--------------------- Coordinate 1 - Multiple-Distance -------------------------\n')
                for atomLine in lines[index2+1 :index2+4]:
                    atom = atomLine.split()
                    if atom[0][0:4] == 'ATOM':
                        if atom[0][-1] == '*':
                            r1 = r1 + " - " + atom[2] + '(' +atom[6] + ')*' + " - "
                        else:
                            r1 = r1 +atom[2] + '(' +atom[6] + ')'
                        #print r1

            
            
            
            
            
            if line == '----------------------- Coordinate 2 - Simple-Distance -------------------------\n':
                index2 = lines.index('----------------------- Coordinate 2 - Simple-Distance -------------------------\n')
                for atomLine in lines[index2+1 :index2+4]:
                    atom = atomLine.split()
                    if atom[0][0:4] == 'ATOM':
                        if atom[0][-1] == '2':
                            r2 = r2 +atom[2] + '(' +atom[6] + ')'
                        else:
                            r2 = r2 +atom[2] + '(' +atom[6] + ')' + " - "
                        #print r2
            
            if line == '--------------------- Coordinate 2 - Multiple-Distance -------------------------\n':
                index2 = lines.index('--------------------- Coordinate 2 - Multiple-Distance -------------------------\n')
                for atomLine in lines[index2+1 :index2+4]:
                    atom = atomLine.split()
                    if atom[0][0:4] == 'ATOM':
                        if atom[0][-1] == '*':
                            r2 = r2 + " - " + atom[2] + '(' +atom[6] + ')*' + " - "
                        else:
                            r2 = r2 +atom[2] + '(' +atom[6] + ')'
                        #print r2

            
            
            
            #print line
            try:
                linex = line.split()
                if linex[0] == "MATRIX2":
                    #print linex
                    i = len(linex) - 1
                    j = j + 1
                    mline = []
                    
                    for item in linex[1:-1]:
                        #print item
                        mline.append(float(item))
                    #print mline
                    
                    matrix_lines.append(mline)
                    
            except:
                pass	
        import numpy as np
        X = np.array(matrix_lines)

                
        parameters[1]['type'  ] = 'matrix'
        parameters[1]['title' ] = 'SCAN2D'
        parameters[1]['matrix'] =  X
        parameters[1]['xlabel'] = r1
        parameters[1]['ylabel'] = r2
        #print parameters
        return parameters

    if '                              EasyHybrid SCAN2D\n' in lines:
        index = lines.index('                              EasyHybrid SCAN2D\n')
        #print lines[index]
        #print index
        i              = 0
        j              = 0        
        matrix_lines   = []
        rcoord1_lines  = []
        rcoord2_lines  = []

        
        r1 = r'Coordinate 1: '
        r2 = r'Coordinate 2: '
        for line in lines[index: -1]:
            if line == '----------------------- Coordinate 1 - Simple-Distance -------------------------\n':
                index2 = lines.index('----------------------- Coordinate 1 - Simple-Distance -------------------------\n')
                for atomLine in lines[index2+1 :index2+4]:
                    atom = atomLine.split()
                    if atom[0][0:4] == 'ATOM':
                        #r1 = r1 
                        
			if atom[0][-1] == '1':
			    parameters[1]['c1_ATOM1_id'  ] = atom[2]   
			    parameters[1]['c1_ATOM1_name'] = atom[6]     
                            c1_ATOM1_id   = atom[2]
			    c1_ATOM1_name = atom[6]
			    
			    r1 = r1 + 'd ' +atom[6] + '(' +atom[2] + ') - '
			    #r1 = r1 +atom[2] + '(' +atom[6] + ')'

                        
                        if atom[0][-1] == '2':
			    parameters[1]['c1_ATOM2_id'  ] = atom[2]   
			    parameters[1]['c1_ATOM2_name'] = atom[6]     
                            r1 = r1 +atom[6] + '(' +atom[2] + ')'
			    
			    c1_ATOM2_id   = atom[2]
			    c1_ATOM2_name = atom[6]


		#c1_ATOM1_id    =  data['c1_ATOM1_id'  ]
		#c1_ATOM1_name  =  data['c1_ATOM1_name']
		c1_ATOM1_name  =  c1_ATOM1_name+'_{'+c1_ATOM1_id+'}'
		#c1_ATOM2_id    =  data['c1_ATOM2_id'  ]
		#c1_ATOM2_name  =  data['c1_ATOM2_name']	
		c1_ATOM2_name  =  c1_ATOM2_name+'_{'+c1_ATOM2_id+'}'
		rcoord1 =   r'$d(' + c1_ATOM1_name + '-' + c1_ATOM2_name+')$' 	    
		    

            if line == '--------------------- Coordinate 1 - Multiple-Distance -------------------------\n':
                index2 = lines.index('--------------------- Coordinate 1 - Multiple-Distance -------------------------\n')
                for atomLine in lines[index2+1 :index2+4]:
                    atom = atomLine.split()
                    if atom[0][0:4] == 'ATOM':
                        #if atom[0][-1] == '*':
                        #    r1 = r1 + " - " + atom[2] + '(' +atom[6] + ')*' + " - "
                        #else:
                        #    r1 = r1 +atom[2] + '(' +atom[6] + ')'
                        #print r1

                        if atom[0][-1] == '1':
			    parameters[1]['c1_ATOM1_id'  ] = atom[2]   
			    parameters[1]['c1_ATOM1_name'] = atom[6]     
                            r1 = r1 +atom[6] + '(' +atom[2] + ')'
			    #r'$\alpha_i > \beta_i$', fontsize=20
			    #r1 = r1 + 'd '+ atom[6] + '_' +atom[2]+ ' '
			    c1_ATOM1_id   = atom[2]
			    c1_ATOM1_name = atom[6]
                        
                        if atom[0][-1] == '2' or atom[0][-1] == '*':
			    parameters[1]['c1_ATOM2_id'  ] = atom[2]   
			    parameters[1]['c1_ATOM2_name'] = atom[6]     
                            r1 = r1 + " - " + atom[6] + '(' +atom[2] + ')*' + " - "
			    #r1 = r1 +atom[6] + '_' +atom[2]+ ' ' +  'd ' +atom[6] + '_' +atom[2]+ ' '
			    c1_ATOM2_id    = atom[2]
                            c1_ATOM2_name  = atom[6]



                        if atom[0][-1] == '3':
			    parameters[1]['c1_ATOM3_id'  ] = atom[2]   
			    parameters[1]['c1_ATOM3_name'] = atom[6]     
                            r1 = r1 +atom[6] + '(' +atom[2] + ')'
			    #r1 = r1 +atom[6] + '_' +atom[2]+ ' '
			    c1_ATOM3_id    =  atom[2]  
			    c1_ATOM3_name  =  atom[6]  
			    

		#c1_ATOM1_id    =  data['c1_ATOM1_id'  ]
		#c1_ATOM1_name  =  data['c1_ATOM1_name']
		c1_ATOM1_name  =  c1_ATOM1_name+'_{'+c1_ATOM1_id+'}'
		#c1_ATOM2_id    =  data['c1_ATOM2_id'  ]
		#c1_ATOM2_name  =  data['c1_ATOM2_name']	
		c1_ATOM2_name  =  c1_ATOM2_name+'_{'+c1_ATOM2_id+'}'
		#c1_ATOM3_id    =  data['c1_ATOM3_id'  ]
		#c1_ATOM3_name  =  data['c1_ATOM3_name']	
		c1_ATOM3_name  =  c1_ATOM3_name+'_{'+c1_ATOM3_id+'}'
		rcoord1 =   r'$d(' + c1_ATOM1_name + '-' + c1_ATOM2_name+')' +'-'+ 'd('+c1_ATOM2_name+ '-' + c1_ATOM3_name+')$'








            
            
            
            if line == '----------------------- Coordinate 2 - Simple-Distance -------------------------\n':
                index2 = lines.index('----------------------- Coordinate 2 - Simple-Distance -------------------------\n')
                for atomLine in lines[index2+1 :index2+4]:
                    atom = atomLine.split()
                    if atom[0][0:4] == 'ATOM':
                        #if atom[0][-1] == '2':
                        #    r2 = r2 +atom[2] + '(' +atom[6] + ')'
                        #else:
                        #    r2 = r2 +atom[2] + '(' +atom[6] + ')' + " - "
                        #print r2
			if atom[0][-1] == '1':
			    parameters[1]['c2_ATOM1_id'  ] = atom[2]   
			    parameters[1]['c2_ATOM1_name'] = atom[6]     
                            r2 = r2 + 'd '+ atom[6] + '(' +atom[2] + ') - '
			    c2_ATOM1_id    = atom[2]
			    c2_ATOM1_name  = atom[6]



                        
                        if atom[0][-1] == '2':
			    parameters[1]['c2_ATOM2_id'  ] = atom[2]   
			    parameters[1]['c2_ATOM2_name'] = atom[6]     
                            r2 = r2 +atom[6] + '(' +atom[2] + ')'
			    c2_ATOM2_id    = atom[2]
			    c2_ATOM2_name  = atom[6]
			
		#c2_ATOM1_id    =  data['c2_ATOM1_id'  ]
		#c2_ATOM1_name  =  data['c2_ATOM1_name']
		c2_ATOM1_name  =  c2_ATOM1_name+'_{'+c2_ATOM1_id+'}'
		#c2_ATOM2_id    =  data['c2_ATOM2_id'  ]
		#c2_ATOM2_name  =  data['c2_ATOM2_name']	
		c2_ATOM2_name  =  c2_ATOM2_name+'_{'+c2_ATOM2_id+'}'
		rcoord2 =   r'$d(' + c2_ATOM1_name + '-' + c2_ATOM2_name+')$'

			
            if line == '--------------------- Coordinate 2 - Multiple-Distance -------------------------\n':
                index2 = lines.index('--------------------- Coordinate 2 - Multiple-Distance -------------------------\n')
                for atomLine in lines[index2+1 :index2+4]:
                    atom = atomLine.split()
                    if atom[0][0:4] == 'ATOM':
                        #if atom[0][-1] == '*':
                        #    r2 = r2 + " - " + atom[2] + '(' +atom[6] + ')*' + " - "
                        #else:
                        #    r2 = r2 +atom[2] + '(' +atom[6] + ')'
                        #print r2
                        if atom[0][-1] == '1':
			    parameters[1]['c2_ATOM1_id'  ] = atom[2]   
			    parameters[1]['c2_ATOM1_name'] = atom[6]     
                            r2 = r2 +atom[6] + '(' +atom[2] + ')'
			    c2_ATOM1_id    = atom[2] 
                            c2_ATOM1_name  = atom[6] 
                        
                        if atom[0][-1] == '2' or atom[0][-1] == '*':
			    parameters[1]['c2_ATOM2_id'  ] = atom[2]   
			    parameters[1]['c2_ATOM2_name'] = atom[6]     
                            r2 = r2 + " - " + atom[6] + '(' +atom[2] + ')*' + " - "
			    c2_ATOM2_id    = atom[2]
			    c2_ATOM2_name  = atom[6]

                        if atom[0][-1] == '3':
			    parameters[1]['c2_ATOM3_id'  ] = atom[2]   
			    parameters[1]['c2_ATOM3_name'] = atom[6]     
                            r2 = r2 +atom[6] + '(' +atom[2] + ')'
			    c2_ATOM3_id    = atom[2] 
                            c2_ATOM3_name  = atom[6] 


		#c2_ATOM1_id    =  data['c2_ATOM1_id'  ]
		#c2_ATOM1_name  =  data['c2_ATOM1_name']
		c2_ATOM1_name  =  c2_ATOM1_name+'_{'+c2_ATOM1_id+'}'
		#c2_ATOM2_id    =  data['c2_ATOM2_id'  ]
		#c2_ATOM2_name  =  data['c2_ATOM2_name']	
		c2_ATOM2_name  =  c2_ATOM2_name+'_{'+c2_ATOM2_id+'}'
		#c2_ATOM3_id    =  data['c2_ATOM3_id'  ]
		#c2_ATOM3_name  =  data['c2_ATOM3_name']	
		c2_ATOM3_name  =  c2_ATOM3_name+'_{'+c2_ATOM3_id+'}'
		rcoord2 =   r'$d(' + c2_ATOM1_name + '-' + c2_ATOM2_name+')' +'-'+ 'd('+c2_ATOM2_name+ '-' + c2_ATOM3_name+')$'





            
            
            #print line
            try:
                linex = line.split()
                if linex[0] == "MATRIX2":
                    #print linex
                    i = len(linex) - 1
                    j = j + 1
                    mline = []
                    
                    for item in linex:#[1:-1]:
                        #print item
                        try:
                            mline.append(float(item))
                        except:
                            pass
                            
                    #print mline
                    
                    matrix_lines.append(mline)
                    
            except:
                pass
                
            

        #rcoord1_lines  = []
        #rcoord2_lines  = []

            try:
                linex = line.split()
                if linex[0] == "RCOORD1":
                    i = len(linex) - 1
                    j = j + 1
                    mline = []
                    
                    for item in linex:#[1:-1]:
                        try:
                            mline.append(float(item))
                        except:
                            pass
                    rcoord1_lines.append(mline)
            except:
                pass	
            
            try:
                linex = line.split()
                if linex[0] == "RCOORD2":
                    i = len(linex) - 1
                    j = j + 1
                    mline = []
                    
                    for item in linex:#[1:-1]:
                        try:
                            mline.append(float(item))
                        except:
                            pass
                    rcoord2_lines.append(mline)
            except:
                pass


        import numpy as np

        X  = np.array(matrix_lines)
        R1 = np.array(rcoord1_lines)
        R2 = np.array(rcoord2_lines)

                
        parameters[1]['type'  ] = 'matrix'
        parameters[1]['title' ] = 'SCAN2D'
        parameters[1]['matrix'] =  X
        
        parameters[1]['R1'    ] = R1
        parameters[1]['R2'    ] = R2
        #parameters[1]['xlabel'] = r1
        #parameters[1]['ylabel'] = r2
        parameters[1]['xlabel'] = rcoord1
	parameters[1]['ylabel'] = rcoord2
	
        #print parameters
        return parameters



