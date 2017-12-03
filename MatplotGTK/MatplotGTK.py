#!/usr/bin/env python
"""
show how to add a matplotlib FigureCanvasGTK or FigureCanvasGTKAgg widget and
a toolbar to a gtk.Window
"""


# uncomment to select /GTK/GTKAgg/GTKCairo
#from matplotlib.backends.backend_gtk import FigureCanvasGTK as FigureCanvas
#from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas
#from matplotlib.backends.backend_gtkcairo import FigureCanvasGTKCairo as FigureCanvas

# or NavigationToolbar for classic
#from matplotlib.backends.backend_gtk import NavigationToolbar2GTK as NavigationToolbar
#from matplotlib.backends.backend_gtkagg import NavigationToolbar2GTKAgg as NavigationToolbar

# implement the default mpl key bindings
#from matplotlib.backend_bases import key_press_handler
#from matplotlib.widgets import Cursor



try:
    #from numpy import arange, sin, pi
    import numpy as np
    import matplotlib.pyplot as plt                                             #
    #import multiprocessing.dummy as multiprocessing
    import matplotlib                                                           #
    from pylab import contour
    from pylab import clabel
    from pylab import colorbar
    from pylab import grid
    #-------------------------------------------------------------------------------------------------
except:
    print 'error'


class PlotGTKWindow:
    def __init__ (self, gtk = True):
        """ Function doc """
        self.Xclick = []
        self.Yclick = []
        self.ax = None

    
    def plot (self, parameters):
        """ Function doc """
	import gtk
	from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas
	from matplotlib.backends.backend_gtkagg import NavigationToolbar2GTKAgg as NavigationToolbar
	from matplotlib.figure import Figure                                                         #

	plots = len(parameters)

	win = gtk.Window()
	win.connect("destroy", lambda x: gtk.main_quit())
	win.set_default_size(400, 300)
	
	title = parameters[1]['energy_model']
	title = parameters[1]['log_file']
	win.set_title(title)

	fig = Figure(figsize=(1,1), dpi=80)
	#canvas = FigureCanvas(fig)  # a gtk.DrawingArea
	#vbox.pack_start(canvas)
	#toolbar = NavigationToolbar(canvas, win)
	#vbox.pack_start(toolbar, False, False)

	if parameters[1]['type'] == 'line':
	    x = parameters[1]['X']
	    y = parameters[1]['Y']
	     
	    ax  = fig.add_subplot(plots, 1, 1,)
	    ax.grid(True)
	    
	    # Setting plot type
	    ax.plot(x, y, 'ko',x, y,'k', picker=5)
	    #ax.plot(z, y, 'ko', z, y,'k', picker=5)
	    
	    ax.spines['right'].set_visible(False)
	    ax.spines['top'].set_visible(True)
	    ax.yaxis.set_ticks_position('left')
	    ax.xaxis.set_ticks_position('bottom')
	    
	    ax.set_xlabel(parameters[1]['xlabel'])
	    ax.set_ylabel(parameters[1]['ylabel'])
			  
	if parameters[1]['type'] == 'matrix':
	    matrix = parameters[1]['matrix']
	    fig, (ax) = plt.subplots(nrows=1)
	    
	    coord1 = parameters[1]['xlabel']
	    coord2 = parameters[1]['ylabel']
	    
	    # Setting plot type
	    im = ax.imshow(matrix, interpolation = 'bicubic')                           #ax.imshow(matrix, interpolation = 'bicubic')       
	    am = ax.contour(matrix, colors='k')
	    ax.clabel(am, inline=1, fontsize=10, fmt='%1.1f',colors='k') # if using imshow, comment this line
	    fig.colorbar(im, ax=ax)                          # and remove comment here             
	    
	    # Set x and y labels
	    ax.set_xlabel(coord2)
	    ax.set_ylabel(coord1)
	
	#self.figure_plot(parameters, fig)
	vbox = gtk.VBox()
	win.add(vbox)
	canvas = FigureCanvas(fig)  
	vbox.pack_start(canvas)
	toolbar = NavigationToolbar(canvas, win)
	vbox.pack_start(toolbar, False, False)
	'''
	status_bar = gtk.Statusbar()
	vbox.pack_end(status_bar, False, False)
	status_bar.push(0, '')
	#'''
	win.show_all()
	gtk.main()


















class PlotGTKWindow_old_not_used:
    def __init__ (self, gtk = True):
        """ Function doc """
        self.Xclick = []
        self.Yclick = []
        self.ax = None

    
    def plot (self, parameters):
        """ Function doc """
        if parameters is None:
	    return False
        
        def tk_plot ():
            from Tkinter import Tk, TOP, BOTH
            import matplotlib
            matplotlib.use('TkAgg')
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg

            """ Function doc """
            window=Tk()
            window.wm_title("EasyHybrid TkWindow Plot")
            fig = matplotlib.figure.Figure()
            canvas = FigureCanvasTkAgg(fig, master=window)
            canvas.show()
            canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
            canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)
            toolbar = NavigationToolbar2TkAgg(canvas, window)
            log_file = parameters[1].get('log_file','log_file unknown')
            window.wm_title(log_file)
            self.figure_plot(parameters, fig)
            window.mainloop()            
       
       
        def gtk_plot ():
            """ Function doc """
            #import gtk
            from matplotlib.figure import Figure                                                         #
            #from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas            #
            #from matplotlib.backends.backend_gtkagg import NavigationToolbar2GTKAgg as NavigationToolbar #
           
            #win = gtk.Window()
            #win.connect("destroy", lambda x: gtk.main_quit())
            #win.set_default_size(560,420)

            log_file = parameters[1].get('log_file','log_file unknown')

            #win.set_title(log_file)

            #vbox = gtk.VBox()
            #win.add(vbox)
            fig = Figure(figsize=(1,1), dpi=80)
            #canvas = FigureCanvas(fig)  # a gtk.DrawingArea

            #vbox.pack_start(canvas)
            #toolbar = NavigationToolbar(canvas, win)
            #vbox.pack_start(toolbar, False, False)

            #'''
            #status_bar = gtk.Statusbar()
            #vbox.pack_end(status_bar, False, False)
            #status_bar.push(0, '')
            #'''
            
	    self.figure_plot(parameters, fig)

            #win.show_all()
            #gtk.main()

        #try:
        #import matplotlib.backends.backend_gtkagg # arrumar isso depois! :D
        gtk_plot()
        #print 'Using GTK plot'
        #except:
        #    simulate=multiprocessing.Process(None, tk_plot)
        #    simulate.start()
        #    print 'Using TK plot'

    
    def  figure_plot(self, parameters, fig):
        """ Function doc """
        import mpl_toolkits.axisartist as AA
	from mpl_toolkits.axes_grid1 import host_subplot

        plots = len(parameters)

	import gtk
	from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas
	from matplotlib.backends.backend_gtkagg import NavigationToolbar2GTKAgg as NavigationToolbar

	win = gtk.Window()
	win.connect("destroy", lambda x: gtk.main_quit())
	win.set_default_size(400, 300)
	


        
	for i in parameters:
            if parameters[i]['type'] == 'line':
		title = parameters[i]['energy_model']
		title = parameters[i]['log_file']
		win.set_title(title)
		
		x = parameters[i]['X']
                y = parameters[i]['Y']
		 
                ax  = fig.add_subplot(plots, 1, i,)
                ax.grid(True)
                
                # Setting plot type
                ax.plot(x, y, 'ko',x, y,'k', picker=5)
		#ax.plot(z, y, 'ko', z, y,'k', picker=5)
                
                ax.spines['right'].set_visible(False)
                ax.spines['top'].set_visible(True)
                ax.yaxis.set_ticks_position('left')
                ax.xaxis.set_ticks_position('bottom')
                
                ax.set_xlabel(parameters[i]['xlabel'])
                ax.set_ylabel(parameters[i]['ylabel'])

                #def onpick(event):
		#			ydata = y
		#			ind = event.ind
		#			frame = ind[0] + 1
		#			iy = str(ydata[ind])
		#			print 'Structure_%s = %s' % (str(frame), iy)
                #
                #fig.canvas.mpl_connect('pick_event', onpick)
                win.show_all()
                gtk.main()  
		              
            if parameters[i]['type'] == 'matrix':
                matrix = parameters[i]['matrix']
                fig, (ax) = plt.subplots(nrows=1)
		
                coord1 = parameters[1]['xlabel']
                coord2 = parameters[1]['ylabel']
		
		# Setting plot type
                im = ax.imshow(matrix, interpolation = 'bicubic')                           #ax.imshow(matrix, interpolation = 'bicubic')       
                am = ax.contour(matrix, colors='k')
                ax.clabel(am, inline=1, fontsize=10, fmt='%1.1f',colors='k') # if using imshow, comment this line
                fig.colorbar(im, ax=ax)                          # and remove comment here             
		
		# Set x and y labels
		ax.set_xlabel(coord2)
		ax.set_ylabel(coord1)
		
                # a gtk.DrawingArea

                
		#print parameters[1]

	vbox = gtk.VBox()
	win.add(vbox)
	canvas = FigureCanvas(fig)  
	vbox.pack_start(canvas)
	toolbar = NavigationToolbar(canvas, win)
	vbox.pack_start(toolbar, False, False)
	win.show_all()
	gtk.main()




























'''
win = gtk.Window()
win.connect("destroy", lambda x: gtk.main_quit())
win.set_default_size(400, 300)
win.set_title("Embedding in GTK")

vbox = gtk.VBox()
win.add(vbox)


cmap = matplotlib.cm.get_cmap(name='jet', lut=None)
matrix = parameters[i]['matrix']
fig = Figure(figsize=(5, 4), dpi=100)
ax  = fig.add_subplot(111)
ax.grid(c='k', ls='-')#, alpha=0.3)

im  = ax.imshow(matrix, cmap=cmap, interpolation ='bicubic')

fig.colorbar(im, ax=ax)

canvas = FigureCanvas(fig)  # a gtk.DrawingArea
vbox.pack_start(canvas)
toolbar = NavigationToolbar(canvas, win)
vbox.pack_start(toolbar, False, False)
	    
win.show_all()
				
     


def on_key_event(event):
    print('you pressed %s' % event.key)
    key_press_handler(event, canvas, toolbar)

canvas.mpl_connect('key_press_event', on_key_event)

win.show_all()
gtk.main()


from numpy.random import uniform, seed
from matplotlib.mlab import griddata
import matplotlib.pyplot as plt
import numpy as np
# make up data.
#npts = int(raw_input('enter # of random points to plot:'))
seed(0)
npts = 200
x = uniform(-2, 2, npts)
y = uniform(-2, 2, npts)
z = x*np.exp(-x**2 - y**2)
# define grid.
xi = np.linspace(-2.1, 2.1, 100)
yi = np.linspace(-2.1, 2.1, 200)
# grid the data.
zi = griddata(x, y, z, xi, yi, interp='linear')
# contour the gridded data, plotting dots at the nonuniform data points.
CS = plt.contour(xi, yi, zi, 15, linewidths=0.5, colors='k')
CS = plt.contourf(xi, yi, zi, 15, cmap=plt.cm.rainbow,
		  vmax=abs(zi).max(), vmin=-abs(zi).max())
plt.colorbar()  # draw colorbar
# plot data points.
plt.scatter(x, y, marker='o', c='b', s=5, zorder=10)
plt.xlim(-2, 2)
plt.ylim(-2, 2)
plt.title('griddata test (%d points)' % npts)
plt.show()
'''

'''
cmap = matplotlib.cm.get_cmap(name='jet', lut=None)
matrix = parameters[i]['matrix']                  
ax  = fig.add_subplot(111)

#ax  = self.fig.add_subplot(self.plots, 1, i)
#im  = ax.imshow(matrix, cmap=cmap.jet, interpolation='nearest')
im  = ax.imshow(matrix, cmap=cmap, interpolation='nearest')

import matplotlib.pyplot as plt

#c = contour(matrix, colors = 'k', linewidths = (1,))
c = plt.contour(matrix, colors = 'k', linewidths = (1,))
plt.colorbar()

clabel(c, fmt = '%2.1f', colors = 'k', fontsize=14)
colorbar(im)
grid(True)

xlabel = parameters[i]['xlabel']
ylabel = parameters[i]['ylabel']
ax.set_xlabel(xlabel)
ax.set_ylabel(ylabel)
'''
