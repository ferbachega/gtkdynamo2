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




from numpy import arange, sin, pi
import numpy as np
import matplotlib.pyplot as plt                                             #
import multiprocessing.dummy as multiprocessing
import matplotlib                                                           #


from pylab import contour
from pylab import clabel
from pylab import colorbar
from pylab import grid
#-------------------------------------------------------------------------------------------------



class PlotGTKWindow:
    def __init__ (self, gtk = True):
        """ Function doc """
        self.Xclick = []
        self.Yclick = []
        self.ax = None

    
    def plot (self, parameters):
        """ Function doc """
        if parameters is None:
            print 'Parameters not found'
            x = arange(0.0,3.0,0.01)
            y = sin(2*pi*x)
            parameters = {1: {
                            'type'  : 'line',
                            'title' : 'test',
                            'X'     : x     ,
                            'Y'     : y     ,
                            'xlabel': 'x\n ',
                            'ylabel': '\nsin'}
                         }
            x = arange(0.0,3.0,0.01)
            y = sin(2*pi*x)
        
        
        print (parameters)
        
        
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
            import gtk
            from matplotlib.figure import Figure                                                         #
            from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas            #
            from matplotlib.backends.backend_gtkagg import NavigationToolbar2GTKAgg as NavigationToolbar #
           
            win = gtk.Window()
            win.connect("destroy", lambda x: gtk.main_quit())
            win.set_default_size(560,420)

            log_file = parameters[1].get('log_file','log_file unknown')

            win.set_title(log_file)

            vbox = gtk.VBox()
            win.add(vbox)
            fig = Figure(figsize=(1,1), dpi=80)
            canvas = FigureCanvas(fig)  # a gtk.DrawingArea

            vbox.pack_start(canvas)
            toolbar = NavigationToolbar(canvas, win)
            vbox.pack_start(toolbar, False, False)

            '''
            status_bar = gtk.Statusbar()
            vbox.pack_end(status_bar, False, False)
            status_bar.push(0, '')
            '''
            self.figure_plot(parameters, fig)

            win.show_all()
            gtk.main()

        #try:
        import matplotlib.backends.backend_gtkagg # arrumar isso depois! :D
        gtk_plot()
        print 'Using GTK plot'
        #except:
        #    simulate=multiprocessing.Process(None, tk_plot)
        #    simulate.start()
        #    print 'Using TK plot'

    
    def  figure_plot(self, parameters, fig):
        """ Function doc """
        
        plots = len(parameters)
        
        for i in parameters:
            
            if parameters[i]['type'] == 'line':
                x = parameters[i]['X']
                y = parameters[i]['Y']
                
                ax  = fig.add_subplot(plots, 1, i,)
                ax.grid(True)
        
                ax.set_xlabel(parameters[i]['xlabel'])
                ax.set_ylabel(parameters[i]['ylabel'])
                ax.plot(x, y, 'ko',x, y,'k', picker=5)
                
            if parameters[i]['type'] == 'matrix':
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
                #ax.contourf(matrix,colors = 'k', linewidths = (1,),origin='image')
                
                #im  = ax.imshow(matrix, cmap=cmap, interpolation='nearest')
                im  = ax.imshow(matrix, cmap=cmap, interpolation ='bicubic')
                #c = plt.contour(matrix, colors = 'k', linewidths = (1,),origin='image')#, extent=extent)
                #c = contour(matrix, colors = 'k', linewidths = (1,))
                fig.colorbar(im, ax=ax)
                #fig.contour(c, ax=ax)
                #fig.colorbar(c, ax=ax)
                
                #from matplotlib.mlab import griddata
                #from numpy.random import uniform, seed
                #seed(0)
                #npts = 200
                #x = uniform(-2, 2, npts)
                #y = uniform(-2, 2, npts)
                #z = x*np.exp(-x**2 - y**2)
                ## define grid.
                #xi = np.linspace(-2.1, 2.1, 100)
                #yi = np.linspace(-2.1, 2.1, 200)
                ## grid the data.
                #zi = griddata(x, y, z, xi, yi, interp='linear')
                ## contour the gridded data, plotting dots at the nonuniform data points.
                #
                #CS = plt.contour(xi, yi, zi, 15, linewidths=0.5, colors='k')
                #CS = plt.contourf(xi, yi, zi, 15, cmap=plt.cm.rainbow,
                #                  vmax=abs(zi).max(), vmin=-abs(zi).max())
                
                #c = plt.contour(matrix, colors = 'k', linewidths = (1,))
                #t = arange(0.0, 3.0, 0.01)
                #s = sin(2*pi*t)

                #ax.plot(t, s)

                canvas = FigureCanvas(fig)  # a gtk.DrawingArea
                vbox.pack_start(canvas)
                toolbar = NavigationToolbar(canvas, win)
                vbox.pack_start(toolbar, False, False)

                def on_key_event(event):
                    print('you pressed %s' % event.key)
                    key_press_handler(event, canvas, toolbar)

                canvas.mpl_connect('key_press_event', on_key_event)

                win.show_all()
                gtk.main()
                
                
                '''
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
    #def plot_matrix (self, parameters):
    #    """ Function doc """
    #
    #    
    #    win = gtk.Window()
    #    win.connect("destroy", lambda x: gtk.main_quit())
    #    win.set_default_size(580,420)
    #    
    #    log_file = parameters['log_file']
    #    title = parameters['title']
    #    win.set_title(log_file)
    #    vbox = gtk.VBox()
    #    win.add(vbox)
    #
    #    #import matplotlib.pyplot as plt
    #    #import matplotlib.cm as cm	
    #    #NOVA LINHA
    #    cmap = cm.get_cmap(name='terrain', lut=None)
    #    
    #    matrix = parameters['matrix']
    #    fig = plt.figure()
    #    
    #    ax  = fig.add_subplot(111)
    #    
    #    #ax  = self.fig.add_subplot(self.plots, 1, i)
    #    
    #    #im  = ax.imshow(matrix, cmap=cmap.jet, interpolation='nearest')
    #    im  = ax.imshow(matrix, cmap=cmap, interpolation='nearest')
    #
    #
    #    #from pylab import contour
    #    #from pylab import clabel
    #    
    #    c = contour(matrix, colors = 'k', linewidths = (1,))
    #    clabel(c, fmt = '%2.1f', colors = 'k', fontsize=14)
    #    
    #    #from pylab import colorbar
    #    
    #    colorbar(im)
    #
    #    #from pylab import grid
    #    grid(True)
    #    xlabel = parameters['xlabel']
    #    ylabel = parameters['ylabel']
    #    ax.set_xlabel(xlabel)
    #    ax.set_ylabel(ylabel)
    #    canvas = FigureCanvas(fig)  # a gtk.DrawingArea
    #    vbox.pack_start(canvas)
    #    toolbar = NavigationToolbar(canvas, win)
    #    vbox.pack_start(toolbar, False, False)
    #    win.show_all()
    #    gtk.main()	
    #
    #
    #
    #
    #
    #
    #    ##----------------------------------------------------------------------#
    #    #from mpl_toolkits.mplot3d import Axes3D
    #    #import matplotlib        
    #    #import numpy as np        
    #    #from matplotlib import cm        
    #    #from matplotlib import pyplot as plt           
    #    #
    #    #win = gtk.Window()
    #    #win.connect("destroy", lambda x: gtk.main_quit())
    #    #win.set_default_size(580,420)
    #    #title = parameters['title']
    #    #win.set_title(title)
    #    #vbox = gtk.VBox()
    #    #win.add(vbox)
    #    #
    #    #fig = plt.figure()
    #    #ax = fig.add_subplot(111, projection='3d')
    #    #Z  = parameters['matrix']
    #    #R1 = parameters['R1'    ]
    #    #R2 = parameters['R2'    ]
    #    #r1 = parameters['xlabel']
    #    #r2 = parameters['ylabel']
    #    #
    #    ## create supporting points in polar coordinates
    #    #ax.plot_surface(R1, R2, Z, rstride=1, cstride=1, cmap=cm.jet)
    #    #canvas = FigureCanvas(fig)  # a gtk.DrawingArea
    #    #vbox.pack_start(canvas)
    #    #toolbar = NavigationToolbar(canvas, win)
    #    #vbox.pack_start(toolbar, False, False)
    #    #win.show_all()
    #    #gtk.main()
    #    ##----------------------------------------------------------------------#
    #
    #
    #
    #
    #
    #    '''
    #    #import matplotlib.pyplot as plt
    #    #import matplotlib.cm as cm	
    #
    #
    #    #import matplotlib.pyplot as plt
    #    #from matplotlib.colors import BoundaryNorm
    #    #from matplotlib.ticker import MaxNLocator
    #    #import numpy as np
    #    #from pprint import pprint 
    #    #from matplotlib import cm
    #    #
    #    #from mpl_toolkits.mplot3d import Axes3D
    #    #import matplotlib
    #    #import numpy as np
    #    #from matplotlib import cm
    #    #from matplotlib import pyplot as plt        
    #    #
    #    #Z  = parameters['matrix']
    #    #R1 = parameters['R1'    ]
    #    #R2 = parameters['R2'    ]
    #    #r1 = parameters['xlabel']
    #    #r2 = parameters['ylabel']
    #    #fig = plt.figure()
    #    #
    #    #ax = fig.add_subplot(111, projection='3d')
    #    #
    #    ## create supporting points in polar coordinates
    #    #ax.plot_surface(R1, R2, Z, rstride=1, cstride=1, cmap=cm.jet)
    #    ##ax.plot_trisurf(x, y, z, cmap=cm.jet, linewidth=0.2)
    #    ##ax.set_zlim3d(0, 1)
    #    #
    #    #plt.show()
    #
    #
    #    #levels = MaxNLocator(nbins=600).tick_values(Z.min(), Z.max())
    #    #cmap = cmap=cm.jet
    #    #norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)
    #    #fig, (ax1) = plt.subplots(nrows=1)
    #    #
    #    #cf = ax1.pcolormesh(R1, R2, Z, cmap=cmap)#, norm=norm)
    #    #CS = ax1.contour (R1, R2, Z, 6, colors='k',)
    #    #
    #    #fig.colorbar(cf, ax=ax1)
    #    #ax1.set_title('contourf with levels')
    #    #
    #    #fig.tight_layout()
    #    #
    #    #plt.show()
    #    '''
    #
    #
if __name__ == "__main__":
    PlotGTKWindow = PlotGTKWindow()
    #editor.load_file('/home/fernando/pDynamoWorkSpace/glucose_Dec_13_2014/2_step_GeometryOptimization/2_step_GeometryOptimization.log')
    
        #parameters[2] = {
        #                'type'  : 'line',
        #                'title' : 'test',
        #                'X'     : x     ,
        #                'Y'     : y     ,
        #                'xlabel': 'x\n ',
        #                'ylabel': '\nsin'}
        #
        
        
        
        
        #parameters = {1: {'matrix': ([[  1.27355418e+01,   2.18695998e+01,   4.19756062e+01,
        #                      7.06152581e+01,   1.05045732e+02,   1.42345891e+02,
        #                      1.79875352e+02,   2.15781651e+02,   2.49166707e+02,
        #                      2.79822668e+02,   3.07821914e+02,   3.33249552e+02,
        #                      3.56139303e+02,   3.76523295e+02,   3.94492107e+02,
        #                      4.10213369e+02,   4.23911476e+02,   4.35833812e+02,
        #                      4.46222875e+02,   4.55300260e+02,   4.63260493e+02,
        #                      4.70270649e+02,   4.76472676e+02,   4.81986502e+02],
        #                   [  1.15710990e+01,   2.05634266e+01,   4.04979589e+01,
        #                      6.89370484e+01,   1.03138333e+02,   1.40182198e+02,
        #                      1.77431755e+02,   2.13039476e+02,   2.46111726e+02,
        #                      2.76443379e+02,   3.04108745e+02,   3.29196560e+02,
        #                      3.51747912e+02,   3.71805271e+02,   3.89468999e+02,
        #                      4.04912919e+02,   4.18363572e+02,   4.30067680e+02,
        #                      4.40265604e+02,   4.49176217e+02,   4.56991210e+02,
        #                      4.63874926e+02,   4.69966795e+02,   4.75384451e+02],
        #                   [  1.02952991e+01,   1.91293359e+01,   3.88715920e+01,
        #                      6.70846074e+01,   1.01025837e+02,   1.37776549e+02,
        #                      1.74702946e+02,   2.09962517e+02,   2.42666797e+02,
        #                      2.72614986e+02,   2.99886059e+02,   3.24575952e+02,
        #                      3.46736132e+02,   3.66420447e+02,   3.83738344e+02,
        #                      3.98868681e+02,   4.12039340e+02,   4.23495940e+02,
        #                      4.33476453e+02,   4.42196832e+02,   4.49845746e+02,
        #                      4.56584550e+02,   4.62549911e+02,   4.67856994e+02],
        #                   [  8.88628907e+00,   1.75382563e+01,   3.70595161e+01,
        #                      6.50119932e+01,   9.86520227e+01,   1.35060783e+02,
        #                      1.71607143e+02,   2.06454082e+02,   2.38719946e+02,
        #                      2.68211176e+02,   2.95015349e+02,   3.19239500e+02,
        #                      3.40947826e+02,   3.60205819e+02,   3.77130921e+02,
        #                      3.91905939e+02,   4.04759245e+02,   4.15934844e+02,
        #                      4.25667980e+02,   4.34171408e+02,   4.41630480e+02,
        #                      4.48203393e+02,   4.54023736e+02,   4.59203895e+02],
        #                   [  7.32884096e+00,   1.57622615e+01,   3.50205736e+01,
        #                      6.26638338e+01,   9.59458890e+01,   1.31946663e+02,
        #                      1.68037499e+02,   2.02387848e+02,   2.34126136e+02,
        #                      2.63070337e+02,   2.89321382e+02,   3.13001007e+02,
        #                      3.34187588e+02,   3.52957793e+02,   3.69435922e+02,
        #                      3.83807444e+02,   3.96300382e+02,   4.07156530e+02,
        #                      4.16607966e+02,   4.24863892e+02,   4.32106026e+02,
        #                      4.38489037e+02,   4.44143232e+02,   4.49177884e+02],
        #                   [  5.63138358e+00,   1.37889126e+01,   3.27209676e+01,
        #                      5.99841673e+01,   9.28280418e+01,   1.28330061e+02,
        #                      1.63864189e+02,   1.97609305e+02,   2.28708149e+02,
        #                      2.56996002e+02,   2.82592048e+02,   3.05635535e+02,
        #                      3.26219501e+02,   3.44430801e+02,   3.60399178e+02,
        #                      3.74311475e+02,   3.86394400e+02,   3.96886821e+02,
        #                      4.06017101e+02,   4.13990437e+02,   4.20984534e+02,
        #                      4.27150176e+02,   4.32613996e+02,   4.37481851e+02],
        #                   [  3.85324183e+00,   1.16463152e+01,   3.01568699e+01,
        #                      5.69362395e+01,   8.92277653e+01,   1.24105650e+02,
        #                      1.58947965e+02,   1.91947323e+02,   2.22267194e+02,
        #                      2.49766476e+02,   2.74586992e+02,   2.96887208e+02,
        #                      3.16774399e+02,   3.34344127e+02,   3.49729861e+02,
        #                      3.63118392e+02,   3.74733947e+02,   3.84811582e+02,
        #                      3.93575256e+02,   4.01225597e+02,   4.07935825e+02,
        #                      4.13852424e+02,   4.19097968e+02,   4.23774533e+02],
        #                   [  2.13718686e+00,   9.43554997e+00,   2.73859307e+01,
        #                      5.35326271e+01,   8.51114303e+01,   1.19193604e+02,
        #                      1.53164827e+02,   1.85238036e+02,   2.14605433e+02,
        #                      2.41155947e+02,   2.65057461e+02,   2.86488201e+02,
        #                      3.05568352e+02,   3.22400110e+02,   3.37118585e+02,
        #                      3.49908699e+02,   3.60990741e+02,   3.70594813e+02,
        #                      3.78939568e+02,   3.86220375e+02,   3.92605388e+02,
        #                      3.98236313e+02,   4.03231248e+02,   4.07688109e+02],
        #                   [  7.33588680e-01,   7.35793276e+00,   2.45566707e+01,
        #                      4.98660591e+01,   8.05140818e+01,   1.13571388e+02,
        #                      1.46437695e+02,   1.77355599e+02,   2.05555513e+02,
        #                      2.30962713e+02,   2.53773570e+02,   2.74185459e+02,
        #                      2.92329211e+02,   3.08310836e+02,   3.22264281e+02,
        #                      3.34370215e+02,   3.44843055e+02,   3.53906414e+02,
        #                      3.61772479e+02,   3.68630434e+02,   3.74642663e+02,
        #                      3.79945538e+02,   3.84652238e+02,   3.88856122e+02],
        #                   [  0.00000000e+00,   5.71938542e+00,   2.19175384e+01,
        #                      4.61226952e+01,   7.55563057e+01,   1.07293517e+02,
        #                      1.38757821e+02,   1.68234354e+02,   1.95002759e+02,
        #                      2.19031314e+02,   2.40546658e+02,   2.59763703e+02,
        #                      2.76820545e+02,   2.91823025e+02,   3.04900161e+02,
        #                      3.16225098e+02,   3.26003747e+02,   3.34451202e+02,
        #                      3.41771585e+02,   3.48146687e+02,   3.53732205e+02,
        #                      3.58658509e+02,   3.63033286e+02,   3.66945062e+02],
        #                   [  3.70808850e-01,   4.90321869e+00,   1.97937581e+01,
        #                      4.25634910e+01,   7.04303589e+01,   1.00481800e+02,
        #                      1.30178759e+02,   1.57865243e+02,   1.82884038e+02,
        #                      2.05254029e+02,   2.25233700e+02,   2.43052869e+02,
        #                      2.58852048e+02,   2.72731431e+02,   2.84809846e+02,
        #                      2.95248581e+02,   3.04241515e+02,   3.11992504e+02,
        #                      3.18695525e+02,   3.24523363e+02,   3.29623778e+02,
        #                      3.34120150e+02,   3.38114117e+02,   3.41688761e+02],
        #                   [  2.31344021e+00,   5.32474540e+00,   1.85419273e+01,
        #                      3.94802863e+01,   6.53585457e+01,   9.32869252e+01,
        #                      1.20781519e+02,   1.46266165e+02,   1.69164110e+02,
        #                      1.89554145e+02,   2.07727772e+02,   2.23925545e+02,
        #                      2.38283448e+02,   2.50888470e+02,   2.61842490e+02,
        #                      2.71289150e+02,   2.79405939e+02,   2.86382141e+02,
        #                      2.92399053e+02,   2.97618512e+02,   3.02178693e+02,
        #                      3.06194751e+02,   3.09761163e+02,   3.12954760e+02],
        #                   [  6.30055271e+00,   7.39752482e+00,   1.85119807e+01,
        #                      3.71549362e+01,   6.05513928e+01,   8.58479706e+01,
        #                      1.10638845e+02,   1.33454429e+02,   1.53819591e+02,
        #                      1.71882787e+02,   1.87967735e+02,   2.02318169e+02,
        #                      2.15055729e+02,   2.26244426e+02,   2.35960701e+02,
        #                      2.44323964e+02,   2.51490355e+02,   2.57631101e+02,
        #                      2.62912182e+02,   2.67482629e+02,   2.71469808e+02,
        #                      2.74979440e+02,   2.78097871e+02,   2.80894907e+02],
        #                   [  1.28136495e+01,   1.15294734e+01,   2.00372069e+01,
        #                      3.58451106e+01,   5.61921394e+01,   7.82804446e+01,
        #                      9.98132730e+01,   1.19461154e+02,   1.36873162e+02,
        #                      1.52272805e+02,   1.66008549e+02,   1.78314580e+02,
        #                      1.89285045e+02,   1.98949597e+02,   2.07350209e+02,
        #                      2.14575110e+02,   2.20754496e+02,   2.26038178e+02,
        #                      2.30574904e+02,   2.34499313e+02,   2.37926561e+02,
        #                      2.40951750e+02,   2.43651667e+02,   2.46087309e+02],
        #                   [  2.23503962e+01,   1.81255994e+01,   2.34338895e+01,
        #                      3.57838801e+01,   5.24419977e+01,   7.06957540e+01,
        #                      8.83998545e+01,   1.04402178e+02,   1.18490266e+02,
        #                      1.30954241e+02,   1.42148568e+02,   1.52279420e+02,
        #                      1.61398881e+02,   1.69491329e+02,   1.76555966e+02,
        #                      1.82644035e+02,   1.87854950e+02,   1.92313845e+02,
        #                      1.96149230e+02,   1.99478533e+02,   2.02401624e+02,
        #                      2.04999627e+02,   2.07336457e+02,   2.09461447e+02],
        #                   [  3.53705983e+01,   2.75395058e+01,   2.89606804e+01,
        #                      3.71529005e+01,   4.94368373e+01,   6.32320286e+01,
        #                      7.65954293e+01,   8.85777539e+01,   9.90939493e+01,
        #                      1.08470323e+02,   1.17038393e+02,   1.24956637e+02,
        #                      1.32222963e+02,   1.38768501e+02,   1.44543408e+02,
        #                      1.49556154e+02,   1.53870347e+02,   1.57581549e+02,
        #                      1.60793476e+02,   1.63602204e+02,   1.66088896e+02,
        #                      1.68318342e+02,   1.70340509e+02,   1.72193186e+02],
        #                   [  5.21520175e+01,   3.99558207e+01,   3.67329502e+01,
        #                      4.00376211e+01,   4.72923625e+01,   5.61092566e+01,
        #                      6.47858207e+01,   7.25634886e+01,   7.94374708e+01,
        #                      8.57236062e+01,   9.17012303e+01,   9.74668288e+01,
        #                      1.02957810e+02,   1.08047956e+02,   1.12633909e+02,
        #                      1.16676017e+02,   1.20196468e+02,   1.23256233e+02,
        #                      1.25930479e+02,   1.28291783e+02,   1.30402065e+02,
        #                      1.32310566e+02,   1.34054920e+02,   1.35663350e+02],
        #                   [  7.26696774e+01,   5.53289414e+01,   4.67265627e+01,
        #                      4.44984799e+01,   4.62329405e+01,   4.97849408e+01,
        #                      5.36865930e+01,   5.73086769e+01,   6.06574055e+01,
        #                      6.39935221e+01,   6.75245878e+01,   7.12796118e+01,
        #                      7.51349380e+01,   7.89065273e+01,   8.24352891e+01,
        #                      8.56297847e+01,   8.84669988e+01,   9.09706797e+01,
        #                      9.31865563e+01,   9.51644502e+01,   9.69488926e+01,
        #                      9.85759236e+01,   1.00073224e+02,   1.01461553e+02],
        #                   [  9.67705961e+01,   7.36368466e+01,   5.91007451e+01,
        #                      5.09392353e+01,   4.69636204e+01,   4.52815194e+01,
        #                      4.46000725e+01,   4.43323498e+01,   4.44313127e+01,
        #                      4.50727864e+01,   4.63847465e+01,   4.83303281e+01,
        #                      5.07287738e+01,   5.33413794e+01,   5.59546588e+01,
        #                      5.84253181e+01,   6.06847946e+01,   6.27199828e+01,
        #                      6.45486041e+01,   6.61999768e+01,   6.77038422e+01,
        #                      6.90855651e+01,   7.03650593e+01,   7.15573857e+01],
        #                   [  1.24845595e+02,   9.55774703e+01,   7.48868582e+01,
        #                      6.07477386e+01,   5.12234970e+01,   4.46386076e+01,
        #                      3.97906119e+01,   3.60563558e+01,   3.32915776e+01,
        #                      3.15721624e+01,   3.09466853e+01,   3.13183357e+01,
        #                      3.24566661e+01,   3.40752350e+01,   3.59116836e+01,
        #                      3.77747937e+01,   3.95532740e+01,   4.11995777e+01,
        #                      4.27058649e+01,   4.40834838e+01,   4.53498371e+01,
        #                      4.65217951e+01,   4.76133091e+01,   4.86351491e+01],
        #                   [  1.58724930e+02,   1.23364230e+02,   9.66668656e+01,
        #                      7.68462069e+01,   6.22153374e+01,   5.12566445e+01,
        #                      4.27834111e+01,   3.60841696e+01,   3.08933045e+01,
        #                      2.71810848e+01,   2.49202999e+01,   2.39622559e+01,
        #                      2.40364514e+01,   2.48184691e+01,   2.60057575e+01,
        #                      2.73659483e+01,   2.87498142e+01,   3.00787359e+01,
        #                      3.13219206e+01,   3.24749926e+01,   3.35450154e+01,
        #                      3.45420950e+01,   3.54756445e+01,   3.63532601e+01],
        #                   [  2.02096098e+02,   1.60991518e+02,   1.28706082e+02,
        #                      1.03717776e+02,   8.45641186e+01,   6.98280837e+01,
        #                      5.82907280e+01,   4.91271801e+01,   4.19402994e+01,
        #                      3.65930177e+01,   3.29866932e+01,   3.09287342e+01,
        #                      3.01186260e+01,   3.02046496e+01,   3.08539798e+01,
        #                      3.18010770e+01,   3.28643742e+01,   3.39377878e+01,
        #                      3.49699593e+01,   3.59425770e+01,   3.68538637e+01,
        #                      3.77084533e+01,   3.85123056e+01,   3.92707144e+01],
        #                   [  2.60102473e+02,   2.13760280e+02,   1.76431364e+02,
        #                      1.46865024e+02,   1.23786676e+02,   1.05836025e+02,
        #                      9.17403056e+01,   8.05560546e+01,   7.17531509e+01,
        #                      6.50870435e+01,   6.03904943e+01,   5.74332757e+01,
        #                      5.58935926e+01,   5.54022517e+01,   5.56056851e+01,
        #                      5.62131066e+01,   5.70162276e+01,   5.78849779e+01,
        #                      5.87495024e+01,   5.95788931e+01,   6.03635798e+01,
        #                      6.11036349e+01,   6.18023575e+01,   6.24634016e+01],
        #                   [  3.38522161e+02,   2.87483594e+02,   2.45670994e+02,
        #                      2.12095249e+02,   1.85630446e+02,   1.64944869e+02,
        #                      1.48708349e+02,   1.35866235e+02,   1.25759783e+02,
        #                      1.18037148e+02,   1.12463171e+02,   1.08773738e+02,
        #                      1.06632185e+02,   1.05659878e+02,   1.05490807e+02,
        #                      1.05816156e+02,   1.06406147e+02,   1.07109993e+02,
        #                      1.07841092e+02,   1.08556922e+02,   1.09240821e+02,
        #                      1.09888903e+02,   1.10502360e+02,   1.11083694e+02]]), 'title': 'SCAN2D', 'xlabel': '0(C) - 5(Cl)', 'ylabel': '3(Br) - 0(C)', 'Y': [], 'X': [], 'type': 'matrix'}}
        #                    
        #
        
        #print parameters


