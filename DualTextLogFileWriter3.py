#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  DualTextLogFileWriter2.py
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
import os
import sys
from pBabel import *
from pCore import *
from pMolecule import *
from pMoleculeScripts import *


def DualTextLog(path):
    """ Function doc """
    GTKDYNAMO_TMP = path

    class DualTextLogFileWriter (TextLogFileWriter):

        def Text(self, text):
            #"""Text."""
            # if self.isActive and ( text is not None ): #old code M.F.
            self.file.write(text)
            # RWM / Bachega
            log_out = open(os.path.join(GTKDYNAMO_TMP, "log.gui.txt"), "a")
            # redirects output to a log text file
            log_out.write(text)
            log_out.close()

    dualLog = DualTextLogFileWriter()
    return dualLog


def main():
    dualLog = DualTextLog('/home/fernando/Pictures/')

    GTKDYNAMO_ROOT = os.getcwd()

    system = Unpickle(GTKDYNAMO_ROOT + '/test/test.pkl')
    system.Summary(log=dualLog)

    system.Energy(log=dualLog)
    #_min_    = pDynamoMinimization(system)
    #_min_    = pDynamoMinimization(system,'Steepest Descent')
    #_min_    = pDynamoMinimization(system,'LBFGS')
    #
    return 0

if __name__ == '__main__':
    main()
