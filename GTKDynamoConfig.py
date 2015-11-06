import json 
import os
    
def Save_EasyHybrid_ConfigFile (home, EasyHybridConfig):
    """ Function doc """
    path = os.path.join(home,'.config')
    if not os.path.exists (path): 
        os.mkdir (path)

    path = os.path.join(path, 'EasyHybrid')
    if not os.path.exists (path): 
        os.mkdir (path)
    
    filename = os.path.join(path,'EasyHybrid.config')
    json.dump(EasyHybridConfig, open(filename, 'w'), indent=2)
    


def Load_EasyHybrid_ConfigFile (home, EasyHybridConfig):
    """ Function doc """
    #.config
    path = os.path.join(home,'.config', 'EasyHybrid', 'EasyHybrid.config')
    
    try:
        EasyHybridConfig = json.load(open(path)) 
    except:
        print 'error: EasyHybrid config file not found'
        print 'open WorkSpace Dialog'
