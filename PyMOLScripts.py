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
            pymol_id = prefix + '_' + type_ + '_step' + str(project.step)
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
            pymol_id = prefix + '_' + type_ + '_step' + \
                str(project.step)  # - Object Name
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




def main():
    ExportFramesToPymol()
    return 0

if __name__ == '__main__':
    main()
