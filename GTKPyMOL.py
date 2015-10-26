#!/usr/bin/env python
text1 = """
#   
#
#   
#   
#
#   
#
#                         ---- GTKDynamo 2.0 - EasyHybrid ----
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
#   - Jose Fernando R Bachega   - Pontifical Catholic University of Rio Grande do Sul - RS, Brazil                            
#   - Troy Wymore               - Pittsburgh Super Computer Center, Pittsburgh PA - USA           
#   - Martin Field              - Institut de Biologie Structurale, Grenoble, France                      
#   - Luis Fernando S M Timmers - Pontifical Catholic University of Rio Grande do Sul - RS, Brazil
#   - Michele Silva             - Pontifical Catholic University of Rio Grande do Sul - RS, Brazil
#    
#   Special thanks to:       
#   - Osmar Norbeto de souza    - Pontifical Catholic University of Rio Grande do Sul - RS, Brazil
#   - Fernando V Maluf          - Univesity of Sao Paulo - SP, Brazil                             
#   - Lucas Assirati            - Univesity of Sao Paulo - SP, Brazil                             
#   - Leonardo R Bachega        - University of Purdue - West Lafayette, IN - USA                 
#   - Richard Garratt           - Univesity of Sao Paulo - SP, Brazil                             
#   - Walter R Paixao-Cortes    - Pontifical Catholic University of Rio Grande do Sul - RS, Brazil
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
#import gtk
#import gtk.gtkgl
from pprint import pprint


#import thread
import threading
import gobject
import sys
import glob
import math
import os



## Imports
#from OpenGL.GL import *
#from OpenGL.GLU import *


import pango
import pymol
from pymol import *
from pymol.cgo import *




# get a temporary file directory
#-------------------------------------------------------------------#
PDYNAMO_SCRATCH = os.environ.get('PDYNAMO_SCRATCH')                 #
if not os.path.isdir(PDYNAMO_SCRATCH):                              #
    print PDYNAMO_SCRATCH, "not found"                              #
    os.mkdir(PDYNAMO_SCRATCH)                                       #
    print "creating: ", PDYNAMO_SCRATCH                             #
                                                                    #
GTKDYNAMO_TMP = os.path.join(PDYNAMO_SCRATCH, '.GTKDynamo')         #
if not os.path.isdir(GTKDYNAMO_TMP):                                #
    os.mkdir(GTKDYNAMO_TMP)                                         #
    print "Temporary files directory:  %s" % GTKDYNAMO_TMP          #
#-------------------------------------------------------------------#


#-----------------------------------------GUI---------------------------------------------------#
from gui.DialogMinimization.Minimization                     import *                           #
from gui.DialogMolecularDynamics.MolecularDynamics           import *                           #
                                                                                                #
from gui.FileChooserWindow                                   import *                           #
from gui.DialogNewProject.NewProject                         import *                           #
from gui.DialogQuantumChemistrySetup.QuantumChemistrySetup   import *                           #
                                                                                                #
from gui.DialogChargeRescale.ImportCoordinates               import ImportCoordinatesDialog     #
from gui.DialogChargeRescale.ImportCoordinates               import ExportCoordinatesDialog     #
                                                                                                #
from gui.DialogAmber12ToAmber11.DialogAmber12ToAmber11       import DialogAmber12ToAmber11      #
                                                                                                #
from gui.DialogNonBond.NonBond                               import *                           #
from gui.WindowScan1D.Scan                                   import *                           #
from gui.WindowScan2D.Scan2D                                 import *                           #
                                                                                                #
from gui.WindowpDynamoSelections.pDynamoSelections           import pDynamoSelectionWindow      #
from gui.DialogPreferences.Preferences                       import *                           #
                                                                                                #
from gui.DialogLoadTrajectory.Trajectory                     import *                           #
from gui.DialogAbout.About                                   import AboutDialog                 #
from gui.DialogNEB.NEBandSAW                                 import NEBDialog                   #
from gui.DialogNEB.NEBandSAW                                 import SAWDialog                   #
from gui.DialogTrajectoryEnergyRefine.TrajectoryEnergyRefine import TrajectoryEnergyRefineDialog#
from gui.MOPACEnergy.MOPACEnergy                             import MOPACSEnergyDialog          #
                                                                                                #
from gui.DialogWorkSpaceDialog.WorkSpace                     import WorkSpaceDialog             #
from gui.DialogChargeRescale.ChargeRescale                   import ChargeRescaleDialog         #
from gui.WindowUmbrellaSampling.UmbrellaSampling             import UmbrellaSamplingWindow      #


#/home/fernando/Documents/gtkdynamo2/gui/DialogPreferences/Preferences.py
#from gui.MainMenu           import  MainMenu                                                                        
#from gui.MainToolBar        import  MainToolBar 
#from gui.GLMenu             import  GLMenu
#from gui.TreeviewHistory    import  TreeviewHistory
#from gui.TreeviewSelections import  TreeviewSelections
#from gui.PyMOLCommandLine   import  PyMOLCommandLine
#from gui.TrajectoryTool     import  TrajectoryTool


import TextEditor.TextEditorWindow as TextEditor                                             #
                                                                                             #
from   MatplotGTK.MatplotGTK          import PlotGTKWindow                                   #
#--------------------------------------------------------------------------------------------#


# pDynamo
from pDynamoProject    import *
from WindowControl     import *

from pDynamoMethods.pDynamoCharges   import compute_selection_total_charge







class MainMenu (object):
        """ Class doc """
        def __init__ (self, GUI=None):
                #self.builder = GUI.builder
                #print 'MainMenu'
                #self.builder = GUI.builder
                self.GUI = GUI

        def on_MainMenu_File_Import_ImportTrajectory_activate (self, menuitem):
                """ Function doc """
                self.TrajectoryDialog.builder.get_object('filechooserbutton1').set_filename(self.project.settings['data_path'])
                self.TrajectoryDialog.builder.get_object('filechooserbutton2').set_filename(self.project.settings['data_path'])
                self.TrajectoryDialog.dialog.run()
                self.TrajectoryDialog.dialog.hide()

        def on_MainMenu_View_ShowSequence_activate(self, button):
                #print """ Function doc """
                if self.builder.get_object('menuitem29').get_active() == True:
                        #cmd.set('valence', 0.1)
                        #self.builder.get_object('vpaned4').show()
                        cmd.set("seq_view", 1)
                else:
                        #cmd.set('valence', 0.0)
                        #self.builder.get_object('vpaned4').hide()
                        cmd.set("seq_view", 0)

        def on_MainMenu_View_ShowPyMOLInternalGUI_activate (self, button):
                """ Function doc """
                if self.builder.get_object('menuitem_internal_GUI').get_active() == True:
                        #cmd.set('valence', 0.1)
                        cmd.set("internal_gui", 1)
                else:
                        #cmd.set('valence', 0.0)
                        cmd.set("internal_gui", 0)

        def on_MainMenu_View_ShowValences_activate(self, button):
                #print """ Function doc """
                if self.builder.get_object('ShowValences').get_active() == True:
                        #cmd.set('valence', 0.1)
                        cmd.do('set valence, 0.1')
                else:
                        #cmd.set('valence', 0.0)
                        cmd.do('set valence, 0.0')		

        
        def on_MainMenu_Edit_Preferences_activate (self, button):
                """ Function doc """
                self.PreferencesDialog.dialog.run()
                self.PreferencesDialog.dialog.hide()

        
        
        def on_MainMenu_View_PYMOLCommand_line_activate(self, button):
                """ Function doc """
                #print """ Function doc """
                if self.builder.get_object('PyMOL_command_line_check').get_active() == True:
                        #cmd.set('valence', 0.1)
                        pymol.cmd.set("internal_feedback", 1) 
                else:
                        #cmd.set('valence', 0.0)
                        pymol.cmd.set("internal_feedback", 0) 
                        
        
        
        
        
        def on_MainMenu_View_ShowTrajectoryTool_clicked (self, button):
                """ Function doc """
                if self.builder.get_object('toolbutton_trajectory_tool').get_active() == True:
                        #cmd.set('valence', 0.1)
                        self.builder.get_object('handlebox1').show()
                else:
                        #cmd.set('valence', 0.0)
                        self.builder.get_object('handlebox1').hide()  
                           
                        

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
                #print WorkSpace, text
                
                path      = os.path.join(WorkSpace, text)
                self._NewProjectDialog.builder.get_object("ProjectDirectory").set_text(path)

                self._NewProjectDialog.dialog.run()
                self._NewProjectDialog.dialog.hide()

        def on_MainMenu_Import_ImportCoordenates_activate (self, menuitem):
                """ Function doc """
                #self.DialogImportCoordinates.builder.get_object('entry_file_name').set_text('teste')
                self.DialogImportCoordinates.dialog.run()
                self.DialogImportCoordinates.dialog.hide()

        def on_MainMenu_Export_ExportCoordenates_activate (self, menuitem):
                """ Function doc """
                self.DialogExportCoordinates.builder.get_object('entry_file_name').set_text('teste')
                self.DialogExportCoordinates.dialog.run()
                self.DialogExportCoordinates.dialog.hide()

        def on_MainMenu_File_OpenFileChooserWindow_clicked(self, button):
                """ Function doc """

                FileChooser = FileChooserWindow()
                FileName = FileChooser.GetFileName(self.builder)

                #print FileName


                if FileName == None:
                        pass

                else:
                        _FileType = GetFileType(FileName)
                        self.PyMOL_initialize()
                        if _FileType in ['pkl', 'yaml']:
                                self.project.load_coordinate_file_as_new_system(FileName)
                                self.project.From_PDYNAMO_to_GTKDYNAMO(type_='new')

                        if _FileType in ['gtkdyn']:
                                self.project.load_GTKDYNAMO_project(FileName)
                        
                self.PyMOL_change_selection_mode()

        def on_MainMenu_File_Quit_activate (self, menuitem):
                """ Function doc """
                print '''\n\nThanks for use EasyHybrid - GTKDynamo 1.9 - \n\n'''
                gtk.main_quit()
                cmd.quit()

        
        def on_MainMenu_Edit_ClearFixedAtoms_activate (self, menuitem):
            """ Function doc """
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
                                                                                                  
            self.builder.get_object('MessageDialogQuestion').format_secondary_text("Remove all atoms from the fixed region?")  
            dialog = self.builder.get_object('MessageDialogQuestion')                                         
                                                                                                              
            a = dialog.run()  # possible "a" valors                                                           
            # 4 step          # -8  -  yes                                                                    
            dialog.hide()     # -9  -  no                                                                     
                              # -4  -  close                                                                  
                              # -5  -  OK                                                                     
                              # -6  -  Cancel   
            if a == -8: 
                self.project.clean_fix_table()
                self.project.SystemCheck( status = True, 
                                                PyMOL = True, 
                                               _color = True, 
                                                _cell = True, 
                                    treeview_selections = True,
                                            ORCA_backup = True)
            else:                                                                                             
                return 0  

        def on_MainMenu_Edit_ClearQCAtoms_activate (self, menuitem):
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
                                                                                                  
            self.builder.get_object('MessageDialogQuestion').format_secondary_text("Remove all atoms from the quantum region?")  
            dialog = self.builder.get_object('MessageDialogQuestion')                                         
                                                                                                              
            a = dialog.run()  # possible "a" valors                                                           
            # 4 step          # -8  -  yes                                                                    
            dialog.hide()     # -9  -  no                                                                     
                              # -4  -  close                                                                  
                              # -5  -  OK                                                                     
                              # -6  -  Cancel                                                                 
            # 5 step                                                                                          
            if a == -8:                                                                                       
                self.project.clean_qc_table()                                                                                 
            else:                                                                                             
                return 0   








        
        def on_MainMenu_Edit_ChargeRescale_activate (self, menuitem):
                """ Function doc """
                self.ChargeRescaleDialog.dialog.run()
                self.ChargeRescaleDialog.dialog.hide()


        def on_MainMenu_Selection_SetQCTable(self, menuitem, click = None):    
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
                    # auto calculate the mm charge from the selected region and set the valor to the spinbutton
                    _sum, _len = self.project.ComputeChargesFromSelection()
                    #_sum, _len = compute_selection_total_charge(self.project.system, selection = None )
                    _sum = int(round(_sum))
                    self.QuantumChemistrySetupDialog.builder.get_object('spinbutton_charge').set_value(_sum)
                    
                    self.QuantumChemistrySetupDialog.dialog.run()
                    self.QuantumChemistrySetupDialog.dialog.hide()                                                                                   
                else:                                                                                             
                    return 0                                                                                      
                # 7 step                                                                                          
                #self.load_trj_windows.run()                                                                      
            else:                                                                                                 
                pass                                                                                   



            print 'QC table:'
            print self.project.settings['qc_table']



        def on_MainMenu_Selection_ComputeCharge_activate(self, menuitem):
            """ Function doc """
            _sum, _len = self.project.ComputeChargesFromSelection()
            self.builder.get_object('EnergyMessageDialog').set_markup("MM Charges")   
            self.builder.get_object('EnergyMessageDialog').format_secondary_text("Selection charge ("+str(_len) +" atoms): " + str(round(_sum, 8)))   
            dialog = self.builder.get_object('EnergyMessageDialog')
            dialog.run()                                                                
            dialog.hide()
        
        #def on_MainMenu_Calculate_Scan1D_activate(self, menuItem):
        #    """ Function ChargeRescaleDialogdoc """
        #    self.ScanDialog.dialog.run()
        #    self.ScanDialog.dialog.hide()  

        def on_MainMenu_Calculate_Scan1D_activate(self, menuitem):
                """ Function doc """
                if self.ScanWindow.Visible == False:
                        #print self.project.settings['step']
                        text = str(self.project.settings['step'] + 1) + '_step_Scan'
                        #print text			
                        self.ScanWindow.OpenWindow(text)
                
                
                #try:
                #    _FileType = GetFileType(FileName)
                #
                #    if _FileType in ['pkl', 'yaml']:
                #        self.project.load_coordinate_file_as_new_system(FileName)
                #        self.project.From_PDYNAMO_to_GTKDYNAMO(type_='new')
                #except:
                #    pass


        def on_MainMenu_Calculate_Scan2D_activate(self, menuItem):
                if self.ScanWindow2D.Visible == False:
                        #print self.project.settings['step']
                        text = str(self.project.settings['step'] + 1) + '_step_Scan2D'
                        #print text	
                        self.ScanWindow2D.OpenWindow(text)

        def on_MainMenu_Calculate_UmbrellaSampling_activate(self, menuItem):
                if self.UmbrellaSamplingWindow.Visible == False:
                        text = str(self.project.settings['step'] + 1) + '_step_UmbrellaSampling'
                        self.UmbrellaSamplingWindow.OpenWindow(text)


        def on_MainMenu_Calculate_SAW_activate(self, menuItem):
                self.SAWDialog.dialog.run()
                self.SAWDialog.dialog.hide()

        def on_MainMenu_Calculate_NEB_activate(self, menuItem):
                '''
                #print self.project.settings['step']
                text = str(self.project.settings['step'] + 1) + '_step_GeometryOptmization'
                self._02MinimizationWindow.builder.get_object(
                    "02_window_entry_traj_name").set_text(text)
                self._02MinimizationWindow.dialog.run()
                self._02MinimizationWindow.dialog.hide()
                '''
                text = str(self.project.settings['step'] + 1) + '_NEB'
                self.NEBDialog.builder.get_object("trajectory_name").set_text(text)
                self.NEBDialog.dialog.run()
                self.NEBDialog.dialog.hide()
        
        def  on_MainMenu_Calculate_EnergyRefine_activate(self, menuItem):
            """ Function doc """
            self.EnergyRefineDialog.dialog.run()
            self.EnergyRefineDialog.dialog.hide()

            
            
            
            

        def on_MainMenu_Extensions_MOPACEnergy(self, menuItem):
            """ Function doc """
            self.DialogMOPACSEnergy.dialog.run()
            self.DialogMOPACSEnergy.dialog.hide()
            #print 'MOPACEnergy'

        def on_MainMenu_Edit_NonBondingModels_activate(self, button):
                """ Function doc """
                self.NonBondDialog.dialog.run()
                self.NonBondDialog.dialog.hide()


        def on_Analysis_PlotLogGraph_activate (self, button):
            """ Function doc """
            
            FileChooser = FileChooserWindow()
            FileName = FileChooser.GetLogFileName(self.builder)
            
            parameters = ParseProcessLogFile(FileName)
            PlotGTKWindow(parameters)
                

            #if FileName == None:
            #        pass
            #
            #else:
            #        _FileType = GetFileType(FileName)
            #        self.PyMOL_initialize()
            #        if _FileType in ['dat','log' , '*']:
            #                self.project.load_coordinate_file_as_new_system(FileName)
            #                self.project.From_PDYNAMO_to_GTKDYNAMO(type_='new')
            #
            #        if _FileType in ['gtkdyn']:
            #                self.project.load_GTKDYNAMO_project(FileName)
            #        
            #self.PyMOL_change_selection_mode()

        def on_Amber12ToAmber11_activate (self, button):
            """ Function doc """
            self.DialogAmber12ToAmber11.dialog.run()
            self.DialogAmber12ToAmber11.dialog.hide()           


        def on_MainMenu_Help_About_activate(self, button):
                """ Function doc """
                self.AboutDialog.dialog.run()
                self.AboutDialog.dialog.hide()
	
class MainToolBar(object):
    """ Class doc """

    def __init__ (self, GUI):
        """ Class initialiser """
        #self.builder = GUI.builder
        #print 'MainMenu'
        #self.builder = GUI.builder
        self.GUI = GUI

    def on_toolbutton_mplay_clicked (self, button):
        """ Function doc """
        cmd.mplay()

    def on_toolbutton_mstop_clicked (self, button):
        """ Function doc """
        cmd.mstop()

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
        if response == gtk.RESPONSE_OK: 
            filename = chooser.get_filename()
            chooser.destroy()
            self.project.Save_Project_To_File (filename, 'pkl')
        else:
            chooser.destroy()
            return None

    def on_toolbutton_sequence_toggled (self, button):
        """ Function doc """
        if self.builder.get_object('toolbutton_sequence').get_active() == True:
                #print '"seq_view", 1'
                pymol.cmd.set("seq_view", 1)
        else:
                #print '"seq_view", 0'
                pymol.cmd.set("seq_view", 0) 		
 
    def on_toolbar_showCell_toggled (self, button):
        """ Function doc """
        
        if button.get_active():
            self.project.ShowCell = True
        
        else:
            self.project.ShowCell = False
            # print '# If control reaches here, the toggle button is up'
            #self.builder.get_object('notebook3').hide()
        self.project.SystemCheck(status = True, PyMOL = False, _color = False, _cell = True, treeview_selections = True)

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
            if response == gtk.RESPONSE_OK: 
                filename = chooser.get_filename()
                chooser.destroy()
                self.project.Save_Project_To_File (filename, 'pkl')
            else:
                chooser.destroy()
                return None

        else:
            filename = self.project.settings['filename']
            self.project.Save_Project_To_File (filename, 'pkl')

    def on_ToolBar_buttonMeasure_toggled (self, button):
        """ Function doc """
        if button.get_active():
            ## print '# If control reaches here, the toggle button is down'
            self.builder.get_object('notebook3').show()
            self.builder.get_object('togglebutton1').set_active (1)
            #pymol.cmd.set("internal_gui", 1)
        else:
            # print '# If control reaches here, the toggle button is up'
            self.builder.get_object('notebook3').hide()
            #pymol.cmd.set("internal_gui", 0)       
    def on_ToolBar_buttonpDynamoSelections_clicked(self, button):
        """ Function doc """
        if self.project.system == None:
            print 'system empty'
        else:
            if self.pDynamoSelectionWindow.Visible == False:
                self.pDynamoSelectionWindow.OpenWindow()  

    def on_ToolBar_CheckSystem_clicked(self, button):
        """ Function doc """
        filein = self.project.SystemCheck(_color = False)
        #filein = self.project.settings['job_history'][self.selectedID]['log']
        editor = TextEditor.GTKDynamoTextEditor(filein)
        
    def on_ToolBar_SinglePoint_clicked(self, button):
        """ Function doc """
        energy = self.project.ComputeEnergy()
        #colocar um check system aqui 
        self.builder.get_object('EnergyMessageDialog').format_secondary_text("Total energy: " + str(energy) + " KJ/mol")   
        dialog = self.builder.get_object('EnergyMessageDialog')
        dialog.run()                                                                
        dialog.hide()
                
    def on_ToolBar_QuantumChemistrySetup_clicked(self, button):
        """ Function doc """
        self.QuantumChemistrySetupDialog.dialog.run()
        self.QuantumChemistrySetupDialog.dialog.hide()

    def on_ToolBar_OptmizationSetup_clicked(self, button):
        """ Function doc """
        #print self.project.settings['step']
        text = str(self.project.settings['step'] + 1) + '_step_GeometryOptmization'
        self._02MinimizationWindow.builder.get_object(
            "02_window_entry_traj_name").set_text(text)
        self._02MinimizationWindow.dialog.run()
        self._02MinimizationWindow.dialog.hide()

    def on_ToolBar_MolecularDynamicsSetup_clicked (self, button):
        """ Function doc """
        #print self.project.settings['step']
        text = str(self.project.settings['step'] + 1) + '_step_MolecularDynamics'
        self.MolecularDynamicsWindow.builder.get_object("MMDialog_entry_trajectory_name").set_text(text)
        self.MolecularDynamicsWindow.dialog.run()
        self.MolecularDynamicsWindow.dialog.hide()
        
    def on_ToolBar_ChangeSelectionMode_toggled(self, button):
        #if self.builder.get_object('togglebutton1').get_active():
        #	# print '# If control reaches here, the toggle button is down'
        #	self.builder.get_object('togglebutton1').set_label('Editing')
        #	self.builder.get_object('label_viewing').set_label('Picking')
        #	self.builder.get_object('combobox1').set_sensitive(False)
        #	cmd.edit_mode(1)
        #	self.project.settings['edit_mode_button'] = True
        #
        #else:
        #	# print '# If control reaches here, the toggle button is up'
        #
        #	self.builder.get_object('togglebutton1').set_label('Viewing')
        #	self.builder.get_object('label_viewing').set_label('Selecting')
        #	self.builder.get_object('combobox1').set_sensitive(True)
        #	cmd.edit_mode(0)
        #	self.project.settings['edit_mode_button'] = False
        #
        self.PyMOL_change_selection_mode()
        
    def on_ToolBar_ChangeSelectionMode_changed(self, button):
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

    def on_ToolBar_ClearSystemInMemory_clicked (self, button):
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
                self.project = pDynamoProject(data_path       = GTKDYNAMO_TMP      , 
                                              builder         = self.builder       , 
                                              window_control  = self.window_control,
                                              GTKDynamoConfig = self.GTKDynamoConfig )                                   

                self.project.PyMOL = True                                                                                                    #
                #----------------------------------------------------------------------------------------------------------------------------#  

                cmd.delete('all')
                pymol_objects  = cmd.get_names()
                liststore = self.builder.get_object('liststore2')
                self.project.window_control.TREEVIEW_ADD_DATA2(liststore, self.project.settings['job_history'] , None)
                
                
                self.project.SystemCheck()
                self.PyMOL_initialize()
                #cmd.delete('all')                                                                                  
            else:                                                                                             
                return 0 

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

class GLMenu(object):
    """
    #--------------------------------------------#
    #                GL AREA MENU                #
    #--------------------------------------------# 
    """

    def __init__ (self, GUI):
        """ Class initialiser """
        #self.builder = GUI.builder
        #print 'MainMenu'
        #self.builder = GUI.builder
        self.GUI = GUI


    def on_GLAreaMenu_itemActive_view (self, item, click = None):
        """ Function doc """ 
        #PyMOL_Obj = self.selectedObj
        if item == self.builder.get_object('gl_menuitem_zoon'):
            cmd.zoom()
        if item == self.builder.get_object('gl_menuitem_orient'):
            cmd.orient()
        if item == self.builder.get_object('gl_menuitem_center'):
            cmd.center()
        if item == self.builder.get_object('gl_menuitem_reset'):
            cmd.reset()
        if item == self.builder.get_object('gl_menuitem_ray'):
            cmd.ray()
                
    def on_GLAreaMenu_itemActive_CleanQCTable(self, menuitem, click = None):    
        self.project.clean_qc_table()
        #print self.project.settings['qc_table']

    def on_GLAreaMenu_itemActive_SetFixTable(self, menuitem, click=None):
        table = PymolGetTable('sele')
        self.project.put_fix_table(table)
        #print self.project.settings['fix_table']

    def on_GLAreaMenu_itemActive_CleanFixTable(self, menuitem, click=None):
        self.project.clean_fix_table()
        #print self.project.settings['fix_table']

    def on_GLAreaMenu_itemActive_SetPruneTable(self, menuitem, click=None):
        #print "aqui"
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
            #print self.project.settings['prune_table']                                                                                     
            #self.QuantumChemistrySetupDialog.dialog.run()
            #self.QuantumChemistrySetupDialog.dialog.hide()                                                                                   
        else:                                                                                             
            return 0                                                                                      

    def on_GLAreaMenu_PutLalbel_itemActive(self, menuitem, click=None):
        """ Function doc """
        #print 'teste'
        
        
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

    def on_gl_show_hide_items_activate (self, item, event):
        
        #print """ gl menu items """
        if item == self.builder.get_object('gl_menuitem_show_lines'):
            cmd.show ('lines', 'sele')
        if item == self.builder.get_object('gl_menuitem_show_sticks'):
            cmd.show ('sticks', 'sele')
        if item == self.builder.get_object('gl_menuitem_show_ribbon'):
            cmd.show ('ribbon', 'sele')
        if item == self.builder.get_object('gl_menuitem_show_cartoon'):
            cmd.show ('cartoon', 'sele')
        if item == self.builder.get_object('gl_menuitem_show_mesh'):
            cmd.show ('mesh', 'sele')
        if item == self.builder.get_object('gl_menuitem_show_surface'):
            cmd.show ('surface', 'sele')
        if item == self.builder.get_object('gl_menuitem_hide_lines'):
            cmd.hide ('lines', 'sele')
            #cmd.util.cnc(PyMOL_Obj)
        if item == self.builder.get_object('gl_menuitem_hide_sticks'):
            cmd.hide ('sticks', 'sele')
        if item == self.builder.get_object('gl_menuitem_hide_ribbon'):
            cmd.hide ('ribbon', 'sele')
        if item == self.builder.get_object('gl_menuitem_hide_cartoon'):
            cmd.hide ('cartoon', 'sele')
        if item == self.builder.get_object('gl_menuitem_hide_mesh'):
            cmd.hide ('mesh', 'sele')
        if item == self.builder.get_object('gl_menuitem_hide_surface'):
            cmd.hide ('surface', 'sele')
        
        
        # Colors
        if item == self.builder.get_object('gl_menuitem_color_black'):
            cmd.color('grey10','sele')
            cmd.util.cnc('sele')
        if item == self.builder.get_object('gl_menuitem_color_green'):
            cmd.util.cbag('sele')
        if item == self.builder.get_object('gl_menuitem_color_cyan'):
            cmd.util.cbac('sele')
        if item == self.builder.get_object('gl_menuitem_color_magenta'):
            cmd.util.cbam('sele')
        if item == self.builder.get_object('gl_menuitem_color_yellow'):
            cmd.util.cbay('sele')
        if item == self.builder.get_object('gl_menuitem_color_salmon'):
            cmd.util.cbas('sele')
        if item == self.builder.get_object('gl_menuitem_color_white'):
            cmd.util.cbaw('sele')
        if item == self.builder.get_object('gl_menuitem_color_slate'):
            cmd.util.cbab('sele')
        if item == self.builder.get_object('gl_menuitem_color_orange'):
            cmd.util.cbao('sele')
        if item == self.builder.get_object('gl_menuitem_color_purple'):
            cmd.util.cbap('sele')
        if item == self.builder.get_object('gl_menuitem_color_pink'):
            cmd.util.cbak('sele')

class TreeviewHistory(object):
    """ Class doc """

    def __init__ (self):
        """ Class initialiser """
        pass

    #def handle_history_click(self, tree, event):
    #    if event.button == 3:
    #        print "Mostrar menu de contexto botao3"
    #   
    #    if event.button == 1:
    #        print "Mostrar menu de contexto botao1"

    def on_treeview2_show_logFile (self, item):
        """ Function doc """
        #pprint(self.project.settings['job_history'][self.selectedID]['log'])
        filein = self.project.settings['job_history'][self.selectedID]['log']
        #print   self.project.settings['job_history'][self.selectedID]['log']
        editor = TextEditor.GTKDynamoTextEditor(filein)
        #editor.load_file(filein)
    def on_menuitem_PlotLogFile_activate(self, item):
        """ Function doc """
        filein = self.project.settings['job_history'][self.selectedID]['log']
        #print    self.project.settings['job_history'][self.selectedID]['log']
        parameters = ParseProcessLogFile(filein)
        
        #xlabel = 'Frames'
        #ylabel = 'Energy (KJ)' 
        #title  = os.path.split(filein)[-1]
        #print  X, Y
        #
        #parameters = {
        #             'title' : title ,
        #             'X'     : X     ,
        #             'Y'     : Y     ,
        #             'xlabel': xlabel,
        #             'ylabel': ylabel,
        #             }
        
        PlotGTKWindow(parameters)

    def on_show_items_activate (self, item, event):
        """ Function doc """ 
        PyMOL_Obj = self.selectedObj

        if item == self.builder.get_object('menuitem_show_lines'):
            cmd.show ('lines', PyMOL_Obj)

        if item == self.builder.get_object('menuitem_show_sticks'):
            cmd.show ('sticks', PyMOL_Obj)

        if item == self.builder.get_object('menuitem_show_ribbon'):
            cmd.show ('ribbon', PyMOL_Obj)

        if item == self.builder.get_object('menuitem_show_cartoon'):
            cmd.show ('cartoon', PyMOL_Obj)

        if item == self.builder.get_object('menuitem_show_mesh'):
            cmd.show ('mesh', PyMOL_Obj)

        if item == self.builder.get_object('menuitem_show_surface'):
            cmd.show ('surface', PyMOL_Obj)

        if item == self.builder.get_object('menuitem_center'):
            cmd.center(PyMOL_Obj)

    def on_menuitem_set_as_active_activate (self, item):#, event):
        """ Function doc """
        #label     = self.builder.get_object('TreeViewObjLabel').get_text()
        actualObj = self.project.settings['PyMOL_Obj']
        label     = 'test'
        PyMOL_Obj = self.selectedObj
        data_path = self.project.settings['data_path']
        file_out  = 'exportXYZ.xyz'
        state     = -1
        
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
                                                                                              
        self.builder.get_object('MessageDialogQuestion').format_secondary_text("Set object: " +PyMOL_Obj +" as active?")  
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
            filename = PyMOL_export_XYZ_to_file(PyMOL_Obj, label, data_path, file_out, state)
            self.project.load_coordinate_file_to_system(filename)
            self.project.settings['PyMOL_Obj'] = PyMOL_Obj
            self.project.SystemCheck(status = True, PyMOL = True, _color = False, _cell = True, treeview_selections = True)
            
            #liststore = self.builder.get_object('liststore2')
            #self.window_control.TREEVIEW_ADD_DATA2(liststore, self.project.settings['job_history'] , PyMOL_Obj)
            #print filename                                                                
        else:                                                                                             
            return 0 
        
    def on_hide_items_activate (self, item, event):
        """ Function doc """ 
        PyMOL_Obj = self.selectedObj

        if item == self.builder.get_object('menuitem_hide_everything'):
            cmd.hide ('everything', PyMOL_Obj)

        if item == self.builder.get_object('menuitem_hide_lines'):
            cmd.hide ('lines', PyMOL_Obj)

        if item == self.builder.get_object('menuitem_hide_sticks'):
            cmd.hide ('sticks', PyMOL_Obj)

        if item == self.builder.get_object('menuitem_hide_ribbon'):
            cmd.hide ('ribbon', PyMOL_Obj)

        if item == self.builder.get_object('menuitem_hide_cartoon'):
            cmd.hide ('cartoon', PyMOL_Obj)

        if item == self.builder.get_object('menuitem_hide_mesh'):
            cmd.hide ('mesh', PyMOL_Obj)

        if item == self.builder.get_object('menuitem_hide_surface'):
            cmd.hide ('surface', PyMOL_Obj)

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
        
        if self.project.settings['fix_table'] != []:
            #PymolPutTable(self.project.settings['fix_table'], "FIX_atoms")
            cmd.color(self.GTKDynamoConfig['fixed'],'FIX_atoms')




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


		if event.button == 2:
			selection     = tree.get_selection()
			model         = tree.get_model()
			(model, iter) = selection.get_selected()
			pymol_object = model.get_value(iter, 0) 
			
			string2 = 'select sele, '+ pymol_object
			cmd.do(string2)
			cmd.center('sele')

           
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

class TreeviewSelections(object):
	'''                                            
	#      ---------------------------------  
	#           PyMOL TREEVIEW  methods    
	#      ---------------------------------

	'''   
	def on_treeview_PyMOL_Selections_button_release_event (self, tree, event):
		if event.button == 3:
			#print "Mostrar menu de contexto botao3"
			selection     = tree.get_selection()
			model         = tree.get_model()
			(model, iter) = selection.get_selected()
			if iter != None:
				#self.selectedID  = str(model.get_value(iter, 0))  # @+
				self.selectedObj = str(model.get_value(iter, 0))
				self.builder.get_object('TreeViewObjLabel').set_label('- ' +self.selectedObj+' -' )
				
				widget = self.builder.get_object('treeview_menu')
				widget.popup(None, None, None, event.button, event.time)
		
		if event.button == 2:
			selection     = tree.get_selection()
			model         = tree.get_model()
			(model, iter) = selection.get_selected()
			pymol_object = model.get_value(iter, 0) 
			
			string2 = 'select sele, '+ pymol_object
			cmd.do(string2)
			cmd.center('sele')
		
		
		if event.button == 1:
			selection     = tree.get_selection()
			model         = tree.get_model()
			(model, iter) = selection.get_selected()
			pymol_object = model.get_value(iter, 0) 
			
			string2 = 'select sele, '+ pymol_object
			cmd.do(string2)
			cmd.enable('sele')

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
		#pprint (self.project.settings['job_history'][ID])
        #
        #nao printa mais o (self.project.settings['job_history'][ID])

class PyMOLCommandLine(object):	
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

class TrajectoryTool(object):
	'''                                            
	#      ---------------------------------  
	#          TrajectoryTool  methods    
	#      ---------------------------------

	''' 
	
	def __init__ (self):
		""" Class initialiser """
		pass


	
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


class GTKDynamoConfig(object):
    """ Class doc """
    def __init__ (self):
        """ Class initialiser """
        pass

    def Save_GTKDYNAMO_ConfigFile (self, filename = None):
        """ Function doc """
        path = os.path.join(self.HOME,'.config')
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
        path = os.path.join(self.HOME,'.config', 'GTKDynamo', 'gtkdynamo.config')
        
        try:
            self.GTKDynamoConfig = json.load(open(path)) 
        except:
            print 'error: GTKDynamo config file not found'
            print 'opening WorkSpace Dialog'
    
class gtkdynamo_main(threading.Thread,
                     MainMenu, 
					 MainToolBar, 
                     GLMenu, 
                     TreeviewHistory, 
                     TreeviewSelections, 
                     PyMOLCommandLine,
                     TrajectoryTool,
                     GTKDynamoConfig):


    def PyMOL_change_selection_mode (self):
        """ Function doc """
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

    def PyMOL_initialize (self):
        """ Function doc """
        cmd.delete('all')
        #-------------------- config PyMOL ---------------------#
        #                                                       #
                                                                #
        #cmd.button("double_left","None","None")                 #
        #cmd.button("single_right","None","None")                #
        pymol.cmd.set("internal_gui", 0)                        #
        #pymol.cmd.set("internal_gui_mode", 1)                   #
        #pymol.cmd.set("internal_feedback", 0)                   #
        #pymol.cmd.set("internal_gui_width", 220)                #
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
        
        
        #BG color
        try:
            cmd.bg_color(self.GTKDynamoConfig['bg_color'])
        except:
            cmd.bg_color('black')
        
        
        #cmd.do("set field_of_view, 70")                         #
        cmd.do("set ray_shadows,off")                           #
        cmd.do('set cartoon_highlight_color, 24')               #
        cmd.set('label_size', 20.00)                            #
        cmd.set('label_color', 'white')                         #
        cmd.set('auto_zoom', 1)                                 #
        #cmd.extend('axes', axes)
        #axes()
        #-------------------------------------------------------#
        

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
                #print i 
                name  = i.name
                #print name
            
            #print 'depois'

            
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
        #print 'Index:', DynamicList  # remover este print no futuro
        self.project.settings['dynamic_list'] = DynamicList
        self.project.set_qc_DynamicBondsList()



    def __init__(self):
            
        print '           Intializing EasyHybrid - GTKDynamo GUI object          '
        self.SCRATCH        = os.environ.get('PDYNAMO_SCRATCH')
        try:
            self.ORCA           = os.environ.get('ORCA')
        except:
            self.ORCA           = ''
            pass
        self.HOME           = os.environ.get('HOME')
        self.GTKDYNAMO_ROOT = os.environ.get('GTKDYNAMO_ROOT')
        self.GTKDYNAMO_GUI  = os.path.join(self.GTKDYNAMO_ROOT, "gui")
        

        #---------------------------------- GTKDYNAMO ------------------------------------#
                                                                                          #
        self.builder = gtk.Builder()                                                      #
        self.builder.add_from_file(                                                       #
            os.path.join(self.GTKDYNAMO_GUI, "MainGUI.glade"))                            #
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
                               'HideWorkSpaceDialog': False    ,  
                               'WorkSpace'          : self.HOME,  
                               'ORCAPATH'           : self.ORCA,
                               'bg_color'           : 'black'  ,
                               'fixed'              : 'grey80' ,
                               'color'              : 'radon'  ,
                               'History'            : {}       }                              

        self.Load_GTKDYNAMO_ConfigFile()
        self.changed = False
        
        try:
            a = self.GTKDynamoConfig['ORCAPATH']
        except:
            self.GTKDynamoConfig['ORCAPATH'] = self.ORCA
        
        
        
        
        #-------------------- config GLarea --------------------#
        #container = self.builder.get_object("container")        #
        #pymol.start()                                           #
        #cmd = pymol.cmd                                         #
        #container.pack_end(glarea)                              #
        #glarea.show()                                           #
        # Remove pymol's scary messages                         #
        #pymol.button(0, 1, 0, 0, 0)                             #
        #-------------------------------------------------------

              #------------------------------------------------#
              #-               PyMOL_initialize                #
              #------------------------------------------------#
        #------------------------------------------------------------#
        #self.PyMOL_initialize()                                      #
        #print text1                                                  #
        #------------------------------------------------------------#
        

        
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
                                      data_path       = GTKDYNAMO_TMP,                                                               #
                                      builder         = self.builder,                                                                #
                                      GTKDynamoConfig = self.GTKDynamoConfig,                                                        #
                                      window_control  = self.window_control)                                                         #
        self.project.PyMOL = True                                                                                                    #
        #----------------------------------------------------------------------------------------------------------------------------#

       
        self.project.settings['data_path'] = GTKDYNAMO_TMP


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
        self.ScanWindow                  = ScanWindow(self)                                     #
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
        
        self.DialogAmber12ToAmber11 = DialogAmber12ToAmber11(self)
        
        self.PreferencesDialog   = PreferencesDialog(self)
                                                                                                #
        self.UmbrellaSamplingWindow = UmbrellaSamplingWindow(self)                              #
                                                                                                #
        self.DialogImportCoordinates = ImportCoordinatesDialog(self)                            #
                                                                                                #
        self.DialogExportCoordinates = ExportCoordinatesDialog(self)                            #
        
        self.AboutDialog             = AboutDialog(self)
        self.SAWDialog               = SAWDialog(self)
        self.NEBDialog               = NEBDialog(self)
        self.EnergyRefineDialog      = TrajectoryEnergyRefineDialog(self)
        
        
        
        self.DialogMOPACSEnergy      = MOPACSEnergyDialog(self)
        
        #---------------------------------------------------------------------------------------#
        self.graph = None


        
        if self.GTKDynamoConfig['HideWorkSpaceDialog'] == False:
            self.WorkSpaceDialog.dialog.run()
            self.WorkSpaceDialog.dialog.hide()

        
        
        # hide widgets - not ethe final version
        self.builder.get_object('toolbutton7_print_tudo').hide()
        #self.builder.get_object('hbox4').hide()
        #cmd.button("double_left","None","None")                 #
        #cmd.button("single_right","None","None")                #
        
        

    def run(self):
        gtk.main()





import pymol
#threading.Thread.__init__(self)                        #
#threading.Thread.__init__(self)                        #
                                                        #
pymol.finish_launching()                                #
        #cmd.button("double_left","None","None")        #

##cmd.button("single_right","None","None")               #
#pymol.cmd.set("internal_gui", 0)                        #
##pymol.cmd.set("internal_gui_mode", 1)                  #
##pymol.cmd.set("internal_feedback", 0)                  #
##pymol.cmd.set("internal_gui_width", 220)               #
#pymol.cmd.set("cartoon_fancy_helices", 'on')            #
#sphere_scale = 0.25                                     #
#stick_radius = 0.15                                     #
#label_distance_digits = 4                               #
#mesh_width = 0.3                                        #
#cmd.set('sphere_scale', sphere_scale)                   #
#cmd.set('stick_radius', stick_radius)                   #
#cmd.set('label_distance_digits', label_distance_digits) #
#cmd.set('mesh_width', mesh_width)                       #
#cmd.set("retain_order")         # keep atom ordering    #
#cmd.bg_color("grey")            # background color      #
#cmd.do("set field_of_view, 70")                         #
#cmd.do("set ray_shadows,off")                           #
#cmd.do('set cartoon_highlight_color, 24')               #
#cmd.set('label_size', 20.00)                            #
#cmd.set('label_color', 'white')                         #
#cmd.set('auto_zoom', 1)                                 #
##cmd.extend('axes', axes)                               #
##axes()                                                 #
##-------------------------------------------------------#




gtk.gdk.threads_init()

from pymol import *
print "Creating object"
gtkdynamo = gtkdynamo_main()
gtkdynamo.PyMOL_initialize()
gtkdynamo.run()

#
#gtkdynamo = gtkdynamo_main()
#pymol.finish_launching()    
#gtk.gdk.threads_init()
##PyMOL_GUIConfig()

#masters = MastersMain()
#masters.run()
#fecha o gateway quando for sair do programa
#p.terminate()
#return 0

#import sys
#if len(sys.argv) > 1:
#    gtkdynamo.project.load_coordinate_file_as_new_system(sys.argv[1])
#    gtkdynamo.project.From_PDYNAMO_to_GTKDYNAMO(type_='new')

#gtkdynamo.run()
