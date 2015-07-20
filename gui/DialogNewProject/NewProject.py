#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  mydialog.py
#
#  Copyright 2014 Fernando Bachega <fernando@bachega>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#
#
import os
import gtk
import gobject
from PyMOLScripts.PyMOLScripts import *
from WindowControl import *
import time

#GTKDYNAMO_ROOT   = os.environ.get('GTKDYNAMO_ROOT')
#GTKDYNAMO_ROOT   = '/home/fernando/Dropbox/GTKPyMOL'
#GTKDYNAMO_ROOT   = '/home/labio/Dropbox/GTKPyMOL'
#GTKDYNAMO_ROOT = os.getcwd()
GTKDYNAMO_ROOT = os.environ.get('GTKDYNAMO_ROOT')

GTKDYNAMO_GUI = os.path.join(GTKDYNAMO_ROOT, "gui")


class NewProjectDialog():

    """ Class doc """
    def on_new_project_entry_changed (self, entry):
		""" Function doc """
		text      = self.builder.get_object("new_project_entry").get_text()
		WorkSpace = self.GTKDynamoSession.GTKDynamoConfig['WorkSpace']
		try:
			path      = os.path.join(WorkSpace, text)
			
			self.builder.get_object("ProjectDirectory").set_text(path)
		except:
			pass
			
    def on_combobox1_changed(self, combobox):
        """ Function doc """

        fftype = self.builder.get_object("combobox1").get_active_text()

        if fftype == "AMBER":
            print fftype
            self.builder.get_object("amber_prmtop_label").  show()
            self.builder.get_object("amber_prmtop_chooser").show()
            self.builder.get_object("charmm_topologies_label").hide()
            self.builder.get_object("charmm_topologies_chooser").hide()
            self.builder.get_object("opls_prmtop_label").hide()
            self.builder.get_object("opls_prmtop_chooser").hide()

        if fftype == "CHARMM":
            print fftype
            self.builder.get_object("opls_prmtop_label").hide()
            self.builder.get_object("opls_prmtop_chooser").hide()

            self.builder.get_object("amber_prmtop_label").  show()
            self.builder.get_object("amber_prmtop_chooser").show()
            self.builder.get_object("charmm_topologies_label").show()
            self.builder.get_object("charmm_topologies_chooser").show()

        if fftype == "GROMACS":
            print fftype
            self.builder.get_object("amber_prmtop_label").  show()
            self.builder.get_object("amber_prmtop_chooser").show()
            self.builder.get_object("charmm_topologies_label").hide()
            self.builder.get_object("charmm_topologies_chooser").hide()
            self.builder.get_object("opls_prmtop_label").hide()
            self.builder.get_object("opls_prmtop_chooser").hide()

        if fftype == "OPLS":
            print fftype
            self.builder.get_object("amber_prmtop_label").  hide()
            self.builder.get_object("amber_prmtop_chooser").hide()
            self.builder.get_object("opls_prmtop_label").show()
            self.builder.get_object("opls_prmtop_chooser").show()
            self.builder.get_object("charmm_topologies_label").  hide()
            self.builder.get_object("charmm_topologies_chooser").hide()

        if fftype == "pDynamo files(*.pkl,*.yaml)":
            self.builder.get_object("opls_prmtop_label").hide()
            self.builder.get_object("opls_prmtop_chooser").hide()

            self.builder.get_object("amber_prmtop_label").  hide()
            self.builder.get_object("amber_prmtop_chooser").hide()
            self.builder.get_object("charmm_topologies_label").  hide()
            self.builder.get_object("charmm_topologies_chooser").hide()

        if fftype == "Other(*.pdb,*.xyz,*.mol2...)":
            self.builder.get_object("opls_prmtop_label").hide()
            self.builder.get_object("opls_prmtop_chooser").hide()

            self.builder.get_object("amber_prmtop_label").  hide()
            self.builder.get_object("amber_prmtop_chooser").hide()
            self.builder.get_object("charmm_topologies_label").  hide()
            self.builder.get_object("charmm_topologies_chooser").hide()

    # "old import_molmec_system(*args): "
    def on_button1_clicked_create_new_project(self, button):
        
        
        BufferText =  self.builder.get_object('textview1').get_buffer()  #
        BufferText = BufferText.get_text(*BufferText.get_bounds(), include_hidden_chars=False)
        #print BufferText
        
        #print '\n\n\n' + BufferText + '\n\n\n' + 'teste aqui'
                
        project          = self.project
        name             = self.builder.get_object("new_project_entry").get_text()
        ProjectDirectory = self.builder.get_object("ProjectDirectory").get_text()
        
        ProjectDirectory = ProjectDirectory.split('/')
        path = '/'
        for i in ProjectDirectory:
            path = os.path.join(path, i)
            if not os.path.exists (path): 
                os.mkdir (path)
        
       #data_path = self.builder.get_object("filechooserbutton1").get_filename()
        data_path = self.builder.get_object("ProjectDirectory").get_text()
        FileType = self.builder.get_object("combobox1").get_active_text()			# combo box combox_model
        filename = os.path.join(data_path,name)
        
        
        
        filesin = {}
        
        try:
            import shutil
        except:
            print "shutil module is no available"

        if FileType == "AMBER":
            filesin['amber_params'] = self.builder.get_object(
                "amber_prmtop_chooser").get_filename()
            filesin['amber_coords'] = self.builder.get_object(
                "amber_inpcrd_chooser").get_filename()

        elif FileType == "CHARMM":
            filesin['charmm_params'] = self.builder.get_object(
                "amber_prmtop_chooser").get_filename()
            filesin['charmm_topologies'] = self.builder.get_object(
                "charmm_topologies_chooser").get_filename()
            filesin['charmm_coords'] = self.builder.get_object(
                "amber_inpcrd_chooser").get_filename()

        elif FileType == "GROMACS":
            filesin['gromacs_params'] = self.builder.get_object(
                "amber_prmtop_chooser").get_filename()					#
            filesin['gromacs_coords'] = self.builder.get_object(
                "amber_inpcrd_chooser").get_filename()

        elif FileType == "OPLS":
            filesin['opls_params'] = self.builder.get_object(
                "opls_prmtop_chooser").get_filename()
            filesin['opls_coords'] = self.builder.get_object(
                "amber_inpcrd_chooser").get_filename()

        elif FileType == "pDynamo files(*.pkl,*.yaml)":
            filesin['pDynamoFile'] = self.builder.get_object(
                "amber_inpcrd_chooser").get_filename()					#

        elif FileType == "Other(*.pdb,*.xyz,*.mol2...)":
            filesin['coordinates'] = self.builder.get_object(
                "amber_inpcrd_chooser").get_filename()					#


        self.project          = self.GTKDynamoSession.project
       
        #self.project.DeleteActualProject()
        self.project.Create_New_Project(
            name, data_path, FileType, filesin, BufferText)
        
        self.project.Save_Project_To_File (filename = filename, type_ = 'pkl')
        
        
        # self.project.From_PDYNAMO_to_GTKDYNAMO()
        self.project.system.Summary()
        self.project.settings['add_info']  =  BufferText

        #

    def __init__(self, GTKDynamoSession = None):
		""" Class initialiser """
		self.builder          = gtk.Builder()

		if GTKDynamoSession != None:
			self.project          = GTKDynamoSession.project
			self.main_builder     = GTKDynamoSession.builder
			self.GTKDynamoSession = GTKDynamoSession

		self.builder.add_from_file(
			os.path.join(GTKDYNAMO_GUI,'DialogNewProject', 'NewProjectDialog.glade'))
		self.builder.connect_signals(self)
		self.dialog = self.builder.get_object('dialog1')
		self.dualLog = None
		#self.scrath  = os.environ.get('PDYNAMO_SCRATCH')
		#
		#self.builder.get_object('ProjectDirectory').set_text(self.scrath )
		'''
		--------------------------------------------------
		-                                                -
		-	              WindowControl                  -
		-                                                -
		--------------------------------------------------
		'''
		self.window_control = WindowControl(self.builder)

		#----------------- Setup ComboBoxes -------------------------#
		combobox = 'combobox1'                                      #
		combolist = ["AMBER",                                        #
					 "CHARMM",                                       #
					 #
					 "GROMACS",
					 #
					 "OPLS",
					 #
					 "pDynamo files(*.pkl,*.yaml)",
					 "Other(*.pdb,*.xyz,*.mol2...)"]                 #
		#
		self.window_control.SETUP_COMBOBOXES(combobox, combolist, 0)
		#------------------------------------------------------------#

		localtime = time.asctime(time.localtime(time.time()))
		print "Local current time :", localtime
		localtime = localtime.split()

		#  0     1    2       3         4
		#[Sun] [Sep] [28] [02:32:04] [2014]
		text = 'NewProjec_' + localtime[1] + \
			'_' + localtime[2] + '_' + localtime[4]
		self.builder.get_object("new_project_entry").set_text(text)


		#WorkSpace = self.GTKDynamoSession.GTKDynamoConfig['WorkSpace']
		#path      = os.path.join(WorkSpace, text)
		#self.builder.get_object("ProjectDirectory").set_text(text)

def main():
    dialog = NewProjectDialog()
    dialog.dialog.run()
    dialog.dialog.hide()
if __name__ == '__main__':
    main()
