from bpy.types import Operator, Menu
import os
import bpy


class VNT_OT_user_general_settings(Operator):
    """User general settings"""
    bl_label = "User general settings"
    bl_idname = "vnt.user_general_settings"
    bl_description = "Open user general settings window"
    
    def draw(self, context):
        layout = self.layout
            
        row = layout.row()
        row.label(text = "User Settings Section")
        row.label(text = "Requires PyQt integration.")
        
    def execute(self, context):     
        return {'FINISHED'}
        
    def invoke(self, context, event):
        return context.window_manager.invoke_popup(self, width=380)
    
    
class VNT_OT_venturial_homepage(Operator):
    """Click to visit Venturial's Homepage"""
    bl_label = "Open Venturial Homepage" 
    bl_idname = "vnt.venturial_homepage"
    bl_description = "Open default browser to navigate to Venturial's Homepage"

    def execute(self, context):     
        return {'FINISHED'}
    
class VNT_OT_fossee_homepage(Operator):
    """Click to visit FOSSEE's Homepage"""
    bl_label = "Open FOSSEE Homepage" 
    bl_idname = "vnt.fossee_homepage"
    bl_description = "Open default browser to navigate to FOSSEE's Homepage"

    def execute(self, context):     
        return {'FINISHED'}

class VNT_OT_close_venturial(Operator):
    """Close Venturial"""
    bl_label = "Exit" 
    bl_idname = "vnt.close_venturial"
    bl_description = "Click to Venturial. A confirmation prompt will appear before disabling the addon."
    
    def draw(self, context):
        scn = context.scene
        
        layout = self.layout
        row = layout.row()
        row.alignment = "CENTER"
        row.label(text="       Click OK to confirm Exit.")
        row = layout.row()
        row.alignment = "CENTER"
        row.label(text="       To re-enable OpenFOAM-GUI:")
        row = layout.row()
        row.alignment = "CENTER"
        row.label(text="Go to Edit-> Preferences->Add-ons -> Search 'Venturial' -> Tick Checkbox.")
        
    def execute(self, context):   
        bpy.ops.preferences.addon_disable(module="venturial")  
        return {'FINISHED'}
        
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=410)