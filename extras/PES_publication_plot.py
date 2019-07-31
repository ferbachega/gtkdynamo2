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

Usage: python PES_publication_plot.py  -i inputfile <options>



Options:
                   -h , -H   help 
                   
                   -cmap color map (string), default is 'jet'
                        see the options:
                        https://matplotlib.org/examples/color/colormaps_reference.html
                   
                   -vmin (int), default is 'energy.min'  
                   
                   -vmax (int), default is 'energy.max' 
                   
                   -shading (string or False), default is = 'gouraud'
                   
                   
                   -----------  contour  ------------
                   
                   -lspacing   (int), default is 10
                   -lcolor     (char), default is 'k'
                   -fontsize   (int), default is 14
                   
                   
                   ----------------------------------
                   
                   inline=1, fontsize=14, fmt='%1.1f',colors='k'
'''



import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator
import matplotlib.colors as colors
import numpy as np
from pprint import pprint


import sys

print sys.argv
#i, col_title in enumerate(["Name", "Age", "Profession"])

args = sys.argv




def parser_tags (args):
	""" Function doc """
	

	
	if '-vmax' in args:
		index = args.index('-vmax')
		vmax  = int(args[index+1])
	else:
		vmax  = 200

	if '-vmin' in args:
		index = args.index('-vmin')
		vmin  = int(args[index+1])
	else:
		vmin  = 0

	if '-cmap' in args:
		index = args.index('-cmap')
		cmap  = args[index+1]
	else:
		cmap  = 'jet'




	if '-shading' in args:
		index =  args.index('-shading')
		shading = args[index+1]
	else:
		shading  = 'gouraud'



	if '-lspacing' in args:
		index = args.index('-lspacing')
		lspacing = int(args[index+1])
	else:
		lspacing = 20
	
	if '-lcolor' in args:
		index = args.index('-lcolor')
		lcolor= args[index+1]
	else:
		lcolor  =  'k'
	
	
	if '-fontsize' in args:
		index = args.index('-fontsize')
		fontsize = int(args[index+1])
	else:
		fontsize  =  14
	
	
	
	
	if '-i' in args:
		index = args.index('-i')
		log_file  = args[index+1]
	else:
		log_file  = None
	
	
	input_parm = {'vmax'     :vmax    , 
				  'vmin'     :vmin    , 
				  'cmap'     :cmap    , 
				  'shading'  :shading , 
				  'lspacing' :lspacing, 
				  'lcolor'   :lcolor  , 
				  'fontsize' :fontsize,
				  'log_file' :log_file
				  } 
	
	
	return input_parm


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
                            
			    r1 = r1 + 'd ' +atom[6] + '(' +atom[2] + ') - '
			    #r1 = r1 +atom[2] + '(' +atom[6] + ')'

                        
                        if atom[0][-1] == '2':
			    parameters[1]['c1_ATOM2_id'  ] = atom[2]   
			    parameters[1]['c1_ATOM2_name'] = atom[6]     
                            r1 = r1 +atom[6] + '(' +atom[2] + ')'


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
			    
                        
                        if atom[0][-1] == '2' or atom[0][-1] == '*':
			    parameters[1]['c1_ATOM2_id'  ] = atom[2]   
			    parameters[1]['c1_ATOM2_name'] = atom[6]     
                            r1 = r1 + " - " + atom[6] + '(' +atom[2] + ')*' + " - "
			    #r1 = r1 +atom[6] + '_' +atom[2]+ ' ' +  'd ' +atom[6] + '_' +atom[2]+ ' '

                        if atom[0][-1] == '3':
			    parameters[1]['c1_ATOM3_id'  ] = atom[2]   
			    parameters[1]['c1_ATOM3_name'] = atom[6]     
                            r1 = r1 +atom[6] + '(' +atom[2] + ')'
			    #r1 = r1 +atom[6] + '_' +atom[2]+ ' '
            
            
            
            
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

                        
                        if atom[0][-1] == '2':
			    parameters[1]['c2_ATOM2_id'  ] = atom[2]   
			    parameters[1]['c2_ATOM2_name'] = atom[6]     
                            r2 = r2 +atom[6] + '(' +atom[2] + ')'
			
			
			
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

                        
                        if atom[0][-1] == '2' or atom[0][-1] == '*':
			    parameters[1]['c2_ATOM2_id'  ] = atom[2]   
			    parameters[1]['c2_ATOM2_name'] = atom[6]     
                            r2 = r2 + " - " + atom[6] + '(' +atom[2] + ')*' + " - "

                        if atom[0][-1] == '3':
			    parameters[1]['c2_ATOM3_id'  ] = atom[2]   
			    parameters[1]['c2_ATOM3_name'] = atom[6]     
                            r2 = r2 +atom[6] + '(' +atom[2] + ')'
            
            
            
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




input_parm = parser_tags(args)

print input_parm

vmax     =input_parm['vmax'    ]
vmin     =input_parm['vmin'    ]
cmap     =input_parm['cmap'    ]
shading  =input_parm['shading' ]
lspacing =input_parm['lspacing']
lcolor   =input_parm['lcolor'  ]
fontsize =input_parm['fontsize']
log_file =input_parm['log_file']





if '-h' in args or '-H' in args or log_file == None:
    print text



else:
    '''
    cmaps = [('Perceptually Uniform Sequential', [
			    'viridis', 'plasma', 'inferno', 'magma']),
		     ('Sequential', [
			    'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
			    'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
			    'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn']),
		     ('Sequential (2)', [
			    'binary', 'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink',
			    'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia',
			    'hot', 'afmhot', 'gist_heat', 'copper']),
		     ('Diverging', [
			    'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu',
			    'RdYlBu', 'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic']),
		     ('Qualitative', [
			    'Pastel1', 'Pastel2', 'Paired', 'Accent',
			    'Dark2', 'Set1', 'Set2', 'Set3',
			    'tab10', 'tab20', 'tab20b', 'tab20c']),
		     ('Miscellaneous', [
			    'flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern',
			    'gnuplot', 'gnuplot2', 'CMRmap', 'cubehelix', 'brg', 'hsv',
			    'gist_rainbow', 'rainbow', 'jet', 'nipy_spectral', 'gist_ncar'])]


    '''







    #cmap     = 'jet'#'nipy_spectral'#'copper'#'PuBuGn'#'inferno'#'jet'
    #vmin     = None
    #vmax     = 250#None
    #lspacing = 20
    #lcolor   = 'k'
    #fontsize = 14



    data  = log_parser (log_file)
    data =  data[1]





    z = data['matrix']
    r1 = []
    for line in data['R1']:
	    if line == []:
		    pass
	    else:
		    #print line[0]
		    if line[0]:
			    r1.append(line[0])



    z = data['matrix']
    x = data['R2'][0]
    y = np.array(r1)


    if vmin == None:
	    vmin=z.min()
    if vmax == None:
	    vmax=z.max()

    print 'z', len(z) , type(z)
    print 'y', len(y) , type(y)
    print 'x', len(x) , type(x)#


    print z
    print y
    print x

    print 'c1_ATOM1_id'  , data['c1_ATOM1_id'  ]
    print 'c1_ATOM1_name', data['c1_ATOM1_name']



    levels = MaxNLocator(nbins=100).tick_values(z.min(), z.max())
    # pick the desired colormap, sensible levels, and define a normalization
    # instance which takes data values and translates those into levels.


    cmap = plt.get_cmap(cmap)


    norm = BoundaryNorm(levels, 
					    ncolors=cmap.N, 
					    clip=True)


    #norm= colors.LogNorm(vmin=z.min(), vmax=z.max())
    norm= colors.PowerNorm(gamma=1./2.)
    #fig, (ax0, ax1) = plt.subplots(nrows=2)
    norm =  colors.Normalize(vmin=z.min(), vmax=z.max())
    norm =  colors.Normalize(vmin=vmin, vmax=vmax)



    fig, (ax0) = plt.subplots(nrows=1)


    im = ax0.pcolormesh(x, y, z, cmap=cmap, norm=norm, shading = shading)

    #im = ax0.imshow(x,y,z, interpolation = 'bicubic')

    #c = ax0.contour(  colors='black', alpha=0.3, linewidths=2)

    am = ax0.contour(x,y,z,lspacing, colors=lcolor)
    ax0.clabel(am, inline=1, fontsize=fontsize, fmt='%1.1f',colors=lcolor)

    #x,y,z, levels=numpy.linspace(-5.0, 0.0, 50), cmap='Blues_r'
    #im = ax0.contourf(x,y,z, cmap='rainbow')

    #ax.imshow(matrix, interpolation = 'bicubic') 

    FontSize = 20

    # Set the tick labels font
    axis_font = {'fontname':'Arial', 'size':'14'}
    for tick in (ax0.xaxis.get_major_ticks()):
	    tick.label.set_fontname('Arial')
	    tick.label.set_fontsize(FontSize)

    for tick in (ax0.yaxis.get_major_ticks()):
	    tick.label.set_fontname('Arial')
	    tick.label.set_fontsize(FontSize) 

    coord1 = data['xlabel']
    coord2 = data['ylabel']
    ax0.set_xlabel(coord2, **axis_font)
    ax0.set_ylabel(coord1, **axis_font)



    #ax0.set_ylabel(r'$\sum_{i=0}^\infty x_i$')

    '''
    cmap     = 'jet'
    vmin     = None
    vmax     = None
    shading  = 'gouraud'
    lspacing = 10
    lcolor   = 'k'
    fontsize = 14
    '''



    cbar = fig.colorbar(im, ax=ax0)
    cbar.ax.tick_params(labelsize=FontSize)
    #ax0.set_title('pcolormesh with levels')

    '''
    # contours are *point* based plots, so convert our bound into point
    # centers
    cf = ax1.contourf(x[:-1, :-1] + dx/2.,
				      y[:-1, :-1] + dy/2., z, levels=levels,
				      cmap=cmap)
    fig.colorbar(cf, ax=ax1)
    ax1.set_title('contourf with levels')
    '''
    # adjust spacing between subplots so `ax1` title and `ax0` tick labels
    # don't overlap
    fig.tight_layout()

    plt.show()
