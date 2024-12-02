from bpy.types import Operator
from bpy.props import IntProperty

class VNT_OT_more_tutorials_viewer(Operator):
    """Pop-up viewer for other tutorials"""
    bl_label = "View More Tutorials" 
    bl_idname = "vnt.viewmoretutorials"
    bl_description = "Click to view more tutorials"
    
    def draw(self, context):
        scn = context.scene
        
        layout = self.layout
        row = layout.row()

        row.label(text="Enlist all tutorials here")
        
    def execute(self, context):    
        return {'FINISHED'}
        
    def invoke(self, context, event):
        return context.window_manager.invoke_popup(self, width=300)
    

class VNT_OT_tutorial_viewer(Operator):
    """PyQt operator to open tutorial viewer"""
    bl_label = "Open a tutorial" 
    bl_idname = "vnt.open_tutorial"
    bl_description = "Click to view more tutorials"
    
    tut_index_id : IntProperty()
    
    def draw(self, context):
        scn = context.scene
        
        layout = self.layout
        row = layout.row()

        row.label(text="Tutorial No.: " + str(self.tut_index_id))
        
    def execute(self, context):    
        return {'FINISHED'}
        
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=300)