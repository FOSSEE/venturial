from bpy.types import Operator
import bpy, bmesh

class VNT_OT_generate_edge(Operator):
    """Generate a curved edge of selected type. This automatically enables the edge visualizer."""
    bl_idname = "vnt.generate_edge"
    bl_description = "Generate an edge of selected type. This automatically enables an edge visualizer."
    bl_label = ""

    def __init__(self):
        self.execution_method = {"ARC": "generate_arc",
                                 "POLYLINE": "generate_polyline",
                                 "SPLINE": "generate_spline",
                                 "BSPLINE": "generate_bspline"}
    
    def generate_arc(self, context, obj):
        bm = bmesh.from_edit_mesh(obj.data)
        sel_edges = [i for i in bm.edges if i.select == True]
        mat = obj.matrix_world
        
        if len(sel_edges) == 1:
            verts = [mat @ v.co for v in sel_edges[0].verts]
            print((verts[0] + verts[1])/2)  
        else:
            self.report({"INFO"}, "Select only a single edge")
       
    def generate_polyline(self, context, obj):
        print("generate polyline")
         
    def generate_spline(self, context, obj):
        print("generate spline")
        
    def generate_bspline(self, context, obj):
        print("generate bspline")
    
    def execute(self, context):
        cs = context.scene
        obj = context.active_object
        
        if obj.mode == 'EDIT':
            getattr(self, self.execution_method[cs.edge_type])(context, obj)
        else:
            self.report({"INFO"}, "Enter Edit Mode")
            
        return {'FINISHED'}
    
    
class VNT_OT_edit_edge(Operator):
    """Edit a curved edge. This automatically enables the edge visualizer."""
    bl_idname = "vnt.edit_edge"
    bl_description = "Edit a curved edge. This automatically enables the edge visualizer."
    bl_label = ""
    
    def execute(self, context):
        return {'FINISHED'}

    
class VNT_OT_destroy_edge(Operator):
    """Removes selected curved edges. This automatically disables the edge visualizer if not already disabled."""
    bl_idname = "vnt.destroy_edge"
    bl_description = "Removes selected curved edges. This automatically disables the edge visualizer if not already disabled."
    bl_label = ""
    
    def execute(self, context):
        
        return {'FINISHED'}