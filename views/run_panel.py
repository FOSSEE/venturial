from venturial.models.run_panel_operators import *
    
class run_panel:
 
    def draw(self, ptr, context):
        scn = context.scene
        
        sec1 = ptr.row(align=True)
        sec1.scale_y = 1.4
        sec1.ui_units_y = 2.0
        sec1.prop(scn, "geo_design_options", expand=True)
        
        row = ptr.row()
        row.active_default = True
        row.operator(VNT_OT_fill_dict_file.bl_idname, icon="FILE_TICK", text="Generate Blockmesh Dictionary")
        
        row.active_default = False
        row.alert = True
        row.operator(VNT_OT_cleardictfileonly.bl_idname, icon="TRASH", text="Clear Blockmesh Dictionary")
        row.ui_units_y = 1.7