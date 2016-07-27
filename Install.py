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




#------------------------------------------------------------------------------
if not sys.platform.startswith('win'):
	HOME         = os.environ.get('HOME')
else:            
	HOME         = os.environ.get('PYMOL_PATH')
#------------------------------------------------------------------------------

   
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------


	






class InstallEasyHybrid:
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

    
    
    def install_easyhybrid (self):
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
       

    def _get_system_parameters (self):
        """ Function doc """
        print '''
        Operational system:
            
            (1) Ubuntu / Debian / Mint   (apt-get)
            (2) Fedora / CentOS          (yum)
            (3) Suse   / OpenSuse        (zypper)
            (4) Gentoo                   (emerge)
            (5) MacOS                    (port) 
            (6) Other                    (Do it by yourself...)         
        
        '''
        sys = raw_input('\nPlease, choose the OS by the number(1):')
        
        if sys == '':
            sys = '1'
        
        
        if sys in ['1','2','3','4','5','6']:
            sys_dic = {
                       '1' : 'debian',  #'apt-get',
                       '2' : 'fedora',  #'yum'    ,
                       '3' : 'suse'  ,  #'zypper' ,
                       '4' : 'gentoo',  #'emerge' ,
                       '5' : 'macos' ,  #'port'   ,     
                       '6' : 'other' , 
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
        try:
            self.orca_folder  = os.environ.get('ORCA')
            #print "\nORCA path found "
            self.ORCA    = True
        except:          
            self.ORCA    = False

        
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
                    os.system("sudo yum install gtk2")
                

                if self.OpSystem == 'gentoo':
                    os.system("sudo emerge -av gtk")
                    os.system("sudo emerge -av gtk2")


                if self.OpSystem == 'macos':
                    os.system("sudo port install gtk2")

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
                    os.system("sudo yum install pygtk")
                    os.system("sudo yum install pygtk2")


                if self.OpSystem == 'gentoo':
                    os.system("sudo emerge -av pygtk")


                if self.OpSystem == 'macos':
                    os.system("sudo port install py27-pygtk")
                
                if self.OpSystem == 'other':
                    print '\nPlease install pyGTK\n'
                
            except:
                print  'pyGTK instalation failed'


    def install_PyMOL ( self ):
        """
               #-----------------------------------#
               #                                   #
               #               PYMOL               #
               #                                   #
               #-----------------------------------#
        """
                                     
        s = raw_input('\nWould like install PyMOL (Y/n):') 
        
        if s in self.answer:                                                                          
            try:
                if OpSystem == 'debian':                                                               
                    os.system("sudo apt-get install pymol")  
                
                if OpSystem == 'suse':                                                                 
                    os.system("sudo zypper install pymol")  
                                  
                
                if self.OpSystem == 'fedora':
                    os.system("sudo yum install pymol")


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
        #-----------------------------------------------------------------------





    
    def  _install_python_dev (self):
        """ Function doc """
        try:
            if self.OpSystem == 'debian':                                                    
                os.system("sudo apt-get install python-dev")                       


            if self.OpSystem == 'suse':                                                      
                os.system("sudo zypper install python-devel") 


            if self.OpSystem == 'fedora':
                os.system("sudo yum install python-devel")
            

            if self.OpSystem == 'gentoo':
                os.system("sudo emerge -av python-devel")


            if self.OpSystem == 'macos':
                os.system("sudo port install python-devel") # rever esta parte
                os.system("sudo port install python-dev")   # rever esta parte
        except:
            print  'python-dev instalation failed'

        
    def _install_Cython (self, folder = None, verison = None, Cython = None):
        #Cython-0.19 
        #-------------------------------------------------------------------------------------#
        #folder = os.getcwd()                                                                 #
        print "\n\n\nInstalling Cython (superuser permission required)..."                    #
        path   = os.path.join(folder, verison + "/thirdParty/" + Cython)                      #
        os.chdir(path)                                                                        #
        #os.system("ls ")                                                                     #
        os.system("sudo python setup.py install")                                             #
        print "Cython installation done."                                                     #
        #-------------------------------------------------------------------------------------#        
    
    def _install_PyYAML (self, folder= None, verison= None, PyYAML= None):
        """ Function doc """
        #PyYAML-3.10
        #-------------------------------------------------------------------------------------#
        os.system("ls ")                                                                      #
        print "\n\n\nInstalling PyYAML..."                                                    #
        path   = os.path.join(folder, verison + "/thirdParty/" + PyYAML)                      #
        os.chdir(path)                                                                        #
        #os.system("ls ")                                                                     #
        os.system("sudo python setup.py install")	                                          #
        print "PyYAML installation done."                                                     #
        #-------------------------------------------------------------------------------------#
    
    def install_pDynamo ( self ):
        s = raw_input('\nWould like to auto install pDynamo? (Y/n):')
        
        if s in self.answer:
        
            try:
                
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


                s = raw_input('\nWhere would you like to install pDynamo? (' + HOME +'):')
                if s == '':
                    s = self.HOME					
                folder = s
                os.chdir(s)

                # WGET - DOWNLOAD
                #-------------------------------------------------------------------------------------#
                os.system("wget https://sites.google.com/site/pdynamomodeling/" + verison + ".tgz")   #
                #-------------------------------------------------------------------------------------#

                # TARGZ
                #-------------------------------------------------------------------------------------#
                os.system("tar -xzvf "+ verison + ".tgz")                                             #
                #-------------------------------------------------------------------------------------#

                '''                 #Cython-0.19                 '''
                s = raw_input('\nWould like install Cython? (Y/n):')
                if s in self.answer:   			
                    self._install_Cython (self, folder = folder, verison = verison, Cython = Cython)
                    
                    
                    
                '''                #PyYAML-3.10                '''
                s = raw_input('\nWould like install PyYAML?(Y/n):')
                if s in self.answer:  
                    self._install_PyYAML (self, folder = folder, verison = verison, PyYAML = PyYAML)
                    


                # PDYNAMO
                #--------------------------------------------------------------------------------------------#
                path   = os.path.join(folder, verison + "/installation")                                     #
                os.chdir(path)                                                                               #
                os.system("ls ")                                                                             #
                pDy_installation_path = path                                                                 #
                #--------------------------------------------------------------------------------------------#

                
                
                #--------------------------------------------------
                #                    PYTHON DEV
                #--------------------------------------------------
                self._install_python_dev()
                #--------------------------------------------------
                
                

                print "Installing pDynamo"                                                                  
                os.system("python Install.py")	                                                            
                #bashrc  -  pDynamo                                                                         
                self.answer = ["Y", "y", "Yes", "yes", "YES", "yEs", "yeS", ""]	                            
                s = raw_input('\nWould like to auto add information to the .bashrc file? -pDynamo- (Y/n):') 
                                                                                                            
                text = "\n#pDynamo \n"                                                                      
                text = text + "source " + pDy_installation_path + "/environment_bash.com\n"                 
                                                                                                            
                if s in self.answer:                                                                        
                    arq  = open(os.path.join(HOME +"/.bashrc"), "a")                                        
                    arq.writelines(text)                                                                    
                    arq.close()                                                                             
                    print "The .bashrc file has been modified"                                              
                    print "obs:if you are using CSH please do it manually"                                  
                                                                                                            
                else:                                                                                       
                    print "\n\nPlease add to the .bashrc the following lines:"                              
                    print text                                                                              
                    print "\n\nobs:if you are using CSH please do it manually"		                        
                                                                                                            
                #-------------------------------------------------------------------------------------------

            except:
                print "\n - - -pDynamo installation failed - - - "
                print "\nPlease check: \nhttps://sites.google.com/site/pdynamomodeling/installation\n"
        else:
            print "\nPlease check: \nhttps://sites.google.com/site/pdynamomodeling/installation\n"
        














































    def install_matplotlib ( self, system = 'debian'):
        """ Function doc """
        
               #-----------------------------------#
               #                                   #
               #             matplotlib            #
               #                                   #
               #-----------------------------------#

        #Checking matplotlib
        #-----------------------------------------------------------------------------------------
        print "\nChecking matplotlib"                                                             
        try:                                                                                      
            from matplotlib import *                                                              
            print "matplotlib..................OK"                                                
        
        except:                                                                                   
            print "matplotlib..................Fail"                                              
            print "Please install matplotlib"                                                     
                                                                                                
            s = raw_input('\nWould like install matplotlib (Y/n):')                               
            if s in self.answer:                                                                  
                try:
                    if OpSystem == 'suse':                                                      
                        os.system("sudo zypper install python-numpy-devel")
                        os.system("sudo zypper install python-matplotlib")
                        os.system("sudo zypper install python-matplotlib-gtk2")
                
                    elif OpSystem == 'debian':                                                    
                        os.system("sudo apt-get install python-matplotlib")                       
                    
                    else:
                        print 'ops - lascou!'
                    
                except:
                    print  'matplotlib instalation failed'
        #-----------------------------------------------------------------------------------------

    def install_ORCA ( self, system = None):
              
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

            
            arq  = open(os.path.join(HOME +"/.bashrc"), "a")                                   
            arq.writelines(text)                                                               
            arq.close()                                                                        
            print "The .bashrc file has been modified"                                         
            print "obs:if you are using CSH please do it manually"                             
                                                                                               
        else:                                                                                  
            print "\n\nPlease add to the .bashrc the following lines:"                         
            #print text                                                                         
            print "\n\nobs:if you are using CSH please do it manually"		                   
        #------------------------------------------------------------------------------------------#

    def install_EasyHybrid ( self, gtkdyn_folder = None, ):
        """ Function doc """

               #-----------------------------------#
               #                                   #
               #             EasyHybrid            #
               #                                   #
               #-----------------------------------#


        if system == True:
            os.chdir(gtkdyn_folder)
            folder = gtkdyn_folder
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


            # Editing bashrc file and chsrc
            if not sys.platform.startswith('win'):
                HOME         = os.environ.get('HOME')
            else:            
                HOME         = os.environ.get('PYMOL_PATH')

            try:
                #bashrc
                self.answer = ["Y", "y", "Yes", "yes", "YES", "yEs", "yeS", ""]	
                s = raw_input('\nWould like to auto add information to the .bashrc file? -easyhybrid- (Y/n):')
                
                    
                text = "\n#EasyHybrid \n"
                text = text + "source " + folder + "/environment_bash.com\n"
                text = text + "alias easyhybrid='" + folder +"/GTKPyMOL.py'\n"
                text = text + "export LC_ALL=en_US.UTF-8\n"		
                text = text + "export LANG=en_US.UTF-8\n"	
                text = text + "export LANGUAGE=en_US.UTF-8\n"	
                
                
                
                
                if s in self.answer:
                    arq  = open(os.path.join(HOME +"/.bashrc"), "a")
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

        else:
            print "\n - - - Installation failed - - - \n"
            









install = InstallEasyHybrid(log = True)
install.install_easyhybrid()





























