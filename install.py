#!/usr/bin/env python
text1 = """
#	
#
#	
#	
#
#	
#
#                            ---- GTKDynamo ----
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
#       GTKDynamo team:
#       - Jose Fernando R Bachega  < Univesity of Sao Paulo - SP, Brazil                              >
#       - Troy Wymore              < Pittsburgh Super Computer Center, Pittsburgh PA - USA            >
#       - Martin Field             < Institut de Biologie Structurale, Grenoble, France               >		
#       - Luis Fernando S M Timmers< Pontifical Catholic University of Rio Grande do Sul - RS, Brazil >
#
#       Special thanks to:
#       - Lucas Assirati           < Univesity of Sao Paulo - SP, Brazil                              >
#       - Leonardo R Bachega       < University of Purdue - West Lafayette, IN - USA                  >
#       - Richard Garratt          < Univesity of Sao Paulo - SP, Brazil                              >
#
#
#
#				        ---	GTKDynamo Installation	---
#		
"""  



import threading
import gobject
import sys
import glob, math, os


#apenas um teste

#System
import datetime
import time
print text1


if not sys.platform.startswith('win'):
	HOME         = os.environ.get('HOME')
else:            
	HOME         = os.environ.get('PYMOL_PATH')


system = True			
answer = ["Y", "y", "Yes", "yes", "YES", "yEs", "yeS", ""]	


#check_list =    { 
#			   "pymol" : True,
#		  "matplotlib" : True,
#			   "pygtk" : True,
#				 "gtk" : True,
#		  "python-dev" : True,
#		     "pDynamo" : True	
#			    {	

folder         = os.getcwd()
gtkdyn_folder  = folder			


'''
# Debian/Ubuntu/Mint
sudo apt-get install pymol
 
# Fedora
yum install pymol
 
# Gentoo
emerge -av pymol
 
# openSUSE (12.1 and later)
sudo zypper install pymol
 
# CentOS with EPEL
rpm -i http://download.fedoraproject.org/pub/epel/6/i386/epel-release-6-5.noarch.rpm
yum --enablerepo=epel install pymol
'''


print "\nChecking GTK and pyGTK"
try:
	import pygtk
	print "pygtk.......................OK"
except:
	print "pygtk.......................Fail"
	print "Please install  pygtk"
	system = False


try:
	import gtk
	print "gtk.........................OK"
except:
	print "gtk.........................Fail"
	print "Please install  gtk"
	system = False




       #-----------------------------------#
       #                                   #
       #               GTKGL               #
       #                                   #
       #-----------------------------------#

#Checking GTKGL
#----------------------------------------------------------------------------------------#
print "\nChecking GTKGL"                                                                 #
try:                                                                                     #
    import gtk.gtkgl
    print "GTKGL.......................OK"                                               #
except:                                                                                  #
	print "GTKGL.......................Fail"                                             #
	print "Please install GTKGL"                                                         #
	                                                                                     #
	s = raw_input('\nWould like install GTKGL - Ubuntu/Debian/Mint users only - (Y/n):') #
	if s in answer:                                                                      #
		try:                                                                             #
			os.system("sudo apt-get install python-gtkglext1")                           #
		except:                                                                          #
			pass 	                                                                     #
	else:                                                                                #
		system = False                                                                   #
#----------------------------------------------------------------------------------------#





       #-----------------------------------#
       #                                   #
       #              PyOpenGL             #
       #                                   #
       #-----------------------------------#
       
#Checking PyOpenGL
#------------------------------------------------------------------------------------------#
print "\nChecking PyOpenGL"                                                                #
try:                                                                                       #
    from OpenGL.GL import *                                                                #
    from OpenGL.GLU import *                                                               #
    print "PyOpenGL....................OK"                                                 #
except:                                                                                    #
	print "PyOpenGL....................Fail"                                               #
	print "Please install PyOpenGL"                                                        #
	                                                                                       #
	s = raw_input('\nWould like install PyOpenGL - Ubuntu/Debian/Mint users only - (Y/n):')#
	if s in answer:                                                                        #
		try:                                                                               #
			os.system("sudo apt-get install python-opengl")                                #
		except:                                                                            #
			pass 	                                                                       #
	else:                                                                                  #
		system = False                                                                     #
#------------------------------------------------------------------------------------------#



       #-----------------------------------#
       #                                   #
       #               PYMOL               #
       #                                   #
       #-----------------------------------#

#Checking PyMOL
#----------------------------------------------------------------------------------------#
print "\nChecking PyMOL"                                                                 #
try:                                                                                     #
	import pymol                                                                         #
	print "PyMOL.......................OK"                                               #
except:                                                                                  #
	print "PyMOL.......................Fail"                                             #
	print "Please install PyMOL"                                                         #
	                                                                                     #
	s = raw_input('\nWould like install PyMOL - Ubuntu/Debian/Mint users only - (Y/n):') #
	if s in answer:                                                                      #
		try:                                                                             #
			os.system("sudo apt-get install pymol")                                      #
		except:                                                                          #
			pass 	                                                                     #
	else:                                                                                #
		system = False                                                                   #
#----------------------------------------------------------------------------------------#



       #-----------------------------------#
       #                                   #
       #             matplotlib            #
       #                                   #
       #-----------------------------------#

#Checking matplotlib
#----------------------------------------------------------------------------------------------#
print "\nChecking matplotlib"                                                                  #
try:                                                                                           #
	from matplotlib import *                                                                   #
	print "matplotlib..................OK"                                                     #
except:                                                                                        #
	print "matplotlib..................Fail"                                                   #
	print "Please install matplotlib"                                                          #
	                                                                                           #
	s = raw_input('\nWould like install matplotlib - Ubuntu/Debian/Mint users only - (Y/n):')  #
	if s in answer:                                                                            #
		try:                                                                                   #
			os.system("sudo apt-get install python-matplotlib")                                #
		except:                                                                                #
			pass 	                                                                           #
	else:                                                                                      #
		system = False                                                                         #
#----------------------------------------------------------------------------------------------#







       #-----------------------------------#
       #                                   #
       #              pDynamo              #
       #                                   #
       #-----------------------------------#

print "\nChecking pDynamo"
_pDynamo = True
try:
	from pBabel           import *
	print "pBabel......................OK"

except:
	print "pBabel......................Fail"
	system = False
	_pDynamo = False
try:
	from pCore            import * 
	print "pCore.......................OK"
except:
	print "pCore.......................Fail"
	system = False
	_pDynamo = False
try:
	from pMolecule       import * 
	print "pMolecule...................OK"
except:
	print "pMolecule...................Fail"
	system = False
	_pDynamo = False
try:
	from pMoleculeScripts import * 
	print "pMoleculeScripts............OK"
except:
	print "pMoleculeScripts............Fail"
	system = False
	_pDynamo = False

if _pDynamo == False:
    print "\npDynamo is not installed.\n"
    #bashrc

    s = raw_input('\nWould like to auto install pDynamo? - Ubuntu/Debian/Mint users only - (Y/n):')
    if s in answer:
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
                    PyYAML  = "PyYAML-3.10"
                version = s2
                

            verison = "pDynamo-" + version


            s = raw_input('\nWhere would you like to install pDynamo? (' + HOME +'):')
            if s == '':
                s = HOME					
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


            s = raw_input('\nWould like install Cython - Ubuntu/Debian/Mint users only - (Y/n):')
            if s in answer:   			
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


            s = raw_input('\nWould like install PyYAML - Ubuntu/Debian/Mint users only - (Y/n):')
            if s in answer:  
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
                


            # PDYNAMO
            #--------------------------------------------------------------------------------------------#
            path   = os.path.join(folder, verison + "/installation")                                     #
            os.chdir(path)                                                                               #
            os.system("ls ")                                                                             #
                                                                                                         #
            pDy_installation_path = path                                                                 #
                                                                                                         #
            try:                                                                                         #
                os.system("sudo apt-get install python-dev")                                             #
            except:                                                                                      #
                pass                                                                                     #
                                                                                                         #
            print "Installing pDynamo"                                                                   #
            os.system("python Install.py")	                                                             #
                                                                                                         #
            #bashrc  -  pDynamo                                                                          #
            answer = ["Y", "y", "Yes", "yes", "YES", "yEs", "yeS", ""]	                                 #
            s = raw_input('\nWould like to auto add information to the .bashrc file? -pDynamo- (Y/n):')  #
                                                                                                         #
                                                                                                         #
            text = "\n#pDynamo \n"                                                                       #
            text = text + "source " + pDy_installation_path + "/environment_bash.com\n"                  #
                                                                                                         #
            if s in answer:                                                                              #
                arq  = open(os.path.join(HOME +"/.bashrc"), "a")                                         #
                arq.writelines(text)                                                                     #
                arq.close()                                                                              #
                print "The .bashrc file has been modified"                                               #
                print "obs:if you are using CSH please do it manually"                                   #
            #				os.system("source " + pDy_installation_path + "/environment_bash.com")                   #
                                                                                                         #
            else:                                                                                        #
                print "\n\nPlease add to the .bashrc the following lines:"                               #
                print text                                                                               #
                print "\n\nobs:if you are using CSH please do it manually"		                         #
                                                                                                         #
            #--------------------------------------------------------------------------------------------# 

            _pDynamo = True
            system = True


            if version == "1.7.2":
                try:
                    print "replacing GaussianCubeFileWriter.py"
                    shutil.copy2("GaussianCubeFileWriter.py ", pDy_installation_path +"/pBabel-1.7.2/pBabel")
                    #print "\n\nPlease move GaussianCubeFileWriter.py  to" +pDy_installation_path+ "/pBabel-1.7.2/pBabel manualy""
                except:
                    print "Fail, trying to move GaussianCubeFileWriter.py  to" +pDy_installation_path+ "/pBabel-1.7.2/pBabel"

                    
					
					
					
        except:
            print "\n - - -pDynamo installation failed - - - "
            print "\nPlease check: \nhttps://sites.google.com/site/pdynamomodeling/installation\n"
	else:
		print "\nPlease check: \nhttps://sites.google.com/site/pdynamomodeling/installation\n"
	









       #-----------------------------------#
       #                                   #
       #             GTKDYNAMO             #
       #                                   #
       #-----------------------------------#


if system == True:
	os.chdir(gtkdyn_folder)
	folder = gtkdyn_folder
	sh_gtkdynamo_root           = "GTKDYNAMO_ROOT="
	sh_extport_gtkdynamo_root   = " ; export GTKDYNAMO_ROOT"
	csh_gtkdynamo_root          = "setenv GTKDYNAMO_ROOT " 

	# creating the environment file
	
	
	
	try:
		# SH
		arq  = open(os.path.join("environment_bash.com"), "w")
		text = ""
		text = text + '''#!/bin/bash \n\n# . Bash environment variables and paths to be added to a user's ".bash_profile" file.\n# . Some modifications may be necessary to work properly (e.g. GTKDYNAMO_ROOT and PYTHONPATH).\n\n'''
		text = text + sh_gtkdynamo_root + folder + sh_extport_gtkdynamo_root
		arq.writelines(text)
		arq.close()
		print "\n\n"
		print "creating the file: environment_bash.com"
		
		#CSH
		arq  = open(os.path.join("environment_cshell.com"), "w")
		text = ""
		text = text + '''#!/bin/bash\n\n# . Cshell environment variables and paths to be added to a user's ".cshrc" file.\n# . Some modifications may be necessary to work properly (e.g. GTKDYNAMO_ROOT and PYTHONPATH).\n\n'''
		text = text + csh_gtkdynamo_root + folder 
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
		answer = ["Y", "y", "Yes", "yes", "YES", "yEs", "yeS", ""]	
		s = raw_input('\nWould like to auto add information to the .bashrc file? -GTKDynamo- (Y/n):')
		
			
		text = "\n#GTKDynamo \n"
		text = text + "source " + folder + "/environment_bash.com\n"
		text = text + "alias gtkdynamo='" + folder +"/GTKPyMOL.py'\n"
		text = text + "export LC_ALL=en_US.UTF-8\n"		
		text = text + "export LANG=en_US.UTF-8\n"	
		text = text + "export LANGUAGE=en_US.UTF-8\n"	
		
		
		
		
		if s in answer:
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
	
	

try:
	os.system("bash")
except:
	pass		

	
	
	
	
	
	
	
	
	
	
	
	
