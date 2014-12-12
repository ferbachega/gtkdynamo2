# pDynamo
from pBabel import *
from pCore import *
from pMolecule import *
from pMoleculeScripts import *

#
# GTKDynamo
from pDynamoMinimization      import *
from pDynamoEnergy            import *
from pDynamoMolecularDynamics import *
from pymol import cmd
from PyMOLScripts import *
from LogParse import ParseSummaryLogFile, ParseProcessLogFile

import time
import json


class pDynamoProject():

    def __init__(self, data_path=None, PyMOL=False, name='untitled', builder=None, window_control=None):

        #self.name = name
        '''
        self.AtomColors = {1 : 'util.cbag',   # green
                           2 : 'util.cbac',   # cyan
                           3 : 'util.cbam',   # light magenta
                           4 : 'util.cbay',   # yellow
                           5 : 'util.cbas',   # salmon
                           6 : 'util.cbaw',   # white/grey
                           7 : 'util.cbab',   # slate
                           8 : 'util.cbao',   # bright orange
                           9 : 'util.cbap',   # purple
                          10 : 'util.cbak'}   # pink 

        self.parameters = {
                          'Number of Atoms'      : '0', 
                          'Energy Model'         : 'UNK',
                          'Number of QC Atoms'   : '0',
                          'Number of Fixed Atoms': '0'         
                          }
        
        MM_representation  = {'lines'  :True ,
                              'stick'  :False,
                              'ribbon' :False,
                              'cartoon':False,
                              'dot'    :False,
                              'sphere' :False,
                              'mesh'   :False,
                              'surface':False                             
                              }
                           
        QC_representation  = {'lines'  :False,
                               'stick'  :True ,
                              'ribbon' :False,
                              'cartoon':False,
                              'dot'    :False,
                              'sphere' :True ,
                              'mesh'   :False,
                              'surface':False                             
                              }
        
        FIX_representation = {'lines'  :False,
                              'stick'  :False,
                              'ribbon' :False,
                              'cartoon':False,
                              'dot'    :False,
                              'sphere' :False,
                              'mesh'   :False,
                              'surface':False,
                              'color'  :'grey80'                          
                              }
        '''

        
        self.settings = {
                       'force_field'  : None,
                       'parameters'   : None,
                       'topology'     : None,
                       'coordinates'  : None,
                       
                       'nbModel_type' : 'NBModelABFS',
                       #'nbModel'      : "NBModelABFS()",
                       'ABFS_options' : {"innerCutoff": 8.0, "outerCutoff": 12.0, "listCutoff": 13.5},
                       'types_allowed': {'pdb': True, 'xyz': False, 'mol2': False},

                       'prune_table'  : [],
                       'fix_table'    : [],
                       'qc_table'     : [],
                       
                       'QC'           : False,
                       'potencial'    : None,
                       'qc_method'    : None,
                       
                       'data_path'    : data_path,   # estah sendo usado 
                       'step'         : 0,
                       'last_step'    : None,
                      
                       
                       
                       'job_history'  :{
                                       # actual style
                                       #'1': ['Step_1', 'new', '"AMBER/AM1/ABFS"', '43', 'black']  
                                       
                                       # new propose
                                       #'1': {                                                      
                                       #      'object'    : 'Step1'           ,
                                       #      'type'      : 'new/min/dyn/prn' ,
                                       #      'parameters': parameters        ,       -  extracted from the log -  checksystem
                                       #      'potencial' : "AMBER/AM1/ABFS"  ,
                                       #      'CQatoms'   : '43'              ,
                                       #      'color'     : 'black'
                                       #     }
                                       },
                       
                       'PyMOL_Obj'     : None,
                       'pymol_session' : None,   #  - pdynamo pkl/yaml file
                       'filename'      : None,
                       'pDynamo_system': None    #  - pymol pse file
                       } 
        self.nbModel        = "NBModelABFS()"
        self.parameters     = None
        self.system         = None          
        self.PyMOL          = PyMOL         
        self.dualLog        = None          
        self.builder        = builder       
        self.window_control = window_control
        self.ActiveMode     = False 
        
        
        ''' 
                   BondTable  
        
        
        
                          A1   A2      Bond   Active
                                     
        BondTable      = {(1,  2)  :   [1.1,   True]}
        
        BondTable[1,2] = [atomic_dic["C"][2] + atomic_dic["H"][2], True]
        
        
        '''
        self.BondTable = {}
        
        
    def set_AMBER_MM(self, amber_params, amber_coords, dualLog=None):
        self.system = AmberTopologyFile_ToSystem(amber_params, dualLog)
        self.system.coordinates3 = AmberCrdFile_ToCoordinates3(
            amber_coords, dualLog)
        self.settings['force_field'] = "AMBER"
        self.settings['parameters']  = amber_params
        self.settings['coordinates'] = amber_coords
        self.settings['potencial']   = "MM"

    def set_CHARMM_MM(self, charmm_params, charmm_topologies, dualLog=None):

        parameters = CHARMMParameterFiles_ToParameters(
            [(charmm_params)],  dualLog)
        self.system = CHARMMPSFFile_ToSystem(os.path.join(
            charmm_topologies), isXPLOR=True, log=dualLog, parameters=parameters)
        self.settings['force_field'] = "CHARMM"
        self.settings['parameters']  = charmm_params
        self.settings['topology']    = charmm_topologies
        self.settings['potencial']   = "MM"

    def set_GROMACS_MM(self, gromacs_params, gromacs_coords, dualLog=None):

        parameters = GromacsParameters_ToParameters(
            gromacs_params,  log=dualLog)
        self.system = GromacsDefinitions_ToSystem(
            gromacs_params,  log=dualLog, parameters=parameters)
        self.system.coordinates3 = GromacsCrdFile_Process(
            gromacs_coords,  system=self.system,  log=dualLog)

        self.settings['force_field'] = "GROMACS"
        self.settings['potencial']   = "MM"
        self.settings['parameters']  = gromacs_params
        self.settings['coordinates'] = gromacs_coords

    def set_OPLS_MM(self, opls_params, opls_coords,  dualLog=None):

        path_levels = opls_params.split("/")
        path = "/"

        for level in path_levels:
            # "if the parameters directory is included, does not consider"
            if level != path_levels[-1]:
                path = path + '/' + level

        print "Your path is ", path
        print "your parameters are: ", path_levels[-1]

        mmModel = MMModelOPLS(path_levels[-1], path=path)

        file_type = opls_coords.split(".")
        file_type = file_type[-1]

        if file_type == "mol":
            self.system = MOLFile_ToSystem(
                os.path.join(opls_coords), log=dualLog)

        elif file_type == "pdb":
            self.system = PDBFile_ToSystem(
                opls_coords, log=dualLog, modelNumber=1, useComponentLibrary=True)

        elif file_type == "mol2":
            self.system = MOL2File_ToSystem(
                os.path.join(opls_coords), log=dualLog)

        self.system.DefineMMModel(mmModel)
        self.settings['force_field'] = "OPLS"
        self.settings['potencial']   = "MM"
        self.settings['parameters']  = opls_params
        self.settings['coordinates'] = opls_coords
        #return self.system

    def set_qc_parameters_MNDO(self, qc_method, charge, multiplicity):
        qc_table = self.settings['qc_table']                                                     
        nbModel  = self.nbModel
        qcModel  = QCModelMNDO (qc_method )
        self.system.electronicState = ElectronicState  ( charge = charge, multiplicity = multiplicity )

        if len(qc_table) != 0:
            Qgroup = Selection (qc_table)
            self.system.DefineQCModel ( qcModel, qcSelection = Qgroup)
            self.system.DefineNBModel ( nbModel )
            self.settings['potencial'] = "QC"
            self.settings['QC']        = True
            self.set_nbModel_to_system()
            
        else:
            self.system.DefineQCModel ( qcModel )
            self.settings['potencial'] = "QC"
            self.settings['QC']        = True
        
        
        self.SystemCheck()
        self.set_qc_DynamicBondsList()

    def set_qc_parameters_DFT (self, qc_method, charge, multiplicity, density_tol, Maximum_SCF, densityBasis, functional, orbitalBasis):
        nbModel   = self.nbModel
        qc_table  = self.settings['qc_table']                                                     
        converger = DIISSCFConverger ( densityTolerance = float(density_tol), maximumSCFCycles = int(Maximum_SCF) )
        
        qcModel   = QCModelDFT (converger = converger, 
                             densityBasis = densityBasis, 
                               functional = functional,  
                             orbitalBasis = orbitalBasis  )
        
        self.system.electronicState = ElectronicState  ( charge = charge, multiplicity = multiplicity )

        if len(qc_table) != 0:
            Qgroup = Selection (qc_table)
            self.system.DefineQCModel ( qcModel, qcSelection = Qgroup)
            self.system.DefineNBModel ( nbModel )
            self.settings['potencial'] = "QC"
            self.settings['QC']      = True
            self.set_nbModel_to_system()
        else:
            self.system.DefineQCModel ( qcModel )
            self.settings['potencial'] = "QC"
            self.settings['QC']      = True
        self.SystemCheck()

    def set_qc_parameters_ORCA(self, qc_method, charge, multiplicity, qc_table, orca_string, ORCA_pal, ORCA_command, pDynamo_scratch):
        """
        #scratch='/home/ramon/scratch'
        #command='/home/ramon/progs/orca_3_0_0_linux_x86-64/orca'
        """

        nbModel     = NBModelABFS( )
        PAL         = " PAL"+str(ORCA_pal)
       
        print "number of processor = ", PAL
        
        if ORCA_pal == 1:
            qcModel = QCModelORCA (orca_string, scratch = pDynamo_scratch, command =  ORCA_command)

        else:
            orca_string = orca_string + PAL
            qcModel = QCModelORCA (orca_string, scratch = pDynamo_scratch, command =  ORCA_command)

        if len(qc_table) != 0:
            Qgroup  = Selection (qc_table)
            self.system.DefineQCModel ( qcModel,  dualLog, qcSelection = Qgroup)
            nbModel = NBModelORCA ( )
            self.system.DefineNBModel ( nbModel )
            self.system.Summary ( dualLog )
            
            self.settings['potencial'] = "QC"
            self.settings['QC']  	 = True
        else:
            self.system.DefineQCModel ( qcModel )
            self.system.Summary (dualLog )

            self.settings['potencial'] = "QC"
            self.settings['QC']      = False	
        self.system.electronicState           = ElectronicState  ( charge = charge, multiplicity = multiplicity )

    def set_qc_DynamicBondsList(self):
        lista  = self.settings['qc_table']
        self.BondTable       = {}
        for i in lista:
            for j in lista: 
                if i != j:
                    atom1    = self.system.atoms[i]
                    atom2    = self.system.atoms[j]
                    element1 = PeriodicTable.Symbol (atom1.atomicNumber ).upper ( )
                    element2 = PeriodicTable.Symbol (atom2.atomicNumber ).upper ( )
                    #BondTable[i,j] = [atomic_dic[element1][2] + atomic_dic[element2][2], True]



                    Distance_i_j             = self.system.coordinates3.Distance (i,j)
                    Rcov                     = (atomic_dic[element1][2] + atomic_dic[element2][2]) + (atomic_dic[element1][2] + atomic_dic[element2][2])/50
                    Bond_Unbond              = None
                    if Distance_i_j <= Rcov:
                        Bond_Unbond  = True
                    else:
                        Bond_Unbond  = False

                    #PyMOL_BondTable[i+1,j+1] = [atomic_dic[element1][2] + atomic_dic[element2][2], True]
                    #print i+1, element1, j+1,element2, "BOND: ", Rcov, Distance_i_j, Bond_Unbond
                    self.BondTable[i+1,j+1] = [Rcov, Bond_Unbond]

        print self.BondTable


    
    def DeleteActualProject (self):
        """ Function doc """
        
        self.settings = {
                       'add_info'     : None,
                       'force_field'  : None,
                       'parameters'   : None,
                       'topology'     : None,
                       'coordinates'  : None,
                       
                       'nbModel_type' : 'NBModelABFS',
                       #'nbModel'      : "NBModelABFS()",
                       'ABFS_options' : {"innerCutoff": 8.0, "outerCutoff": 12.0, "listCutoff": 13.5},
                       'types_allowed': {'pdb': True, 'xyz': False, 'mol2': False},

                       'prune_table'  : [],
                       'fix_table'    : [],
                       'qc_table'     : [],
                       
                       'QC'           : False,
                       'potencial'    : None,
                       'qc_method'    : None,
                       
                       'data_path'    : None,   # estah sendo usado 
                       'step'         : 0,
                       'last_step'    : None,
                      
                       
                       
                       'job_history'  :{
                                       # actual style
                                       #'1': ['Step_1', 'new', '"AMBER/AM1/ABFS"', '43', 'black']  
                                       
                                       # new propose
                                       #'1': {                                                      
                                       #      'object'    : 'Step1'           ,
                                       #      'type'      : 'new/min/dyn/prn' ,
                                       #      'parameters': parameters        ,       -  extracted from the log -  checksystem
                                       #      'potencial' : "AMBER/AM1/ABFS"  ,
                                       #      'CQatoms'   : '43'              ,
                                       #      'color'     : 'black'
                                       #     }
                                       },
                       
                       'PyMOL_Obj'     : None,
                       'filename'      : None,   # ex.  /home/fernando/pDynamoWorkSpace/Enolase_Dec_11_2014/projectBaseName
                       'pymol_session' : None,   #    - pdynamo pkl/yaml file
                       'pDynamo_system': None    #    - pymol pse file
                       } 
        #self.nbModel        = "NBModelABFS()"
        #self.parameters     = None
        #self.system         = None          
        #self.PyMOL          = True       
        #self.dualLog        = None          
        #self.builder        = builder       
        #self.window_control = window_control
        #self.ActiveMode     = False 
        
    
    def Create_New_Project(self, name = "UNK",  # str
                           data_path  = None,  # str
                           FileType   = None,  # str
                           filesin    = None,  # dictionary
                           BufferText = None):  # buffertext
        """ Function doc """

        self.name = name

        if data_path is not None:
            self.settings['data_path'] = data_path

        FileType = FileType
        filesin = filesin

        if FileType == "AMBER":
            amber_params = filesin['amber_params']
            amber_coords = filesin['amber_coords']
            self.set_AMBER_MM(amber_params, amber_coords, self.dualLog)
            self.set_nbModel_to_system()
        
        elif FileType == "CHARMM":
            charmm_params = filesin['charmm_params']
            charmm_topologies = filesin['charmm_topologies']
            charmm_coords = filesin['charmm_coords']
            
            self.set_CHARMM_MM(charmm_params, charmm_topologies, self.dualLog)
            filetype = self.load_coordinate_file_to_system(
                charmm_coords, self.dualLog)
            self.set_nbModel_to_system()
        
        elif FileType == "GROMACS":
            gromacs_params = filesin['gromacs_params']
            gromacs_coords = filesin['gromacs_coords']

            self.set_GROMACS_MM(gromacs_params, gromacs_coords, self.dualLog)
            self.set_nbModel_to_system()
        
        
        elif FileType == "OPLS":
            opls_params = filesin['opls_params']
            opls_coords = filesin['opls_coords']
            self.set_OPLS_MM(opls_params, opls_coords, self.dualLog)
            self.set_nbModel_to_system()
        
        elif FileType == "pDynamo files(*.pkl,*.yaml)":
            NewSystem = filesin["pDynamoFile"]					#
            self.load_coordinate_file_as_new_system(NewSystem, self.dualLog)

        
        elif FileType == "Other(*.pdb,*.xyz,*.mol2...)":
            NewSystem = filesin["coordinates"]					#
            self.load_coordinate_file_as_new_system(NewSystem, self.dualLog)

        
        print BufferText
        #text  = BufferText.get_text()
        #print text
        ## nbModel applied
        #if FileType is not "pDynamo files(*.pkl,*.yaml)":
        #    self.set_nbModel_to_system()

        
        #self.system.Summary(
        #    log=DualTextLog(self.data_path, str(self.step + 1) + '_' + self.name + ".log"))

        self.From_PDYNAMO_to_GTKDYNAMO(type_='new')

    def Save_Project_To_File (self, filename = 'actual_state', type_ = 'pkl'):
        """ Function doc """
        path     = filename.split('/')
        
        FileName = path.pop()
        
        new_data_path = '/'
        for i in path:
            new_data_path = os.path.join(new_data_path,i)


        
        self.settings['pDynamo_system' ] = FileName + '.pkl'
        self.settings['pymol_session']   = FileName + '.pse'
        self.settings['filename']        = filename
        
        settings2 = self.settings
        settings2['prune_table'] = []
        settings2['fix_table'  ] = []  
        #settings2['qc_table'   ] = []  
        settings2['data_path'  ] = new_data_path
        
        FOLDER  = self.settings['data_path']
        
        print 'New data path:  ',new_data_path
        json.dump(settings2,     open(filename+'.gtkdyn', 'w'), indent=2) # json file
        print 'exporting file: ', filename+'.gtkdyn'
        
        self.export_state_to_file    (filename, type_)                    # pkl  file
        print 'exporting file: ', filename+'.pkl'
        
        cmd.save                     (filename+'.pse', 'pse')             # pse  file
        print 'exporting file: ', filename+'.pse'

    
    def export_state_to_file (self, filename, type_):

		filename = AddFileTypeSuffix(filename, type_)     # from PyMOLScripts

		if type_   == "xyz":
			XYZFile_FromSystem ( filename, self.system )
		
		elif type_ == "pdb":
			PDBFile_FromSystem ( filename, self.system )

		elif type_ == "mol2":
			MOL2File_FromSystem ( filename, self.system )
		
		elif type_ == "pkl":
			try:
				XMLPickle ( filename, self.system )
			except:
				Pickle ( filename, self.system )

		elif type_ == "yaml":
			YAMLPickle ( filename, self.system )
		
		elif type_ == "mol":
			MOLFile_FromSystem ( filename, self.system )

		elif filetype == "cif":
			mmCIFFile_FromSystem ( filename, self.system )

		elif type_ == "psf":
			CHARMMPSFFile_FromSystem( filename, self.system )

		elif  type_ == "crd":
			AmberCrdFile_FromSystem( filename, self.system )

		else:
			print "file type not supported"


   
    def SystemCheck(self, status = True, PyMOL = True ):
        if self.system == None:
            print "System empty"
            StatusText =''
            self.window_control.STATUSBAR_SET_TEXT(StatusText)
            return 0
        
        if status == True:
            """ Function doc """
            SummaryFile             = "Summary"+'_Step'+str(self.settings['step'])+".log"
            self.system.Summary(log = DualTextLog(self.settings['data_path'], SummaryFile))
            self.parameters         = ParseSummaryLogFile(os.path.join(self.settings['data_path'], SummaryFile))
            
            #-------------------------------------#
            #              STATUSBAR              #
            #-------------------------------------#
            StatusText = ''
            if self.parameters is not None:
                StatusText = StatusText + '  Atoms: ' + self.parameters['Number of Atoms'] + "   "
                #print self.parameters['Number of Atoms']
                StatusText = StatusText + '  Potencial: ' + self.parameters['Energy Model']+ "   "
                #print self.parameters['Energy Model']
                StatusText = StatusText + '  QC Atoms: ' + self.parameters['Number of QC Atoms']+ "   "
                #print self.parameters['Number of QC Atoms']
                StatusText = StatusText + '  Fixed Atoms: ' + self.parameters['Number of Fixed Atoms']+ "   "
                #print self.parameters['Number of Fixed Atoms']
                StatusText = StatusText + '  Step: ' + str(self.settings['step'])+ "   "
                StatusText = StatusText + '  Crystal Class: ' + self.parameters['Crystal Class']+ "   "
                #StatusText = StatusText + '  Connected: ' +self.PyMOL_Obj + "   "
                
                StatusText = StatusText + '  Project Folder: ' + self.settings['data_path']+ "   "
                #print self.parameters['Crystal Class']
            self.window_control.STATUSBAR_SET_TEXT(StatusText)        
        else:
            pass

        
        if PyMOL == True:
            PyMOL_Obj      = self.settings['PyMOL_Obj']
            #cmd.util.cbap(PyMOL_Obj)
            cmd.color('grey10',PyMOL_Obj)
            cmd.util.cnc(PyMOL_Obj)
            
            if self.settings['QC'] == True:
                if self.settings['qc_table'] != []:
                    print PyMOL_Obj
                    cmd.hide('stick',  PyMOL_Obj)
                    cmd.hide("sphere", PyMOL_Obj)
                    try:
                        cmd.delete("QC_atoms")
                    except:
                        pass
                    
                    PymolPutTable(self.settings['qc_table'], "QC_atoms")
                    command = 'select QC_atoms, (' + PyMOL_Obj + ' and  QC_atoms )'
                    cmd.do(command)

                    cmd.show("stick",  "QC_atoms")
                    cmd.show("sphere", "QC_atoms")
                
                if self.settings['qc_table'] == []:
                    self.settings['qc_table']  = (self.system.energyModel.qcAtoms.QCAtomSelection ( ) )
                    try:
                        cmd.show("stick",  PyMOL_Obj)
                        cmd.show("sphere" ,PyMOL_Obj)
                    except:
                        a = None	
            else:
                pass
            
            if self.settings['fix_table'] != []:
                #PyMOL_Obj = self.job_history[self.step][0] #= [type_, pymol_id, "potencial", "1192.0987"]
                
                try:
                    cmd.delete("FIX_atoms")
                except:
                    pass
                    
                PymolPutTable(self.settings['fix_table'], "FIX_atoms")
                command = 'select FIX_atoms, (' + PyMOL_Obj + ' and  FIX_atoms )'
                cmd.do(command)
                command2 = 'color grey80, FIX_atoms'
                cmd.do(command2)
            
            try:
                #cmd.do('disable sele')
                cmd.disable("sele")
            except:
                pass
            try:
                #cmd.do('disable FIX_atoms')
                cmd.disable("FIX_atoms")

            except:
                pass
            try:
                #cmd.do('disable QC_atoms')
                cmd.disable("QC_atoms")
            except:
                pass
            
            pymol_objects2 = cmd.get_names('selections')
            liststore      = self.builder.get_object('liststore1')
            self.window_control.TREEVIEW_ADD_DATA (liststore, pymol_objects2)

            if self.PyMOL == True:
                #print self.parameters
                pass
    
        else:
            pass
        
    
    
    
    

    #def Open_GTKDYN_Project():
    #    '''Function description'''
    #    self.load_coordinate_file_as_new_system(NewSystem)
    #
    #    #                parei aqui !!!
    #
        # para abrir um projeto eh preciso inicialmente abrir uma arquivo pkl
        # abrir um sessao do pymol
        # resgatar os objetos do pymol conectados ao pDynamo

        # para abrir um projeto do pDynamo basta abrir um arquivo pkl e enviar
        # ao PyMOL > From_PDYNAMO_to_GTKDYNAMO


    def From_PDYNAMO_to_GTKDYNAMO(self, type_='UNK'):
        """ 
                                From_PDYNAMO_to_GTKDYNAMO

            esse metodo eh responsavel por:
                contar o passo
                exportar o frame atual para o pymol
                exportar as informacoes relevantes para as treeviews
                e adicionar informacoes ao history  via IncrementStep()
        """
        
        print 'step antes',self.settings['step']
        self.IncrementStep()
        print 'step depois',self.settings['step']

        if self.PyMOL == True:
            self.SystemCheck(True, False)
            #      pDyanmo  -- >  PyMOL
            pymol_id = ExportFramesToPymol(self, type_)
            self.settings['PyMOL_Obj'] = pymol_id
            
            
            #                OLD
            #
            #self.job_history[self.step] = [pymol_id                             ,  
            #                               type_                                ,    # - process type
            #                               self.parameters['Energy Model']      ,    # - potencial 
            #                               self.parameters['Number of QC Atoms'],    # - QC atoms
            #                               'black'                                   # - color
            #                               ]
            
            
            #                NEW
            #            
            self.settings['job_history'][str(self.settings['step'])] = {
                                                                   'object'    : pymol_id                             ,
                                                                   'type'      : type_                                , 
                                                                   'parameters': self.parameters                      , 
                                                                   'potencial' : self.parameters['Energy Model']      , 
                                                                   'CQatoms'   : self.parameters['Number of QC Atoms'], 
                                                                   'color'     : 'black'
                                                                   }

            
            pymol_objects  = cmd.get_names()
            liststore = self.builder.get_object('liststore2')
            
            self.window_control.TREEVIEW_ADD_DATA2(liststore, self.settings['job_history'] , pymol_id)
            
            #-------------------------------------#
            #             SystemCheck             #
            #-------------------------------------#           
            self.SystemCheck()
        else:
            print 'PyMOL ==',  self.PyMOL

    def load_coordinate_file_as_new_system(self, filename, dualLog=None):
        self.settings['prune_table']= []
        self.settings['fix_table']  = []
        self.settings['qc_table']   = []
        self.settings['QC']         = False
        type_ = GetFileType(filename)
        print filename
        print type_
        if type_ == "xyz":
            self.system = XYZFile_ToSystem(filename,  dualLog)

        # Quando o arquivo de coordenadas eh um PDB
        elif type_ == "pdb":
            # importa o arquivo xyz gerado pela funcao anterior
            self.system = PDBFile_ToSystem(filename,  log=dualLog)

        elif type_ == "cif":
            self.system = mmCIFFile_ToSystem(filename,  dualLog)

        elif type_ == "mop":
            self.system = MopacInputFile_ToSystem(filename,  dualLog)

        elif type_ == "mol":
            self.system = MOLFile_ToSystem(filename, log=dualLog)

        # --- pkl ---

        elif type_ == "pkl":
            self.system = Unpickle(filename)
            try:
                self.settings[
                    'fix_table'] = self.system.hardConstraints.fixedAtoms
                # print 'fix_table = :',self.settings['fix_table']
            except:
                a = None

            try:
                qc_table = list(
                    self.system.energyModel.qcAtoms.QCAtomSelection())
                boundaryAtoms = list(
                    self.system.energyModel.qcAtoms.BoundaryAtomSelection())

                self.settings['boundaryAtoms'] = boundaryAtoms
                # print 'qc_table : '  , qc_table
                print 'boundaryAtoms', (boundaryAtoms)

                qc = []
                for l in qc_table:
                    if l in boundaryAtoms:
                        print l
                    else:
                        qc.append(l)

                self.settings['qc_table'] = qc
                self.settings['QC']       = True
                print 'qc_table : ', self.settings['qc_table']
            except:
                print "System has no QC atoms"

        # --- yaml ---

        elif type_ == "yaml":
            self.system = YAMLUnpickle(filename)

            try:
                self.settings['fix_table'] = list(
                    self.system.hardConstraints.fixedAtoms)
                print 'fix_table = :', self.settings['fix_table']
            except:
                a = None

            try:
                qc_table = list(
                    self.system.energyModel.qcAtoms.QCAtomSelection())
                boundaryAtoms = list(
                    self.system.energyModel.qcAtoms.BoundaryAtomSelection())

                self.settings['boundaryAtoms'] = boundaryAtoms
                # print 'qc_table : '  , qc_table
                print 'boundaryAtoms', (boundaryAtoms)

                qc = []
                for l in qc_table:
                    if l in boundaryAtoms:
                        print l
                    else:
                        qc.append(l)

                self.settings['qc_table'] = qc
                self.settings['QC']     = True
                print 'qc_table : ', self.settings['qc_table']
            except:
                print "System has no QC atoms"

        else:
            return "ops!"
        try:
            self.system.Summary(dualLog)
        except:
            print "system empty"

        return type_

    def load_coordinate_file_to_system(self, filename, dualLog=None):
        type_ = GetFileType(filename)
        # print type_

        if type_ == "xyz":
            self.system.coordinates3 = XYZFile_ToCoordinates3(
                os.path.join(filename),  dualLog)

        # When the coordinate file is a PDB
        elif type_ == "pdb":
            # Uses the gtkdin_PDBFile_ToCoordinates3 functions - converts a PDB
            # to XYZ
            filename = gtkdin_PDBFile_ToCoordinates3(filename)
            # imports the xyz file
            self.system.coordinates3 = XYZFile_ToCoordinates3(
                os.path.join(filename),  dualLog)
            os.remove("tmp_out.xyz")

        elif type_ == "xpk":
            try:
                self.system.coordinates3 = Unpickle(filename)
            except:
                self.system.coordinates3 = XMLUnpickle(filename)

        elif type_ == "pkl":
            try:
                self.system.coordinates3 = Unpickle(filename)
            except:
                self.system.coordinates3 = XMLUnpickle(filename)

        elif type_ == "yaml":
            self.system.coordinates3 = YAMLUnpickle(filename)

        elif type_ == "chm":
            self.system.coordinates3 = CHARMMCRDFile_ToCoordinates3(
                os.path.join(filename),  dualLog)

        elif type_ == "crd":
            self.system.coordinates3 = AmberCrdFile_ToCoordinates3(
                os.path.join(filename),  dualLog)

        elif type_ == "mol":
            self.system.coordinates3 = MOLFile_ToCoordinates3(
                os.path.join(filename),  log=dualLog)
        else:
            return "ops!"

        #self.system.Summary(  dualLog )

        return type_

    def load_trajectory_to_system(self, first, last, stride, traj_name, new_pymol_object):
        cmd.disable('all')

        i = 0 
        i = i + first
        outPath = ( traj_name )
        print first, last, stride

        trajectory = SystemGeometryTrajectory (traj_name, self.system, mode = "r" )
        i = 0
        a = 0
        i = i + first
        export_type = 'pdb'

        while trajectory.RestoreOwnerData ( ):
            if export_type == 'pdb':
                if a == i:
                    PDBFile_FromSystem ( os.path.join ( outPath, new_pymol_object +".pdb" ), self.system)
                    cmd.load( os.path.join ( outPath, new_pymol_object +".pdb"))
                    i = i + stride
                    print "loading file: ",i
                if a == last:
                    break
                a=a+1
            else:
                if a == i:
                    XYZFile_FromSystem ( os.path.join ( outPath, new_pymol_object +".xyz" ), self.system)
                    cmd.load( os.path.join ( outPath, new_pymol_object +".xyz"))
                    i = i + stride
                    print "loading file: ",i
                if a == last:
                    break
                a=a+1	
        type_ = 'trj'
        
        put_new_obj_in_treeview = False
        
        self.settings['PyMOL_Obj'] = new_pymol_object
        
        for i in self.settings['job_history']:
            if self.settings['PyMOL_Obj'] in self.settings['job_history'][i]:
                put_new_obj_in_treeview = True

        
        if put_new_obj_in_treeview == False:
            self.IncrementStep()
            self.settings['job_history'][str(self.settings['step'])] = {
                                                                   'object'    : new_pymol_object                     ,
                                                                   'type'      : type_                                , 
                                                                   'parameters': self.parameters                      , 
                                                                   'potencial' : self.parameters['Energy Model']      , 
                                                                   'CQatoms'   : self.parameters['Number of QC Atoms'], 
                                                                   'color'     : 'black'
                                                                   }
            
                                                                                #[ new_pymol_object,  
                                                                                #type_ , 
                                                                                #self.parameters['Energy Model'], 
                                                                                #self.parameters['Number of QC Atoms']]  # it is only a test 
            pymol_objects  = cmd.get_names()
            liststore = self.builder.get_object('liststore2')
            self.window_control.TREEVIEW_ADD_DATA2(liststore, self.settings['job_history'], self.settings['PyMOL_Obj'])
            self.SystemCheck()
        
    def load_GTKDYNAMO_project(self, filename):
        """ Function doc """
        #print self.settings
        print filename
        
        
        path     = filename.split('/')
        FileName = path.pop()
        new_data_path = '/'
        for i in path:
            new_data_path = os.path.join(new_data_path,i)
        print new_data_path
        

        
        
        self.settings              = json.load(open(filename)) 
        self.settings['data_path'] = new_data_path
        
        print os.path.join( new_data_path, self.settings['pymol_session'])
        print os.path.join(new_data_path,self.settings['pDynamo_system'])

        self.load_coordinate_file_as_new_system(os.path.join(new_data_path,self.settings['pDynamo_system']))
        cmd.load (  os.path.join( new_data_path, self.settings['pymol_session'])   )
        
        pymol_objects  = cmd.get_names()
        liststore      = self.builder.get_object('liststore2')
        
        print pymol_objects
        print self.settings['job_history']
        pymol_id =  self.settings['PyMOL_Obj']
        self.window_control.TREEVIEW_ADD_DATA2(liststore, self.settings['job_history'] , self.settings['PyMOL_Obj'])
        self.SystemCheck()
        

    def set_nbModel_to_system(self):
        ABFS_options = self.settings['ABFS_options']
        nbModel = self.settings['nbModel_type']

        if nbModel == 'NBModelFull':
            nbModel = NBModelFull()
            self.system.DefineNBModel(nbModel)

        elif nbModel == 'NBModelABFS':
            nbModel = NBModelABFS()
            self.system.DefineNBModel(NBModelABFS(**ABFS_options))

        elif nbModel == 'NBModelGABFS':
            nbModel = NBModelGABFS()
            self.system.DefineNBModel(NBModelGABFS(**ABFS_options))

        elif nbModel == 'NBModelSSBP':
            nbModel = NBModelSSBP()
            self.system.DefineNBModel(nbModel)
        
        
        self.nbModel = nbModel
        self.SystemCheck()

    def put_prune_table(self, prune_table):
        #self.settings['prune_table']=[]
        print 'prune'
        
        self.settings['fix_table']  = []
        self.settings['qc_table']   = []
        self.settings['QC']         = False 
        self.system                 = PruneByAtom(self.system, Selection(prune_table))
      
        self.settings['prune_table'].append(prune_table)
        self.From_PDYNAMO_to_GTKDYNAMO(type_='prn')
        print 'pruned'        
        
    def put_fix_table(self, fix_table):
        self.system.DefineFixedAtoms(Selection(fix_table))
        
        self.settings['fix_table'] = fix_table
        
        self.SystemCheck()

    def clean_fix_table(self):
        self.system.DefineFixedAtoms(None)
        self.settings['fix_table'] = []
        self.SystemCheck()

    def put_qc_table(self, qc_table):
        self.settings['qc_table'] = qc_table
        #self.settings['QC'] = 'yes'
    def clean_qc_table(self):
        self.system.DefineQCModel (None)
        self.settings['qc_table'] = []
        self.SystemCheck()

    
    
    def IncrementStep(self):
        # {1:[process, pymol_id, potencial, energy]}
        #self.step = self.step + 1
        self.settings['step']      = self.settings['step'] + 1
        self.settings['last_step'] = self.settings['step']

    def ExportStateToFile(self, filename, type_):
        #self.ActiveModeCheck()
        filename = AddFileTypeSuffix(filename, type_)

        if type_ == "xyz":
            XYZFile_FromSystem(filename, self.system)

        elif type_ == "pdb":
            PDBFile_FromSystem(filename, self.system)

        elif type_ == "mol2":
            MOL2File_FromSystem(filename, self.system)

        elif type_ == "pkl":
            try:
                XMLPickle(filename, self.system)

            except:
                Pickle(filename, self.system)

        elif type_ == "yaml":
            YAMLPickle(filename, self.system)

        elif type_ == "mol":
            MOLFile_FromSystem(filename, self.system)

        elif filetype == "cif":
            mmCIFFile_FromSystem(filename, self.system)

        elif type_ == "psf":
            CHARMMPSFFile_FromSystem(filename, self.system)

        elif type_ == "crd":
            AmberCrdFile_FromSystem(filename, self.system)

        else:
            print "file type not supported"

        return filename, type_

    def ComputeEnergy(self):  # Compute Energy
        self.ActiveModeCheck()
        pDynamoEnergy(self.system, self.settings['data_path'])

    def Minimization(self, method='Conjugate Gradient', parameters=None):
        """ Function doc """

        self.ActiveModeCheck()
        #                               Minimization                                       #
        #    required: (system = None, _type_ = 'ConjugateGradient', parameters = None)    #
        # _type_  : 'ConjugateGradient' 'SteepestDescent' 'LBFGS'
        # #

        pDynamoMinimization(self.system, method, parameters, self.settings['data_path'])

        #------------------  increment step  ---------------#
        #
        self.From_PDYNAMO_to_GTKDYNAMO(type_='min')
        #
        #---------------------------------------------------#

        return True

    def MolecularDynamics(self, parameters):
        """ Function doc """
        print parameters

        self.ActiveModeCheck()

        #pDynamoMinimization(self.system, method, parameters, self.data_path)
        RunMolecularDynamics( self.system, self.settings['data_path'], parameters)
        
        
        #------------------  increment step  ---------------#
        #
        self.From_PDYNAMO_to_GTKDYNAMO(type_='dyn')
        #
        #---------------------------------------------------#

        return True
    
    def Scan1D (self, parameters):
        """ Function doc """
        print parameters

        self.ActiveModeCheck()

        #pDynamoMinimization(self.system, method, parameters, self.data_path)
        RunScan( self.system, self.settings['data_path'], parameters)
        
        
        #------------------  increment step  ---------------#
        #                                                   #
        self.From_PDYNAMO_to_GTKDYNAMO(type_='dyn')         #
        #                                                   #
        #---------------------------------------------------#

        return True   
    
    def ActiveModeCheck(self):
        """ Function doc """
        #return 0
        if self.ActiveMode:
            print "\n\n                  Using GTKDynamo in active mode \n\n"
            
            data_path  	 = self.settings['data_path']
            pymol_object = self.settings['PyMOL_Obj']
            
            print pymol_object
            
            state    	 = -1
            label        = "tmp file"
            file_out     = "tmp.xyz"	
            
            filename     = PyMOL_export_XYZ_to_file(pymol_object, label, data_path, file_out, state)	
            print filename
            self.load_coordinate_file_to_system  ( filename , self.dualLog)	
        else:
            print "Using GTKDynamo in passive mode"



def main():
    teste = pDynamoProject()
    teste.Minimization()
    return 0


if __name__ == '__main__':
    main()
