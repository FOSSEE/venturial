import bpy, bmesh

def update_mesh_dict_names(self, context):
    context.scene.bm_dict_name = 'blockMeshDict' if 'BlockMesh' in self.prompt_meshing_tool else ''
    context.scene.shm_dict_name = 'snappyHexMeshDict' if 'SnappyHexMesh' in self.prompt_meshing_tool else ''

def update_snapping(self, context):
    bpy.context.scene.tool_settings.use_snap = context.scene.snapping
    if context.scene.snapping == True:
        bpy.context.scene.tool_settings.snap_elements = {context.scene.snapping_methods}
        
def update_snapping_method(self, context):
    bpy.context.scene.tool_settings.snap_elements = {context.scene.snapping_methods}
    
def update_cellxyz(self, context):
    
    scn = context.scene
    for i in range(0, len(scn.bcustom)):
        if scn.bcustom[i].enabled:
            scn.bcustom[i].setcellx = self.cell_x
            scn.bcustom[i].setcelly = self.cell_y
            scn.bcustom[i].setcellz = self.cell_z
            

def update_mode(self, context):
    bpy.ops.object.mode_set(mode = 'EDIT' if self.mode != 'OBJECT' else self.mode)
    if self.mode != 'OBJECT': bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type=self.mode, action='TOGGLE')
       
def update_face_mode(self, context):
    if self.face_sel_mode == True:
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE', action='TOGGLE')
        obj = context.edit_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        
        for f in bm.faces:
            f.select = False
        bm.select_flush_mode()   
        me.update()
        
    else:
        bpy.ops.object.mode_set(mode = 'OBJECT')
        

def update_uicategory_mode(self, context):
    context.scene.meshing_tool = context.scene.mfile_item[self.mfile_item_index].ITEM_type
    
def update_current_tool_text_1(self, context):
    context.scene.current_tool_text = context.scene.meshing_tool
    
def update_current_tool_text_2(self, context):
    context.scene.current_tool_text = context.scene.solution_tools

def get_active_projects(self, context):
    
    cs = context.scene
    
    if len(cs.mfile_item) == 0:
        items = [("", "", "")]
    else:
        items = []
        for i in cs.mfile_item:
            element = (str(i.ITEM_identifier), i.ITEM_name, "")
            items.append(element)

    return items