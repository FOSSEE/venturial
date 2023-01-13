from bpy.types import Operator

class VNT_OT_user_guide(Operator):
    bl_label = "User Guide" 
    bl_idname = "vnt.userguide"
    bl_description = "Open User Guide" 

    def execute(self, context):
        return {'FINISHED'}
    
class VNT_OT_developer_guide(Operator):
    bl_label = "Developer Guide" 
    bl_idname = "vnt.developerguide"
    bl_description = "Open Developer Guide" 

    def execute(self, context):
        return {'FINISHED'}
    
class VNT_OT_feature_request(Operator):
    bl_label = "Feature Request" 
    bl_idname = "vnt.feature_request"
    bl_description = "Request a Feature" 

    def execute(self, context):
        return {'FINISHED'}
    
class VNT_OT_report_bugs(Operator):
    bl_label = "Request Bugs" 
    bl_idname = "vnt.requestbugs"
    bl_description = "Request Bugs" 

    def execute(self, context):
        return {'FINISHED'}
    
class VNT_OT_developer_support(Operator):
    bl_label = "Developer Support" 
    bl_idname = "vnt.developersupport"
    bl_description = "Request support from developer" 

    def execute(self, context):
        return {'FINISHED'}
    
class VNT_OT_user_community(Operator):
    bl_label = "User Community" 
    bl_idname = "vnt.usercommunitty"
    bl_description = "Check the Venturial User community" 

    def execute(self, context):
        return {'FINISHED'}
    
class VNT_OT_developer_community(Operator):
    bl_label = "Developer Community" 
    bl_idname = "vnt.developercommunity"
    bl_description = "Check the OpenFOAM-GUI Developer community" 

    def execute(self, context):
        return {'FINISHED'}
    
class VNT_OT_release_notes(Operator):
    bl_label = "Release Notes" 
    bl_idname = "vnt.releasenotes"
    bl_description = "Open Release Notes Panel to view changes in OpenFOAM-GUI versions" 

    def execute(self, context):
        return {'FINISHED'}