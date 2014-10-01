#!/usr/bin/env python


# System
import datetime
import time
import pygtk
pygtk.require('2.0')
import gtk


import thread
import threading
import gobject
import sys
import glob
import math
import os


if not sys.platform.startswith('win'):
    HOME = os.environ.get('HOME')
else:
    HOME = os.environ.get('PYMOL_PATH')


GTKDYNAMO_ROOT = os.environ.get('GTKDYNAMO_ROOT')
GTKDYNAMO_GUI = os.path.join(GTKDYNAMO_ROOT, "gui")


try:
    # gtk.rc_parse('gtkrc')
    gtk.rc_parse(os.path.join(GTKDYNAMO_ROOT, '.gtkrc'))

except:
    print '\n\n\ file not found \n\n'
    pass


builder = gtk.Builder()
builder.add_from_file("gui.glade")


class main_window():

    def __init__(self):
        """ Class initialiser """
        self.builder = builder
        self.window_main = builder.get_object("dialog1")
        self.window_main.show_all()
        gtk.main()

main_window = main_window()
