import json 
import os
    
def Save_GTKDYNAMO_ConfigFile (home, GTKDynamoConfig):
    """ Function doc """
    path = os.path.join(home,'.config')
    if not os.path.exists (path): 
        os.mkdir (path)

    path = os.path.join(path, 'GTKDynamo')
    if not os.path.exists (path): 
        os.mkdir (path)
    
    filename = os.path.join(path,'gtkdynamo.config')
    json.dump(GTKDynamoConfig, open(filename, 'w'), indent=2)
    


def Load_GTKDYNAMO_ConfigFile (home, GTKDynamoConfig):
    """ Function doc """
    #.config
    path = os.path.join(home,'.config', 'GTKDynamo', 'gtkdynamo.config')
    
    try:
        GTKDynamoConfig = json.load(open(path)) 
    except:
        print 'error: GTKDynamo config file not found'
        print 'open WorkSpace Dialog'
