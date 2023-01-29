from bpy.types import Operator

class VNT_OT_dev_mode(Operator):
    """Click to Enable/Disable Developer Mode"""
    
    bl_label = "Developer Mode" 
    bl_idname = "vnt.devmode"
    bl_description = "Open Developer Mode" 
    
    def execute(self, context):
        return {'FINISHED'}

class VNT_OT_dev_tools(Operator):
    """Click to view developer tools"""
    
    bl_label = "Developer Tools" 
    bl_idname = "vnt.devtools"
    bl_description = "Open Developer Tools" 

    def execute(self, context):
        return {'FINISHED'}