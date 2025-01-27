from bpy.types import Operator
from bpy.props import BoolProperty, EnumProperty

class SelectUnselectEdges(Operator):
    bl_label = "Select or Unselect Edges from list"
    bl_idname = "custom.select_unselect_alledges"
    bl_options = {'REGISTER','UNDO'}
    
    select_all : BoolProperty()
    # Add Confirmation Prompt Dialog Box
    def execute(self, context):
        pass
        return {'FINISHED'}

class ClearAllEdges(Operator):
    bl_label = "Clear All Edge Types from List"
    bl_idname = "custom.clear_all_edges"
    bl_options = {'REGISTER','UNDO'}
    
    # Add Confirmation Prompt Dialog Box
    def execute(self, context):
        pass
        return {'FINISHED'}


class edgeactions(Operator):
    bl_idname = "custom.arc_action"
    bl_label = ""
    bl_description = "Add/Remove arc or Move arc Up/Down"
    bl_options = {'REGISTER'}

    action: EnumProperty(items=(('REMOVE', "Remove", ""),
                                          ('ADD', "Add", "")))

    def invoke(self, context, event):
        scn = context.scene
        obj = context.active_object
        idx = scn.acustom_index
        try:
            item = scn.acustom[idx]
        except IndexError:
            pass
        
        idx = scn.pcustom_index    
        try:
            item = scn.pcustom[idx]
        except IndexError:
            pass
            
        idx = scn.scustom_index
        try:
            item = scn.scustom[idx]
        except IndexError:
            pass
        
        idx = scn.bscustom_index
        try:
            item = scn.bscustom[idx]
        except IndexError:
            pass
            
        if self.action == 'REMOVE':
            
            if scn.edgelist == 'arc':
                info = '"%s" removed from list' % (scn.acustom[idx].fandl)
                scn.acustom_index -= 1
                scn.acustom.remove(idx)
                self.report({'INFO'}, info)
                
            if scn.edgelist == 'polyLine':
                info = 'Item "%s" removed from list' % (scn.pcustom[idx].name)
                scn.pcustom_index -= 1
                scn.pcustom.remove(idx)
                self.report({'INFO'}, info)
                
            if scn.edgelist == 'spline':
                info = 'Item "%s" removed from list' % (scn.scustom[idx].name)
                scn.scustom_index -= 1
                scn.scustom.remove(idx)
                self.report({'INFO'}, info)
                
            if scn.edgelist == 'BSpline':
                info = 'Item "%s" removed from list' % (scn.bscustom[idx].name)
                scn.bscustom_index -= 1
                scn.bscustom.remove(idx)
                self.report({'INFO'}, info)

        if self.action == 'ADD':
                
            if obj:
                    
                if objname_checker(obj.name):
                        
                    if obj.mode == 'EDIT':
                        bm = bmesh.from_edit_mesh(obj.data)
                        sel_vert = [elem.index for elem in bm.select_history if isinstance(elem, bmesh.types.BMVert)]
            
                        if len(sel_vert) == 2:
                            if scn.edgelist == 'arc':
                                item = scn.acustom.add()
                                item.fandl = "arc " + str(sel_vert[0]) + " " + str(sel_vert[1])
                                scn.acustom_index = len(scn.acustom)-1
                                self.report({'INFO'}, "Vertices Added. Set Interpolation Point.")
                            
                            if scn.edgelist == 'polyLine':
                                for i in range(0, scn.ipcnt):
                                    item = scn.pcustom.add()
                                    item.fandl = "polyLine " + str(sel_vert[0]) + " " + str(sel_vert[1])
                                    scn.pcustom_index = len(scn.pcustom)-1
                                    self.report({'INFO'}, "Vertices Added. Set Interpolation Point.")
                                        
                            if scn.edgelist == 'spline':
                                for i in range(0, scn.ipcnt):
                                    item = scn.scustom.add()
                                    item.fandl = "spline " + str(sel_vert[0]) + " " + str(sel_vert[1])
                                    scn.scustom_index = len(scn.scustom)-1
                                    self.report({'INFO'}, "Vertices Added. Set Interpolation Point.")
                            
                            if scn.edgelist == 'BSpline':
                                for i in range(0, scn.ipcnt):
                                    item = scn.bscustom.add()
                                    item.fandl = "BSpline " + str(sel_vert[0]) + " " + str(sel_vert[1])
                                    scn.bscustom_index = len(scn.bscustom)-1
                                    self.report({'INFO'}, "Vertices Added. Set Interpolation Point.")
                                    
                        else:
                            self.report({'INFO'}, "Select  Only 2 Vertices")
                        
                    else:        
                        self.report({'INFO'}, "Enter Edit Mode")
                    
                else:
                    self.report({'INFO'}, "Add Block from GUI/Enter Name Properly")
                
            else:
                self.report({'INFO'}, "Select a Block/Geometry.")
                    
        return {"FINISHED"}

class show_curvededge(Operator):
    bl_idname = "show.curved_edge"
    bl_label = "Select Item(s) in Viewport"
    bl_description = "Show Selected Edge in Viewport"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        scn = context.scene
        if scn.edgelist == "arc":
            return bool(context.scene.acustom)
        
        if scn.edgelist == "polyLine":
            return bool(context.scene.pcustom)
        
        if scn.edgelist == "spline":
            return bool(context.scene.scustom)
        
        if scn.edgelist == "BSpline":
            return bool(context.scene.bscustom)

    def execute(self, context):
        scn = context.scene
        obj = bpy.context.active_object
        bm = bmesh.from_edit_mesh(obj.data)
        
        if scn.edgelist == "arc":
            for i in range(0, len(scn.acustom)):
                if scn.acustom[i].enabled:
                    CE_verts = []
                    edgedata = scn.acustom[i].fandl                            
                    CE_verts = [int(s) for s in edgedata.split() if s.isdigit()]
                    for v in bm.verts:
                        if v.index in (CE_verts):
                            v.select = True
                            bmesh.update_edit_mesh(obj.data)   
                            
        if scn.edgelist == "polyLine":
            for i in range(0, len(scn.pcustom)):
                if scn.pcustom[i].enabled:
                    CE_verts = []
                    edgedata = scn.pcustom[i].fandl                            
                    CE_verts = [int(s) for s in edgedata.split() if s.isdigit()]
                    for v in bm.verts:
                        if v.index in (CE_verts):
                            v.select = True
                            bmesh.update_edit_mesh(obj.data)
                    
        if scn.edgelist == "spline":
            for i in range(0, len(scn.scustom)):
                if scn.scustom[i].enabled:
                    CE_verts = []
                    edgedata = scn.scustom[i].fandl                            
                    CE_verts = [int(s) for s in edgedata.split() if s.isdigit()]
                    for v in bm.verts:
                        if v.index in (CE_verts):
                            v.select = True
                            bmesh.update_edit_mesh(obj.data)
        
        if scn.edgelist == "BSpline":
            for i in range(0, len(scn.bscustom)):
                if scn.bscustom[i].enabled:
                    CE_verts = []
                    edgedata = scn.bscustom[i].fandl                            
                    CE_verts = [int(s) for s in edgedata.split() if s.isdigit()]
                    for v in bm.verts:
                        if v.index in (CE_verts):
                            v.select = True
                            bmesh.update_edit_mesh(obj.data)  

        return{'FINISHED'}
    
    
class clear_currentedge(Operator):
    """Clear all items of the list"""
    bl_idname = "clear.current_edge"
    bl_label = "Clear Current Selected Edges"
    bl_description = "Clear All Edges from Current Edge List"
    bl_options = {'INTERNAL'}

    @classmethod
    def poll(cls, context):
        scn = context.scene
      
        if scn.edgelist == "arc":
            return bool(context.scene.acustom)
        
        if scn.edgelist == "polyLine":
            return bool(context.scene.pcustom)
        
        if scn.edgelist == "spline":
            return bool(context.scene.scustom)
        
        if scn.edgelist == "BSpline":
            return bool(context.scene.bscustom)

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        scn = context.scene
        if scn.edgelist == "arc":
            context.scene.acustom.clear()
            self.report({'INFO'}, "All arc edges removed.")
            
        if scn.edgelist == "polyLine":
            context.scene.pcustom.clear()
            self.report({'INFO'}, "All polyLine edges removed.")
            
        if scn.edgelist == "spline":
            context.scene.scustom.clear()
            self.report({'INFO'}, "All spline edges removed.")
            
        if scn.edgelist == "BSpline":
            context.scene.bscustom.clear()
            self.report({'INFO'}, "All BSpline edges removed.")
            
        return{'FINISHED'}
