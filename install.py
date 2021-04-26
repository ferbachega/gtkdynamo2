#!/usr/bin/env python
text1 = """
#
#
#
#
#
#
#
#                         ---- EasyHybrid %s - GTKDynamo ----
#
#
#       Copyright 2012 Jose Fernando R Bachega  <ferbachega@gmail.com>
#
#               visit: https://sites.google.com/site/EasyHybrid/
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
#   EasyHybrid team:
#   - Jose Fernando R Bachega   - Pontifical Catholic University of Rio Grande do Sul - RS, Brazil
#   - Troy Wymore               - Pittsburgh Super Computer Center, Pittsburgh PA - USA
#   - Martin Field              - Institut de Biologie Structurale, Grenoble, France
#   - Luis Fernando S M Timmers - Pontifical Catholic University of Rio Grande do Sul - RS, Brazil
#   - Michele Silva             - Pontifical Catholic University of Rio Grande do Sul - RS, Brazil
#
#   Special thanks to:
#   - Osmar Norberto de Souza   - Pontifical Catholic University of Rio Grande do Sul - RS, Brazil
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
""" % ('2.0')
print text1




#------------------------------------------------------------------------------
#import threading

#import gobject

import sys

#import glob

#import math

import os

#System

import datetime

import time
#------------------------------------------------------------------------------




class InstallPDynamo:
    '''
    #-------------------------------------------------------------------------#
    #                        Installing pDynamo                               #
    #-------------------------------------------------------------------------#
    '''
    def __init__ (self):
        """ Function doc """
        pass
        
    def _install_python_dev (self):
        """ Function doc """
        try:
            if self.OpSystem == 'debian':                                                    
                os.system("sudo apt-get install python-dev")                       


            if self.OpSystem == 'suse':                                                      
                os.system("sudo zypper install python-devel") 


            if self.OpSystem == 'centos':
                os.system("sudo yum install python-devel")
            
            if self.OpSystem == 'fedora':
                os.system("sudo dnf install python-devel")
            
            if self.OpSystem == 'gentoo':
                os.system("sudo emerge -av python-devel")

            if self.OpSystem == 'macos':
                pass
                #os.system("sudo port install python-devel") # rever esta parte
                #os.system("sudo port install python-dev")   # rever esta parte
        except:
            print  'python-dev instalation failed'

    def _install_Cython (self, folder = None, verison = None, Cython = None):
        s = raw_input('\nWould like install Cython? (Y/n):')
        
        if s in self.answer: 
            #Cython-0.19 
            #-------------------------------------------------------------------------------------#
            #folder = os.getcwd()                                                                 #
            print "\n\n\nInstalling Cython (superuser permission required)..."                    #
            path   = os.path.join(folder, verison + "/thirdParty/" + Cython)                      #
            os.chdir(path)                                                                        #
            os.system("sudo python setup.py install")                                             #
            print "Cython installation done."                                                     #
            return True
            #-------------------------------------------------------------------------------------# 
        else:
            return False
        
    def _install_PyYAML (self, folder= None, verison= None, PyYAML= None):
        """ Function doc """
        s = raw_input('\nWould like install PyYAML? (Y/n):')
        
        if s in self.answer: 
            #PyYAML-3.10
            #-------------------------------------------------------------------------------------#
            os.system("ls ")                                                                      #
            print "\n\n\nInstalling PyYAML..."                                                    #
            path   = os.path.join(folder, verison + "/thirdParty/" + PyYAML)                      #
            os.chdir(path)                                                                        #
            os.system("sudo python setup.py install")	                                          #
            print "PyYAML installation done."                                                     #
            #-------------------------------------------------------------------------------------#
            return True
        else:
            return False
            
    def _get_Cython_PyYAML_version (self):
        """ Function doc """
        s = raw_input('\n(1)pDynamo-1.9.0\n(2)pDynamo-1.8.0\n(3)pDynamo-1.7.2\n(4)other\nSelect a pDynamo version(1):')
        
        if s == "1" or s == "":
            version = "1.9.0"
            Cython  = "Cython-0.19"
            PyYAML  = "PyYAML-3.10"

        if s == "2":
            version = "1.8.0"
            Cython  = "Cython-0.19"
            PyYAML  = "PyYAML-3.10"

        if s == "3":
            version = "1.7.2"
            Cython  = "Cython-0.15.1"
            PyYAML  = "PyYAML-3.09"

        if s == "4":
            s2      = raw_input('Type the required version (eg. "1.7.2"):')
            Cython  = raw_input('Type the Cython version (Cython-0.19):')
            PyYAML  = raw_input('Type the PyYAML version (PyYAML-3.10):')
            
            if Cython == "":
                Cython = "Cython-0.19"
            if PyYAML == "":
                PyYAML = "PyYAML-3.10"
            version = s2
        verison = "pDynamo-" + version
        
        return Cython, PyYAML, verison

    def _wget_pDynamo (self, verison = None):
        
        """ Function doc """

        s = raw_input('\nWhere would you like to install pDynamo? (' + self.HOME +'):')

        if s == '':
            s = self.HOME					

        folder = s
        os.chdir(s)



            # checking for the pDynamo installation file - eg: pDynamo-1.9.0.tgz
        if os.path.isfile(verison + ".tgz"):
            pass
        else:
            #-----------------------------------------------------------------------------------
            # WGET - DOWNLOAD
            #-----------------------------------------------------------------------------------
            #os.system("wget https://sites.google.com/site/pdynamomodeling/" + verison + ".tgz") 
            os.system("wget https://sites.google.com/site/gtkdynamo/download/pDynamo-1.9.0.tgz") 
            #-----------------------------------------------------------------------------------

        

        #-----------------------------------------------------------------------------------
        # TARGZ
        #-----------------------------------------------------------------------------------
        os.system("tar -xzvf "+ verison + ".tgz")                                           
        #-----------------------------------------------------------------------------------
        return folder
    
    def _install_pDynamo_script (self, folder = None , verison = None ):
        """ Function doc """
        #--------------------------------------------------------------#
        #                          PDYNAMO                             #
        #--------------------------------------------------------------#
        path   = os.path.join(folder, verison + "/installation")       #
        os.chdir(path)                                                 #
        pDy_installation_path = path                                   #
        #--------------------------------------------------------------#

        print "Installing pDynamo"                                                                  
        os.system("python Install.py")	                                                            
        #bashrc  -  pDynamo                                                                         
        self.answer = ["Y", "y", "Yes", "yes", "YES", "yEs", "yeS", ""]	                            
        
        if self.OpSystem == 'macos':
            s = raw_input('\nWould like to auto add information to the .profile? -pDynamo- (Y/n):')
        else:
            s = raw_input('\nWould like to auto add information to the .bashrc? -pDynamo- (Y/n):') 

        text = "\n#pDynamo \n"                                                                      
        text = text + "source " + pDy_installation_path + "/environment_bash.com\n"                 
                                                                                                    
        if s in self.answer:                                                                        
            if self.OpSystem == 'macos':
                arq  = open(os.path.join(self.HOME +"/.profile"), "a")
            else:
                arq  = open(os.path.join(self.HOME +"/.bashrc"), "a")                                        
            
            
            arq.writelines(text)                                                                    
            arq.close()                                                                             
            print "The .bashrc file has been modified"                                              
            print "obs:if you are using CSH please do it manually"                                  
                                                                                                    
        else:                                                                                       
            print "\n\nPlease add to the .bashrc the following lines:"                              
            print text                                                                              
            print "\n\nobs:if you are using CSH please do it manually"		                        

    def install_pDynamo ( self ):
        '''
        |install python dev| -> |obtaing pDynamo versions| -> |wget pDynamo| 

                                ||
                                ||
                               \  /
                                \/
        
        -> |install Cython| -> |install PyYAML| -> |install pdynamo|
        '''
        s = raw_input('\nWould like to auto install pDynamo? (Y/n):')
        if s in self.answer:
        
            #try:

            
            
            #-------------------------------------------------------------------------------------#
            #                       obtaing Cython, PyYAML and pDynamo versions                   #
            #-------------------------------------------------------------------------------------#
            Cython, PyYAML, verison = self._get_Cython_PyYAML_version()
            print Cython, PyYAML, verison
            
            #-------------------------------------------------------------------------------------#
            folder = self._wget_pDynamo(verison = verison)                                        #
            #-------------------------------------------------------------------------------------#
        
            #-------------------------------------------------------------------------------------#
            #                                    PYTHON DEV                                       #
            #-------------------------------------------------------------------------------------#
            self._install_python_dev()                                                            #
            #-------------------------------------------------------------------------------------#
            
            #-------------------------------------------------------------------------------------#
            #                                    Cython-0.19                                      #
            #-------------------------------------------------------------------------------------#
            self._install_Cython (folder = folder, verison = verison, Cython = Cython)            #
            #-------------------------------------------------------------------------------------#
            

            #-------------------------------------------------------------------------------------#
            #                                   #PyYAML-3.10                                      #
            #-------------------------------------------------------------------------------------#
            self._install_PyYAML (folder = folder, verison = verison, PyYAML = PyYAML)            #
            #-------------------------------------------------------------------------------------#


            #-------------------------------------------------------------------------------------#
            #                                Installing pDynamo                                   #
            #-------------------------------------------------------------------------------------#
            self._install_pDynamo_script ( folder = folder , verison = verison )                  #
            #-------------------------------------------------------------------------------------#


            #except:
            #    print "\n - - -pDynamo installation failed - - - "
            #    print "\nPlease check: \nhttps://sites.google.com/site/pdynamomodeling/installation\n"
        else:
            print "\nPlease check: \nhttps://sites.google.com/site/pdynamomodeling/installation\n"
        

class InstallPyMOL:
    '''
    #-----------------------------------#
    #               PYMOL               #
    #-----------------------------------#
    '''    
    def __init__ (self):
        """ Class initialiser """
        pass

    def install_PyMOL ( self ):
        s = raw_input('\nWould like install PyMOL (Y/n):') 
        
        if s in self.answer:                                                                          
            
            try:
                #print self.OpSystem
                if self.OpSystem == 'debian':                                                               
                    os.system("sudo apt-get install pymol")  
                
                if self.OpSystem == 'suse':                                                                 
                    os.system("sudo zypper install pymol")  
                                  
                
                if self.OpSystem == 'centos':
                    os.system("sudo yum install pymol")
                
                
                if self.OpSystem == 'fedora':
                    os.system("sudo dnf install pymol")
                

                if self.OpSystem == 'gentoo':
                    os.system("sudo emerge -av pymol")                
                

                if self.OpSystem == 'macos':
                    os.system("sudo port install tcl -corefoundation")
                    os.system("sudo port install tk -quartz")
                    os.system("sudo port install pymol")                 
                
                
                if self.OpSystem == 'other':
                    print '\nPlease install pyGTK\n'
                    
 
            except:
                print 'PyMOL instalation failed'


class InstallGTK:
    '''
    #-----------------------------------#
    #           GTK  and   PyGTK        #
    #-----------------------------------#
    '''    
    def __init__ (self):
        """ Class initialiser """
        pass

    def install_GTK   ( self):
        s = raw_input('\nWould like install GTK (Y/n):')
        if s in self.answer:
            print "\nInstalling GTK\n"

            try:
                if self.OpSystem == 'debian':                                                    
                    os.system("sudo apt-get install libgtk2.0-0")
                    os.system("sudo apt-get install python-gtk2")                       
                

                if self.OpSystem == 'suse':                                                      
                    os.system("sudo zypper install gtk2") 

                
                if self.OpSystem == 'fedora':
                    os.system("sudo dnf install gtk2")
                    os.system("sudo dnf install gtk3")

                
                if self.OpSystem == 'centos':
                    os.system("sudo yum install gtk2")
                    os.system("sudo dnf install gtk3")

                
                if self.OpSystem == 'gentoo':
                    os.system("sudo emerge -av gtk")
                    os.system("sudo emerge -av gtk2")
                    os.system("sudo emerge -av gtk3")

                if self.OpSystem == 'macos':
                    os.system("sudo port install gtk2")
                    os.system("sudo port install gtk-engines2")
                    os.system("sudo port install gtk-theme-switch")

                if self.OpSystem == 'other':
                    print '\nPlease install GTK2\n'

            except:
                print  'GTK instalation failed'
    
    def install_pyGTK ( self ):
        """ Function doc """
        s = raw_input('\nWould like install PyGTK (Y/n):')
        if s in self.answer:
        
            print "\n Installing pyGTK \n"
            try:
                if self.OpSystem == 'debian':                                                    
                    os.system("sudo apt-get install python-gtk2") 


                if self.OpSystem == 'suse':                                                      
                    os.system("sudo zypper install python-gtk") 

                
                if self.OpSystem == 'fedora':
                    os.system("sudo dnf install  pygtk2")
                    #os.system("")
                
                if self.OpSystem == 'centos':
                    os.system("sudo yum install pygtk")
                    os.system("sudo yum install pygtk2")


                if self.OpSystem == 'gentoo':
                    os.system("sudo emerge -av pygtk")
                    os.system("sudo emerge -av pygtk2")


                if self.OpSystem == 'macos':
                    os.system("sudo port install py27-pygtk")
                
                if self.OpSystem == 'other':
                    print '\nPlease install pyGTK\n'
                
            except:
                print  'pyGTK instalation failed'


class InstallMatPlotLib:
    """
   #-----------------------------------#
   #             matplotlib            #
   #-----------------------------------#
    
    """
    
    def __init__ (self):
        """ Class initialiser """
        pass

    def install_matplotlib ( self ):
        s = raw_input('\nWould like install matplotlib (Y/n):')                               
        if s in self.answer:
            try:
                if self.OpSystem == 'debian':                                                    
                    os.system("sudo apt-get install python-matplotlib")                     
                
                
                if self.OpSystem == 'suse':                                                      
                    os.system("sudo zypper install python-numpy-devel")
                    os.system("sudo zypper install python-matplotlib")
                    os.system("sudo zypper install python-matplotlib-gtk2")

                
                if self.OpSystem == 'fedora':
                    os.system("sudo dnf install  python-matplotlib")
                    os.system("sudo dnf install  python2-matplotlib-gtk")

                
                if self.OpSystem == 'centos':
                    os.system("sudo yum install python-numpy-devel")
                    os.system("sudo yum install python-matplotlib")
                    os.system("sudo yum install python-matplotlib-gtk2") 


                if self.OpSystem == 'gentoo':
                    os.system("sudo emerge -av python-numpy-devel")
                    os.system("sudo emerge -av python-matplotlib")
                    os.system("sudo emerge -av python-matplotlib-gtk2")


                if self.OpSystem == 'macos':
                    os.system("sudo port install py27-matplotlib +gtk2")

                

                if self.OpSystem == 'other':
                    print '\nPlease install python-matplotlib / python-matplotlib-gtk2'

            except:
                print  'matplotlib instalation failed'


class InstallEasyHybrid (InstallPDynamo, InstallPyMOL, InstallGTK, InstallMatPlotLib):
    """ Class doc """
    
    def __init__ (self, log = False):
        """ Class initialiser """
        #-----------------------------------------------#
        #                   System
        #-----------------------------------------------#
        self.OpSystem  = None
        self.log       = log
        #-----------------------------------------------#

        #-----------------------------------------------
        if not sys.platform.startswith('win'):
            self.HOME = os.environ.get('HOME')
        else:         
            self.HOME = os.environ.get('PYMOL_PATH')
        #-----------------------------------------------


        #-----------------------------------------------#
        #                  installer
        self.answer  = ["Y", "y", "Yes", "yes", "YES", "yEs", "yeS", ""]	
        #-----------------------------------------------#

        
        #-----------------------------------------------#
        #            installation parameters            #
        #-----------------------------------------------#
        self.GTK        = False
        self.pyGTK      = False
        self.python_dev = False
        self.PyMOL      = False
        self.matplotlib = False
        self.pDynamo    = False
        self.ORCA       = False
        self.easyhybrid = False
        #-----------------------------------------------#
        
        #-----------------------------------------------#
        self.folder         = os.getcwd()
        self.gtkdyn_folder  = os.getcwd()
        self.orca_folder    = ''
        #-----------------------------------------------#
    
    def install_all (self):
        """ Function doc """
        self._get_system_parameters()
        

        """ OpSystem """
        if self.OpSystem:
            self._check_dependencies()
        else:
            print '\nInstallation aborted! \n\n'
            return False

        
        """ GTK """
        if self.GTK:
            pass
        else:
            self.install_GTK()


        """ pyGTK """
        if self.pyGTK:
            pass
        else:
            self.install_pyGTK()


        
        """ PyMOL """
        if self.PyMOL:
            pass
        else:
            self.install_PyMOL()



        """ matplotlib """
        if self.matplotlib:
            pass
        else:
            self.install_matplotlib()

        
        
        """ pDynamo """
        if self.pDynamo:
            pass
        else:
            self.install_pDynamo()

        
        
        """ ORCA """
        if self.ORCA:
            pass
        else:
            self.install_ORCA()
       
       
        """ EasyHybrid """
        if self.easyhybrid:
            pass
        else:
            self.install_EasyHybrid()
            
        

        try:
            if self.OpSystem == 'macos':
                os.system('bash')#("source ~/.profile")
            else:
                os.system('bash')#("source ~/.bashrc")        
        except:
            print ""
            
        
    def _get_system_parameters (self):
        """ Function doc """
        print '''
        Operational system:
            
            (1) Ubuntu / Debian / Mint   (apt-get)
            (2) Fedora                   (dnf)
            (3) Suse   / OpenSuse        (zypper)
            (4) Gentoo                   (emerge)
            (5) MacOS                    (port) 
            (6) CentOS                   (yum)
            (0) Other                    (Do it by yourself...)         
        
        '''
        sys = raw_input('\nPlease, choose the OS by the number(1):')
        if sys == '':
            sys = '1'
        
        
        if sys in ['1','2','3','4','5','6']:
            sys_dic = {
                       '1' : 'debian',  # apt-get ,
                       '2' : 'fedora',  # dnf     ,
                       '3' : 'suse'  ,  # zypper  ,
                       '4' : 'gentoo',  # emerge  ,
                       '5' : 'macos' ,  # port'   ,     
                       '6' : 'centos',  # yum
                       '0' : 'other' , 
                       }

            self.OpSystem  =sys_dic[sys]
            print self.OpSystem
        

        else:
            self.OpSystem = None
            print self.OpSystem
        
    
    def _check_dependencies (self):
        """ Function doc """
        
        """  - - - GTK - - - """
        print "\nChecking dependencies"
        try:
            import gtk
            print "gtk.........................OK"
            self.GTK        = True
            
            
            
        except:
            print "gtk.........................Fail"
            #print "Please install  gtk"
            self.GTK        = False
        
        
        """  - - - pyGTK - - - """
        #print "\nChecking pyGTK"                
        try:
            import pygtk
            print "pygtk.......................OK"
            self.pyGTK      = True
        except:
            print "pygtk.......................Fail"
            #print "Please install  pygtk"
            self.pyGTK      = False


        """  - - - PyMOL - - - """
        #print "\nChecking PyMOL"                
        try:                                         
            import pymol                             
            print "PyMOL.......................OK"
            self.PyMOL      = True  
        except:                                      
            print "PyMOL.......................Fail" 
            #print "Please install PyMOL"
            self.PyMOL      = False           
        
        
        """  - - - MatPlotLib - - - """
        #print "\nChecking matplotlib"                
        try:                                         
            from matplotlib import *                 
            from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas
            print "matplotlib..................OK"
            self.matplotlib = True   
        
        
        
        
        except:                                      
            print "matplotlib..................Fail" 
            #print "Please install matplotlib"
            self.matplotlib = False  




        """  - - - pDynamo - - - """
        print "\nChecking pDynamo"
        try:
            from pBabel           import *
            print "pBabel......................OK"
            self.pDynamo = True
        except:
            print "pBabel......................Fail"
            self.pDynamo = False
        
        
        try:
            from pCore            import * 
            print "pCore.......................OK"
            self.pDynamo = True
        except:
            print "pCore.......................Fail"
            self.pDynamo = False
        
        
        try:
            from pMolecule       import * 
            print "pMolecule...................OK"
            self.pDynamo = True
        except:
            print "pMolecule...................Fail"
            self.pDynamo = False
        
        
        try:
            from pMoleculeScripts import * 
            print "pMoleculeScripts............OK"
            self.pDynamo = True
        except:
            print "pMoleculeScripts............Fail"
            self.pDynamo = False


        """  - - - ORCA - - - """
        self.orca_folder  = os.environ.get('ORCA')
        if self.orca_folder is None:
            self.ORCA    = False
        else:
            self.ORCA    = True
        '''--------------------'''
        
        
        
        if self.log :
            self._print_parameters()


    def _print_parameters (self):
        """ Function doc """
        print 'GTK        =',self.GTK       
        print 'pyGTK      =',self.pyGTK     
        print 'python_dev =',self.python_dev
        print 'PyMOL      =',self.PyMOL     
        print 'matplotlib =',self.matplotlib
        print 'pDynamo    =',self.pDynamo   
        print 'ORCA       =',self.ORCA      
        print 'easyhybrid =',self.easyhybrid
    
    
    def install_ORCA ( self ):
              
               #-----------------------------------#
               #                                   #
               #              O R C A              #
               #                                   #
               #-----------------------------------#

        #------------------------------------------------------------------------------------------#
        print "\nInstalling ORCA\n"
        print '''ORCA is a general purpose ab initio and DFT quantum chemistry program 
        that can be used in conjunction with pDynamo either as a stand-alone QC model 
        or as part of a hybrid potential. An example of ORCA's use is provided in the 
        release in the file, tutorials/orca/ORCAExample.py (pDynamo folder).ORCA is a 
        separate program that is obtained and installed independently of pDynamo. 
        Full details are given on the ORCA web site: 

        https://orcaforum.cec.mpg.de

        Once installed, ORCA should be ready to use with pDynamo as long as the 
        directory where the ORCA executables have been put is defined as part of the 
        user's PATH variable. 
        '''                                                                
        self.answer = ["Y", "y", "Yes", "yes", "YES", "yEs", "yeS", ""]	                           
        s = raw_input('\nWould you like to put ORCA (for ab initio calculations) in your .bashrc file:(Y/n):')                            


        if s in self.answer:                                                                        
            home = raw_input('\nSpecify your ORCA home:')                            
            text  =  "\n#ORCA - ab initio calculations"
            text  =  "\nexport ORCA='"+home+"'"
            text  += "\nPATH=$ORCA:$PATH\n"

            
            arq  = open(os.path.join(self.HOME +"/.bashrc"), "a")                                   
            arq.writelines(text)                                                               
            arq.close()                                                                        
            print "The .bashrc file has been modified"                                         
            print "obs:if you are using CSH please do it manually"                             
                                                                                               
        else:                                                                                  
            print "\n\nPlease add to the .bashrc the following lines:"                         
            #print text                                                                         
            print "\n\nobs:if you are using CSH please do it manually"		                   
        #------------------------------------------------------------------------------------------#

    
    
    
    
    
    
    
    
    def install_EasyHybrid ( self):
        """ Function doc """

           #-----------------------------------#
           #                                   #
           #             EasyHybrid            #
           #                                   #
           #-----------------------------------#

        os.chdir(self.gtkdyn_folder)
        folder = self.gtkdyn_folder
        sh_EasyHybrid_root           = "EasyHybrid_ROOT="
        sh_extport_EasyHybrid_root   = " ; export EasyHybrid_ROOT"
        csh_EasyHybrid_root          = "setenv EasyHybrid_ROOT " 

        # creating the environment file
        
        try:
            # SH
            arq  = open(os.path.join("environment_bash.com"), "w")
            text = ""
            text = text + '''#!/bin/bash \n\n# . Bash environment variables and paths to be added to a user's ".bash_profile" file.\n# . Some modifications may be necessary to work properly (e.g. EasyHybrid_ROOT and PYTHONPATH).\n\n'''
            text = text + sh_EasyHybrid_root + folder + sh_extport_EasyHybrid_root
            arq.writelines(text)
            arq.close()
            print "\n\n"
            print "creating the file: environment_bash.com"
            
            #CSH
            arq  = open(os.path.join("environment_cshell.com"), "w")
            text = ""
            text = text + '''#!/bin/bash\n\n# . Cshell environment variables and paths to be added to a user's ".cshrc" file.\n# . Some modifications may be necessary to work properly (e.g. EasyHybrid_ROOT and PYTHONPATH).\n\n'''
            text = text + csh_EasyHybrid_root + folder 
            arq.writelines(text)
            arq.close()
            print "creating the file: environment_cshell.com"

        except:
            print "Fail, trying to build the environment file: permission denied"

        
        try:
            
            text = "\n#EasyHybrid \n"
            text = text + "source " + folder + "/environment_bash.com\n"
            text = text + "alias easyhybrid='" + folder +"/GTKPyMOL.py'\n"
            text = text + "export LC_ALL=en_US.UTF-8\n"		
            text = text + "export LANG=en_US.UTF-8\n"	
            text = text + "export LANGUAGE=en_US.UTF-8\n"	            
            
            if self.OpSystem == 'macos':
                s = raw_input('\nWould like to auto add information to the .profile? -EasyHybrid- (Y/n):')
            else:
                s = raw_input('\nWould like to auto add information to the .bashrc? -EasyHybrid- (Y/n):') 
            
            if s in self.answer:
                
                if self.OpSystem == 'macos':
                    arq  = open(os.path.join(self.HOME +"/.profile"), "a")
                else:
                    arq  = open(os.path.join(self.HOME +"/.bashrc"), "a")

                arq.writelines(text)
                arq.close()
                print "The .bashrc file has been modified"
                print "obs:if you are using CSH please do it manually"

            else:
                print "\n\nPlease add to the .bashrc the following lines:"
                print text
                print "\n\nobs:if you are using CSH please do it manually"
        except:
            print "Fail, trying to build the environment file: permission denied"

        try:
            os.system("chmod +x GTKPyMOL.py")
        except:
            pass

        print "\n - - - Installation successful - - - \n"
        print '          "Happy simulating :)"          \n\n'


install = InstallEasyHybrid()
install.install_all()


























