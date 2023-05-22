from bpy.types import Panel
from venturial.utils.interface import layout_control_functions

class recents_menu:
    """tutorial menu layout"""
    
    def layout(self, content, context):
       
        cs = context.scene
        col2row1 = content.split(factor = 0.25, align = True)
        col2c1r1 = col2row1.column(align=True).row(align=True)
        col2c2r1 = col2row1.column(align=True).row(align=True)
        
        col2c1r1.box().label(text="Recents")
        col2c1r1.scale_y = 1.01
        col2c1r1.ui_units_y = 1.4
        
        col2c2r1 = col2c2r1.split(factor = 0.78, align=True)
        s1 = col2c2r1.column(align=True).row(align=True)
        s2 = col2c2r1.column(align=True).split(align=True)
        
        s1.prop(cs, "search_recents", text="", icon = "VIEWZOOM")
        s1.scale_y = 1.45
        s1.ui_units_y = 1.4
        
        s2.popover(VNT_PT_filter_recents.bl_idname, text="", icon="FILTER")
        s2.scale_y = 1.45
        s2.ui_units_y = 1.4
        
        ptr = content.row().box()
        for i in range(0, len(cs.rec_item)):
            col2row2r2c1 = ptr.column().row().box()
            col2row2r2c1.label(text=cs.rec_item[i].REC_name)
            #getattr(layout_control_functions(), "wrapText")(context, cs.rec_item[i], col2row2r2c1)
        #ptr.scale_y = 1.4
        #ptr.template_list("VNT_UL_recents", "", cs, "rec_item", cs, "rec_item_index", rows=2)
        
class VNT_PT_filter_recents(Panel):
    """A pop-up UI panel for filter recents"""
    bl_idname = "VNT_PT_filter_recents"
    bl_label = ""
    bl_space_type =  "VIEW_3D"   
    bl_region_type = "UI"
    bl_options = {'INSTANCED'}

    def draw(self, context):
        layout = self.layout
        cs = context.scene
        
        row = layout.row(align=True)
        row.label(text="tutorial recents")