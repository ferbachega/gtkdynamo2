"""
Demonstrates similarities between pcolor, pcolormesh, imshow and pcolorfast
for drawing quadrilateral grids.

"""




#filein = '/home/fernando/pDynamoWorkSpace/Ramon_AM1/11_step_Scan2D/Scan2D.log'

filein = '/home/fernando/pDynamoWorkSpace/SN2_CL_CH3Br/15_step_Scan2D/Scan2D_PM7_Nov_21_11:26:10_2015.log'





import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator
import numpy as np
from pprint import pprint 
from matplotlib import cm

import os
EasyHybrid_ROOT = os.environ.get('EasyHybrid_ROOT')
#from   EasyHybrid_ROOT.MatplotGTK.MatplotGTK          import PlotGTKWindow                                   #



def ParseProcessLogFile(log_file):
    """ Function doc """
    parameters = {
                  1: {
                     'type'  : 'line'    ,   # line / matrix
                     'title' : ''        ,   #
                     'X'     : []        ,   # X 
                     'Y'     : []        ,   # Y 
                     'xlabel': 'x label' ,   # xlabel,
                     'ylabel': 'y label' ,   # ylabel,
                     }
                 }
    parameters[1]['log_file'] = log_file
    
    log = open( log_file , "r")
    #print log
    lines = log.readlines()
    
    #print lines
    
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
        parameters[1]['xlabel'] = r1
        parameters[1]['ylabel'] = r2
        
        #print parameters
        return parameters

    if '----------------------------- EasyHybrid - MOPAC Energy Refine ---------------------------------\n' in lines:
        index = lines.index('----------------------------- EasyHybrid - MOPAC Energy Refine ---------------------------------\n')
        #print lines[index]
        #print index
        i              = 0
        j              = 0        
        matrix_lines   = []
        rcoord1_lines  = []
        rcoord2_lines  = []

        
        r1 = ''
        r2 = ''
        n_r1 = 0
        for line in lines[index: -1]:
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
                    n_r1 += 1
            except:
                pass	
            
            print n_r1
            
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
        parameters[1]['xlabel'] = r1
        parameters[1]['ylabel'] = r2
        
        #print parameters
        return parameters


parameters = ParseProcessLogFile(filein)

R1 = parameters[1]['R1']
R2 = parameters[1]['R2']
Z  = parameters[1]['matrix']
pprint 

x = R1
y = R2
g = Z


print len(x), len(y), len(g) 



levels = MaxNLocator(nbins=600).tick_values(g.min(), g.max())
cmap = cmap=cm.jet
norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)
fig, (ax1) = plt.subplots(nrows=1)


cf = ax1.pcolormesh(x, y, g, cmap=cmap, norm=norm)
CS = ax1.contour (x, y, g, 6, colors='k',)



fig.colorbar(cf, ax=ax1)
ax1.set_title('contourf with levels')

# adjust spacing between subplots so `ax1` title and `ax0` tick labels 
# don't overlap
fig.tight_layout()

plt.show()


from mpl_toolkits.mplot3d import Axes3D
import matplotlib
import numpy as np
from matplotlib import cm
from matplotlib import pyplot as plt

fig = plt.figure()

ax = fig.add_subplot(111, projection='3d')

# create supporting points in polar coordinates
ax.plot_surface(x, y, g, rstride=1, cstride=1, cmap=cm.jet)



#ax.plot_trisurf(x, y, z, cmap=cm.jet, linewidth=0.2)
#ax.set_zlim3d(0, 1)

plt.show()

'''
--------------------- Coordinate 1 - Multiple-Distance -------------------------
ATOM1                  =            134  ATOM NAME1             =              O
ATOM2*                 =           3434  ATOM NAME2             =              P
ATOM3                  =           3439  ATOM NAME3             =              O
SIGMA ATOM1/ATOM3      =        1.00000  SIGMA ATOM3/ATOM1      =       -1.00000
NWINDOWS               =             16  FORCE CONSTANT         =       4000.000
DMINIMUM               =       -0.56270  DINCREMENT             =        0.10000
--------------------------------------------------------------------------------
--------------------- Coordinate 2 - Multiple-Distance -------------------------
ATOM1                  =           3439  ATOM NAME1             =              O
ATOM2*                 =            167  ATOM NAME2             =              H
ATOM3                  =            166  ATOM NAME3             =              O
SIGMA ATOM1/ATOM3      =        1.00000  SIGMA ATOM3/ATOM1      =       -1.00000
NWINDOWS               =             16  FORCE CONSTANT         =       4000.000
DMINIMUM               =       -1.08777  DINCREMENT             =        0.10000
--------------------------------------------------------------------------------


'''







