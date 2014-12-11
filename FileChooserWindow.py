

import os
import gtk
import gobject
GTKDYNAMO_ROOT = os.environ.get('GTKDYNAMO_ROOT')
GTKDYNAMO_ROOT = '/home/fernando/Dropbox/GTKPyMOL'
GTKDYNAMO_ROOT = '/home/labio/Dropbox/GTKPyMOL'
GTKDYNAMO_GUI = os.path.join(GTKDYNAMO_ROOT, "gui")


class FileChooserWindow():

    """ Class doc """

    def GetFileName(self, builder):
        """ Function doc """
        _01_window_main = builder.get_object("win")
        filename = None
        chooser = gtk.FileChooserDialog("Open File...", _01_window_main,
                                        gtk.FILE_CHOOSER_ACTION_OPEN,
                                        (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                         gtk.STOCK_OPEN, gtk.RESPONSE_OK))

        filter = gtk.FileFilter()  # adiciona o filtro de busca de arquivos
        filter.set_name("GTKDynamo projects - *.gtkdyn")
        #
        filter.add_mime_type("GTKDynamo projects")
        filter.add_pattern("*.gtkdyn")
        #
        chooser.add_filter(filter)
        filter = gtk.FileFilter()
        filter.set_name("pDynamo pkl files  - *.pkl")
        filter.add_pattern("*.pkl")
        #
        #
        chooser.add_filter(filter)
        filter = gtk.FileFilter()
        filter.set_name("pDynamo yaml files  - *.yaml")
        filter.add_pattern("*.yaml")
        #
        chooser.add_filter(filter)
        filter = gtk.FileFilter()
        filter.set_name("All files")
        filter.add_pattern("*")
        #
        chooser.add_filter(filter)  # termina  - filtro de arquivos.

        # chooser.set_current_folder(data_path)

        response = chooser.run()
        if response == gtk.RESPONSE_OK:
            filename = chooser.get_filename()
        chooser.destroy()

        return filename


    def GetFolderName(self, window):
        """ Function doc """
        #_01_window_main = builder.get_object("win")
        
        
        filename = None
        chooser = gtk.FileChooserDialog("Open File...", window,
                                        gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
                                        (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                         gtk.STOCK_OPEN, gtk.RESPONSE_OK))

        filter = gtk.FileFilter()  # adiciona o filtro de busca de arquivos
        filter.set_name("GTKDynamo projects - *.gtkdyn")
        #
        filter.add_mime_type("GTKDynamo projects")
        filter.add_pattern("*.gtkdyn")
        #
        chooser.add_filter(filter)
        filter = gtk.FileFilter()
        filter.set_name("pDynamo pkl files  - *.pkl")
        filter.add_pattern("*.pkl")
        #
        #
        chooser.add_filter(filter)
        filter = gtk.FileFilter()
        filter.set_name("pDynamo yaml files  - *.yaml")
        filter.add_pattern("*.yaml")
        #
        chooser.add_filter(filter)
        filter = gtk.FileFilter()
        filter.set_name("All files")
        filter.add_pattern("*")
        #
        chooser.add_filter(filter)  # termina  - filtro de arquivos.

        # chooser.set_current_folder(data_path)

        response = chooser.run()
        if response == gtk.RESPONSE_OK:
            filename = chooser.get_filename()
        chooser.destroy()

        return filename
