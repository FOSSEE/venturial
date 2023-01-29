from venturial.views.header.view import (VNT_MT_file_menu, 
                                         VNT_PT_uicategory, 
                                         VNT_MT_about_venturial,
                                         VNT_MT_about_fossee,
                                         VNT_MT_help_menu)

from venturial.models.header.general_operators import VNT_OT_close_venturial
from venturial.utils.custom_icon_object_generator import *


class header_layout:
    """Class that consists of methods to define venturial's header layout"""
    
    def draw(self, layout, context):
        cs = context.scene
        row = layout.row(align = True) 
        row.menu(VNT_MT_file_menu.bl_idname, text="File")
        
        row = layout.row(align = True)
        row.popover(VNT_PT_uicategory.bl_idname, text=cs.ui_category) 
        
        row = layout.row()        
        row.prop(cs, "mode", icon_only=True, expand = True)
        row = layout.row()
        
        x = context.region.width
        scale_left = 0.00380986745213549*x - 1.2709867452135493 #if cs.category_expand == True else 0.0049986745213549*x - 1.2709867452135493
        
        row.scale_x = scale_left 
        row.label(icon='BLANK1')

        layout.menu(VNT_MT_about_venturial.bl_idname, text="  Venturial  ", icon_value=custom_icons["venturial_logo"]["venturial_logo"].icon_id)
        
        row = layout.row(align=True)
        scale_right = 0.0039970986745213549*x - 0.83 #if cs.category_expand == True else 0.00397986745213549*x - 0.83
        row.scale_x = scale_right
        row.label(icon='BLANK1')
        
        layout.menu(VNT_MT_about_fossee.bl_idname, text="  FOSSEE  ", icon_value=custom_icons["fossee_logo"]["fossee_logo"].icon_id)    
        
        layout.menu(VNT_MT_help_menu.bl_idname, text="  Help  ", icon="QUESTION")
       
        layout.alert = True
        layout.operator(VNT_OT_close_venturial.bl_idname, text="", icon="PANEL_CLOSE")
        layout.alert = False