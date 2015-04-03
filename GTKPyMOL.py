#!/usr/bin/env python
text1 = """
#   
#
#   
#   
#
#   
#
#                         ---- GTKDynamo 2.0 ----
#                           
#       
#       Copyright 2012 Jose Fernando R Bachega  <ferbachega@gmail.com>
#
#               visit: https://sites.google.com/site/gtkdynamo/
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#   
#   GTKDynamo team:
#   - Jose Fernando R Bachega   < Univesity of Sao Paulo - SP, Brazil                              >
#   - Troy Wymore               < Pittsburgh Super Computer Center, Pittsburgh PA - USA            >
#   - Martin Field              < Institut de Biologie Structurale, Grenoble, France               >        
#   - Osmar Norbeto de souza    < Pontifical Catholic University of Rio Grande do Sul - RS, Brazil >
#   - Luis Fernando S M Timmers < Pontifical Catholic University of Rio Grande do Sul - RS, Brazil >
#   - Walter R Paixao-Cortes    < Pontifical Catholic University of Rio Grande do Sul - RS, Brazil >
#   - Michele Silva             < Pontifical Catholic University of Rio Grande do Sul - RS, Brazil >     
#                               
#   Special thanks to:          
#   - Fernando V Maluf          < Univesity of Sao Paulo - SP, Brazil                              >
#   - Lucas Assirati            < Univesity of Sao Paulo - SP, Brazil                              >
#   - Leonardo R Bachega        < University of Purdue - West Lafayette, IN - USA                  >
#   - Richard Garratt           < Univesity of Sao Paulo - SP, Brazil                              >
#
#
#   Cite this work as:
#   J. F. R. Bachega, L. F. S. M. Timmers, L. Assirati, L. B. Bachega, M. J. Field, 
#   T. Wymore. J. Comput. Chem. 2013, 34, 2190-2196. DOI: 10.1002/jcc.23346
#
#       
"""


texto_d1 = "\n\n                       -- simple-distance --\n\nFor simple-distance, select two atoms in pymol using the editing mode\nfollowing the diagram:\n\n   R                    R\n    \                  /\n     A1--A2  . . . . A3\n    /                  \ \n   R                    R\n         ^            ^\n         |            |\n        pk1  . . . . pk2\n                d1\n"
texto_d2d1 = "\n                       -- multiple-distance --\n\nFor multiple-distance, select three atoms in pymol using the editing mode\nfollowing the diagram:\n\n   R                    R\n    \                  /\n     A1--A2  . . . . A3\n    /                  \ \n   R                    R\n     ^   ^            ^\n     |   |            |\n    pk1-pk2  . . . . pk3\n       d1       d2\n"


dialog_text = {
    'error_topologies/Parameters': "Error: the topology, parameters or coordinates do not match the system type: ",
    'error_coordiantes': "Error: the coordinates do not match the loaded system.",
    'error_trajectory': "Error: the trajectory does not match the loaded system.",
    'delete': "Delete memory system.",
    'prune': "Warning: this is an irreversible process. Do you want to continue?",
    'qc_region': "Warning: no quantum region has been defined. Would you like to put all atoms in the quantum region?",
    'delete2': "Warning: there is a system loaded in memory. Are you sure that you want to delete it?"
}
#

# System
import datetime
import time
import pygtk
pygtk.require('2.0')
import gtk
import gtk.gtkgl
from pprint import pprint


#import thread
import threading
import gobject
import sys
import glob
import math
import os



# Imports
from OpenGL.GL import *
from OpenGL.GLU import *




if not sys.platform.startswith('win'):
    HOME = os.environ.get('HOME')
else:
    HOME = os.environ.get('PYMOL_PATH')


#GTKDYNAMO_ROOT = os.getcwd()
GTKDYNAMO_ROOT = os.environ.get('GTKDYNAMO_ROOT')

GTKDYNAMO_GUI = os.path.join(GTKDYNAMO_ROOT, "gui")
print GTKDYNAMO_GUI


PDYNAMO_SCRATCH = os.environ.get('PDYNAMO_SCRATCH')
if not os.path.isdir(PDYNAMO_SCRATCH):
    print PDYNAMO_SCRATCH, "not found"
    os.mkdir(PDYNAMO_SCRATCH)
    print "creating: ", PDYNAMO_SCRATCH 
    
GTKDYNAMO_TMP = os.path.join(PDYNAMO_SCRATCH, '.GTKDynamo')
if not os.path.isdir(GTKDYNAMO_TMP):
    os.mkdir(GTKDYNAMO_TMP)
    print "Temporary files directory:  %s" % GTKDYNAMO_TMP



# GUI 
from gui.MinimizationWindow          import *  # window 2  - minimization
from gui.MolecularDynamicsWindow     import *

from gui.FileChooserWindow           import *
from gui.NewProjectDialog            import *
from gui.QuantumChemistrySetupDialog import *

from gui.NonBondDialog               import *
from gui.ScanWindow                  import *
from gui.pDynamoSelectionsWindow     import pDynamoSelectionWindow

from gui.ScanWindow2D                import *

from gui.TrajectoryDialog            import *
from gui.WorkSpaceDialog             import WorkSpaceDialog
from gui.ChargeRescaleDialog         import ChargeRescaleDialog

import TextEditor.TextEditorWindow as TextEditor

from   MatplotGTK.MatplotGTK          import PlotGTKWindow


# pDynamo
from pDynamoProject  import *
from WindowControl   import *
#-------------------------#
#                         #
#   GTKDYNAMO TEMP DIR    #
#                         #
#-------------------------#

# get a temporary file directory
'''
GTKDYNAMO_ROOT is a system variable exported by 
"enviroment_bash.sh" file present into gtkdynamo main folder
GTKDYNAMO_TMP is a temporary folder where logs will be genareted
'''



global slab
slab    = 50
zoom    = 1.0
angle   = 0.0
sprite  = None
zfactor = 0.005
global clicado, ZeroX, ZeroY, Buffer, Zero_ViewBuffer, Menu
clicado = False
ZeroX   = 0
ZeroY   = 0
Buffer  = 0
Zero_pointerx = 0
Zero_pointery = 0
Zero_ViewBuffer = None

Menu =  True





def draw(glarea, event):
    # Get surface and context
    glcontext = glarea.get_gl_context()
    gldrawable = glarea.get_gl_drawable()

    # Start opengl context
    if not gldrawable.gl_begin(glcontext):
        return

    # Actual drawing
    global sprite, angle, zoom

    # Clear screen
    #rabbyt.clear((0.0, 0.0, 0.0))

    # Render sprite
    if sprite is not None:
        sprite.rot = angle
        sprite.scale = zoom
        sprite.render()

    # Flush screen
    gldrawable.swap_buffers()
    pymol.draw()
    # End opengl context
    gldrawable.gl_end()

    return True

# Resizing function


def reshape(glarea, event):

    reshape = event
    reshape_x = reshape.width
    reshape_y = reshape.height
    pymol.reshape(reshape_x, reshape_y, 0)
    pymol.idle()
    # pymol.draw()

    # Get surface and context
    glcontext = glarea.get_gl_context()
    gldrawable = glarea.get_gl_drawable()

    # Start opengl context
    if not gldrawable.gl_begin(glcontext):
        return

    # Get widget dimensions
    x, y, width, height = glarea.get_allocation()

    pymol.reshape(width, height, True)

    # Reset rabbyt viewport
    #rabbyt.set_viewport((width, height))
    # rabbyt.set_default_attribs()

    # End opengl context
    pymol.draw()
    gldrawable.swap_buffers()
    gldrawable.gl_end()
    #

    return True

# Initialization function


def init(glarea):
    print 'init'
    # Get surface and context
    glcontext = glarea.get_gl_context()
    gldrawable = glarea.get_gl_drawable()

    # Start opengl context
    if not gldrawable.gl_begin(glcontext):
        return

    # Get widget dimensions
    x, y, width, height = glarea.get_allocation()

    # Reset rabbyt viewport
    #rabbyt.set_viewport((width, height))
    # rabbyt.set_default_attribs()

    # Get sprite variable
    global sprite

    # Load sprite
    #sprite = rabbyt.Sprite('sprite.png')

    # End opengl context
    gldrawable.gl_end()

    return True

# Idle function


def idle(glarea):
    # Get vars
    global angle, zoom, zfactor

    # Update angle
    angle += 1.0
    if angle > 359:
        angle = 0.0

    # Update zoom
    if zoom > 10 or zoom < 1:
        zfactor = -zfactor
        zoom += zfactor

    # Needed for synchronous updates
    glarea.window.invalidate_rect(glarea.allocation, False)
    glarea.window.process_updates(False)

    return True

# Map events function


def map(glarea, event):
    # print 'map'
    # Add idle event
    gobject.idle_add(idle, glarea)
    return True


def slabchange(button, event):
    global slab
    x, y, width, height = glarea.get_allocation()
    if event.direction == gtk.gdk.SCROLL_UP:
        step = 1.5
        slab = slab + step
        slab = slab + step
        # if  slab >=100:
        #   slab = 100
    else:
        step = -1.5

        slab = slab + step
        if slab <= -5:
            slab = -5
    pymol.cmd.clip('slab', slab)
    #cmd.zoom(buffer = Buffer)
    return step
    pymol.button(button, 0, x, y, 0)
    pymol.idle()


def show_context_menu(widget, event):
    x, y, state = event.window.get_pointer()
    if clicado:
        if event.button == 3:
            widget.popup(None, None, None, event.button, event.time)
    

def mousepress(button, event):
    global ZeroX, ZeroY
    
    ZeroX, ZeroY, state = event.window.get_pointer()
    
    #print ZeroX, ZeroY
    
    x, y, width, height = glarea.get_allocation()

    print event.button
    
    if event.button == 3:
        global clicado
        clicado = True
        x, y, width, height = glarea.get_allocation()
        #print x, y, width, height
        mousepress = event
        button = mousepress.button - 1
        pointerx = int(mousepress.x)
        pointery = int(mousepress.y)
        calc_y = height - pointery
        #print pointerx,pointery,calc_y
        #cmd.zoom(buffer=calc_y)
        pymol.button(button, 0, pointerx , calc_y, 0)



        
    if event.button != 3:
        x, y, width, height = glarea.get_allocation()
        mousepress = event
        button = mousepress.button - 1
        pointerx = int(mousepress.x)
        pointery = int(mousepress.y)
        calc_y = height - pointery
        pymol.button(button, 0, pointerx, calc_y, 0)
    
    if gtkdynamo.builder.get_object('toolbutton6_measure').get_active():
        Distances = DistancesFromPKSelection()
        Angles    = AnglesFromPKSelection()
        Dihedral  = DihedralFromPKSelection()
        gtkdynamo.MeasureToolPutValores(Distances, Angles, Dihedral)
        
        
def mouserelease(button, event):
    x, y, width, height = glarea.get_allocation()
    mouserelease = event
    button = mouserelease.button - 1
    pointerx = int(mouserelease.x)
    pointery = int(mouserelease.y)
    calc_y = height - pointery
    
    if event.button != 3:
        pymol.button(button, 1, pointerx, calc_y, 0)
    
    if event.button == 3:
        #clicado = False
        pymol.button(button, 1, pointerx, calc_y, 0)

    
    
    
def mousemove(button, event):
    global clicado, Buffer,Zero_pointerx, Zero_pointery, Zero_ViewBuffer, Menu
    x, y, width, height = glarea.get_allocation()
    clicado = False
    mousemove = event
    pointerx = int(mousemove.x)
    pointery = int(mousemove.y)

    calc_y2  = (float(Zero_pointery - pointery))/10.0
    calc_y   = height - pointery
    
    #if clicado:
    #    global ZeroY
    #    print 'a'
    #    print clicado
    #    print Menu
    #    Buffer = (calc_y2)
    #    _view   = cmd.get_view()
    #    
    #    print _view
    #    if Zero_ViewBuffer == None:
    #       Zero_ViewBuffer = _view[11]
    #    
    #    _view11 = Zero_ViewBuffer - Buffer
    #    _view15 = _view[15]       - Buffer
    #    _view16 = _view[16]       + Buffer
    #    
    #    _view2 = (_view[0], _view[1], _view[2],
    #             _view[3], _view[4], _view[5],
    #             _view[6], _view[7], _view[8],
    #             _view[9], _view[10],_view11,
    #             _view[12],_view[13],_view[14],
    #             _view15,  _view16,  _view[17])
    #    
    #    print Buffer, _view11, _view15,_view16
    #    cmd.set_view(_view2)
    #    Zero_pointerx   = pointerx
    #    Zero_pointery   = pointery
    #    Zero_ViewBuffer = _view11
    #    pymol.drag(pointerx, calc_y, 0)
    #    pymol.idle()
    #else:
    pymol.drag(pointerx, calc_y, 0)
    pymol.idle()

def my_menu_func(menu):
    print "Menu clicado"

def context_menu():
    builder = gtkdynamo.builder
    menu = builder.get_object('GLArea_menu')
    #menu = gtk.Menu()
    #menu_item = gtk.MenuItem("Sweet menu")
    #menu_item.connect(
    #    'activate', gtkdynamo.on_MainMenu_File_NewProject_activate)
    #menu.append(menu_item)
   #menu_item.show()
   #menu_item = gtk.MenuItem("Salty menu")
   #menu.append(menu_item)
   #menu_item.show()
    return menu


# Create opengl configuration
try:
    # Try creating rgb, double buffering and depth test modes for opengl
    glconfig = gtk.gdkgl.Config(mode=(gtk.gdkgl.MODE_RGB |
                                      gtk.gdkgl.MODE_DOUBLE |
                                      gtk.gdkgl.MODE_DEPTH))
except:
    # Failed, so quit
    sys.exit(0)


class gtkdynamo_main():

    def testGTKMatplotLib(self, button):
        """ Function doc """
        import gtk

        from matplotlib.figure import Figure
        from numpy import arange, sin, pi

        # uncomment to select /GTK/GTKAgg/GTKCairo
        #from matplotlib.backends.backend_gtk import FigureCanvasGTK as FigureCanvas
        from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas
        #from matplotlib.backends.backend_gtkcairo import FigureCanvasGTKCairo as FigureCanvas
        from matplotlib.backends.backend_gtkagg import NavigationToolbar2GTKAgg as NavigationToolbar

        #win = gtk.Window()
        #win.connect("destroy", lambda x: gtk.main_quit())
        # win.set_default_size(400,300)
        #win.set_title("Embedding in GTK")
        box = self.builder.get_object('vbox4')
        self.graph = box

        f = Figure(figsize=(5, 4), dpi=100)
        a = f.add_subplot(111)
        #t = arange(0.0,3.0,0.01)
        #s = sin(2*pi*t)
        t = range(0, 10)
        s = range(0, 10)

        t = [0,
             5,
             10,
             15,
             20,
             25,
             30,
             35,
             40,
             45,
             50,
             55,
             60,
             65,
             70,
             75,
             80,
             85,
             90,
             95,
             100,
             105,
             110,
             115,
             120,
             125,
             130,
             135,
             140,
             145,
             150,
             155,
             160,
             165,
             170,
             175,
             180,
             185,
             190,
             195,
             200]

        s = [-913.53086808,
             -1978.05074306,
             -2218.21815405,
             -2333.01919415,
             -2391.82858579,
             -2435.17776079,
             -2486.44564867,
             -2543.07423428,
             -2571.71716511,
             -2598.62940311,
             -2616.98004127,
             -2631.60794731,
             -2648.00535887,
             -2661.72725012,
             -2675.65233140,
             -2686.34375946,
             -2696.94907090,
             -2708.65130605,
             -2718.73853503,
             -2726.36193409,
             -2732.59504750,
             -2737.83623730,
             -2742.33435229,
             -2745.28712806,
             -2748.82036113,
             -2752.12502818,
             -2754.57566090,
             -2756.97531091,
             -2758.83136980,
             -2760.53521449,
             -2762.79017667,
             -2764.47319544,
             -2765.99011566,
             -2767.77186148,
             -2770.20329165,
             -2772.66204338,
             -2775.05818125,
             -2776.97966619,
             -2779.02106271,
             -2781.43441141,
             -2783.70324049]

        a.plot(t, s, 'ko', t, s, 'k')
        #a.plot(x, y, 'ko',x, y,'k')
        canvas = FigureCanvas(f)  # a gtk.DrawingArea
        self.graph.pack_start(canvas)
        toolbar = NavigationToolbar(canvas, self.graph)
        self.graph.pack_end(toolbar, False, False)
        self.graph.show_all()
        # gtk.main()

    
    '''
    #--------------------------------------------#
    #                GL AREA MENU                #
    #--------------------------------------------#  
    '''
    
    def on_GLAreaMenu_itemActive_SetQCTable(self, menuitem, click = None):    
        table    = PymolGetTable('sele')
        oldTable = self.project.settings['qc_table']
        self.project.put_qc_table(table)
        newTable = self.project.settings['qc_table']
        
        if newTable != oldTable:
            '''
                                                      d i a l o g
                                             #  -  I M P O R T A N T  -  #                                   
                                #---------------------------------------------------------#                  
                                #                                                         #                  
                                #        Message Dialog  -  when 2 buttons will be shown  #                  
                                #  1 -create the warning message                          #                  
                                #  2 -hide the actual dialog - optional                   #                  
                                #  3 -show the message dialog                             #                  
                                #  4 -hide the message dialog                             #                  
                                #  5 -check the returned valor by the message dialog      #                  
                                #  6 -do something                                        #                  
                                #  7 -restore the actual dialog - optional                #                  
                                #---------------------------------------------------------#                  
            '''
                                                                                                  
            self.builder.get_object('MessageDialogQuestion').format_secondary_text("A new quantum region has been defined. Would you like setup your QC paramaters now?")  
            dialog = self.builder.get_object('MessageDialogQuestion')                                         
                                                                                                              
            a = dialog.run()  # possible "a" valors                                                           
            # 4 step          # -8  -  yes                                                                    
            dialog.hide()     # -9  -  no                                                                     
                              # -4  -  close                                                                  
                              # -5  -  OK                                                                     
                              # -6  -  Cancel                                                                 
                                                                                                              
            # 5 step                                                                                          
            if a == -8:                                                                                       
                # 6 step                                                                                      
                self.QuantumChemistrySetupDialog.dialog.run()
                self.QuantumChemistrySetupDialog.dialog.hide()                                                                                   
            else:                                                                                             
                return 0                                                                                      
            # 7 step                                                                                          
            #self.load_trj_windows.run()                                                                      
        else:                                                                                                 
            pass                                                                                   




        print self.project.settings['qc_table']

    def on_GLAreaMenu_itemActive_CleanQCTable(self, menuitem, click = None):    
        self.project.clean_qc_table()
        print self.project.settings['qc_table']

    def on_GLAreaMenu_itemActive_SetFixTable(self, menuitem, click=None):
        table = PymolGetTable('sele')
        self.project.put_fix_table(table)
        print self.project.settings['fix_table']

    def on_GLAreaMenu_itemActive_CleanFixTable(self, menuitem, click=None):
        self.project.clean_fix_table()
        print self.project.settings['fix_table']

    def on_GLAreaMenu_itemActive_SetPruneTable(self, menuitem, click=None):
        print "aqui"
        table = PymolGetTable('sele')
        '''
                                                  d i a l o g
                                         #  -  I M P O R T A N T  -  #                                   
                            #---------------------------------------------------------#                  
                            #                                                         #                  
                            #        Message Dialog  -  when 2 buttons will be showed #                  
                            #  1 -create the warning message                          #                  
                            #  2 -hide the actual dialog - optional                   #                  
                            #  3 -show the message dialog                             #                  
                            #  4 -hide the message dialog                             #                  
                            #  5 -check the returned valor by the message dialog      #                  
                            #  6 -do something                                        #                  
                            #  7 -restore the actual dialog - optional                #                  
                            #---------------------------------------------------------#                  
        '''
                                                                                              
        self.builder.get_object('MessageDialogQuestion').format_secondary_text("Warning: Prune the system is an irreversible process. Do you want to continue?")  
        dialog = self.builder.get_object('MessageDialogQuestion')                                         
                                                                                                          
        a = dialog.run()  # possible "a" valors                                                           
        # 4 step          # -8  -  yes                                                                    
        dialog.hide()     # -9  -  no                                                                     
                          # -4  -  close                                                                  
                          # -5  -  OK                                                                     
                          # -6  -  Cancel                                                                 
                                                                                                          
        # 5 step                                                                                          
        if a == -8:                                                                                       
            # 6 step 
            self.project.put_prune_table(table)
            print self.project.settings['prune_table']                                                                                     
            #self.QuantumChemistrySetupDialog.dialog.run()
            #self.QuantumChemistrySetupDialog.dialog.hide()                                                                                   
        else:                                                                                             
            return 0                                                                                      

    def on_GLAreaMenu_PutLalbel_itemActive(self, menuitem, click=None):
        """ Function doc """
        print 'teste'
        
        
        string = ""
        showTable = []
        
        if self.builder.get_object('menuitem_index').get_active():
            showdic.append('index')
        
        if self.builder.get_object('menuitem_atom_name').get_active():
            showdic.append('name')

        if self.builder.get_object('menuitem_residue_name').get_active():
            showdic.append('resn')

        if self.builder.get_object('menuitem_residue_number').get_active():
            showdic.append('resi')
            
        if self.builder.get_object('menuitem_partial_charge').get_active():
            showdic.append('partial_charge')
        
        if item in showTable:
            string = string + item +','

       
        cmd.label('sele', string)
        #if menu

    '''                                            
    #      ---------------------------------  
    #              MAIN MENU  methods    
    #      ---------------------------------
    
    '''
    def on_MainMenu_File_Import_menuitemImportTrajectory_activate (self, menuitem):
        """ Function doc """
        self.TrajectoryDialog.builder.get_object('filechooserbutton1').set_filename(self.project.settings['data_path'])
        self.TrajectoryDialog.builder.get_object('filechooserbutton2').set_filename(self.project.settings['data_path'])
        self.TrajectoryDialog.dialog.run()
        self.TrajectoryDialog.dialog.hide()

    def on_MainMenu_View_menuitemShowValences_activate(self, button):
        print """ Function doc """
        if self.builder.get_object('ShowValences').get_active() == True:
            #cmd.set('valence', 0.1)
            cmd.do('set valence, 0.1')
        else:
            #cmd.set('valence', 0.0)
            cmd.do('set valence, 0.0')

    def on_MainMenu_File_NewProject_activate(self, button):
        """ Function doc """
        localtime = time.asctime(time.localtime(time.time()))
        #print "Local current time :", localtime
        localtime = localtime.split()        
        #  0     1    2       3         4
        #[Sun] [Sep] [28] [02:32:04] [2014]
        text = 'NewProjec_' + localtime[1] + \
            '_' + localtime[2] + '_' + localtime[4]
        self._NewProjectDialog.builder.get_object("new_project_entry").set_text(text)
        
        
        WorkSpace = self.GTKDynamoConfig['WorkSpace']
        path      = os.path.join(WorkSpace, text)
        self._NewProjectDialog.builder.get_object("ProjectDirectory").set_text(path)

        self._NewProjectDialog.dialog.run()
        self._NewProjectDialog.dialog.hide()

    def on_MainMenu_File_OpenFileChooserWindow_clicked(self, button):
        """ Function doc """

        FileChooser = FileChooserWindow()
        FileName = FileChooser.GetFileName(self.builder)
        print FileName
        try:
            _FileType = GetFileType(FileName)

            if _FileType in ['pkl', 'yaml']:
                self.project.load_coordinate_file_as_new_system(FileName)
                self.project.From_PDYNAMO_to_GTKDYNAMO(type_='new')
            
            if _FileType in ['gtkdyn']:
                self.project.load_GTKDYNAMO_project(FileName)
                try:
                    if self.project.settings['edit_mode_button'] == True:
                        self.builder.get_object('togglebutton1').set_active (1)
                    else:
                        self.builder.get_object('togglebutton1').set_active (0)
                except:
                    pass
                
        except:
            pass

    
    def on_imagemenuitem9_activate (self, menuitem):
        """ Function doc """
        self.ChargeRescaleDialog.dialog.run()
        self.ChargeRescaleDialog.dialog.hide()
    
    
    #def on_MainMenu_Calculate_menuitemScan1D_activate(self, menuItem):
    #    """ Function ChargeRescaleDialogdoc """
    #    self.ScanDialog.dialog.run()
    #    self.ScanDialog.dialog.hide()  
    
    def on_MainMenu_Calculate_menuitemScan1D_activate(self, menuitem):
        """ Function doc """
        
        if self.ScanWindow.Visible == False:
            self.ScanWindow.OpenWindow()
        
        
        #try:
        #    _FileType = GetFileType(FileName)
        #
        #    if _FileType in ['pkl', 'yaml']:
        #        self.project.load_coordinate_file_as_new_system(FileName)
        #        self.project.From_PDYNAMO_to_GTKDYNAMO(type_='new')
        #except:
        #    pass
    
    
    def on_MainMenu_Calculate_menuitemScan2D_activate(self, menuItem):
        if self.ScanWindow2D.Visible == False:
            self.ScanWindow2D.OpenWindow()

    def on_MainMenu_Edit_menuitemNonBondingModels_activate(self, button):
        """ Function doc """
        self.NonBondDialog.dialog.run()
        self.NonBondDialog.dialog.hide()



    '''                                            
    #      ---------------------------------  
    #              TOOL BAR  methods    
    #      ---------------------------------
    
    '''
    def on_toolbutton7_print_tudo_clicked (self, button):
        """ Function doc """
        pprint(self.project.settings)
        cell = self.project.importCellParameters()
        print cell
        #self.project.Save_Project_To_File()

    def on_ToolBar_buttonSave_As_Project_clicked(self, button):
        _01_window_main = self.builder.get_object("win")
        data_path       = self.project.settings['data_path']

        filename = None

        chooser = gtk.FileChooserDialog("Save File...",   _01_window_main ,
                                        gtk.FILE_CHOOSER_ACTION_SAVE         ,
                                       (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, 
                                        gtk.STOCK_SAVE, gtk.RESPONSE_OK))

 
 
 
        chooser.set_current_folder(data_path)
        response = chooser.run()
        if response == gtk.RESPONSE_OK: filename = chooser.get_filename()
        chooser.destroy()

        #return filename	        
                

        self.project.Save_Project_To_File (filename, 'pkl')
    
    
    def on_toolbar_showCell_toggled (self, button):
        """ Function doc """
        
        if button.get_active():
            self.project.ShowCell = True
        
        else:
            self.project.ShowCell = False
            # print '# If control reaches here, the toggle button is up'
            #self.builder.get_object('notebook3').hide()
        self.project.SystemCheck()
    
    def on_ToolBar_buttonSaveProject_clicked(self, button):
        """ Function doc """
        _01_window_main = self.builder.get_object("win")
        data_path       = self.project.settings['data_path']
        
        filename = None
        
        
        if 'filename' in self.project.settings:
            pass
        else:
            self.project.settings['filename'] = None
        
        
        if self.project.settings['filename'] == None:
            chooser = gtk.FileChooserDialog("Save File...",   _01_window_main ,
                                            gtk.FILE_CHOOSER_ACTION_SAVE         ,
                                           (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, 
                                            gtk.STOCK_SAVE, gtk.RESPONSE_OK))
            chooser.set_current_folder(data_path)
            response = chooser.run()
            if response == gtk.RESPONSE_OK: filename = chooser.get_filename()
            chooser.destroy()

            self.project.Save_Project_To_File (filename, 'pkl')
        else:
            filename = self.project.settings['filename']
            self.project.Save_Project_To_File (filename, 'pkl')
    
    
    def on_ToolBar_buttonMeasure_toggled (self, button):
        """ Function doc """
        if button.get_active():
            # print '# If control reaches here, the toggle button is down'
            self.builder.get_object('notebook3').show()
            self.builder.get_object('togglebutton1').set_active (1)
        else:
            # print '# If control reaches here, the toggle button is up'
            self.builder.get_object('notebook3').hide()
            
    
    def on_ToolBar_buttonpDynamoSelections_clicked(self, button):
        """ Function doc """
        if self.project.system == None:
            print 'system empty'
        else:
            if self.pDynamoSelectionWindow.Visible == False:
                self.pDynamoSelectionWindow.OpenWindow()  
    
    def on_ToolBar_buttonCheckSystem_clicked(self, button):
        """ Function doc """
        filein = self.project.SystemCheck()
        #filein = self.project.settings['job_history'][self.selectedID]['log']
        editor = TextEditor.GTKDynamoTextEditor(filein)
        #editor.load_file(filein)





    def on_ToolBar_buttonSinglePoint_clicked(self, button):
        """ Function doc """
        energy = self.project.ComputeEnergy()
        self.builder.get_object('EnergyMessageDialog').format_secondary_text("Total energy: " + str(energy) + " KJ/mol")   
        dialog = self.builder.get_object('EnergyMessageDialog')
        dialog.run()                                                                
        dialog.hide()
        
            

    def on_ToolBar_buttonQuantumChemistrySetup_clicked(self, button):
        """ Function doc """
        self.QuantumChemistrySetupDialog.dialog.run()
        self.QuantumChemistrySetupDialog.dialog.hide()

    def on_ToolBar_buttonOptmizationSetup_clicked(self, button):
        """ Function doc """
        print self.project.settings['step']
        text = str(self.project.settings['step'] + 1) + '_step_GeometryOptmization'
        self._02MinimizationWindow.builder.get_object(
            "02_window_entry_traj_name").set_text(text)
        self._02MinimizationWindow.dialog.run()
        self._02MinimizationWindow.dialog.hide()

    def on_ToolBar_buttonMolecularDynamicsSetup_clicked (self, button):
        """ Function doc """
        print self.project.settings['step']
        text = str(self.project.settings['step'] + 1) + '_step_MolecularDynamics'
        self.MolecularDynamicsWindow.builder.get_object("MMDialog_entry_trajectory_name").set_text(text)
        self.MolecularDynamicsWindow.dialog.run()
        self.MolecularDynamicsWindow.dialog.hide()
        
    def on_ToolBar_togglebbuttonChangeSelectionMode_toggled(self, button):
        if self.builder.get_object('togglebutton1').get_active():
            # print '# If control reaches here, the toggle button is down'
            self.builder.get_object('togglebutton1').set_label('Editing')
            self.builder.get_object('label_viewing').set_label('Picking')
            self.builder.get_object('combobox1').set_sensitive(False)
            cmd.edit_mode(1)
            self.project.settings['edit_mode_button'] = True

        else:
            # print '# If control reaches here, the toggle button is up'

            self.builder.get_object('togglebutton1').set_label('Viewing')
            self.builder.get_object('label_viewing').set_label('Selecting')
            self.builder.get_object('combobox1').set_sensitive(True)
            cmd.edit_mode(0)
            self.project.settings['edit_mode_button'] = False

    def on_ToolBar_comboboxChangeSelectionMode_changed(self, button):
        """ Function doc """
        mode = self.builder.get_object('combobox1').get_active_text()
        if mode == "Atom":
            cmd.set("mouse_selection_mode", 0)
        if mode == "Residue":
            cmd.set("mouse_selection_mode", 1)
        if mode == "Chain":
            cmd.set("mouse_selection_mode", 2)
        if mode == "Molecule":
            cmd.set("mouse_selection_mode", 5)

    def on_ToolBar_toolbutton_ClearSystemInMemory_clicked (self, button):
        """ Function doc """
        if self.project.system != None:
            '''
                                                      d i a l o g
                                             #  -  I M P O R T A N T  -  #                                   
                                #---------------------------------------------------------#                  
                                #                                                         #                  
                                #        Message Dialog  -  when 2 buttons will be showed #                  
                                #  1 -create the warning message                          #                  
                                #  2 -hide the actual dialog - optional                   #                  
                                #  3 -show the message dialog                             #                  
                                #  4 -hide the message dialog                             #                  
                                #  5 -check the returned valor by the message dialog      #                  
                                #  6 -do something                                        #                  
                                #  7 -restore the actual dialog - optional                #                  
                                #---------------------------------------------------------#                  
            '''
                                                                                                  
            self.builder.get_object('MessageDialogQuestion').format_secondary_text("Warning: there is a system loaded in memory. Are you sure that you want to delete it?")  
            dialog = self.builder.get_object('MessageDialogQuestion')                                         
                                                                                                              
            a = dialog.run()  # possible "a" valors                                                           
            # 4 step          # -8  -  yes                                                                    
            dialog.hide()     # -9  -  no                                                                     
                              # -4  -  close                                                                  
                              # -5  -  OK                                                                     
                              # -6  -  Cancel                                                                 
                                                                                                              
            # 5 step                                                                                          
            if a == -8:                                                                                       
				# 6 step 
				#--------------------------------------------------GTKDynamo project---------------------------------------------------------#
				self.project = None
				self.project = pDynamoProject(data_path  =GTKDYNAMO_TMP, 
											  builder=self.builder, 
											  window_control=self.window_control)                                   

				self.project.PyMOL = True                                                                                                    #
				#----------------------------------------------------------------------------------------------------------------------------#  

				cmd.delete('all')
				pymol_objects  = cmd.get_names()
				liststore = self.builder.get_object('liststore2')
				self.project.window_control.TREEVIEW_ADD_DATA2(liststore, self.project.settings['job_history'] , None)
				
				
				self.project.SystemCheck()
				#cmd.delete('all')                                                                                  
            else:                                                                                             
                return 0 



    '''                                            
    #      ---------------------------------  
    #           PyMOL TREEVIEW  methods    
    #      ---------------------------------
    
    '''   
    def on_menuitem_pink_activate(self, item):
        """ Function doc """
        print 'on_menuitem_pink_activate'
    
    def on_treeview2_show_logFile (self, item):
        """ Function doc """
        #pprint(self.project.settings['job_history'][self.selectedID]['log'])
        filein = self.project.settings['job_history'][self.selectedID]['log']
        print    self.project.settings['job_history'][self.selectedID]['log']
        editor = TextEditor.GTKDynamoTextEditor(filein)
        #editor.load_file(filein)

    def on_menuitem_PlotLogFile_activate(self, item):
        """ Function doc """
        filein = self.project.settings['job_history'][self.selectedID]['log']
        print    self.project.settings['job_history'][self.selectedID]['log']
        X,Y = ParseProcessLogFile(filein)
        
        xlabel = 'Frames'
        ylabel = 'Energy (KJ)' 
        title  = os.path.split(filein)[-1]
        print  X, Y
        
        parameters = {
                     'title' : title ,
                     'X'     : X     ,
                     'Y'     : Y     ,
                     'xlabel': xlabel,
                     'ylabel': ylabel,
                     }
        
        PlotGTKWindow(parameters)


    def on_color_items_activate (self, item, event):
        """ Function doc """
        #print 'view log'
        #pprint(self.project.settings['job_history'][self.selectedID])
        
        PyMOL_Obj = self.selectedObj
        
        if item == self.builder.get_object('menuitem_black'):
            cmd.color('grey10',PyMOL_Obj)
            cmd.util.cnc(PyMOL_Obj)
        
        if item == self.builder.get_object('menuitem_green'):
            cmd.util.cbag(PyMOL_Obj)
        
        if item == self.builder.get_object('menuitem_cyan'):
            cmd.util.cbac(PyMOL_Obj)
        
        if item == self.builder.get_object('menuitem_magenta'):
            cmd.util.cbam(PyMOL_Obj)
        
        if item == self.builder.get_object('menuitem_yellow'):
            cmd.util.cbay(PyMOL_Obj)
        
        if item == self.builder.get_object('menuitem_salmon'):
            cmd.util.cbas(PyMOL_Obj)
        
        if item == self.builder.get_object('menuitem_white'):
            cmd.util.cbaw(PyMOL_Obj)
        
        if item == self.builder.get_object('menuitem_slate'):
            cmd.util.cbab(PyMOL_Obj)
        
        if item == self.builder.get_object('menuitem_orange'):
            cmd.util.cbao(PyMOL_Obj)
        
        if item == self.builder.get_object('menuitem_purple'):
            cmd.util.cbap(PyMOL_Obj)
        
        if item == self.builder.get_object('menuitem_pink'):
            cmd.util.cbak(PyMOL_Obj)


    def on_treeview_PyMOL_Objects_button_release_event(self, tree, event):
        if event.button == 3:
            #print "Mostrar menu de contexto botao3"
            selection     = tree.get_selection()
            model         = tree.get_model()
            (model, iter) = selection.get_selected()
            if iter != None:
                self.selectedID  = str(model.get_value(iter, 1))  # @+
                self.selectedObj = str(model.get_value(iter, 2))
                self.builder.get_object('TreeViewObjLabel').set_label('- ' +self.selectedObj+' -' )
                
                widget = self.builder.get_object('treeview_menu')
                widget.popup(None, None, None, event.button, event.time)
            
        if event.button == 1:
            #print "Mostrar menu de contexto botao1"
            selection     = tree.get_selection()
            model         = tree.get_model()
            (model, iter) = selection.get_selected()
            
            if iter != None:
                #print model, iter
                pymol_object  = model.get_value(iter, 2)  # @+
                true_or_false = model.get_value(iter, 0)
                #print pymol_object
                if true_or_false == False:
                    cmd.enable(pymol_object)
                    true_or_false = True
                    model.set(iter, 0, true_or_false)
                    # print true_or_false
                
                else:
                    cmd.disable(pymol_object)
                    true_or_false = False
                    model.set(iter, 0, true_or_false)

    
    def on_treeview_PyMOL_Selections_button_release_event (self, tree, event):
        """ Function doc """
        selection     = tree.get_selection()
        model         = tree.get_model()
        (model, iter) = selection.get_selected()
        pymol_object = model.get_value(iter, 0)  

        string2 = 'select sele, '+ pymol_object
        cmd.do(string2)
        cmd.enable('sele')
    

    def handle_history_click(self, tree, event):
        if event.button == 3:
            print "Mostrar menu de contexto botao3"
       
        if event.button == 1:
            print "Mostrar menu de contexto botao1"

     
    def on_treeview2_select_cursor_parent (self, tree, path, column):
        """ Function doc """
        print 'select_cursor_parent' 
    
    def handle_history_keypress(self, widget, event):
        if gtk.gdk.keyval_name(event.keyval) == 'Delete':
            print 'Excluir item'

    def on_treeview2_select(self, tree, path, column):
        print "aqui keybord"
    
  
    def on_treeview2_select_cursor_row (self, tree, path, column):
        """ Function doc """
        print "aqui select_cursor_row"

    def  on_treeviewcolumn2_clicked(self, column):
        """ Function doc """
        print 'treeviewcolumn2_clicked'
 
    def on_cellrenderertoggle1_toggled (self, cell, path):
        """ Function doc """
        print 'cellrenderertoggle1'
        """
        Sets the toggled state on the toggle button to true or false.
        """
        print cell, path
        #model[path][1] = not model[path][1]
        #print "Toggle '%s' to: %s" % (model[path][0], model[path][1],)
        #return

    #def on_treeview2_select_cursor_row2 (self, tree, path, column):
    #   """ Function doc """
    #   print "Mostrar menu de contexto botao1"
    #   selection     = tree.get_selection()
    #   model         = tree.get_model()
    #   (model, iter) = selection.get_selected()
    #   pymol_object  = model.get_value(iter, 2)  # @+
    #   true_or_false = model.get_value(iter, 0)
    #   
    #   print pymol_object, true_or_false
    
    
    def  on_treeview2_select_cursor_parent(self, tree, path, column):
        """ Function doc """
        model = tree.get_model()  # @+
        iter = model.get_iter(path)  # @+
        pymol_object = model.get_value(iter, 2)  # @+
        true_or_false = model.get_value(iter, 0)
        # atomtype = model.get_value( iter, 2) #@+
        # print true_or_false

        if true_or_false == False:
            cmd.enable(pymol_object)
            true_or_false = True
            model.set(iter, 0, true_or_false)
            # print true_or_false

        else:
            cmd.disable(pymol_object)
            true_or_false = False
            model.set(iter, 0, true_or_false)
            # print true_or_false
    
    def row_activated(self, tree, path, column):

        model = tree.get_model()   
        iter = model.get_iter(path)  
        pymol_object = model.get_value(iter, 0)  

        string2 = 'select sele, '+ pymol_object
        cmd.do(string2)
        cmd.enable('sele')
    
    def row_activated2(self, tree, path, column):
        model = tree.get_model()  # @+
        iter = model.get_iter(path)  # @+
        ID = model.get_value(iter, 1)  # @+
        pprint (self.project.settings['job_history'][ID])

        
        #true_or_false = model.get_value(iter, 0)
        ## atomtype = model.get_value( iter, 2) #@+
        ## print true_or_false
        #
        #if true_or_false == False:
        #    cmd.enable(pymol_object)
        #    true_or_false = True
        #    model.set(iter, 0, true_or_false)
        #    # print true_or_false
        #
        #else:
        #    cmd.disable(pymol_object)
        #    true_or_false = False
        #    model.set(iter, 0, true_or_false)
        #    # print true_or_false
    


    '''                                            
    #      ---------------------------------  
    #           PyMOL COMMAND LINE    
    #      ---------------------------------
    
    '''

    def on_PyMOLCommandLine_entry1_activate(self, button):
        """ Function doc """
        command = self.builder.get_object('entry1').get_text()
        print command
        cmd.do(command)


    
    '''                                            
    #      ---------------------------------  
    #          TrajectoryTool  methods    
    #      ---------------------------------
    
    ''' 
    def on_TrajectoryTool_Entry_Push(self, entry, data=None):
		self.on_TrajectoryTool_HSCALE_update()	

    def on_TrajectoryTool_HSCALE_update (self):
        """ Function doc """
        MAX  = int(self.builder.get_object('trajectory_max_entrey').get_text())
        MIN  = int(self.builder.get_object('trajectory_min_entrey').get_text())

        scale = self.builder.get_object("trajectory_hscale")
        scale.set_range(MIN, MAX)
        scale.set_increments(1, 10)
        scale.set_digits(0)

    def on_TrajectoryTool_BarSetFrame(self, hscale, text= None,  data=None):            # SETUP  trajectory window
        valor = hscale.get_value()
        cmd.frame( int (valor) )
        BondTable = self.project.BondTable
        
        if self.builder.get_object('checkbutton_DynamicBonds').get_active():
            lista     = self.project.settings['dynamic_list']
            PyMOL_Obj = self.project.settings['PyMOL_Obj']
            #print lista, PyMOL_Obj
            for i in lista:
                for j in lista: 
                    if i != j:
                        #print i, j 
                        #bond_unbond1 = self.project.BondTable[i+1,j+1][1]
                        #Rcov         = self.project.BondTable[i+1,j+1][0]
                        #print lista[i], lista[j]
                        #print bond_unbond1, Rcov
                        
                        dist         = cmd.get_distance(PyMOL_Obj+' and index '+ str(i+1), 
                                                        PyMOL_Obj+' and index '+ str(j+1), 
                                                        int (valor) )
                        
                        if dist > self.project.BondTable[i+1,j+1][0]:
                            cmd.unbond(PyMOL_Obj+' and index '+ str(i+1), 
                                       PyMOL_Obj+' and index '+ str(j+1))
                        else:
                            cmd.bond(PyMOL_Obj+' and index '+ str(i+1), 
                                     PyMOL_Obj+' and index '+ str(j+1))

        if self.builder.get_object('toolbutton6_measure').get_active():
            selections = cmd.get_names("selections")
            Distances  = DistancesFromPKSelection(selections)
            Angles     = AnglesFromPKSelection(selections)
            Dihedral   = DihedralFromPKSelection(selections)
            self.MeasureToolPutValores(Distances, Angles, Dihedral)

        
    
    
    
    def MeasureToolPutValores(self, distances = None, angles = None, dihedral = None):
        if distances != None:
            if distances['pk1pk2'] != None:
                self.builder.get_object('pk1pk2').set_sensitive(True)
                self.builder.get_object('pk1pk2').set_text(distances['pk1pk2'])
            else:
                self.builder.get_object('pk1pk2').set_sensitive(False)
                self.builder.get_object('pk1pk2').set_text('')
                
                
            if distances['pk1pk3'] != None:
                self.builder.get_object('pk1pk3').set_sensitive(True)
                self.builder.get_object('pk1pk3').set_text(distances['pk1pk3'])
            else:
                self.builder.get_object('pk1pk3').set_sensitive(False)
                self.builder.get_object('pk1pk3').set_text('')
                
                
            if distances['pk1pk4'] != None:
                self.builder.get_object('pk1pk4').set_sensitive(True)
                self.builder.get_object('pk1pk4').set_text(distances['pk1pk4'])
            else:
                self.builder.get_object('pk1pk4').set_sensitive(False)
                self.builder.get_object('pk1pk4').set_text('')
                
                
            if distances['pk2pk3'] != None:
                self.builder.get_object('pk2pk3').set_sensitive(True)
                self.builder.get_object('pk2pk3').set_text(distances['pk2pk3'])
            else:
                self.builder.get_object('pk2pk3').set_sensitive(False)
                self.builder.get_object('pk2pk3').set_text('')

            if distances['pk2pk4'] != None:
                self.builder.get_object('pk2pk4').set_sensitive(True)
                self.builder.get_object('pk2pk4').set_text(distances['pk2pk4'])
            else:
                self.builder.get_object('pk2pk4').set_sensitive(False)
                self.builder.get_object('pk2pk4').set_text('')
                 
            if distances['pk3pk4'] != None:
                self.builder.get_object('pk3pk4').set_sensitive(True)
                self.builder.get_object('pk3pk4').set_text(distances['pk3pk4'])
            else:
                self.builder.get_object('pk3pk4').set_sensitive(False)   
                self.builder.get_object('pk3pk4').set_text('')

        if  angles != None:
            if angles['pk1pk2pk3'] != None:
                self.builder.get_object('pk1pk2pk3').set_sensitive(True)
                self.builder.get_object('pk1pk2pk3').set_text(angles['pk1pk2pk3'])
            else:
                self.builder.get_object('pk1pk2pk3').set_sensitive(False)
                self.builder.get_object('pk1pk2pk3').set_text('')


            if angles['pk2pk3pk4'] != None:
                self.builder.get_object('pk2pk3pk4').set_sensitive(True)
                self.builder.get_object('pk2pk3pk4').set_text(angles['pk2pk3pk4'])
            else:
                self.builder.get_object('pk2pk3pk4').set_sensitive(False) 
                self.builder.get_object('pk2pk3pk4').set_text('')
        #print dihedral
        if  dihedral != None:
            if dihedral['pk1pk2pk3pk4'] != None:
                self.builder.get_object('pk1pk2pk3pk4').set_sensitive(True)
                self.builder.get_object('pk1pk2pk3pk4').set_text(dihedral['pk1pk2pk3pk4'])
            else:
                self.builder.get_object('pk1pk2pk3pk4').set_sensitive(False)

    
    def Save_GTKDYNAMO_ConfigFile (self, filename = None):
        """ Function doc """
        path = os.path.join(self.home,'.config')
        if not os.path.exists (path): 
            os.mkdir (path)

        path = os.path.join(path, 'GTKDynamo')
        if not os.path.exists (path): 
            os.mkdir (path)
        
        filename = os.path.join(path,'gtkdynamo.config')
        json.dump(self.GTKDynamoConfig, open(filename, 'w'), indent=2)
        

    def Load_GTKDYNAMO_ConfigFile (self, filename = None):
        """ Function doc """
        #.config
        path = os.path.join(self.home,'.config', 'GTKDynamo', 'gtkdynamo.config')
        
        try:
            self.GTKDynamoConfig = json.load(open(path)) 
        except:
            print 'error: GTKDynamo config file not found'
            print 'open WorkSpace Dialog'
        

    def on_button_ImportPKSelectionToDynamicList_activate (self, button):
        """ Function doc """
        
        
        text = ''
        atoms = []
        #print 'aqui'
        DynamicList = []
        try:
            atom1 = PymolGetTable('pk1')
            DynamicList.append(atom1[0])
            model = cmd.get_model('pk1') 
            atoms  = model.atoms

            for i in atoms:
                print i 
                name  = i.name
                print name
            
            print 'depois'

            
        except:
            pass
        try:
            atom2 = PymolGetTable('pk2')
            DynamicList.append(atom2[0])
        except:
            pass
        try:
            atom3 = PymolGetTable('pk3')
            DynamicList.append(atom3[0])
        except:
            pass
        try:
            atom4 = PymolGetTable('pk4')
            DynamicList.append(atom4[0])
        except:
            pass
        print 'Index:', DynamicList  # remover este print no futuro
        self.project.settings['dynamic_list'] = DynamicList
        self.project.set_qc_DynamicBondsList()

        
        #pymol_obj   = cmd.get_model(obj, state)                 # importing pymol selection
        #model_split = pymol_obj.atom	
        #
        #for i in model_split:
        #    line = [] 		
        #    idx = i.name			                                          
        #    X = i.coord[0]			                                          
        #    Y = i.coord[1]			                                          
        #    Z = i.coord[2]			                                          
        #    line = idx +"     " + str(X)+ "     "+ str(Y)+ "     " + str(Z)   
        #    text.append(line + "\n")										  

    
    
    def __init__(self):

        print '           Intializing GTKdynamo GUI object          '
        self.home = os.environ.get('HOME')
        self.scratch = os.environ.get('PDYNAMO_SCRATCH')
        
        self.GTKDYNAMO_ROOT = os.environ.get('GTKDYNAMO_ROOT')
        self.GTKDYNAMO_GUI = os.path.join(self.GTKDYNAMO_ROOT, "gui")
        

        #---------------------------------- GTKDYNAMO ------------------------------------#
        #                                                                                 #
        self.builder = gtk.Builder()                                                      #
        self.builder.add_from_file(                                                       #
            os.path.join(self.GTKDYNAMO_GUI, "01_GTKDynamo_main.glade"))                  #
        self.builder.add_from_file(                                                       #
            os.path.join(self.GTKDYNAMO_GUI, 'MessageDialogQuestion.glade'))              #
        self.win = self.builder.get_object("win")                                         #
        self.win.show()                                                                   #
        self.builder.connect_signals(self)                                                #
        self.selectedID = None                                                            #
        self.MeasureToolVisible = False                                                   #
        self.builder.get_object('notebook3').hide()                                       #
                                                                                          #
        #---------------------------------------------------------------------------------#
        self.GTKDynamoConfig = {                              
                               'HideWorkSpaceDialog': False,  
                               'WorkSpace'          : None ,  
                               'History'            : {}   }                              

        self.Load_GTKDYNAMO_ConfigFile()
        self.changed = False
        
        
        
        #-------------------- config GLarea --------------------#
        container = self.builder.get_object("container")        #
        pymol.start()                                           #
        cmd = pymol.cmd                                         #
        container.pack_end(glarea)                              #
        glarea.show()                                           #
        #-------------------------------------------------------#
    
        
        
        #-------------------- config PyMOL ---------------------#
        #                                                       #
        pymol.cmd.set("internal_gui", 0)                        #
        pymol.cmd.set("internal_gui_mode", 0)                   #
        pymol.cmd.set("internal_feedback", 0)                   #
        pymol.cmd.set("internal_gui_width", 220)                #
        pymol.cmd.set("cartoon_fancy_helices", 'on')            #  
        sphere_scale = 0.25                                     #
        stick_radius = 0.15                                     #
        label_distance_digits = 4                               #
        mesh_width = 0.3                                        #
        cmd.set('sphere_scale', sphere_scale)                   #
        cmd.set('stick_radius', stick_radius)                   #
        cmd.set('label_distance_digits', label_distance_digits) #
        cmd.set('mesh_width', mesh_width)                       #
        cmd.set("retain_order")         # keep atom ordering    #
        cmd.bg_color("grey")            # background color      #
        cmd.do("set field_of_view, 70")                         #
        cmd.do("set ray_shadows,off")                           #
        cmd.do('set cartoon_highlight_color, 24')               #
        cmd.set('label_size', 20.00)
        cmd.set('label_color', 'white')
        cmd.set('auto_zoom', 1)                                 #
        #-------------------------------------------------------#
        
        
        print text1

        

        
              #------------------------------------------------#
              #-                 WindowControl                 #
              #------------------------------------------------#
        #------------------------------------------------------------#
        self.window_control = WindowControl(self.builder)            #
        scale = self.builder.get_object("trajectory_hscale")         #
        scale.set_range(1, 100)                                      #
        scale.set_increments(1, 10)                                  #
        scale.set_digits(0)                                          #
        #------------------------------------------------------------#

        #--------------------- Setup ComboBoxes ---------------------#
        #                                                            #
        combobox = 'combobox1'                                       #
        combolist = ["Atom", "Residue", "Chain", "Molecule"]         #
        self.window_control.SETUP_COMBOBOXES(combobox, combolist, 1) #
        #------------------------------------------------------------#


        
        #--------------------------------------------------GTKDynamo project---------------------------------------------------------#
        self.project = pDynamoProject(                                                                                               #
            data_path=GTKDYNAMO_TMP, builder=self.builder, window_control=self.window_control)                                       #
        self.project.PyMOL = True                                                                                                    #
        #----------------------------------------------------------------------------------------------------------------------------#

       
        self.project.data_path = GTKDYNAMO_TMP


        #------------------------------ GTKDynamo Dialogs --------------------------------------#
        #                                                                                       #
        '''os dialogs precisam ser criados aqui para que nao percam as alteracoes               #
        # que o usuario farah nas 'entries' '''                                                 #
        #                                                                                       #
        self._02MinimizationWindow       = MinimizationWindow(self)                             #
                                                                                                #
        self.MolecularDynamicsWindow     = MolecularDynamicsWindow(self)                        #
                                                                                                #
        self._NewProjectDialog           = NewProjectDialog(self)                               #
                                                                                                #
        self.QuantumChemistrySetupDialog = QuantumChemistrySetupDialog(self)                    #
                                                                                                #
        self.NonBondDialog               = NonBondDialog(self)                                  #
                                                                                                #
        self.ScanWindow                  = ScanWindow(self)
                                                                                                #
        self.ScanWindow2D = ScanWindow2D(self)                                                  #                               
                                                                                                #
        self.TrajectoryDialog = TrajectoryDialog(self)                                          #
                                                                                                #
        self.WorkSpaceDialog = WorkSpaceDialog(self)                                            #
                                                                                                #
        self.pDynamoSelectionWindow = pDynamoSelectionWindow(self)                              #
                                                                                                #
        self.ChargeRescaleDialog = ChargeRescaleDialog(self)                                    #
        #---------------------------------------------------------------------------------------#

        #------------------------------ GTKDynamo Dialogs ------------------------------------------------#
        #                                                                                                 #
        '''os dialogs precisam ser criados aqui para que nao percam as alteracoes                         #
        # que o usuario farah nas 'entries' '''                                                           #
        #                                                                                                 #
        self._02MinimizationWindow       = MinimizationWindow(self)                                       #
                                                                                                          #
        self.MolecularDynamicsWindow     = MolecularDynamicsWindow(self)                                  #
                                                                                                          #
        self._NewProjectDialog           = NewProjectDialog(self)                                         #
                                                                                                          #
        self.QuantumChemistrySetupDialog = QuantumChemistrySetupDialog(self)                              #
                                                                                                          #
        self.NonBondDialog               = NonBondDialog(self)                                            #
                                                                                                          #
        self.ScanWindow = ScanWindow(self)                                                                #
                                                                                                          #                                                                                                          #
        self.TrajectoryDialog = TrajectoryDialog(self)                                                    #
                                                                                                          #
        self.WorkSpaceDialog = WorkSpaceDialog(self)
        
        self.pDynamoSelectionWindow = pDynamoSelectionWindow(self)
        
        #-------------------------------------------------------------------------------------------------#
        self.graph = None
 





        #------------------------ GTKDynamo Config -------------------------#
        '''                                                                 #
                                                                            #
        '''                                                                 #
                                                                            #

                                                                            #
        #-------------------------------------------------------------------#

        
        if self.GTKDynamoConfig['HideWorkSpaceDialog'] == False:
            self.WorkSpaceDialog.dialog.run()
            self.WorkSpaceDialog.dialog.hide()



    def run(self):
        gtk.main()


print "Creating object"
# Create our glarea widget
glarea = gtk.gtkgl.DrawingArea(glconfig)
#glarea.set_size_request(400, 400)
glarea.connect_after('realize', init)
glarea.connect('configure_event', reshape)
glarea.connect('expose_event', draw)
glarea.connect('map_event', map)
glarea.set_events(glarea.get_events() | gtk.gdk.BUTTON_PRESS_MASK | gtk.gdk.BUTTON_RELEASE_MASK |
                  gtk.gdk.POINTER_MOTION_MASK | gtk.gdk.POINTER_MOTION_HINT_MASK | gtk.gdk.KEY_PRESS_MASK)


                                                      
glarea.connect("button_press_event"  , mousepress)      
glarea.connect("button_release_event", mouserelease)  
glarea.connect("motion_notify_event" , mousemove)      


#glarea.connect("button_press_event",   _mouseButton)
#glarea.connect("button_release_event", _mouseButton)
#glarea.connect("motion_notify_event",  _mouseButton)



glarea.connect("scroll_event", slabchange)


glarea.set_can_focus(True)

import pymol2
pymol = pymol2.PyMOL(glarea)
gtkdynamo = gtkdynamo_main()
#glarea.connect_object("button_press_event", show_context_menu, context_menu())
glarea.connect_object("button_release_event", show_context_menu, context_menu())

import sys
if len(sys.argv) > 1:
    gtkdynamo.project.load_coordinate_file_as_new_system(sys.argv[1])
    gtkdynamo.project.From_PDYNAMO_to_GTKDYNAMO(type_='new')

gtkdynamo.run()
