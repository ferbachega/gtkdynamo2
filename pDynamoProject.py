# pDynamo
from pBabel import *
from pCore import *
from pMolecule import *
from pMoleculeScripts import *

# GTKDynamo
from pDynamoMinimization import *

from pymol import cmd
from PyMOLScripts import *
from LogParse import ParseSummaryLogFile, ParseProcessLogFile

class pDynamoProject():

    def __init__(self, data_path=None, PyMOL=False, name='untitled', builder=None, window_control=None):

        self.name = name

        self.parameters = {
                          'Number of Atoms'      : '0', 
                          'Energy Model'         : 'UNK',
                          'Number of QC Atoms'   : '0',
                          'Number of Fixed Atoms': '0'         
                          }

        
        self.settings = {'project_name' : 'my_project',
                         'force_field'  : None,
                         'parameters'   : None,
                         'topology'     : None,
                         'coordinates'  : None,
                         'nbModel_type' : 'NBModelABFS',
                         'nbModel'      : "NBModelABFS()",
                         'ABFS_options' : {"innerCutoff": 8.0, "outerCutoff": 12.0, "listCutoff": 13.5},
                         'prune_table'  : [],
                         'fix_table'    : [],
                         'qc_table'     : [],
                         'QCMM'         : "No",
                         'potencial'    : None,
                         'qc_method'    : None,
                         'charge'       : None,
                         'multiplicity' : None,
                         'density_tol'  : None,
                         'Maximum_SCF'  : None,
                         'ORCA_method'  : None,
                         'ORCA_SCF'     : None,
                         'ORCA_basis'   : None,
                         'ORCA_pal'     : None,
                         'kappa'        : None,
                         'data_path'    : None,
                         'last_step'    : None,
                         'last_frame'   : None,
                         'last_pymol_id': None,
                         'pymol_session': None}

        self.parameters = None
        
        self.types_allowed = {'pdb': True, 'xyz': False, 'mol2': False}

        self.system = None

        self.data_path = data_path

        self.step = 0

        self.job_history = {}
        
        

        self.PyMOL = PyMOL
        self.dualLog = None
        self.builder = builder
        self.window_control = window_control


    def set_AMBER_MM(self, amber_params, amber_coords, dualLog=None):
        self.system = AmberTopologyFile_ToSystem(amber_params, dualLog)
        self.system.coordinates3 = AmberCrdFile_ToCoordinates3(
            amber_coords, dualLog)
        self.settings['force_field'] = "AMBER"
        self.settings['parameters'] = amber_params
        self.settings['coordinates'] = amber_coords
        self.settings['potencial'] = "MM"

    def set_CHARMM_MM(self, charmm_params, charmm_topologies, dualLog=None):

        parameters = CHARMMParameterFiles_ToParameters(
            [(charmm_params)],  dualLog)
        self.system = CHARMMPSFFile_ToSystem(os.path.join(
            charmm_topologies), isXPLOR=True, log=dualLog, parameters=parameters)
        self.settings['force_field'] = "CHARMM"
        self.settings['parameters'] = charmm_params
        self.settings['topology'] = charmm_topologies
        self.settings['potencial'] = "MM"

    def set_GROMACS_MM(self, gromacs_params, gromacs_coords, dualLog=None):

        parameters = GromacsParameters_ToParameters(
            gromacs_params,  log=dualLog)
        self.system = GromacsDefinitions_ToSystem(
            gromacs_params,  log=dualLog, parameters=parameters)
        self.system.coordinates3 = GromacsCrdFile_Process(
            gromacs_coords,  system=self.system,  log=dualLog)

        self.settings['force_field'] = "GROMACS"
        self.settings['potencial'] = "MM"
        self.settings['parameters'] = gromacs_params
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
        self.settings['potencial'] = "MM"
        self.settings['parameters'] = opls_params
        self.settings['coordinates'] = opls_coords
        return self.system

    def Create_New_Project(self, name="UNK",  # str
                           data_path=None,  # str
                           FileType=None,  # str
                           filesin=None,  # dictionary
                           BufferText=None):  # buffertext
        """ Function doc """

        self.name = name

        if data_path is not None:
            self.data_path = data_path

        FileType = FileType
        filesin = filesin

        if FileType == "AMBER":
            amber_params = filesin['amber_params']
            amber_coords = filesin['amber_coords']
            self.set_AMBER_MM(amber_params, amber_coords, self.dualLog)

        elif FileType == "CHARMM":
            charmm_params = filesin['charmm_params']
            charmm_topologies = filesin['charmm_topologies']
            charmm_coords = filesin['charmm_coords']

            self.set_CHARMM_MM(charmm_params, charmm_topologies, self.dualLog)
            filetype = self.load_coordinate_file_to_system(
                charmm_coords, self.dualLog)

        elif FileType == "GROMACS":
            gromacs_params = filesin['gromacs_params']
            gromacs_coords = filesin['gromacs_coords']

            self.set_GROMACS_MM(gromacs_params, gromacs_coords, self.dualLog)

        elif FileType == "OPLS":
            opls_params = filesin['opls_params']
            opls_coords = filesin['opls_coords']
            self.set_OPLS_MM(opls_params, opls_coords, self.dualLog)

        elif FileType == "pDynamo files(*.pkl,*.yaml)":
            NewSystem = filesin["pDynamoFile"]					#
            self.load_coordinate_file_as_new_system(NewSystem, self.dualLog)

        elif FileType == "Other(*.pdb,*.xyz,*.mol2...)":
            NewSystem = filesin["coordinates"]					#
            self.load_coordinate_file_as_new_system(NewSystem, self.dualLog)

        # nbModel applied
        if FileType is not "pDynamo files(*.pkl,*.yaml)":
            self.set_nbModel_to_system()

        
        #self.system.Summary(
        #    log=DualTextLog(self.data_path, str(self.step + 1) + '_' + self.name + ".log"))

        self.From_PDYNAMO_to_GTKDYNAMO(type_='new')

    def SystemCheck(self):
        """ Function doc """
        SummaryFile = "Summary"+'_Step'+str(self.step)+".log"
        self.system.Summary(log=DualTextLog(self.data_path, SummaryFile))
        
        self.parameters = ParseSummaryLogFile(os.path.join(self.data_path, SummaryFile))
        if self.PyMOL == True:
            #print self.parameters
            pass
    
    def Open_GTKDYN_Project():
        '''Function description'''
        self.load_coordinate_file_as_new_system(NewSystem)

        #                parei aqui !!!

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
        self.IncrementStep()

        if self.PyMOL == True:
            pymol_id = ExportFramesToPymol(self, type_)

            # cmd.get_names("selections")+cmd.get_names()
            pymol_objects = cmd.get_names()
            pymol_objects2 = cmd.get_names('selections')

            liststore = self.builder.get_object('liststore1')
            self.window_control.TREEVIEW_ADD_DATA(liststore, pymol_objects2)

            liststore = self.builder.get_object('liststore2')
            self.window_control.TREEVIEW_ADD_DATA2(
                liststore, pymol_objects, pymol_id)

            self.job_history[self.step] = [
                type_, pymol_id, "potencial", "1192.0987"]  # this is only a test

            
            #-------------------------------------#
            #             SystemCheck             #
            #-------------------------------------#           
            
            self.SystemCheck()
            #print self.parameters
            
            #-------------------------------------#
            #               STATUSBAR             #

            StatusText = ''
            if self.parameters is not None:
                StatusText = StatusText + '  Atoms: ' + self.parameters['Number of Atoms'] + "   "
                print self.parameters['Number of Atoms']
                StatusText = StatusText + '  Potencial: ' + self.parameters['Energy Model']+ "   "
                print self.parameters['Energy Model']
                StatusText = StatusText + '  QC Atoms: ' + self.parameters['Number of QC Atoms']+ "   "
                print self.parameters['Number of QC Atoms']
                StatusText = StatusText + '  Fixed Atoms: ' + self.parameters['Number of Fixed Atoms']+ "   "
                print self.parameters['Number of Fixed Atoms']
                StatusText = StatusText + '  Step: ' + str(self.step)+ "   "
                StatusText = StatusText + '  Crystal Class: ' + self.parameters['Crystal Class']+ "   "
                print self.parameters['Crystal Class']
            self.window_control.STATUSBAR_SET_TEXT(StatusText)

        else:
            print 'PyMOL ==',  self.PyMOL

    def load_coordinate_file_as_new_system(self, filename, dualLog=None):
        self.settings['prune_table']=[]
        self.settings['fix_table']  =[]
        self.settings['qc_table']   =[]
        self.settings['QCMM']       ='no'
        type_ = GetFileType(filename)

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

        self.settings['nbModel'] = nbModel

    def put_prune_table(self, prune_table):
        #self.settings['prune_table']=[]
        print 'prune'
        
        self.settings['fix_table']  = []
        self.settings['qc_table']   = []
        self.settings['QCMM']       = 'no'  
        self.system                 = PruneByAtom(self.system, Selection(prune_table))
      
        self.settings['prune_table'].append(prune_table)
        self.From_PDYNAMO_to_GTKDYNAMO(type_='prn')
        print 'pruned'        
        
        
    def put_fix_table(self, fix_table):
        self.system.DefineFixedAtoms(Selection(fix_table))
        self.settings['fix_table'] = fix_table

    def put_qc_table(self, qc_table):
        self.settings['qc_table'] = qc_table
        self.settings['QCMM'] = 'yes'

    # , process = 'Unknow', pymol_id = 'Unknow', potencial = 'Unknow', energy = 'Unknow'):
    def IncrementStep(self):
        # {1:[process, pymol_id, potencial, energy]}
        self.step = self.step + 1
        self.settings['last_step'] = self.step

    def ExportStateToFile(self, filename, type_):

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

    def Minimization(self, method='Conjugate Gradient', parameters=None):
        """ Function doc """

        #                               Minimization                                       #
        #    required: (system = None, _type_ = 'ConjugateGradient', parameters = None)    #
        # _type_  : 'ConjugateGradient' 'SteepestDescent' 'LBFGS'
        # #

        pDynamoMinimization(self.system, method, parameters, self.data_path)

        #------------------  increment step  ---------------#
        #
        self.From_PDYNAMO_to_GTKDYNAMO(type_='min')
        #
        #---------------------------------------------------#

        return True


def main():
    teste = pDynamoProject()
    teste.Minimization()
    return 0


if __name__ == '__main__':
    main()
