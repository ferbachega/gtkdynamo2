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
import time
from pBabel import *
from pCore import *
from pMolecule import *
from pMoleculeScripts import *


def DualTextLog(path, filename="log.gui.txt"):
    """ The new  DualTextLog writes the log files right to the 
    diretory where the job is already running."""

    header = '''
#-----------------------------------------------------------------------------#
#                                                                             #
#                                GTKDYNAMO                                    #
#                        - A pDynamo graphical tool -                         #
#                                                                             #
#-----------------------------------------------------------------------------#
#                                                                             #
#     Developed by Jose Fernando R Bachega and Luis Fernando S M Timmers      #
#                            <ferbachega@gmail.com>                           #
#                                                                             #
#             visit: https://sites.google.com/site/gtkdynamo/                 #
#                   Univesity of Sao Paulo - SP, Brazil                       #
#      Pontifical Catholic University of Rio Grande do Sul - RS, Brazil       #
#                                                                             #
#                                                                             #
#   GTKDynamo team:                               Special thanks to:          #
#   - Jose Fernando R Bachega           |         - Fernando V Maluf          #
#   - Troy Wymore                       |         - Lucas Assirati            #
#   - Martin Field                      |         - Leonardo R Bachega        #
#   - Osmar Norbeto de souza            |         - Richard Garratt           #
#   - Luis Fernando S M Timmers         |                                     #
#   - Walter R Paixao-Cortes            |                                     #
#   - Michele Silva                     |                                     #
#                                                                             #
#   Cite this work as:                                                        #
#   J.F.R. Bachega, L.F.S.M. Timmers, L.Assirati, L.B. Bachega, M.J. Field,   #
#   T. Wymore. J. Comput. Chem. 2013, 34, 2190-2196. DOI: 10.1002/jcc.23346   #
#                                                                             #
#-----------------------------------------------------------------------------#

'''
    path = path

    #------------------------------------------------------------------------------------#
    #               Removing the temp file: residual log files.txt                       #
    #------------------------------------------------------------------------------------#
    #
    try:
        os.rename(os.path.join(path, filename), os.path.join(
            path, filename + '.old'))     #
    #
    except:
        #
        pass
    #------------------------------------------------------------------------------------#
    log_out = open(os.path.join(path, filename), "a")

    localtime = time.asctime(time.localtime(time.time()))                 #
    localtime = "Generated on:" + localtime + '\n\n'
    header = header + localtime
    log_out.write(header)
    log_out.close()
    # Generated in: Tue Sep 30 16:57:58 2014

    class DualTextLogFileWriter (TextLogFileWriter):

        def Text(self, text):
            #"""Text."""
            # if self.isActive and ( text is not None ): #old code M.F.
            self.file.write(text)
            log_out = open(os.path.join(path, filename), "a")  # RWM / Bachega
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
    _min_ = pDynamoMinimization(system, 'Steepest Descent')
    #_min_    = pDynamoMinimization(system,'LBFGS')
    #
    return 0

if __name__ == '__main__':
    main()
