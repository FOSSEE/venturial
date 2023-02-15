from bpy.types import Panel

class visualizer_view_controller:
    """Methods defining the sections of the blockmesh visualizer tool"""
    
    def geometry_visualizer(self, content, context):
        cs = context.scene
        row1 = content.row().box()
        
        title = row1.row()
        title.label(text= "Geometry")
        
        r1spt = row1.split(factor = 0.4)
        
        r1c1 = r1spt.row(align=True)
        r1c1.prop(cs, "statistics", toggle=True, text="Statistics") #statistics
        r1c1.popover(VNT_PT_statistics_settings.bl_idname, text="", icon="DOWNARROW_HLT") #statistics settings
        
        r1c2 = r1spt.row(align=True)
        
        r1c2spt = r1c2.split(factor=0.7, align=True)
        r1c2r1 = r1c2spt.row(align=True)
        r1c2r2 = r1c2spt.row(align=True)
                
        r1c2r1.prop(cs, "geo_params", expand=True)
        r1c2r2.prop(cs, "outline_color", text="")
        
        row2 = row1.row()
        
        r2spt = row2.split(factor = 0.4)
        
        r2c1 = r2spt.row()
    
        r2c2 = r2spt.row()
        
        r2c2spt = r2c2.split(factor=0.46, align=True)
        r2c2r1 = r2c2spt.row()
        r2c2r2 = r2c2spt.row()
        
        r2c2r1.prop(cs, "shading", expand=True) #object mode/wire frame mode
        r2c2r2.prop(cs, "wire_opacity", slider=True) #wireframe mode opacity
        
        row3 = row1.row()
        
        r3spt = row3.split(factor = 0.4)
        
        r3c1 = r3spt.row()
    
        r3c2 = r3spt.row()
        
        r3c2spt = r3c2.split(factor=0.46, align=True)
        r3c2r1 = r3c2spt.row(align=True)
        r3c2r2 = r3c2spt.row()
        
        r3c2r1.prop(cs, "bfc", toggle=True, text="BFC") #backface culling
        r3c2r1.prop(cs, "xray", toggle=True, text="X-ray") #xray
        r3c2r2.prop(cs, "xray_opacity", slider=True) #xray opacity control
        
        

class VNT_PT_statistics_settings(Panel):
    """A pop-up UI panel for setting geometry statistics"""
    bl_idname = "VNT_PT_statistics_settings"
    bl_label = ""
    bl_space_type =  "VIEW_3D"   
    bl_region_type = "UI"
    bl_options = {'INSTANCED'}

    def draw(self, context):
        layout = self.layout
        cs = context.scene

        row = layout.row()
        row.label(text = "options for setting statistics panel")
        