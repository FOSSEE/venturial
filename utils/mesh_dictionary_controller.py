import bpy, json

class mesh_dictionary_controller:
    def dict_initiate(self, optr, context):
        
        scn = context.scene
        bmdict={'convertToMeters':[],
                'vertices':[],
                'blocks':[],
                'edges':[],
                'boundary':[],
                'mergePatchPairs':[]}
        
        m = json.dumps(bmdict, sort_keys=True, indent=2)
        f = context.scene.mfile_item[context.scene.mfile_item_index].ITEM_name
        
        try:
            text_block = bpy.data.texts[f + '.json']
            optr.report({'INFO'},"DICTIONARY PRESENT,RESETTING VALUES")    
        
        except KeyError:
            text_block = bpy.data.texts.new(f + '.json') 
            optr.report({'INFO'},"DICTIONARY INITIALIZED")     
        text_block.from_string(m)
        
        
    def dict_update():
        pass