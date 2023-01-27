from venturial.models.blockmesh_panel_operators import *


class blockmesh_panel_layout:
    """Class that defines the layout of the blockmesh panel"""
    
    def draw(self, layout, context):
        
        # ------------------------- Shabby code to replicate Blender's horizontal tabs. ----------------------------
        # ------------------------- This is a fix to bounding boxes issue for operator selection. ------------------
        # ------------------------- It's Shabby but does the job. --------------------------------------------------
        cs = context.scene
        x = cs.scene_blockmesh_panel_categories
        
        
        row1 = layout.row(align=True)
        row1.ui_units_y = 0.001
        
        scale_active = 1.45
        scale_inactive = 1.75
        
        c1 = row1.split(factor=0.2, align=True)
        
        c1a = c1.row(align=True)
        c1b = c1.row(align=True)
        
        c1a.operator(VNT_OT_blockmesh_panel_categories.bl_idname, 
                    text="Recents", 
                    depress= True if x == "Recents" else False, 
                    emboss= True if x == "Recents" else False).blockmesh_panel_options = "Recents"
        c1a.scale_y = scale_active if x == "Recents" else scale_inactive
    
        c2 = c1b.split(factor=0.25 if x == "Design" else 0.25, align=True)
        c2a = c2.row(align=True)
        c2a.operator(VNT_OT_blockmesh_panel_categories.bl_idname, 
                    text="Design", 
                    depress= True if x == "Design" else False,
                    emboss= True if x == "Design" else False).blockmesh_panel_options = "Design"
        c2a.scale_y = scale_active if x == "Design" else scale_inactive
        c2b = c2.row(align=True)
        
        c3 = c2b.split(factor=0.33 if x == "Edges" else 0.33, align=True)
        
        c3a = c3.row(align=True)
        c3a.operator(VNT_OT_blockmesh_panel_categories.bl_idname, 
                    text="Edges", 
                    depress= True if x == "Edges" else False,
                    emboss= True if x == "Edges" else False).blockmesh_panel_options = "Edges"
        
        c3a.scale_y = scale_active if x == "Edges" else scale_inactive
        c3b = c3.row(align=True)
        
        c4 = c3b.split(factor=0.505 if x == "Visualize" else 0.5, align=True)
        c4a = c4.row(align=True)
        c4a.operator(VNT_OT_blockmesh_panel_categories.bl_idname, 
                    text="Visualize", 
                    depress= True if x == "Visualize" else False,
                    emboss= True if x == "Visualize" else False).blockmesh_panel_options = "Visualize"
        c4a.scale_y = scale_active if x == "Visualize" else scale_inactive
        
        c4b = c4.row(align=True)
        c4b.operator(VNT_OT_blockmesh_panel_categories.bl_idname, 
                     text="Run", 
                     depress= True if x == "Run" else False,
                     emboss= True if x == "Run" else False).blockmesh_panel_options = "Run"
        c4b.scale_y = scale_active if x == "Run" else scale_inactive
        
        
        row2 = layout.row(align=True)
        row2.scale_y = 0.75
        
        if x == "Recents":
            f1 = 0.195
        elif x == "Design":
            f1 = 0.205
        else:
            f1 = 0.20
        
        c1 = row2.split(factor=f1, align=True)
        c1a = c1.row(align=True) 
        c1a.box().label(text="") if x != "Recents" else c1a.row(align=True)
        
        c1b = c1.row(align=True)
        if x == "Design":
            f2 = 0.24
        elif x == "Edges":
            f2 = 0.255
        else:
            f2 = 0.25
        
        
        c2 = c1b.split(factor=f2, align=True)
        c2a = c2.row(align=True)
        c2a.box().label(text="") if x != "Design" else c2a.row(align=True)
        
        c2b = c2.row(align=True)
        if x == "Edges":
            f3 = 0.3175
        elif x == "Visualize":
            f3 = 0.337
        else:
            f3 = 0.33333
            
        c3 = c2b.split(factor=f3, align=True)
        c3a = c3.row(align=True)
        c3a.box().label(text="") if x != "Edges" else c3a.row(align=True)
        
        c3b = c3.row(align=True)
        if x == "Visualize":
            f4 = 0.4875
        elif x == "Run":
            f4 = 0.5075
        else:
            f4 = 0.5
        
        c4 = c3b.split(factor=f4, align=True)
        c4a = c4.row(align=True)
        c4a.box().label(text="") if x != "Visualize" else c4a.row(align=True)
        
        c4b = c4.row(align=True)
        c4b.box().label(text="") if x != "Run" else c4b.row(align=True)
        
        # -----------------------------------------------------------------------------------------------------