import json
from pathlib import Path

def add_tutorials_to_scene():
    #get list of all tutorials in preferred directory
    
    tutorials = [x for x in Path("/home/rajdeepadak/.config/blender/3.2/scripts/addons/venturial/tutorials").glob('**/*') if x.is_file() and x.suffix == ".json"]
    #print(tutorials)
    
    
    for i in tutorials:
        with open(i, 'r') as inp: 
            tut_dict = json.load(inp)
            print(tut_dict['name'])

add_tutorials_to_scene()