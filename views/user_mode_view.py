from bpy.types import Panel
from venturial.views.blockmesh.layout import blockmesh_layout
from venturial.views.header.layout import header_layout

class VNT_PT_usermodeview(Panel):
    """Main Panel Layout of User Mode"""
    bl_idname = "VNT_PT_usermodeview"
    bl_label = ""
    bl_space_type =  "VIEW_3D"   
    bl_region_type = "UI"
    bl_category = "Venturial"
    
    def draw_header(self, context):
        layout = self.layout   
        
        getattr(header_layout(), "draw")(layout, context)
        
    def draw(self, context):
        layout = self.layout
        
        getattr(blockmesh_layout(), "draw")(layout, context)
        
        
    
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
       
        
        #row1.box().operator(
        # split = row1.split(factor=0.35, align=False)
                    
        # r1col1 = split.column()
        
        # r1col1a = r1col1.row()
        # r1col1b = r1col1.row()
        # r1col1c = r1col1.row()
        
        # r1col2 = split.column()
        
        # r1col2a = r1col2.row().column()
        # r1col2b = r1col2.row().column()
        # r1col2c = r1col2.row()
            
        # getattr(mesh_file_manager(), "draw")(r1col1a.box(), context)
        # getattr(get_vertices(), "draw")(r1col1b.box(), context)
        # getattr(boundary_control(), "draw")(r1col1c.box(), context)
        
        #if context.scene.geo_design_options == "Design":
             #getattr(geometry_designer(), "draw")(row1, context)
        # elif context.scene.geo_design_options == "Edges":
        #     getattr(edges_panel(), "draw")(r1col2a, context)
        # #elif context.scene.geo_design_options == "Visualization":
        #     #getattr(visualization_panel(), "draw")(r1col2a, context)
        # else:
        #     getattr(run_panel(), "draw")(r1col2a, context)

        # getattr(geometry_designer_blocks(), "draw")(r1col2b.box(), context)
        # getattr(get_boundaries(), "draw")(r1col2c.box(), context)
        
        
        
