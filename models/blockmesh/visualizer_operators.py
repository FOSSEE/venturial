import bpy
import numpy as np
import bgl
import blf
import gpu
from gpu_extras.batch import batch_for_shader
from bpy_extras.view3d_utils import location_3d_to_region_2d
from bpy.types import Operator
from bpy.props import BoolProperty, IntProperty

class VNT_OT_vertex_data_control(Operator):
    """Modal Operator to view vertex properties of a selected geometry"""
    bl_idname = "vnt.vertex_data_control"
    bl_description = "Toggle to view vertex properties"
    bl_label = ""
    
    quit_modal_x : IntProperty()
    quit_modal_y : IntProperty()
    
    def get_vertex_properties(self, geo):
        vert_prop = {}
        
        for v in geo.data.vertices:
            if v.select:
                vert_prop[v.index] = list(np.around(np.array(geo.matrix_world @ v.co), 3))
                
        return vert_prop
        
    def draw_vertex_properties(self, operator, context):
        cs = context.scene
        for i, j in self.get_vertex_properties(bpy.context.active_object).items():
            text_pos = location_3d_to_region_2d(context.region, context.space_data.region_3d, j)
            
            blf.position(0, text_pos[0], text_pos[1], 0)
            blf.size(0, cs.vert_text_size, cs.vert_text_size)
            
            blf.color(0, cs.vert_text_color[0], cs.vert_text_color[1], cs.vert_text_color[2], cs.vert_text_color[3])
            
            #Shabby code here |. Modify this later 
            #                 V
            if cs.vert_props == {"Indices"}:
                x = str(i)
                
            elif cs.vert_props == {"Coordinates"}:
                x = "(" + ",".join(str(m) for m in j) + ")"
                
            elif cs.vert_props == {"Indices", "Coordinates"}:
                x = str(i) + " " + "(" + ",".join(str(m) for m in j) + ")"
                
            else: 
                x = ""
                               
            blf.draw(0, x)
 
    def modal(self, context, event):
        cs = context.scene
        context.area.tag_redraw()
        if cs.enable_vert_vis == False:
            
            # get the mouse coordinates when handler is disabled
            x = event.mouse_x 
            y = event.mouse_y
            
            # re-locate to the same location. This is clearly cheating but works
            # as a triggers the handler removal. ;D
            bpy.context.window.cursor_warp(event.mouse_x, event.mouse_y)

            bpy.types.SpaceView3D.draw_handler_remove(self._handle_2d, 'WINDOW')
            
            return {'CANCELLED'}
        
        else:
            return {'PASS_THROUGH'}

    def invoke(self, context, event):
        cs = context.scene
        cs.enable_vert_vis = not cs.enable_vert_vis
        
        if context.area.type == 'VIEW_3D':
            args = (self, context)
            self._handle_2d = bpy.types.SpaceView3D.draw_handler_add(self.draw_vertex_properties, args, 'WINDOW', 'POST_PIXEL')

            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "View3D not found, cannot run operator")
            return {'CANCELLED'}
