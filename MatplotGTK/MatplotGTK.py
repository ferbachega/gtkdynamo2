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
from matplotlib.backend_bases import key_press_handler
#from matplotlib.widgets import Cursor

class PlotGTKWindow:
    
    def on_key_event(self, event):
        print('you pressed %s'%event.key)
        key_press_handler(event, self.canvas, self.toolbar)
    
    def on_pick(self, event):
        thisline = event.artist
        xdata, ydata = thisline.get_data()
        ind = event.ind
        print('on pick line:', zip(xdata[ind], ydata[ind]))
        self.ax.plot(xdata[ind], ydata[ind], 'bo', picker=5)



    def __init__ (self, parameters = None):
        """ Function doc """
        self.win = gtk.Window()
        self.win.connect("destroy", lambda x: gtk.main_quit())
        self.win.set_default_size(560,420)
        self.win.set_title("Embedding in GTK")

        vbox = gtk.VBox()
        self.win.add(vbox)

        self.fig = Figure(figsize=(1,1), dpi=80)
        self.ax  = self.fig.add_subplot(111)
        
        if parameters == None:
            x = arange(0.0,3.0,0.01)
            y = sin(2*pi*x)
            parameters = {
                         'title' : 'test',
                         'X'     : x     ,
                         'y'     : y     ,
                         'xlabel': 'x\n '   ,
                         'ylabel': '\nsin'
                         }
            
            
        else:
            x = parameters['X']
            y = parameters['Y']

        
        self.win.set_title(parameters['title'])
        #self.ax.plot(t,s)
        self.ax.plot(x, y, 'ko',x, y,'k', picker=5)

        self.ax.set_xlabel(parameters['xlabel'])
        self.ax.set_ylabel(parameters['ylabel'])        
        self.ax.grid(True)
        #cursor = Cursor(self.ax, useblit=True, color='red', linewidth=2 )

        
        self.canvas = FigureCanvas(self.fig)  # a gtk.DrawingArea
        vbox.pack_start(self.canvas)
        self.toolbar = NavigationToolbar(self.canvas, self.win)
        vbox.pack_start(self.toolbar, False, False)
        
        
        
        self.canvas.mpl_connect('key_press_event', self.on_key_event)
        print 'antes'
        self.canvas.mpl_connect('pick_event', self.on_pick)
        print 'depois'
        self.win.show_all()
        gtk.main()
    

   
if __name__ == "__main__":
    PlotGTKWindow = PlotGTKWindow()
    #editor.load_file('/home/fernando/pDynamoWorkSpace/glucose_Dec_13_2014/2_step_GeometryOptmization/2_step_GeometryOptmization.log')
    
