from venturial.views.schemas.UIList_schemas import SP_UL_mesh_file_manager
from venturial.models.mesh_file_manager_operators import *

class mesh_file_manager:
    """Mesh manager panel section"""
    
    def draw(self, ptr, context):
        """Method to draw the layout of mesh manager panel section"""
        cs = context.scene
    
        row1 = ptr.row(align=True)
        row1.scale_y = 1.05
            
        row2 = ptr.row(align=False)
        row2.scale_y = 1.35
        row2.active_default = True
        row2.operator(VNT_OT_new_mesh_file.bl_idname, text="New Mesh")
        
        row2 = row2.row()
        row2.active_default = True
        row2.enabled = False
        row2.operator(VNT_OT_build_mesh.bl_idname, text="Build Mesh")
        
        row3 = ptr.row().grid_flow(row_major=True, columns=4, even_columns=False, align = True)
        row3.ui_units_y = 0.55
        row3.operator(VNT_OT_import_mesh.bl_idname, text="", icon="FILEBROWSER")
        row3.operator(VNT_OT_save_mesh.bl_idname, text="", icon="IMPORT")
        row3.operator(VNT_OT_see_older.bl_idname, text="", icon="TIME")
        row3.alert = True
        row3.operator(VNT_OT_delete_mesh_file_items.bl_idname, text="", icon="TRASH")
        row3.alert = True
        
        row4 = ptr.row(align=False)
        row4.scale_y = 1.4
        row4.template_list("SP_UL_mesh_file_manager", "", cs, "mfile_item", cs, "mfile_item_index", rows= 2)
    

        
        
