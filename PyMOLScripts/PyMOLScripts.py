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


atomic_dic = {#Symbol     name         number    Cov(r)     VdW(r)     Mass
                "H"  : ["Hydrogen"     , 1   ,  0.330000 , 1.200000,  1.007940   ],
                "He" : ["Helium"       , 2   ,  0.700000 , 1.400000,  4.002602   ],
                "Li" : ["Lithium"      , 3   ,  1.230000 , 1.820000,  6.941000   ],
                "Be" : ["Beryllium"    , 4   ,  0.900000 , 1.700000,  9.012182   ],
                "B"  : ["Boron"        , 5   ,  0.820000 , 2.080000,  10.811000  ],
                "C"  : ["Carbon"       , 6   ,  0.770000 , 1.950000,  12.010700  ],
                "N"  : ["Nitrogen"     , 7   ,  0.700000 , 1.850000,  14.006700  ],
                "O"  : ["Oxygen"       , 8   ,  0.660000 , 1.700000,  15.999400  ],
                "F"  : ["Fluorine"     , 9   ,  0.611000 , 1.730000,  18.998404  ],
                "Ne" : ["Neon"         , 10  ,  0.700000 , 1.540000,  20.179701  ],
                "Na" : ["Sodium"       , 11  ,  3.06     , 2.270000,  22.989771  ],
                "Mg" : ["Magnesium"    , 12  ,  1.360000 , 1.730000,  24.305000  ],
                "Al" : ["Aluminium"    , 13  ,  1.180000 , 2.050000,  26.981539  ],
                "Si" : ["Silicon"      , 14  ,  0.937000 , 2.100000,  28.085501  ],
                "P"  : ["Phosphorus"   , 15  ,  0.890000 , 2.080000,  30.973761  ],
                "S"  : ["Sulphur"      , 16  ,  1.040000 , 2.000000,  32.064999  ],
                "Cl" : ["Chlorine"     , 17  ,  0.997000 , 1.970000,  35.452999  ],
                "Ar" : ["Argon"        , 18  ,  1.740000 , 1.880000,  39.948002  ],
                "K"  : ["Potassium"    , 19  ,  2.030000 , 2.750000,  39.098301  ],
                "Ca" : ["Calcium"      , 20  ,  1.740000 , 1.973000,  40.077999  ],
                "Sc" : ["Scandium"     , 21  ,  1.440000 , 1.700000,  44.955910  ],
                "Ti" : ["Titanium"     , 22  ,  1.320000 , 1.700000,  47.867001  ],
                "V"  : ["Vanadium"     , 23  ,  1.220000 , 1.700000,  50.941502  ],
                "Cr" : ["Chromium"     , 24  ,  1.180000 , 1.700000,  51.996101  ],
                "Mn" : ["Manganese"    , 25  ,  1.170000 , 1.700000,  54.938049  ],
                "Fe" : ["Iron"         , 26  ,  1.170000 , 1.700000,  55.845001  ],
                "Co" : ["Cobalt"       , 27  ,  1.160000 , 1.700000,  58.933201  ],
                "Ni" : ["Nickel"       , 28  ,  1.150000 , 1.630000,  58.693401  ],
                "Cu" : ["Copper"       , 29  ,  1.170000 , 1.400000,  63.546001  ],
                "Zn" : ["Zinc"         , 30  ,  1.250000 , 1.390000,  65.408997  ],
                "Ga" : ["Gallium"      , 31  ,  1.260000 , 1.870000,  69.723000  ],
                "Ge" : ["Germanium"    , 32  ,  1.188000 , 1.700000,  72.639999  ],
                "As" : ["Arsenic"      , 33  ,  1.200000 , 1.850000,  74.921600  ],
                "Se" : ["Selenium"     , 34  ,  1.170000 , 1.900000,  78.959999  ],
                "Br" : ["Bromine"      , 35  ,  1.167000 , 2.100000,  79.903999  ],
                "Kr" : ["Krypton"      , 36  ,  1.910000 , 2.020000,  83.797997  ],
                "Rb" : ["Rubidium"     , 37  ,  2.160000 , 1.700000,  85.467796  ],
                "Sr" : ["Strontium"    , 38  ,  1.910000 , 1.700000,  87.620003  ],
                "Y"  : ["Yttrium"      , 39  ,  1.620000 , 1.700000,  88.905853  ],
                "Zr" : ["Zirconium"    , 40  ,  1.450000 , 1.700000,  91.223999  ],
                "Nb" : ["Niobium"      , 41  ,  1.340000 , 1.700000,  92.906380  ],
                "Mo" : ["Molybdenum"   , 42  ,  1.300000 , 1.700000,  95.940002  ],
                "Tc" : ["Technetium"   , 43  ,  1.270000 , 1.700000,  98.000000  ],
                "Ru" : ["Ruthenium"    , 44  ,  1.250000 , 1.700000,  101.070000 ],
                "Rh" : ["Rhodium"      , 45  ,  1.250000 , 1.700000,  102.905502 ],
                "Pd" : ["Palladium"    , 46  ,  1.280000 , 1.630000,  106.419998 ],
                "Ag" : ["Silver"       , 47  ,  1.340000 , 1.720000,  107.868202 ],
                "Cd" : ["Cadmium"      , 48  ,  1.480000 , 1.580000,  112.411003 ],
                "In" : ["Indium"       , 49  ,  1.440000 , 1.930000,  114.818001 ],
                "Sn" : ["Tin"          , 50  ,  1.385000 , 2.170000,  118.709999 ],
                "Sb" : ["Antimony"     , 51  ,  1.400000 , 2.200000,  121.760002 ],
                "Te" : ["Tellurium"    , 52  ,  1.378000 , 2.060000,  127.599998 ],
                "I"  : ["Iodine"       , 53  ,  1.387000 , 2.150000,  126.904472 ],
                "Xe" : ["Xenon"        , 54  ,  1.980000 , 2.160000,  131.292999 ],
                "Cs" : ["Cesium"       , 55  ,  2.350000 , 1.700000,  132.905457 ],
                "Ba" : ["Barium"       , 56  ,  1.980000 , 1.700000,  137.326996 ],
                "La" : ["Lanthanum"    , 57  ,  1.690000 , 1.700000,  138.905502 ],
                "Ce" : ["Cerium"       , 58  ,  1.830000 , 1.700000,  140.115997 ],
                "Pr" : ["Praseodymium" , 59  ,  1.820000 , 1.700000,  140.907654 ],
                "Nd" : ["Neodymium"    , 60  ,  1.810000 , 1.700000,  144.240005 ],
                "Pm" : ["Promethium"   , 61  ,  1.800000 , 1.700000,  145.000000 ],
                "Sm" : ["Samarium"     , 62  ,  1.800000 , 1.700000,  150.360001 ],
                "Eu" : ["Europium"     , 63  ,  1.990000 , 1.700000,  151.964005 ],
                "Gd" : ["Gadolinium"   , 64  ,  1.790000 , 1.700000,  157.250000 ],
                "Tb" : ["Terbium"      , 65  ,  1.760000 , 1.700000,  158.925339 ],
                "Dy" : ["Dysprosium"   , 66  ,  1.750000 , 1.700000,  162.500000 ],
                "Ho" : ["Holmium"      , 67  ,  1.740000 , 1.700000,  164.930313 ],
                "Er" : ["Erbium"       , 68  ,  1.730000 , 1.700000,  167.259003 ],
                "Tm" : ["Thulium"      , 69  ,  1.720000 , 1.700000,  168.934204 ],
                "Yb" : ["Ytterbium"    , 70  ,  1.940000 , 1.700000,  173.039993 ],
                "Lu" : ["Lutetium"     , 71  ,  1.720000 , 1.700000,  174.966995 ],
                "Hf" : ["Hafnium"      , 72  ,  1.440000 , 1.700000,  178.490005 ],
                "Ta" : ["Tantalum"     , 73  ,  1.340000 , 1.700000,  180.947906 ],
                "W"  : ["Tungsten"     , 74  ,  1.300000 , 1.700000,  183.839996 ],
                "Re" : ["Rhenium"      , 75  ,  1.280000 , 1.700000,  186.207001 ],
                "Os" : ["Osmium"       , 76  ,  1.260000 , 1.700000,  190.229996 ],
                "Ir" : ["Iridium"      , 77  ,  1.270000 , 1.700000,  192.216995 ],
                "Pt" : ["Platinum"     , 78  ,  1.300000 , 1.720000,  195.078003 ],
                "Au" : ["Gold"         , 79  ,  1.340000 , 1.660000,  196.966553 ],
                "Hg" : ["Mercury"      , 80  ,  1.490000 , 1.550000,  200.589996 ],
                "Tl" : ["Thallium"     , 81  ,  1.480000 , 1.960000,  204.383301 ],
                "Pb" : ["Lead"         , 82  ,  1.480000 , 2.020000,  207.199997 ],
                "Bi" : ["Bismuth"      , 83  ,  1.450000 , 1.700000,  208.980377 ],
                "Po" : ["Polonium"     , 84  ,  1.460000 , 1.700000,  209.000000 ],
                "At" : ["Astatine"     , 85  ,  1.450000 , 1.700000,  210.000000 ],
                "Rn" : ["Radon"        , 86  ,  2.400000 , 1.700000,  222.000000 ],
                "Fr" : ["Francium"     , 87  ,  2.000000 , 1.700000,  223.000000 ],
                "Ra" : ["Radium"       , 88  ,  1.900000 , 1.700000,  226.000000 ],
                "Ac" : ["Actinium"     , 89  ,  1.880000 , 1.700000,  227.000000 ],
                "Th" : ["Thorium"      , 90  ,  1.790000 , 1.700000,  232.038101 ],
                "Pa" : ["Protactinium" , 91  ,  1.610000 , 1.700000,  231.035873 ],
                "U"  : ["Uranium"      , 92  ,  1.580000 , 1.860000,  238.028915 ],
                "Np" : ["Neptunium"    , 93  ,  1.550000 , 1.700000,  237.000000 ],
                "Pu" : ["Plutionium"   , 94  ,  1.530000 , 1.700000,  244.000000 ],
                "Am" : ["Americium"    , 95  ,  1.070000 , 1.700000,  243.000000 ],
                "Cm" : ["Curium"       , 96  ,  0.000000 , 1.700000,  247.000000 ],
                "Bk" : ["Berkelium"    , 97  ,  0.000000 , 1.700000,  247.000000 ],
                "Cf" : ["Californium"  , 98  ,  0.000000 , 1.700000,  251.000000 ],
                "Es" : ["Einsteinium"  , 99  ,  0.000000 , 1.700000,  252.000000 ],
                "Fm" : ["Fermium"      , 100 ,  0.000000 , 1.700000,  257.000000 ],
                "Md" : ["Mendelevium"  , 101 ,  0.000000 , 1.700000,  258.000000 ],
                "No" : ["Nobelium"     , 102 ,  0.000000 , 1.700000,  259.000000 ],
                "Lr" : ["Lawrencium"   , 103 ,  0.000000 , 1.700000,  262.000000 ],
                "Rf" : ["Rutherfordiu" , 104 ,  0.000000 , 1.700000,  261.000000 ],
                "Db" : ["Dubnium"      , 105 ,  0.000000 , 1.700000,  262.000000 ],
                "Sg" : ["Seaborgium"   , 106 ,  0.000000 , 1.700000,  263.000000 ],
                "Bh" : ["Bohrium"      , 107 ,  0.000000 , 1.700000,  264.000000 ],
                "Hs" : ["Hassium"      , 108 ,  0.000000 , 1.700000,  265.000000 ],
                "Mt" : ["Meitnerium"   , 109 ,  0.000000 , 1.700000,  268.000000 ],
                "Xx" : ["Dummy"        , 0   ,  0.000000 , 0.000000,  0.000000   ],
                "X"  : ["Dummy"        , 0   ,  0.000000 , 0.000000,  0.000000   ]
              }



'''
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
'''



from pymol import *
from pymol import cmd
from pymol.cgo import *

SCRATCH = os.environ.get('PDYNAMO_SCRATCH')


'''
	             #==================================================#
	             #             NEW GTKDYNAMO FUCTIONS               #
	             #==================================================#


'''


def DihedralFromPKSelection (selections = []):
    """ Function doc """
    dihedral = {}
    if 'pk4' in selections:
        dihedral['pk1pk2pk3pk4'] = str(cmd.get_dihedral ('pk1','pk2','pk3','pk4')) 
    else:
        dihedral['pk1pk2pk3pk4'] = None  
    return dihedral

def AnglesFromPKSelection(selections = []):
    """ Function doc """
    angles = {} 
    
    if 'pk3' in selections:
        angles['pk1pk2pk3'] = str(cmd.get_angle('pk1','pk2','pk3')) 
    else:    
        angles['pk1pk2pk3'] = None
    
    if 'pk4' in selections:
        angles['pk2pk3pk4'] = str(cmd.get_angle('pk2','pk3', 'pk4') )
    else:
        angles['pk2pk3pk4'] = None
    
    return angles

def DistancesFromPKSelection(selections = []):
    """ Function doc """
    distances = {} 
    try:
        distances['pk1pk2'] = str(cmd.get_distance('pk1','pk2') )
    except:
        distances['pk1pk2'] = None
    try:
        distances['pk1pk3'] = str(cmd.get_distance('pk1','pk3') )
    except:
        distances['pk1pk3'] = None
    try:
        distances['pk1pk4'] = str(cmd.get_distance('pk1','pk4') )
    except:
        distances['pk1pk4'] = None
    try:
        distances['pk2pk3'] = str(cmd.get_distance('pk2','pk3') )
    except:
        distances['pk2pk3'] = None
    try:
        distances['pk2pk4'] = str(cmd.get_distance('pk2','pk4') )
    except:
        distances['pk2pk4'] = None
    try:
        distances['pk3pk4'] = str(cmd.get_distance('pk3','pk4') )
    except:
        distances['pk3pk4'] = None
    return distances
        
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
    #print table
    return table


# Table   --->   PyMOL
def PymolPutTable(table, selection):
    '''
    # old - pymol_put_table        
    # add a selection in PyMOL from a given table [pDynamoProject mainly] 
    # obs: In  pDynamo the index starts in number 0        
    '''
    try:
        cmd.delete(selection)
    except:
        pass
        
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
    #print project.settings['types_allowed']
    if project == None:
        print 'only testing ExportFramesToPymol'
    

    
    else:
        try:
            charges = project.system.energyModel.mmAtoms.AtomicCharges()
            charge_table = list(charges)
        except:
            charge_table = None
                
        data_path = project.settings['data_path']
        types_allowed = project.settings['types_allowed']

        tmp_path = data_path + '/tmp'
        if not os.path.exists(tmp_path):
            os.mkdir(tmp_path)

        # creating a xyz file - coordienate reference
        if types_allowed['xyz'] == True:
            type_ = 'xyz'
            pymol_id ='Step' + str(project.settings['step'])
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
            pymol_id ='Step' + str(project.settings['step'])

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
                
                if charge_table != None:
                    a.partial_charge = charge_table[n]
                    #a.b              = charge_table[n]
                
                #print a.partial_charge , a.b 
                a.coord[0]       = new_coord[n][0]
                a.coord[1]       = new_coord[n][1]
                a.coord[2]       = new_coord[n][2]
                n = n + 1
            
            cmd.delete(pymol_id)
            cmd.load_model(model3, pymol_id)
            
            #cmd.load_model(model3, "_tmp")
            #cmd.update(pymol_id, "_tmp")
            #cmd.delete("_tmp")

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
    #print last_step
    #print working_folder
    #print system
    #print pymol_session
    #print last_pymol_id
    # return 	last_step ,	working_folder,	system,	pymol_session, last_pymol_id
    return _ProjectSettings


def PyMOLRepresentations (representation, selection):
    """ Function doc """
    #print "aqui"
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
	
	mass1 = atomic_dic[pk1_name][4]
	mass3 = atomic_dic[pk3_name][4]
	
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


def DrawCell (cell):
    if cell == None:
        try:
            cmd.delete("box_1")
        except:
            pass
    else:
        #print cell
        minX  = 0.0
        minY  = 0.0
        minZ  = 0.0
        maxX  = cell['a']
        maxY  = cell['b']
        maxZ  = cell['c']


        
        selection="(all)"
        padding=0.0
        linewidth=2.0
        r=1.0
        g=5.0
        b=5.0
        
        #print maxX,maxY,maxZ
        
        boundingBox = [
                LINEWIDTH, float(linewidth),

                BEGIN, LINES,
                COLOR, float(r), float(g), float(b),

                VERTEX, minX, minY, minZ,       #1
                VERTEX, minX, minY, maxZ,       #2

                VERTEX, minX, maxY, minZ,       #3
                VERTEX, minX, maxY, maxZ,       #4

                VERTEX, maxX, minY, minZ,       #5
                VERTEX, maxX, minY, maxZ,       #6

                VERTEX, maxX, maxY, minZ,       #7
                VERTEX, maxX, maxY, maxZ,       #8


                VERTEX, minX, minY, minZ,       #1
                VERTEX, maxX, minY, minZ,       #5

                VERTEX, minX, maxY, minZ,       #3
                VERTEX, maxX, maxY, minZ,       #7

                VERTEX, minX, maxY, maxZ,       #4
                VERTEX, maxX, maxY, maxZ,       #8

                VERTEX, minX, minY, maxZ,       #2
                VERTEX, maxX, minY, maxZ,       #6


                VERTEX, minX, minY, minZ,       #1
                VERTEX, minX, maxY, minZ,       #3

                VERTEX, maxX, minY, minZ,       #5
                VERTEX, maxX, maxY, minZ,       #7

                VERTEX, minX, minY, maxZ,       #2
                VERTEX, minX, maxY, maxZ,       #4

                VERTEX, maxX, minY, maxZ,       #6
                VERTEX, maxX, maxY, maxZ,       #8

                END
        ]
        
        try:
            cmd.delete("box_1")
        except:
            pass
        
        #print boundingBox
        boxName = "box_1"
        cmd.set('auto_zoom', 0)
        cmd.load_cgo(boundingBox,boxName)
        #cmd.set_frame(-1)



def main():
    ExportFramesToPymol()
    return 0

if __name__ == '__main__':
    main()
