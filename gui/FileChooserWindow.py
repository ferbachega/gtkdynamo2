

import os
import gtk
import gobject
EasyHybrid_ROOT = os.environ.get('EasyHybrid_ROOT')
#EasyHybrid_ROOT = '/home/fernando/Dropbox/GTKPyMOL'
#EasyHybrid_ROOT = '/home/labio/Dropbox/GTKPyMOL'
EasyHybrid_GUI = os.path.join(EasyHybrid_ROOT, "gui")


class FileChooserWindow():

    """ Class doc """
    def GetLogFileName(self, builder):
        """ Function doc """
        _01_window_main = builder.get_object("win")
        filename = None
        chooser = gtk.FileChooserDialog("Open File...", _01_window_main,
                                        gtk.FILE_CHOOSER_ACTION_OPEN,
                                        (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                         gtk.STOCK_OPEN, gtk.RESPONSE_OK))

        filter = gtk.FileFilter()  
        filter.set_name("EasyHybrid logs - *.log")
        #
        filter.add_mime_type("EasyHybrid logs")
        filter.add_pattern("*.log")
        #
        chooser.add_filter(filter)
        filter = gtk.FileFilter()
        filter.set_name("All files")
        filter.add_pattern("*")
        #
        chooser.add_filter(filter)  
        # chooser.set_current_folder(data_path)

        response = chooser.run()
        if response == gtk.RESPONSE_OK:
            filename = chooser.get_filename()
        chooser.destroy()

        return filename


    def GetFileName(self, builder):
        """ Function doc """
        _01_window_main = builder.get_object("win")
        filename = None
        chooser = gtk.FileChooserDialog("Open File...", _01_window_main,
                                        gtk.FILE_CHOOSER_ACTION_OPEN,
                                        (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                         gtk.STOCK_OPEN, gtk.RESPONSE_OK))

        filter = gtk.FileFilter()  
        filter.set_name("EasyHybrid projects - *.gtkdyn")
        #
        filter.add_mime_type("EasyHybrid projects")
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
        chooser.add_filter(filter)  
        # chooser.set_current_folder(data_path)

        response = chooser.run()
        if response == gtk.RESPONSE_OK:
            filename = chooser.get_filename()
        chooser.destroy()

        return filename


    def GetFolderName(self, window, multiple = False):
        """ Function doc """
        #_01_window_main = builder.get_object("win")
       
        filename = None
        chooser = gtk.FileChooserDialog("Open File...", window,
                                        gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
                                        (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                         gtk.STOCK_OPEN, gtk.RESPONSE_OK))

        chooser.set_select_multiple(multiple)
            
        response = chooser.run()
        if response == gtk.RESPONSE_OK:
            filenames = chooser.get_filenames()
        chooser.destroy()
        print filenames
        return filenames if multiple else filenames[0]
