from bpy.types import Panel, Menu
import bpy, os, json 

from venturial.models.help_menu_operators import *
from venturial.models.developer_menu_operators import *
from venturial.models.header_operators import *
from venturial.views.geometry_designer import *
from venturial.views.mesh_file_manager import *
from venturial.views.get_vertices import *
from venturial.views.get_boundaries import *
from venturial.views.boundary_control import *
from venturial.views.edges_panel import *
from venturial.views.run_panel import *

banner = {}

def register_venturial_logo():
    img = bpy.utils.previews.new()
    img_path = bpy.utils.script_paths(subdir='addons')[1]+"/venturial/icons/custom_icons/venturial_logo.png"
    img.load("venturial_logo", img_path, 'IMAGE')
    banner["main"] = img
    
def unregister_venturial_logo():
    for img in banner.values():
        bpy.utils.previews.remove(img)
    banner.clear()


fossee = {}

def register_fossee_logo():
    img = bpy.utils.previews.new()
    img_path = bpy.utils.script_paths(subdir='addons')[1]+"/venturial/icons/custom_icons/fossee_logo.png"
    img.load("fossee_logo", img_path, 'IMAGE')
    fossee["main"] = img

def unregister_fossee_logo():
    for img in fossee.values():
        bpy.utils.previews.remove(img)
    fossee.clear()


class AboutVenturial(Menu):
    """Pop-up for Venturial Intro"""
    bl_label = "Venturial" 
    bl_idname = "VNT_MT_about_venturial"
    bl_description = "Show Venturial intro"
    
    def draw(self, context):
        layout = self.layout
    
        row1 = layout.row()
        banner_obj = banner["main"]
        row1.template_icon(icon_value=banner_obj["venturial_logo"].icon_id, scale=12)
        
        row2 = layout.row()
        row2.label(text="Venturial: A GUI for OpenFOAM.")
        
        row3 = layout.row()
        row3.operator(VNT_OT_venturial_homepage.bl_idname, text="Open Venturial's Homepage", icon="URL")
        
    def execute(self, context):     
        return {'FINISHED'}
        
    def invoke(self, context, event):
        return context.window_manager.invoke_popup(self, width=380)


class HelpMenu(Menu):
    """Display help options."""
    bl_idname = "VNT_MT_helpmenu"
    bl_label = ""

    def draw(self, context):
        layout = self.layout

        layout.operator(VNT_OT_user_guide.bl_idname, text = "User Guide", icon="USER")
        layout.operator(VNT_OT_developer_guide.bl_idname, text = "Developer Guide", icon="CONSOLE")
        layout.separator()
        layout.operator(VNT_OT_feature_request.bl_idname, text = "Feature Request", icon = "FILE_CACHE")
        layout.operator(VNT_OT_report_bugs.bl_idname, text = "Report Bugs", icon="GHOST_DISABLED")
        layout.operator(VNT_OT_developer_support.bl_idname, text = "Developer Support", icon="WORLD")
        layout.separator()
        layout.operator(VNT_OT_user_community.bl_idname, text = "User Community", icon="COMMUNITY")
        layout.operator(VNT_OT_developer_community.bl_idname, text = "Developer Community", icon = "COMMUNITY")
        layout.separator()
        layout.operator(VNT_OT_release_notes.bl_idname, text = "Release Notes", icon="MENU_PANEL")
        
class DevMenu(Menu):
    """Display developer options."""
    bl_idname = "VNT_MT_devmenu"
    bl_label = ""

    def draw(self, context):
        layout = self.layout
        layout.operator(VNT_OT_dev_tools.bl_idname, text = "Developer Settings", icon="OPTIONS")
        layout.operator(VNT_OT_dev_mode.bl_idname, text= "Developer Mode", icon="LOCKED")


class AboutFossee(Menu):
    """Pop-up for FOSSEE Intro"""
    bl_label = "FOSSEE" 
    bl_idname = "VNT_MT_about_fossee"
    bl_description = "Show FOSSEE intro"
    
    def draw(self, context):
        layout = self.layout
    
        row1 = layout.row()
        fossee_obj = fossee["main"]
        row1.template_icon(icon_value=fossee_obj["fossee_logo"].icon_id, scale=15)
        
        row2 = layout.row()
        row2.label(text="FOSSEE: Free/Libre Open-Source Software for Education.")
        
        row3 = layout.row()
        row3.operator(VNT_OT_fossee_homepage.bl_idname, text="Open FOSSEE Homepage", icon="URL")
        
    def execute(self, context):     
        return {'FINISHED'}
        
    def invoke(self, context, event):
        return context.window_manager.invoke_popup(self, width=380)
    

class UserModeView(Panel):
    """Main Panel Layout of User Mode"""
    bl_idname = "VNT_PT_usermodeview"
    bl_label = ""
    bl_space_type =  "VIEW_3D"   
    bl_region_type = "UI"
    bl_category = "Venturial"
    
    def draw_header(self, context):
        layout = self.layout   
        cs = context.scene
             
        row = layout.row(align = True)  
        row.prop(cs, "category", text=None if cs.category_expand == True else "", expand = cs.category_expand, emboss = True)
        row.prop(cs, "category_expand", text = "", icon = "FRAME_PREV" if cs.category_expand == True else "FRAME_NEXT")
        row.operator(VNT_OT_user_general_settings.bl_idname, text = "", icon="PREFERENCES")
         
        row = layout.row()
        
        x = context.region.width
        scale_left = 0.00380986745213549*x - 1.2709867452135493 if cs.category_expand == True else 0.0049986745213549*x - 1.2709867452135493
        
        row.scale_x = scale_left 
        row.label(icon='BLANK1')

        banner_obj = banner["main"]
        layout.menu(AboutVenturial.bl_idname, text="  Venturial  ", icon_value=banner_obj["venturial_logo"].icon_id)
        
        row = layout.row(align=True)
        scale_right = 0.0039970986745213549*x - 0.83 if cs.category_expand == True else 0.00397986745213549*x - 0.83
        row.scale_x = scale_right
        row.label(icon='BLANK1')
        
        fossee_obj = fossee["main"]
        layout.menu(AboutFossee.bl_idname, text="  FOSSEE  ", icon_value=fossee_obj["fossee_logo"].icon_id)    
        
        layout.menu(HelpMenu.bl_idname, text="  Help  ", icon="QUESTION")
        layout.menu(DevMenu.bl_idname, text="Dev")
       
        layout.alert = True
        layout.operator(VNT_OT_close_venturial.bl_idname, text="", icon="PANEL_CLOSE")
        layout.alert = False
        
    def draw(self, context):
        layout = self.layout
        
        row1 = layout.row()
        split = row1.split(factor=0.35, align=False)
                    
        r1col1 = split.column()
        
        r1col1a = r1col1.row()
        r1col1b = r1col1.row()
        r1col1c = r1col1.row()
        
        r1col2 = split.column()
        
        r1col2a = r1col2.row().column()
        r1col2b = r1col2.row().column()
        r1col2c = r1col2.row()
            
        getattr(mesh_file_manager(), "draw")(r1col1a.box(), context)
        getattr(get_vertices(), "draw")(r1col1b.box(), context)
        getattr(boundary_control(), "draw")(r1col1c.box(), context)
        
        if context.scene.geo_design_options == "Design":
            getattr(geometry_designer(), "draw")(r1col2a, context)
        elif context.scene.geo_design_options == "Edges":
            getattr(edges_panel(), "draw")(r1col2a, context)
        #elif context.scene.geo_design_options == "Visualization":
            #getattr(visualization_panel(), "draw")(r1col2a, context)
        else:
            getattr(run_panel(), "draw")(r1col2a, context)

        getattr(geometry_designer_blocks(), "draw")(r1col2b.box(), context)
        getattr(get_boundaries(), "draw")(r1col2c.box(), context)
        
