import bpy
import numpy as np
import bgl
import blf
import gpu
from gpu_extras.batch import batch_for_shader
from bpy_extras.view3d_utils import location_3d_to_region_2d
from bpy.types import Operator


def disp_vco_geo(operator, context):
    
    scn = context.scene
    obj = bpy.context.active_object
    
    try:
        if obj.type == "MESH":
            mat = obj.matrix_world
            v3d = context.space_data
            rv3d = v3d.region_3d

            # Vertices from Geometry ----------------------------------------------------------
            verts_geo = []
            vert_ind = []  
            for v in obj.data.vertices:
                if v.select:
                    glob_co = list(mat @ v.co)
                    verts_geo.append([list(np.around(np.array(glob_co), 3)), v.index])
                    vert_ind.append(v.index)

            i = 0
            while i < len(verts_geo):
                pos_text = location_3d_to_region_2d(context.region, rv3d, verts_geo[i][0])
                print(pos_text[0], pos_text[1])
                blf.position(0, pos_text[0], pos_text[1], 0)
                blf.size(0, scn.vert_size, scn.vert_size)
                #print(verts_geo[i][1])
                if scn.en_vert_ic:
                    blf.draw(0, str(verts_geo[i][1]) + ", " + str(verts_geo[i][0]))
                else:
                    blf.draw(0, "uuuu")
                i+=1
    
    except AttributeError:
        pass


class VNT_OT_vertex_data_control(Operator):
    bl_idname = "vnt.vertex_data_blender"
    bl_label = "Simple Modal View3D Operator"

    def modal(self, context, event):
        context.area.tag_redraw()

        if event.type in {'ESC'}:
            bpy.types.SpaceView3D.draw_handler_remove(self._handle_2d, 'WINDOW')
            return {'CANCELLED'}

        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        if context.area.type == 'VIEW_3D':
            args = (self, context)
            self._handle_2d = bpy.types.SpaceView3D.draw_handler_add(disp_vco_geo, args, 'WINDOW', 'POST_PIXEL')

            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "View3D not found, cannot run operator")
            return {'CANCELLED'}
