#!/usr/bin/env python
"""
show how to add a matplotlib FigureCanvasGTK or FigureCanvasGTKAgg widget and
a toolbar to a gtk.Window
"""
import gtk

from matplotlib.figure import Figure
from numpy import arange, sin, pi

# uncomment to select /GTK/GTKAgg/GTKCairo
#from matplotlib.backends.backend_gtk import FigureCanvasGTK as FigureCanvas
from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas
#from matplotlib.backends.backend_gtkcairo import FigureCanvasGTKCairo as FigureCanvas

# or NavigationToolbar for classic
#from matplotlib.backends.backend_gtk import NavigationToolbar2GTK as NavigationToolbar
from matplotlib.backends.backend_gtkagg import NavigationToolbar2GTKAgg as NavigationToolbar

# implement the default mpl key bindings
#from matplotlib.backend_bases import key_press_handler
#from matplotlib.widgets import Cursor

class PlotGTKWindow:
    
    def __init__ (self, parameters = None):
        """ Function doc """
        self.Xclick = []
        self.Yclick = []
        self.ax = None
        
        
        
        if parameters == None:
            x = arange(0.0,3.0,0.01)
            y = sin(2*pi*x)
            parameters = {
                         'type'  : 'line',
                         'title' : 'test',
                         'X'     : x     ,
                         'Y'     : y     ,
                         'xlabel': 'x\n ',
                         'ylabel': '\nsin'
                         }
    

        if parameters['type'] == 'line':
            self.plot_line (parameters)
        if parameters['type'] == 'matrix':
            self.plot_matrix (parameters)


    
    def on_key_event(self, event):
        print('you pressed %s'%event.key)
        key_press_handler(event, self.canvas, self.toolbar)

    
    
    
    
    
    
    
    
    
    '''
    def onpick1(self, event):
        if isinstance(event.artist, Line2D):
            thisline = event.artist
            xdata = thisline.get_xdata()
            ydata = thisline.get_ydata()
            ind = event.ind
            print('onpick1 line:', zip(np.take(xdata, ind), np.take(ydata, ind)))
        elif isinstance(event.artist, Rectangle):
            patch = event.artist
            print('onpick1 patch:', patch.get_path())
        elif isinstance(event.artist, Text):
            text = event.artist
            print('onpick1 text:', text.get_text())    
    
    def onpick2(self, event):
        print('onpick2 line:', event.pickx, event.picky)
    '''
    
    
    
    
    
    
    
    
    
    
    def on_pick(self, event):
        thisline = event.artist
        xdata, ydata = thisline.get_data()
        ind = event.ind
        #print('on pick line:', zip(xdata[ind], ydata[ind]))
        self.ax.plot(xdata[ind], ydata[ind], 'bo', picker=5)
        
        
        print zip(xdata[ind])[0][0], zip(ydata[ind])[0][0]
        #print zip(ydata[ind])[0][0]
        
        
        if len(self.Xclick) <= 2:
            self.Xclick.append(zip(xdata[ind])[0][0])
            self.Yclick.append(zip(ydata[ind])[0][0])
            self.status_bar.push(0, str(zip(xdata[ind])[0][0]))
        else:
            self.Xclick = []
            self.Yclick = []
            
        #print (self.Xclick , self.Yclick)
    
    
     
    def plot_line (self, parameters):

        win = gtk.Window()
        win.connect("destroy", lambda x: gtk.main_quit())
        win.set_default_size(560,420)
        win.set_title("Embedding in GTK")

        vbox = gtk.VBox()
        win.add(vbox)
        fig = Figure(figsize=(1,1), dpi=80)
        self.ax  = fig.add_subplot(111)
        
        win.set_title(parameters['title'])




        x = parameters['X']
        y = parameters['Y']

        self.ax.set_xlabel(parameters['xlabel'])
        self.ax.set_ylabel(parameters['ylabel'])        
        self.ax.grid(True)
        self.ax.plot(x, y, 'ko',x, y,'k', picker=5)
        self.canvas = FigureCanvas(fig)  # a gtk.DrawingArea
        vbox.pack_start(self.canvas)
        self.toolbar = NavigationToolbar(self.canvas, win)
        vbox.pack_start(self.toolbar, False, False)
        
        self.status_bar = gtk.Statusbar()
        vbox.pack_end(self.status_bar, False, False)
        self.status_bar.push(0, '')
        #----------------------------------------------------#
        #self.canvas.mpl_connect('key_press_event', self.on_key_event)  #
        self.canvas.mpl_connect('pick_event', self.on_pick)            #
        #self.canvas.mpl_connect('pick_event', self.onpick2) 
        #----------------------------------------------------#

        
        win.show_all()
        gtk.main()
        
    
    
    def plot_matrix (self, parameters):
        """ Function doc """
        from matplotlib.figure import Figure
        from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas
        from matplotlib.backends.backend_gtkagg import NavigationToolbar2GTKAgg as NavigationToolbar


        win = gtk.Window()
        win.connect("destroy", lambda x: gtk.main_quit())
        win.set_default_size(580,420)

        title = parameters['title']
        win.set_title(title)
        vbox = gtk.VBox()
        win.add(vbox)

        import matplotlib.pyplot as plt
        import matplotlib.cm as cm	
        matrix = parameters['matrix']
        fig = plt.figure()
        ax  = fig.add_subplot(111)
        im  = ax.imshow(matrix, cmap=cm.jet, interpolation='nearest')



        from pylab import contour
        from pylab import clabel
        c = contour(matrix, colors = 'k', linewidths = (1,))
        clabel(c, fmt = '%2.1f', colors = 'k', fontsize=14)



        from pylab import colorbar
        colorbar(im)
        #im1=ax.imshow([[1,2],[2, 3]])
        #plt.colorbar(im1, cax=ax, orientation="horizontal", ticks=[1,2,3])
        #ax.imshow(matrix, cmap=cm.jet, interpolation='nearest', extent=(-4.1,4.5,-4,4))



        from pylab import grid
        #ax.imshow(matrix, cmap=cm.jet, interpolation='bilinear')

        grid(True)
        xlabel = parameters['xlabel']
        ylabel = parameters['ylabel']
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)

        #cb = plt.colorbar(0,10)
        #cb.set_label('counts')		

        canvas = FigureCanvas(fig)  # a gtk.DrawingArea
        vbox.pack_start(canvas)
        toolbar = NavigationToolbar(canvas, win)
        vbox.pack_start(toolbar, False, False)


        win.show_all()
        gtk.main()	

































   
if __name__ == "__main__":
    PlotGTKWindow = PlotGTKWindow()
    #editor.load_file('/home/fernando/pDynamoWorkSpace/glucose_Dec_13_2014/2_step_GeometryOptmization/2_step_GeometryOptmization.log')
    
