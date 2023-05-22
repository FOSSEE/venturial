from bpy.types import Panel, Menu

from venturial.models.header.file_handling_operators import *
from venturial.models.header.developer_menu_operators import *
from venturial.models.header.general_operators import (VNT_OT_venturial_maintools,
                                                       VNT_OT_venturial_homepage,
                                                       VNT_OT_fossee_homepage,
                                                       VNT_OT_user_general_settings)


from venturial.models.header.help_menu_operators import *
from venturial.utils.custom_icon_object_generator import *


class VNT_MT_dev_menu(Menu):
    """Display developer options."""
    bl_idname = "VNT_MT_dev_menu"
    bl_label = ""

    def draw(self, context):
        layout = self.layout
        layout.operator(VNT_OT_dev_tools.bl_idname, text = "Developer Settings", icon="OPTIONS")
        layout.operator(VNT_OT_dev_mode.bl_idname, text= "Developer Mode", icon="LOCKED")

class VNT_MT_file_menu(Menu):
    """File Menu options"""
    bl_label = "File" 
    bl_idname = "VNT_MT_file_menu"
    bl_description = "Open File Menu"
    
    def draw(self, context):
        layout = self.layout
    
        layout.operator(VNT_OT_new_case.bl_idname, text = "New", icon="NEWFOLDER")
        layout.operator(VNT_OT_open_case.bl_idname, text = "Open Case", icon="FOLDER_REDIRECT")
        
        layout.separator()
        
        layout.operator(VNT_OT_build_mesh.bl_idname, text="Build Mesh", icon = "MOD_LINEART")
        layout.operator(VNT_OT_import_mesh.bl_idname, text = "Import Mesh", icon="IMPORT")
        #layout.operator(VNT_OT_save_mesh.bl_idname, text = "Save Mesh", icon="PASTEDOWN")
        
        layout.separator()
        layout.operator(VNT_OT_user_general_settings.bl_idname, text = "Settings", icon="PREFERENCES")
        layout.menu(VNT_MT_dev_menu.bl_idname, text="Development", icon="RNA_ADD")

      
class VNT_PT_uicategory(Panel):
    """A pop-up UI panel for selecting and option from Venturial-tools (Meshing, Solving and Post-processing)"""
    bl_idname = "VNT_PT_uicategory"
    bl_label = ""
    bl_space_type =  "VIEW_3D"   
    bl_region_type = "UI"
    bl_options = {'INSTANCED'}

    def draw(self, context):
        layout = self.layout
        cs = context.scene
        
        row1 = layout.row()
        r1spt = row1.split(align=True)
        a = r1spt.row() 
        b = r1spt.row() 
        
        a.enabled = True if cs.meshing_tool == "BlockMesh" else False
        a.operator(VNT_OT_venturial_maintools.bl_idname, text="BlockMesh", depress=True if cs.meshing_tool != "SnappyHexMesh" else False).maintools = "BlockMesh"
        b.enabled = True if cs.meshing_tool == "SnappyHexMesh" else False
        b.operator(VNT_OT_venturial_maintools.bl_idname, text="SnappyHexMesh", depress=True if cs.meshing_tool != "BlockMesh" else False).maintools = "SnappyHexMesh"
        
        row2 = layout.row()
        row2.operator(VNT_OT_venturial_maintools.bl_idname, text="Solution Modeling").maintools = "Solution Modeling"
        
        row3 = layout.row()
        row3.operator(VNT_OT_venturial_maintools.bl_idname, text="Post-Processing").maintools = "Post-Processing"
        

class VNT_MT_about_venturial(Menu):
    """Pop-up for Venturial Intro"""
    bl_label = "Venturial" 
    bl_idname = "VNT_MT_about_venturial"
    bl_description = "Show Venturial intro"
    
    def draw(self, context):
        layout = self.layout
    
        row1 = layout.row()
        row1.template_icon(icon_value=custom_icons["venturial_logo"]["venturial_logo"].icon_id, scale=10)
        
        row2 = layout.row()
        row2.label(text="Venturial: A GUI for OpenFOAM.")
        
        row3 = layout.row()
        row3.operator(VNT_OT_venturial_homepage.bl_idname, text="Open Venturial's Homepage", icon="URL")
        
    def execute(self, context):     
        return {'FINISHED'}
        
    def invoke(self, context, event):
        return context.window_manager.invoke_popup(self, width=380)
    

class VNT_MT_about_fossee(Menu):
    """Pop-up for FOSSEE Intro"""
    bl_label = "FOSSEE" 
    bl_idname = "VNT_MT_about_fossee"
    bl_description = "Show FOSSEE intro"
    
    def draw(self, context):
        layout = self.layout
    
        row1 = layout.row()
        row1.template_icon(icon_value=custom_icons["fossee_logo"]["fossee_logo"].icon_id, scale=12)
        
        row2 = layout.row()
        row2.label(text="FOSSEE: Free/Libre Open-Source Software for Education.")
        
        row3 = layout.row()
        row3.operator(VNT_OT_fossee_homepage.bl_idname, text="Open FOSSEE Homepage", icon="URL")
        
    def execute(self, context):     
        return {'FINISHED'}
        
    def invoke(self, context, event):
        return context.window_manager.invoke_popup(self, width=380)


class VNT_MT_help_menu(Menu):
    """Display help options."""
    bl_idname = "VNT_MT_help_menu"
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


