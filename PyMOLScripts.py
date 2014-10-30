#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  PyMOLScripts.py
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
##


atomic_dic = { 
			'Ac':227.028,
			'Al':26.9815,
			'Am':243    , 	
			'Sb':121.757,
			'Ar':39.948 , 
			'As':74.9215,
			'At':210    , 	
			'Ba':137.327,
			'Bk':247    , 	
			'Be':9.01218,
			'Bi':208.980,
			'Bh':262    , 	
			'B' :10.811 , 
			'Br':79.904 ,
			'Cd':112.411,
			'Ca':40.078 ,
			'Cf':251    , 	
			'C' :12.011 , 
			'Ce':140.115,
			'Cs':132.905,
			'Cl':35.4527,
			'Cr':51.9961,
			'Co':58.9332,
			'Cu':63.546 ,
			'Cm':247 	,
			'Db':262 	,
			'Dy':162.50 ,
			'Es':252 	,
			'Er':167.26 ,
			'Eu':151.965,
			'Fm':257 	,
			'F'	:18.9984,
			'Fr':223 	,
			'Gd':157.25 ,
			'Ga':69.723 ,
			'Ge':72.61  ,
			'Au':196.966,
			'Hf':178.49 ,
			'Hs':265 	,
			'He':4.00260,
			'Ho':164.930,
			'H' :1.00794,
			'In':114.82 ,
			'I' :126.904,
			'Ir':192.22 ,
			'Fe':55.847 ,
			'Kr':83.80  ,
			'La':138.905,
			'Lr':262 	,	
			'Pb':207.2  ,
			'Li':6.941  ,
			'Lu':174.967,
			'Mg':24.3050,
			'Mn':54.9380,
			'Mt':266 	,
			'Md':258 	,
			'Hg':200.59 ,
			'Mo':95.94  ,
			'Nd':144.24 ,
			'Ne':20.1797,
			'Np':237.048,
			'Ni':58.6934,
			'Nb':92.9063,
			'N' :14.0067,
			'No':259 	,
			'Os':190.2  ,
			'O' :15.9994,
			'Pd':106.42 ,
			'P' :30.9737,
			'Pu':244 	,
			'Po':209 	,
			'K' :39.0983,
			'Pr':140.907,
			'Pm':145 	,
			'Pa':231.035,
			'Ra':226.025,
			'Rn':222 	,
			'Re':186.207,
			'Rh':102.905,
			'Rb':85.4678,
			'Ru':101.07 ,
			'Rf':261 	,
			'Sm':150.36 ,
			'Sc':44.9559,
			'Sg':263 	,
			'Se':78.96  ,
			'Si':28.0855,
			'Ag':107.868,
			'Na':22.9897,
			'Sr':87.62  ,
			'S' :32.066 ,
			'Ta':180.947,
			'Tc':217,
			'Te':127.60, 
			'Tb':158.925,
			'Tl':204.383,
			'Th':232.038,
			'Tm':168.934,
			'Sn':118.710,
			'Ti':47.88  ,
			'W' :183.85 ,
			'U' :238.028,
			'V' :50.9415,
			'Xe':131.29 ,
			'Yb':173.04 ,
			'Y' :88.9058,
			'Zn':65.39  ,
			'Zr':91.224 ,
			
			"H" : 1.0 ,
			"C" : 12.0,
			"O" : 16.0,
			"N" : 14.0,			
			"F" : 19.0,
			"P" : 31.0,		
			"S" : 32.1,
			"Cl": 35.0,
			"CL": 35.0,
			"cl": 35.0,
			"Br": 79.9,
			"BR": 79.9,	
			"I" : 126.0}




from pymol import *
SCRATCH = os.environ.get('PDYNAMO_SCRATCH')


'''
	             #==================================================#
	             #             NEW GTKDYNAMO FUCTIONS               #
	             #==================================================#


'''


def GetFileType(filename):
    file_type = filename.split('.')
    return file_type[-1]


def GTKDynamoTemporaryFolderRefresh():
    """ Function doc """
    import os

    PDYNAMO_SCRATCH = os.environ.get('PDYNAMO_SCRATCH')
    GTKDYNAMO_TMP = os.path.join(PDYNAMO_SCRATCH, '.GTKDynamo')

    if not os.path.isdir(GTKDYNAMO_TMP):
        os.mkdir(GTKDYNAMO_TMP)
        print "Temporary files directory:  %s" % GTKDYNAMO_TMP
    return GTKDYNAMO_TMP


def AddFileTypeSuffix(filename, type_):
    file_type = GetFileType(filename)
    if file_type == type_:
        return filename
    else:
        return filename + '.' + type_


# PyMOL   ---table---> GTKDynamo
def PymolGetTable(selection):
    '''	
    # antiga - pymol_get_table
    # extrai um selecao do pymol na forma de tabela
    '''
    model = cmd.get_model(selection)
    table = []
    n = 1
    for atom in model.atom:
        ids = atom.index
        py_id = int(ids) - 1
        table.append(py_id)
        ids = str(ids)
        n = n + 1
    print table
    return table


# Table   --->   PyMOL
def PymolPutTable(table, selection):
    '''
    # old - pymol_put_table        
    # add a selection in PyMOL from a given table [pDynamoProject mainly] 
    # obs: In  pDynamo the index starts in number 0        
    '''

    # selection that will be generated in the pymol
    selection_string = selection + ", index "
    n = 0												        #
    n_limit = 0									    	        #
    limit = len(table)

    for i in table:                                             #
        selection_string = selection_string + "+" + str(i + 1)
        n = n + 1												#
        n_limit = n_limit + 1									#
        if n == 100:											#
            # generates the pymol selection
            cmd.select(selection, selection_string)
            n = 0 												#
            selection_string = selection + ", index "			#
            #
        if n_limit == limit:									#
            cmd.select(selection, selection_string)
            n = 0
            selection_string = selection + ", index "


# pDynamo ---table---> PyMOL
def ExportTablesToSelection(project=None, pymol_id=None):
    """ Function doc """
    if project.settings['qc_table'] != []:
        PymolPutTable(project.settings['qc_table'], "QC_atoms")
        
        string2 = 'select QC_atoms, (' + pymol_id + ' and  QC_atoms )'
        cmd.do(string2)
        cmd.show("stick", "QC_atoms")
        cmd.show("sphere", "QC_atoms")

    if project.settings['fix_table'] != []:
        PymolPutTable(project.settings['fix_table'], "FIX_atoms")
        string22 = 'select FIX_atoms, (' + pymol_id + ' and  FIX_atoms )'
        cmd.do(string22)
        string5 = 'color grey80, FIX_atoms'
        cmd.do(string5)


def ExportFramesToPymol(project=None, prefix='teste'):
    """
                 the old: export_frames_to_pymol 
    exports a frame from the pDynamo project and load in PyMOL
    obs:An XYZ file is also exportes when an PDB files is exported

    """
    print project.types_allowed
    if project == None:
        print 'only testing ExportFramesToPymol'

    else:
        data_path = project.data_path
        types_allowed = project.types_allowed

        tmp_path = data_path + '/tmp'
        print tmp_path
        if not os.path.exists(tmp_path):
            os.mkdir(tmp_path)

        # creating a xyz file - coordienate reference
        if types_allowed['xyz'] == True:
            type_ = 'xyz'
            #pymol_id = prefix + '_' + type_ + '_step' + str(project.step)
            pymol_id ='Step_' + str(project.step)
            tmp_file = os.path.join(
                tmp_path, AddFileTypeSuffix(pymol_id, type_))
            project.ExportStateToFile(tmp_file, type_)

            try:
                cmd.delete(pymol_id)
            except:
                a = None
            cmd.load(tmp_file)

            """
					Tables To Selection 
			"""
            #ExportTablesToSelection(project, pymol_id)

        if types_allowed['pdb'] == True:
            type_ = 'pdb'
            #pymol_id = prefix + '_' + type_ + '_step' + \
            #    str(project.step)  # - Object Name
            pymol_id ='Step_' + str(project.step)

            # - Object Name +  type
            tmp_file = os.path.join(
                tmp_path, AddFileTypeSuffix(pymol_id, type_))
            project.ExportStateToFile(tmp_file, type_)  # -

            try:
                cmd.delete(pymol_id)
            except:
                a = None

            cmd.load(tmp_file)

            """
					Tables To Selection 
			"""
            #ExportTablesToSelection(project, pymol_id)

            tmp_file = os.path.join(tmp_path, "tmp.xyz")
            project.ExportStateToFile(tmp_file, "xyz")

            #            starts here
            filein = open(tmp_file, 'r')
            n = 0
            new_coord = []
            for line in filein:
                line2 = line.split()
                if n > 1:
                    x = float(line2[1])
                    y = float(line2[2])
                    z = float(line2[3])
                    new_coord.append([x, y, z])
                n = n + 1

            # print "\n xyz  coordienates"
            # for i in new_coord :
            #	print i

            model3 = cmd.get_model(pymol_id)
            # print "\n pdb  coordienates"

            n = 0
            for a in model3.atom:
                # print a.coord[0], a.coord[1], a.coord[2]
                a.coord[0] = new_coord[n][0]
                a.coord[1] = new_coord[n][1]
                a.coord[2] = new_coord[n][2]
                n = n + 1

            cmd.load_model(model3, "_tmp")
            cmd.update(pymol_id, "_tmp")
            cmd.delete("_tmp")

        project.settings['last_pymol_id'] = pymol_id
        cmd.disable("all")
        cmd.enable(pymol_id)
        return pymol_id


def LoadGTKDynamoProjectSettings(filein):
    '''opens a gtkdyn file'''
    last_step = 0
    working_folder = None
    system = None
    pymol_session = None
    last_pymol_id = None

    fullpath = filein.split("/")
    name = fullpath[-1]
    fullpath.pop(-1)
    fullPATH = ""
    for i in fullpath:
        fullPATH = fullPATH + i
        fullPATH = fullPATH + "/"

    arq = open(filein, 'r')
    for line in arq:
        line2 = line.split()
        try:
            if line2[0] == "last_step":
                last_step = line2[2]
                # print last_step
            working_folder = fullPATH
            # print working_folder
            if line2[0] == "system":
                line2Split = line2[2].split("'")
                system = line2Split[1]
                system = fullPATH + system
                # print system
            if line2[0] == "pymol_session":
                line2Split = line2[2].split("'")
                pymol_session = line2Split[1]
                pymol_session = fullPATH + pymol_session
            if line2[0] == "last_pymol_id":
                line2Split = line2[2].split("'")
                last_pymol_id = line2Split[1]
        except:
            pass

    _ProjectSettings = {'last_step': last_step,
                        'working_folder': working_folder,
                        'system': system,
                        'pymol_session': pymol_session,
                        'last_pymol_id': last_pymol_id}
    print last_step
    print working_folder
    print system
    print pymol_session
    print last_pymol_id
    # return 	last_step ,	working_folder,	system,	pymol_session, last_pymol_id
    return _ProjectSettings


def PyMOLRepresentations (representation, selection):
    """ Function doc """
    print "aqui"
    if representation['lines'  ]:
        cmd.show("lines",  selection)

    if representation['stick'  ]:
        cmd.show("stick",  selection)

    if representation['ribbon' ]:
        cmd.show("ribbon",  selection)

    if representation['cartoon']:
        cmd.show("cartoon",  selection)

    if representation['dot'    ]:
        cmd.show("dot",  selection)

    if representation['sphere' ]:
        cmd.show("sphere",  selection)

    if representation['mesh'   ]:
        cmd.show("mesh",  selection)

    if representation['surface']:                           
        cmd.show("surface",  selection)
    
    try:
        cmd.color(representation['color'],  selection)
    except:
        pass


def PyMOL_export_PDB_to_file(obj, data_path, file_out, state = -1):   # Export an PDB file from a PyMOL object
	tmp         = data_path+"/tmp"                          
	if not os.path.exists ( tmp ): os.mkdir ( tmp )         
	file_path   = os.path.join (tmp, file_out)
	
	
	FILE        = file_path 
	#  cmd.save("/home/fernando/Desktop/gordo.pdb", "obj01", -1, "pdb")
	cmd.save(FILE, obj, state, "pdb")
	return FILE
	
	
def PyMOL_export_XYZ_to_file(obj, label, data_path, file_out, state): # Export an XYZ file from a PyMOL object
	'''	
	# antiga      -  pymol_export_XYZ_file
	# obj,       -  pymol object
	# label,     -  second line in the XYZ file "header"
	# data_path, -  working folder
	# file_out   -  file out name
	'''	
	tmp         = data_path+"/tmp"                          
	if not os.path.exists ( tmp ): os.mkdir ( tmp )         

	text        = []                                        # buffer -  list of strings  									
	file_path   = os.path.join (tmp, file_out)              # fullpath 
	arq         = open(file_path, 'w')	
	s           = " "

	pymol_obj   = cmd.get_model(obj, state)                 # importing pymol selection
	model_split = pymol_obj.atom	

	for i in model_split:
		line = [] 		
		idx = i.name			                                          
		X = i.coord[0]			                                          
		Y = i.coord[1]			                                          
		Z = i.coord[2]			                                          
		line = idx +"     " + str(X)+ "     "+ str(Y)+ "     " + str(Z)   
		text.append(line + "\n")										  
	
	header = len(text)							
	arq.writelines(str(header) + "\n")			
	#print header								#
	header2 = label             				
	arq.writelines(header2+ "\n")
	#print header2
	#for i in text:								
	#	print i									#	
	arq.writelines(text)	
	arq.close()				
	
	return file_path


#----------------SCAN FUNCTIONS---------------#
#
#---------------------------------------------#
def compute_sigma_a1_a3 (pk1_name, pk3_name):

	""" example:
		pk1 ---> pk2 ---> pk3
		 N  ---   H  ---  O	    
		 
		 where H is the moving atom
		 calculation only includes N and O ! 
	"""
	
	mass1 = atomic_dic[pk1_name]
	mass3 = atomic_dic[pk3_name]
	
	sigma_pk1_pk3 =  mass1/(mass1+mass3)
	#print "sigma_pk1_pk3: ",sigma_pk1_pk3
	
	sigma_pk3_pk1 =  mass3/(mass1+mass3)
	sigma_pk3_pk1 = sigma_pk3_pk1 *-1
	
	#print "sigma_pk3_pk1: ", sigma_pk3_pk1
	
	return sigma_pk1_pk3, sigma_pk3_pk1

def distance_a1_a2(Xa,Ya,Za,Xb,Yb,Zb):
	dist = ((float(Xa) -float(Xb))**2  + (float(Ya) -float(Yb))**2  + (float(Za) -float(Zb))**2)**0.5
	return dist

def import_ATOM1_ATOM2(pka,pkb):   # get PyMOL pk1 and pk2 
	""" Function doc """
	atom1 = cmd.get_model(pka)
	for a in atom1.atom:
		idx1        = a.index
		atom1_index = int(idx1) -1
		#name1       = a.name
		name1       = a.symbol
		atom1       = idx1	
		X1 = a.coord[0]
		Y1 = a.coord[1]
		Z1 = a.coord[2]	
		#print "Atom1: ", name1,",  index: ",idx1, ", Coordinates: ",X1,Y1,Z1	

	atom2 = cmd.get_model(pkb)
	for a in atom2.atom:
		idx2        = a.index
		atom2_index = int(idx2) -1
		#name2       = a.name
		name2       = a.symbol
		atom2       = idx2
		X2 = a.coord[0]
		Y2 = a.coord[1]
		Z2 = a.coord[2]
		#print "Atom2: ", name2,",  index: ",idx2, ", Coordinates: ",X2,Y2,Z2
	
	distance  = distance_a1_a2(X1,Y1,Z1,X2,Y2,Z2)
	#print "Distance  atom1 ---> atom2  = ", distance 
	return name1 , atom1_index, name2,  atom2_index, distance






def main():
    ExportFramesToPymol()
    return 0

if __name__ == '__main__':
    main()
