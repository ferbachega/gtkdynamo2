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


class PlotGTKWindow:
    
    def on_key_event(self, event):
        print('you pressed %s'%event.key)
        key_press_handler(event, self.canvas, self.toolbar)
    
    def __init__ (self, parameters = None):
        """ Function doc """
        self.win = gtk.Window()
        self.win.connect("destroy", lambda x: gtk.main_quit())
        self.win.set_default_size(520,420)
        self.win.set_title("Embedding in GTK")

        vbox = gtk.VBox()
        self.win.add(vbox)

        fig = Figure(figsize=(1,1), dpi=80)
        ax = fig.add_subplot(111)
        
        if parameters == None:
            x = arange(0.0,3.0,0.01)
            y = sin(2*pi*x)
            parameters = {
                         'title' : 'test',
                         'X'     : x     ,
                         'y'     : y     ,
                         'xlabel': 'x'   ,
                         'ylabel': 'sin'
                         }
            
            
        else:
            x = parameters['X']
            y = parameters['Y']

        
        self.win.set_title(parameters['title'])
        #ax.plot(t,s)
        ax.plot(x, y, 'ko',x, y,'k')

        ax.set_xlabel(parameters['xlabel'])
        ax.set_ylabel(parameters['ylabel'])        
        ax.grid(True)
        
        self.canvas = FigureCanvas(fig)  # a gtk.DrawingArea
        vbox.pack_start(self.canvas)
        self.toolbar = NavigationToolbar(self.canvas, self.win)
        vbox.pack_start(self.toolbar, False, False)
        self.canvas.mpl_connect('key_press_event', self.on_key_event)

        self.win.show_all()
        gtk.main()
    

   
if __name__ == "__main__":
    PlotGTKWindow = PlotGTKWindow()
    #editor.load_file('/home/fernando/pDynamoWorkSpace/glucose_Dec_13_2014/2_step_GeometryOptmization/2_step_GeometryOptmization.log')
    
