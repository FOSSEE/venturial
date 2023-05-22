from venturial.models.tutorials_menu_operators import *
from venturial.utils.interface import layout_control_functions
from bpy.types import Panel

class tutorial_menu:
    """tutorial menu layout"""
    
    def layout(self, content, context):
       
        cs = context.scene
        col2row1 = content.split(factor = 0.22, align = True)
        col2c1r1 = col2row1.column(align=True).row(align=True)
        col2c2r1 = col2row1.column(align=True).row(align=True)
        
        col2c1r1.box().label(text="Get Started")
        col2c1r1.scale_y = 1.01
        col2c1r1.ui_units_y = 1.4
        
        col2c2r1 = col2c2r1.split(factor = 0.6, align=True)
        s1 = col2c2r1.column(align=True).row(align=True)
        s2 = col2c2r1.column(align=True).row(align=True)
        
        s1.prop(cs, "search_tuts", text="", icon = "VIEWZOOM")
        s1.scale_y = 1.45
        s1.ui_units_y = 1.4
        
        s2 = s2.split(factor = 0.32, align=True)
        
        s2c1 = s2.column(align=True).split(align=True)
        s2c2 = s2.column(align=True).row(align=True)
        
        s2c1.active_default = True
        s2c1.popover(VNT_PT_filter_tutorials.bl_idname, text="", icon="FILTER")
        s2c1.scale_y = 1.45
        s2c1.ui_units_y = 1.4
        
        s2c2.operator(VNT_OT_more_tutorials_viewer.bl_idname, text="More")
        s2c2.scale_y = 1.45
        s2c2.ui_units_y = 1.4
        
        ptr = content.row().box()
        
        for i in range(0, len(cs.tut_item)):
            
            col2row2r2c1 = ptr.column().row().box()
            getattr(layout_control_functions(), "wrapText")(context, cs.tut_item[i], col2row2r2c1)
            col2row2r2c1.prop(cs.tut_item[i], "TUT_progress", slider = True, text=" ", icon= 'NONE', icon_only=True, expand=True, emboss=True)
            col2row2r2c1.scale_y = 0.475
        
        
class VNT_PT_filter_tutorials(Panel):
    """A pop-up UI panel for filter tutorials"""
    bl_idname = "VNT_PT_filter_tutorials"
    bl_label = ""
    bl_space_type =  "VIEW_3D"   
    bl_region_type = "UI"
    bl_options = {'INSTANCED'}

    def draw(self, context):
        layout = self.layout
        cs = context.scene
        
        row = layout.row(align=True)
        row.label(text="tutorial filters")