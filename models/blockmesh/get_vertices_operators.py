from bpy.types import Operator
from bpy.props import BoolProperty, EnumProperty
import bpy, bmesh

class VNT_OT_vertactions(Operator):
    bl_idname = "custom.vert_action"
    bl_label = ""
    bl_description = "Add/Remove Vertices or Move Vertices Up/Down"
    bl_options = {'REGISTER'}

    action: EnumProperty(items=(('REMOVE', "Remove", ""),
                                ('ADD', "Add", "")))

    @classmethod
    def poll(self, context):
        return bool(context.scene.simblk)

    def execute(self, context):
        scn = context.scene
        
        idx = scn.vcustom_index

        try:
            item = scn.vcustom[idx]
        except IndexError:
            pass
        
        else:
            if self.action == 'REMOVE':
                
                selverts = []
                for i in range(0, len(scn.vcustom)):
                    if scn.vcustom[i].enabled == True:
                        selverts.append(scn.vcustom[i].vertindex)
                
                for i in selverts:
                    l = len(scn.vcustom)
                    
                    for j in range(0, l):
                        if scn.vcustom[j].vertindex == i: 
                             
                            scn.vcustom_index = j
                            scn.vcustom.remove(j)
                            break 
                    scn.vcustom_index = 0
                        
                info = "Vertices with Indices:" + str(selverts) + "removed from Vertex List"
                self.report({'INFO'}, info)

        if self.action == 'ADD':

            obj = bpy.context.object
            
            if obj:
                mat = obj.matrix_world
                vert_list = []
                
                if obj.mode == 'EDIT':
                    
                    
                    bm=bmesh.from_edit_mesh(obj.data)
                    manual_vcoi = [[list(mat @ v.co), str(v.index)] for v in bm.select_history if isinstance(v, bmesh.types.BMVert)]
                    
                    print(manual_vcoi)
                    for i in manual_vcoiself.report():
                        item = scn.vcustom.add()
                        item.name = str(tuple(list(np.around(np.array(i[0]), 2))))
                        item.vertindex = i[1]
                        scn.vcustom_index = len(scn.vcustom)-1
                        info = '"%s" added to list' % (item.name)
                        self.report({'INFO'}, info)
                                   
                else:
                    self.report({'INFO'}, "Enter Edit Mode")
                    
            else:
                self.report({'INFO'}, "Select Block/Geometry")
            
        return {"FINISHED"}


class VNT_OT_add_update_verts(Operator):
    """Print all items and their properties to the console"""
    bl_idname = "custom.add_update_verts"
    bl_label = "Get Vertices"
    bl_description = "Add/Update vertices of selected Geometry"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(self, context):
        return bool(context.scene.simblk)

    def execute(self, context):
        scn = context.scene

        obj = bpy.context.object
            
        if obj:
            mat = obj.matrix_world
            vert_list = []
            bpy.ops.object.mode_set(mode='EDIT')
            bm=bmesh.from_edit_mesh(obj.data)
            
            if obj.mode == 'EDIT':
                           
                if len(scn.vcustom) > 0:
                    
                    context.scene.vcustom.clear()
                    for v in bm.verts:
                        r = []
                        g = list(mat @ v.co)
                            
                        for i in g:
                            r.append(str(round(i, 3)))
                                
                        m = "(" + r[0] + ", " + r[1] + ", " + r[2] + ")"
                        n = str(v.index)
                        vert_list.append([m, n])
                            
                    for i in vert_list:
                        item = scn.vcustom.add()
                        item.name = i[0]
                        item.vertindex = i[1]
                        scn.vcustom_index = len(scn.vcustom)-1
                        info = '"%s" added to list' % (item.name)
                        self.report({'INFO'}, info)
                    
                    bpy.ops.object.mode_set(mode='OBJECT')
                    
                else:
                    
                    for v in bm.verts:
                        r = []
                        g = list(mat @ v.co)
                            
                        for i in g:
                            r.append(str(round(i, 2)))
                                
                        m = "(" + r[0] + ", " + r[1] + ", " + r[2] + ")"
                        n = str(v.index)
                        vert_list.append([m, n])
                            
                    for i in vert_list:
                        item = scn.vcustom.add()
                        item.name = i[0]
                        item.vertindex = i[1]
                        scn.vcustom_index = len(scn.vcustom)-1
                        info = '"%s" added to list' % (item.name)
                        self.report({'INFO'}, info)
                    
                    bpy.ops.object.mode_set(mode='OBJECT')
                                 
            else:
                self.report({'INFO'}, "Enter Edit Mode")           
        else:
            self.report({'INFO'}, "Select Block/Geometry")
            
        return{'FINISHED'}
    

class VNT_OT_select_unselect_allverts(Operator):
    """Select Items in the Viewport"""
    bl_idname = "custom.select_unselect_allverts"
    bl_label = ""
    bl_description = "Show Selected Vertices in Viewport"
    bl_options = {'REGISTER', 'UNDO'}

    select_all: BoolProperty(
        default=False,
        name="Select all Items of List",
        options={'SKIP_SAVE'})

    @classmethod
    def poll(cls, context):
        return bool(context.scene.vcustom)

    def execute(self, context):
        scn = context.scene
        
        if self.select_all:
                        
            for i in range(0, len(scn.vcustom)):
                scn.vcustom[i].enabled = True
        
        else:
            for i in range(0, len(scn.vcustom)):
                scn.vcustom[i].enabled = False
              
        return{'FINISHED'}


class VNT_OT_clearverts(Operator):
    bl_idname = "custom.clear_verts"
    bl_label = "Remove all vertex data"
    bl_description = "Clear all Vertices of the List"
    bl_options = {'INTERNAL'}

    @classmethod
    def poll(cls, context):
        return bool(context.scene.vcustom)

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        if bool(context.scene.vcustom):
            context.scene.vcustom.clear()
            self.report({'INFO'}, "All items removed")
        else:
            self.report({'INFO'}, "Nothing to remove")
        return{'FINISHED'}