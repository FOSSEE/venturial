# Not included in init.py

from venturial.models.geometry_designer_operators import *
        
class geometry_designer:
    """Geometry Designer panel section for meshing"""
    
    def draw(self, ptr, context):
        """Method to define layout of geometry design panel section"""
        
        cs = context.scene
        
        sec1 = ptr.row(align=True)
        sec1.scale_y = 1.3
        sec1.ui_units_y = 1.125
        sec1.prop(cs, "geo_design_options", expand=True)
        
        sec2 = ptr.row().box()
        row1 = sec2.row(align=True)
        row1.scale_y = 0.75
        row1.separator()
        
        row2 = sec2.row()
        row2.label(text="Cell Shape:")
        row2.prop(cs, "cellShape_units", text="", slider=True)
        row2.prop(cs, "cellShapes", text="")
        row2.operator(VNT_OT_add_to_viewport.bl_idname, text="Add to Viewport")
        
        row3 = sec2.row()
        split = row3.split()
        r3col1 = split.column().row()
        r3col2 = split.column().row()
        r3col2.prop(cs, "ctm", slider=True)
        
        row4 = sec2.row()
        split = row4.split(factor = 0.24)
        
        r4c1 = split.row()
        r4c2 = split.row()
        
        r4c1.prop(cs, "transform", text="Transform")
        
        r4c2.enabled = cs.transform
        r4c2.prop(cs, "transformation_methods", expand=True)
        
        row5 = sec2.row()
        split = row5.split(factor = 0.24)
        
        r5c1 = split.row()
        r5c2 = split.row()
        
        r5c1.prop(cs, "snapping", text="Snapping")
        
        r5c2.enabled = cs.snapping
        r5c2.prop(cs, "snapping_methods", expand=True)
        
        row6 = sec2.row(align=True)
        row6.label(text = "Set Cells:")
        row6.prop(cs, "cell_x", toggle=True)
        row6.prop(cs, "cell_y", toggle=True)
        row6.prop(cs, "cell_z", toggle=True)
        row6.ui_units_y = 1.05
        
        row7 = sec2.row()
        row7.scale_y = 1.3
        
        row7spt = row7.split()
        #row7.ui_units_y = 0.85
        row7a = row7spt.column().row()
        row7b = row7spt.column(align=True).split(align=True)
        
        row7a.active_default = True
        row7a.operator(VNT_OT_compose.bl_idname, text="Compose")
        row7a.operator(VNT_OT_get_blocks.bl_idname, text="Get Blocks")
        row7a.active_default = False
        
        row7bspt = row7b.split(factor = 0.15)
        
        row7ba = row7bspt.row()
        row7ba.operator(VNT_OT_blocksdatacontrol.bl_idname, icon="ADD", text="").action = 'ADD'
        
        row7bb = row7bspt.row()
        
        row7bb.operator(VNT_OT_blocksdatacontrol.bl_idname, icon="REMOVE", text="").action = 'REMOVE'
        row7bb.operator(VNT_OT_showselectedblocks.bl_idname, icon="STICKY_UVS_DISABLE", text="")
        row7bb.operator(VNT_OT_select_unselect_allblocks.bl_idname, icon="STICKY_UVS_LOC", text="")
        
        row7bb.alert = True
        row7bb.operator(VNT_OT_remove_blocks.bl_idname, icon="CANCEL", text="")
        row7bb.operator(VNT_OT_remove_all_blocks.bl_idname, icon="TRASH", text="")
        row7bb.operator(VNT_OT_clearblocks.bl_idname, icon="TRASH", text="")
        
        
class geometry_designer_blocks:
    """Geometry Designer panel section for meshing"""
    
    def draw(self, ptr, context):
        """Method to define layout of geometry design panel section"""
        cs = context.scene
        ptr = ptr.row()
        ptr.scale_y = 1.4
        ptr.template_list("CUSTOM_UL_blocks", "", cs, "bcustom", cs, "bcustom_index", rows=2)
         