from bpy.types import Operator
from bpy.props import EnumProperty

class VNT_OT_mainpanel_layout(Operator):
    """Main panel sub-layout options"""
    bl_label = "Main panel sub-layout options" 
    bl_idname = "vnt.mainpanel_layout"
    bl_description = " "

    mainpanel_options : EnumProperty(items = [('Explore', 'Explore', ''),
                                              ('Geometry', 'Geometry', ''),
                                              ('Edges', 'Edges', ''),
                                              ('Step Controls', 'Steps Controls', ''),
                                              ('Visualize', 'Visualize', ''),
                                              ('Run', 'Run', '')],
                                     default = 'Explore')
    
    def execute(self, context):     
        context.scene.mainpanel_categories = self.mainpanel_options
        
        return {'FINISHED'}