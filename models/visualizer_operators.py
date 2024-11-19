import bpy, bmesh
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
    bl_description = "Toggle to view vertex properties. This also enables X ray view."
    bl_label = ""
    
    quit_modal_x : IntProperty()
    quit_modal_y : IntProperty()
    
    @classmethod
    def poll(cls, context):
        if len(context.selected_objects) == 0: 
            return False
        else:
            return True if context.active_object.type == "MESH" else False
    
    def get_vertex_properties(self, geo):
        vert_prop = {} # Dictionary that contains the properties (index, coordinates) of selected vertices
        
        if geo.mode == "EDIT":
            vertices = bmesh.from_edit_mesh(geo.data).verts
        else:
            vertices = geo.data.vertices
        
        for v in vertices:
            if v.select:
                vert_prop[v.index] = list(np.around(np.array(geo.matrix_world @ v.co), 3))
                # vert_prop[v.index] = list(np.around(np.array(v.co), 3))
        
        return vert_prop
    
    def draw_vertex_properties(self, operator, context, geo):
        cs = context.scene
        for i, j in self.get_vertex_properties(geo).items():
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
            args = (self, context, context.active_object)
            self._handle_2d = bpy.types.SpaceView3D.draw_handler_add(self.draw_vertex_properties, args, 'WINDOW', 'POST_PIXEL')

            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "View3D not found, cannot run operator")
            return {'CANCELLED'}



class VNT_OT_edge_data_control(Operator):
    """Modal Operator to view edge properties of a selected geometry"""
    bl_idname = "vnt.edge_data_control"
    bl_description = "Toggle to view edge properties. This enables the X ray view."
    bl_label = "vnt"
    
    quit_modal_x : IntProperty()
    quit_modal_y : IntProperty()
    
    @classmethod
    def poll(cls, context):
        if len(context.selected_objects) == 0: 
            return False
        else:
            return True if context.active_object.type == "MESH" else False
        
    def draw_line_3d(self, color, start, end):
        bgl.glLineWidth(5)
        self.shader = gpu.shader.from_builtin('3D_UNIFORM_COLOR')
        self.batch = batch_for_shader(self.shader, 'LINES', {"pos": [start, end]})
        self.shader.bind()
        self.shader.uniform_float("color", color)
        self.batch.draw(self.shader)
    
    def get_edge_properties(self, geo):
        
        if geo.mode == "EDIT":
            edges = bmesh.from_edit_mesh(geo.data).edges
        else:
            edges = geo.data.edges
        
        #Shabby code here |. Modify this later 
        #      
        edge_prop = [] # Dictionary that contains the properties (index, coordinates) of selected vertices
        
        for e in edges:
            if e.select:
                v_ = []
                if geo.mode == "EDIT":
                    #v_.append(sum(e.verts))
                    for v in e.verts:
                        v_.append(geo.matrix_world @ v.co)
                        
                    mps = (v_[0]+v_[1])/2
                        
                else:
                    #v_.append(sum(e.vertices))
                    for v in e.vertices:
                        v_.append(geo.matrix_world @ geo.data.vertices[v].co)
                        #v_.append(geo.matrix_world @ v.co)
                        
                    mps = (v_[0]+v_[1])/2
                
                edge_prop.append(mps)
                
        return edge_prop # returns the midpoints of selected edges.
    
    def draw_edge_properties(self, operator, context, geo):
        
        bgl.glEnable(bgl.GL_BLEND)
        bgl.glEnable(bgl.GL_LINE_SMOOTH)
        bgl.glEnable(bgl.GL_DEPTH_TEST)

        for point in self.get_edge_properties(geo):
            self.draw_line_3d((0.0, 1.0, 0.0, 0.7), point, geo.location)
               
        bgl.glDisable(bgl.GL_BLEND)
        bgl.glDisable(bgl.GL_LINE_SMOOTH)
        bgl.glDisable(bgl.GL_DEPTH_TEST)
 
    def modal(self, context, event):                            
        cs = context.scene
        context.area.tag_redraw()
        if cs.enable_edge_vis == False:
            
            # get the mouse coordinates when handler is disabled
            x = event.mouse_x 
            y = event.mouse_y
            
            # re-locate to the same location. This is clearly cheating but works
            # as a triggers the handler removal. ;D
            bpy.context.window.cursor_warp(event.mouse_x, event.mouse_y)

            bpy.types.SpaceView3D.draw_handler_remove(self._handle_3d, 'WINDOW')
            
            return {'CANCELLED'}
        
        else:
            return {'PASS_THROUGH'}

    def invoke(self, context, event):
        
        cs = context.scene
        cs.enable_edge_vis = not cs.enable_edge_vis
        
        if context.area.type == 'VIEW_3D':
    
            args = (self, context, context.active_object)
            self._handle_3d = bpy.types.SpaceView3D.draw_handler_add(self.draw_edge_properties, args, 'WINDOW', 'POST_VIEW')
            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
            
        else:
            self.report({'WARNING'}, "View3D not found, cannot run operator")
            return {'CANCELLED'}
