#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  WindowControl.py
#
#  Copyright 2014 Labio <labio@labio-XPS-8300>
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
import gtk
import gobject
import pango

class WindowControl():

    """ Class doc 
    Needed to fill the contents of combobox, 
    spin buttons and other widgets.

    - this object has been created for the 
    EasyHybrid_main class contains only those 
    methods associated with the events.

    """

    def __init__(self, builder):
        """ Class initialiser """
        self.builder = builder
        self.FileChooserWindow_TrueFalse = False
        self.window3                     = False  # not available yet
        self.ScanWindow                  = False
        self.Scan2DWindow                = False
        
    def SETUP_COMBOBOXES(self, combobox=None, combolist=[], active=0):
        """ Function doc """

        cbox = self.builder.get_object(combobox)  # ----> combobox_MM_model
        store = gtk.ListStore(gobject.TYPE_STRING)
        cbox.set_model(store)

        for i in combolist:
            cbox.append_text(i)

        cell = gtk.CellRendererText()
        cbox.pack_start(cell, True)
        cbox.add_attribute(cell, 'text', 0)
        cbox.set_active(active)
        #'01_main_window_combobox_MM_model'

    def TREEVIEW_ADD_DATA(self, liststore=None, pymol_objects=[], active=0):
        """ Function doc """
        model = liststore  # @+
        model.clear()
        n = 0
        for i in pymol_objects:
            data = [i]
            model.append(data)
            n = n + 1

    def TREEVIEW_ADD_DATA2(self, liststore=None, job_history={}, pymol_id=None):
        """ Function doc """

        model = liststore  
        model.clear()
        n = 0
                       
                       
                       
                         # this is necessary to sort the job_history #
        #-----------------------------------------------------------------------------#
        numbers  = list(job_history)                                                  #
        #print job_history                                                             #
        numbers2 = []                                                                 #
        #print numbers                                                                 #
                                                                                      #
        for i in numbers:                                                             #
            numbers2.append(int(i))                                                   #
        numbers2.sort()                                                               #
        #print numbers2                                                                #
        #-----------------------------------------------------------------------------#


        for i in numbers2:
            i = str(i)
            cell = self.builder.get_object('cellrenderertext2')
            cell.props.weight_set = True
            cell.props.weight = pango.WEIGHT_NORMAL
            data = [False, i                          ,
                           job_history[i]['object']   , #job_history[i][0],
                           job_history[i]['type']     , #job_history[i][1],
                           job_history[i]['potencial']] #job_history[i][2]]

            if job_history[i]['object'] == pymol_id:
               
                cell = self.builder.get_object('cellrenderertext2')
                #cell.props.weight_set = True
                cell.props.weight = pango.WEIGHT_BOLD
                
                data = [True, i                          ,
                              job_history[i]['object']   , 
                              job_history[i]['type']     ,
                              job_history[i]['potencial']]

            model.append(data)
            n = n + 1
        

        '''
        for i in job_history:
            cell = self.builder.get_object('cellrenderertext2')
            cell.props.weight_set = True
            cell.props.weight = pango.WEIGHT_NORMAL
            data = [False, job_history[i]['object']   , #job_history[i][0],
                           job_history[i]['type']     , #job_history[i][1],
                           job_history[i]['potencial']] #job_history[i][2]]
            

            
            if job_history[i]['object'] == pymol_id:
               
                cell = self.builder.get_object('cellrenderertext2')
                #cell.props.weight_set = True
                cell.props.weight = pango.WEIGHT_BOLD
                
                data = [True, job_history[i]['object']   , 
                              job_history[i]['type']     ,
                              job_history[i]['potencial']]

            model.append(data)
            n = n + 1
        '''


    def STATUSBAR_SET_TEXT(self, text):
        """ Function doc """
        self.builder.get_object('statusbar1').push(0, text)

    def SETUP_SPINBUTTON (self, spinbutton, config):
        """ Function doc """
        adjustment  = gtk.Adjustment(config[0],config[1],config[2],config[3],config[4],config[5])
        SpinButton  = self.builder.get_object(spinbutton)
        SpinButton.set_adjustment(adjustment)	
        SpinButton.update()




def main():

    return 0

if __name__ == '__main__':
    main()
