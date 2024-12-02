import bpy, json
from pathlib import Path
from bpy.app.handlers import persistent

@persistent
def add_tutorials_to_scene(scene):
    #get list of all tutorials in preferred directory
    cs = bpy.context.scene
    tutorials = [x for x in Path(cs.pref_pointer.default_tutorials_dir).glob('**/*') if x.is_file() and x.suffix == ".json"]
    #print(tutorials)
    
    if len(cs.tut_item) == 0:
        for i in range(0, len(tutorials)):
            with open(tutorials[i], 'r') as inp: 
                tut_dict = json.load(inp)
                #print(tut_dict['name'])
                item = cs.tut_item.add()
            
                item.TUT_name = tut_dict['name']
                item.TUT_index = i    
    
    #bpy.app.handlers.load_factory_startup_post.remove(add_tutorials_to_scene)