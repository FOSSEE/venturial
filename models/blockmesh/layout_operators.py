from bpy.types import Operator
from bpy.props import EnumProperty

class VNT_OT_blockmesh_panel_layout_options(Operator):
    """Blockmesh Panel Options"""
    bl_label = "Blockmesh Panel Options" 
    bl_idname = "vnt.blockmesh_panel_categories"
    bl_description = " "

    blockmesh_panel_options : EnumProperty(items = [('Recents', 'Recents', ''),
                                                    ('Design', 'Design', ''),
                                                    ('Edges', 'Edges', ''),
                                                    ('Visualize', 'Visualize', ''),
                                                    ('Run', 'Run', '')],
                                           default = 'Recents')
    
    def execute(self, context):     
        context.scene.scene_blockmesh_panel_categories = self.blockmesh_panel_options
        
        return {'FINISHED'}