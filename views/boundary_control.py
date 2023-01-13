from venturial.models.boundary_control_operators import *

class boundary_control:
    def draw(self, ptr, context):
        scn = context.scene
        data = scn.face_name
        
        r0 = ptr.row()
        r0.prop(scn, "face_sel_mode", toggle=True)
        
        r1 = ptr.row()
        
        r1.label(text="Boundary Name:")
        r1.prop(data, "facename")
        
        r2 = ptr.row()
        r2.operator(VNT_OT_set_face_name.bl_idname, text="Set Boundary Name")
        
        r3 = ptr.row()
        r3.label(text="Boundary Condition")
        r3.prop(scn, "bdclist")
        
        r4 = ptr.row()
        r4.operator(VNT_OT_set_type_face.bl_idname, text="Set Boundary Condition")
        
        r4 = ptr.row()
        r4.scale_y = 1.4
        r4.active_default = True
        r4.operator(VNT_OT_faceactions.bl_idname, text="Add Boundary").action = "ADD"
        r4.active_default = False
        
        # new line
        r5 = ptr.row().grid_flow(row_major=True, columns=4, even_columns=False, align = True)
        
        r5.operator(VNT_OT_selectfaces.bl_idname, text="", icon="STICKY_UVS_LOC").select_all = True
        r5.operator(VNT_OT_selectfaces.bl_idname, text="", icon="STICKY_UVS_DISABLE").select_all = False
        r5.operator(VNT_OT_faceactions.bl_idname, text="", icon="REMOVE").action = "REMOVE"
        r5.alert = True
        r5.operator(VNT_OT_clearfaces.bl_idname, text="", icon="TRASH")
        r5.alert = True
        
        #options for remove, delete, select, unselect.        
        