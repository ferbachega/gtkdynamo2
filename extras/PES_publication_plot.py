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
                   
                   -idx   Shows the reaction coordinate as a fuctions of frame indexes
                   
                   -cmap color map (string), default is 'jet'
                        see the options:
                        https://matplotlib.org/examples/color/colormaps_reference.html
                   
                   -vmin (int), default is 'energy.min'  
                   
                   -vmax (int), default is 'energy.max' 
                   
                   -shading (string or False), default is = 'gouraud'
                   
                   -axisfontsize (int), default is 14
                   
                   -----------  contour  ------------
                   
                   -lspacing   (int), default is 10
                   -lcolor     (char), default is 'k'
                   -fontsize   (int), default is 14
                   -fmt        (str), default is '%1.1f'
                   
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

from logParser import log_parser

import sys

print sys.argv
#i, col_title in enumerate(["Name", "Age", "Profession"])

args = sys.argv







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

















def parser_tags (args):
	""" Function doc """
	
	if '-idx' in args:
		idx  = True
	else: 
		idx = False
	
	if '-vmax' in args:
		index = args.index('-vmax')
		vmax  = float(args[index+1])
	else:
		vmax  = 200

	if '-vmin' in args:
		index = args.index('-vmin')
		vmin  = float(args[index+1])
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
	
	
	if '-fmt' in args:
		index = args.index('-fmt')
		fmt   = args[index+1]
	else:
		fmt   = '%1.1f'
	
	if '-axisfontsize' in args:
		index         = args.index('-axisfontsize')
		axisfontsize  = args[index+1]
	else:
		axisfontsize  =  14
		
	
	if '-i' in args:
		index = args.index('-i')
		log_file  = args[index+1]
	else:
		log_file  = None
	
	
	input_parm = {'vmax'         :vmax         , 
				  'vmin'         :vmin         , 
				  'cmap'         :cmap         , 
				  'shading'      :shading      , 
				  'lspacing'     :lspacing     , 
				  'lcolor'       :lcolor       , 
				  'fontsize'     :fontsize     ,
				  'log_file'     :log_file     ,
				  'idx'          :idx          ,
				  'axisfontsize' :axisfontsize ,
				  'fmt'          :fmt
				  } 
	
	
	return input_parm




input_parm = parser_tags(args)

print input_parm

vmax     = input_parm['vmax'    ]
vmin     = input_parm['vmin'    ]
cmap     = input_parm['cmap'    ]
shading  = input_parm['shading' ]
lspacing = input_parm['lspacing']
lcolor   = input_parm['lcolor'  ]
fontsize = input_parm['fontsize']
log_file = input_parm['log_file']
idx      = input_parm['idx']
fmt      = input_parm['fmt']



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

	c2_ATOM1_id    =  data['c2_ATOM1_id'  ]
	c2_ATOM1_name  =  data['c2_ATOM1_name']
	c2_ATOM1_name  =  c2_ATOM1_name+'_{'+c2_ATOM1_id+'}'
	c2_ATOM2_id    =  data['c2_ATOM2_id'  ]
	c2_ATOM2_name  =  data['c2_ATOM2_name']	
	c2_ATOM2_name  =  c2_ATOM2_name+'_{'+c2_ATOM2_id+'}'
	c2_ATOM3_id    =  data['c2_ATOM3_id'  ]
	c2_ATOM3_name  =  data['c2_ATOM3_name']	
	c2_ATOM3_name  =  c2_ATOM3_name+'_{'+c2_ATOM3_id+'}'
	rcoord2 =   r'$d(' + c2_ATOM1_name + '-' + c2_ATOM2_name+')' +'-'+ 'd('+c2_ATOM2_name+ '-' + c2_ATOM3_name+')$'
	
	c1_ATOM1_id    =  data['c1_ATOM1_id'  ]
	c1_ATOM1_name  =  data['c1_ATOM1_name']
	c1_ATOM1_name  =  c1_ATOM1_name+'_{'+c1_ATOM1_id+'}'
	c1_ATOM2_id    =  data['c1_ATOM2_id'  ]
	c1_ATOM2_name  =  data['c1_ATOM2_name']	
	c1_ATOM2_name  =  c1_ATOM2_name+'_{'+c1_ATOM2_id+'}'
	c1_ATOM3_id    =  data['c1_ATOM3_id'  ]
	c1_ATOM3_name  =  data['c1_ATOM3_name']	
	c1_ATOM3_name  =  c1_ATOM3_name+'_{'+c1_ATOM3_id+'}'
	rcoord1 =   r'$d(' + c1_ATOM1_name + '-' + c1_ATOM2_name+')' +'-'+ 'd('+c1_ATOM2_name+ '-' + c1_ATOM3_name+')$'
	
	
	#label_test =  r'$\sum_{i=0}^\infty x_i$'
	
	#label_test =  r'$\ x_i$'
	
	#lista , frame_list = minimum_path(z)
	#print lista
	#print frame_list
	
	#if idx:
	#	#matrix = data['matrix']
	#	#fig, (ax) = plt.subplots(nrows=1)
	#	#
	#	#coord1 = parameters[1]['xlabel']
	#	#coord2 = parameters[1]['ylabel']
	#	#
	#	## Setting plot type
	#	#im = ax.imshow(matrix, interpolation = 'bicubic')                           #ax.imshow(matrix, interpolation = 'bicubic')       
	#	#am = ax.contour(matrix, colors='k')
	#	#ax.clabel(am, inline=1, fontsize=10, fmt='%1.1f',colors='k') # if using imshow, comment this line
	#	#fig.colorbar(im, ax=ax)                          # and remove comment here             
	#	#
	#	## Set x and y labels
	#	#ax.set_xlabel(coord2)
	#	#ax.set_ylabel(coord1)
	#	#import numpy as np
	#	z = data['matrix']
	#	'''
	#	# make these smaller to increase the resolution
	#	dx, dy = 0.15, 0.05
	#
	#	# generate 2 2d grids for the x & y bounds
	#	y, x = np.mgrid[slice(-3, 3 + dy, dy),
	#				slice(-3, 3 + dx, dx)]
	#	z = (1 - x / 2. + x ** 5 + y ** 3) * np.exp(-x ** 2 - y ** 2)
	#	# x and y are bounds, so z should be the value *inside* those bounds.
	#	# Therefore, remove the last value from the z array.
	#	z = z[:-1, :-1]
	#	z_min, z_max = -np.abs(z).max(), np.abs(z).max()
	#	'''
	#	
	#	
	#	#'''
	#	z_min, z_max = -np.abs(z).max(), np.abs(z).max()
	#	
	#	x = range(len(x))
	#	y = range(len(y))
	#	X, Y = np.meshgrid(x, y)
	#	
	#	
	#	fig, ax = plt.subplots()
	#	CS = ax.contour(X, Y, z)
	#	ax.clabel(CS, inline=1, fontsize=10)
	#	ax.set_title('Simplest default with labels')
	#	
	#	
	#	
	#	#fig, ax = plt.subplots(nrows=1)
	#
	#	#c = ax.pcolor( z, cmap='jet', vmin = vmin, vmax = vmax)#, vmin=z_min, vmax=z_max)
	#	
	#	#ax.set_title('pcolor')
	#	#fig.colorbar(c, ax=ax)
	#
	#	fig.tight_layout()
	#	plt.show()
	#	#'''




	#else:
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

	if idx:
		x = range(len(x))
		y = range(len(y))
		X, Y = np.meshgrid(x, y)

	im = ax0.pcolormesh(x, y, z, cmap=cmap, norm=norm, shading = shading)

	#im = ax0.imshow(x,y,z, interpolation = 'bicubic')

	#c = ax0.contour(  colors='black', alpha=0.3, linewidths=2)

	if lspacing == 0:
		am = None
		#ax0.clabel(inline=1, fontsize=fontsize, fmt=fmt,colors=lcolor)

	else:
		am = ax0.contour(x,y,z,lspacing, colors=lcolor)
		ax0.clabel(am, inline=1, fontsize=fontsize, fmt=fmt,colors=lcolor)

	#x,y,z, levels=numpy.linspace(-5.0, 0.0, 50), cmap='Blues_r'
	#im = ax0.contourf(x,y,z, cmap='rainbow')

	#ax.imshow(matrix, interpolation = 'bicubic') 

	FontSize = 20

	# Set the tick labels font
	axis_font = {'fontname':'Michroma', 'size':input_parm['axisfontsize']}
	for tick in (ax0.xaxis.get_major_ticks()):
		tick.label.set_fontname('Arial')
		tick.label.set_fontsize(FontSize)

	for tick in (ax0.yaxis.get_major_ticks()):
		tick.label.set_fontname('Dejavu')
		tick.label.set_fontsize(FontSize) 

	coord1 = data['xlabel']
	coord2 = data['ylabel']
	ax0.set_xlabel(coord2, **axis_font)
	#ax0.set_xlabel(rcoord2, **axis_font)
	ax0.set_ylabel(coord1, **axis_font)
	#ax0.set_ylabel(rcoord1, **axis_font)



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
