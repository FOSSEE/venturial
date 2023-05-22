import bpy
from pathlib import Path
from bpy.app.handlers import persistent

@persistent
def add_recents_to_scene(scene):
    #get list of all tutorials in preferred directory
    cs = bpy.context.scene
    recents = [x.name for x in Path(cs.pref_pointer.default_user_data_path).glob('**/*') if x.is_file() and x.suffix == ".json"]
    
    if len(cs.rec_item) == 0:
        for i in range(0, len(recents)):
            item = cs.rec_item.add()
            
            item.REC_name = recents[i]
            item.REC_index = i
    
    bpy.app.handlers.load_factory_startup_post.remove(add_recents_to_scene)