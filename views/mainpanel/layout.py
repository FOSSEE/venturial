from venturial.models.mainpanel_sublayout_operators import *
from venturial.views.mainpanel.view import layout_controller

class mainPanel:
    """Class that defines the layout of the main panel"""
    
    def draw(self, layout, context):
        """Draws the layout of the main panel"""
        
        cs = context.scene

        r1 = layout.row(align=True)
        r1.prop(cs, "mainpanel_categories", expand=True)

        # var = "Edges" if cs.current_tool_text == "BlockMesh" else "Step Controls"
        # getattr(self, "draw_tool_navigator")(cs.mainpanel_categories, var, layout)

        getattr(layout_controller(cs.mainpanel_categories), "output")(layout, context)
        
    #TODO: Fix this later. Need to change options dynamically for blockMesh and snappyHexMesh
    def draw_tool_navigator(self, x, var, layout):
        """Horizontal tool navigator"""

        # ----------- Shabby code to replicate Blender's horizontal tabs. ----------------------------
        # ----------- This is a fix to bounding boxes issue #1 for operator selection. ---------------
        # ----------- It's Shabby but does the job. --------------------------------------------------
        row1 = layout.row(align=True)
        row1.ui_units_y = 0.001
        
        scale_active = 1.45
        scale_inactive = 1.75
        
        c1 = row1.split(factor=0.2, align=True)
        
        c1a = c1.row(align=True)
        c1b = c1.row(align=True)
        
        c1a.operator(VNT_OT_mainpanel_layout.bl_idname, 
                    text="Explore", 
                    depress= True if x == "Explore" else False, 
                    emboss= True if x == "Explore" else False).mainpanel_options = "Explore"
        c1a.scale_y = scale_active if x == "Explore" else scale_inactive
    
        c2 = c1b.split(factor=0.25 if x == "Geometry" else 0.25, align=True)
        c2a = c2.row(align=True)
        c2a.operator(VNT_OT_mainpanel_layout.bl_idname, 
                    text="Geometry", 
                    depress= True if x == "Geometry" else False,
                    emboss= True if x == "Geometry" else False).mainpanel_options = "Geometry"
        c2a.scale_y = scale_active if x == "Geometry" else scale_inactive
        c2b = c2.row(align=True)
        
        c3 = c2b.split(factor=0.33 if x == var else 0.33, align=True)
        
        c3a = c3.row(align=True)
        c3a.operator(VNT_OT_mainpanel_layout.bl_idname, 
                    text= var, 
                    depress= True if x == var else False,
                    emboss= True if x == var else False).mainpanel_options = var
        
        c3a.scale_y = scale_active if x == var else scale_inactive
        c3b = c3.row(align=True)
        
        c4 = c3b.split(factor=0.505 if x == "Visualize" else 0.5, align=True)
        c4a = c4.row(align=True)
        c4a.operator(VNT_OT_mainpanel_layout.bl_idname, 
                    text="Visualize", 
                    depress= True if x == "Visualize" else False,
                    emboss= True if x == "Visualize" else False).mainpanel_options = "Visualize"
        c4a.scale_y = scale_active if x == "Visualize" else scale_inactive
        
        c4b = c4.row(align=True)
        c4b.operator(VNT_OT_mainpanel_layout.bl_idname, 
                     text="Run", 
                     depress= True if x == "Run" else False,
                     emboss= True if x == "Run" else False).mainpanel_options = "Run"
        c4b.scale_y = scale_active if x == "Run" else scale_inactive
        
        
        row2 = layout.row(align=True)
        row2.scale_y = 0.75
        row2.ui_units_y = 0.95
        
        if x == "Explore":
            f1 = 0.195
        elif x == "Geometry":
            f1 = 0.205
        else:
            f1 = 0.20
        
        c1 = row2.split(factor=f1, align=True)
        c1a = c1.row(align=True) 
        c1a.box().label(text="") if x != "Explore" else c1a.row(align=True)
        
        c1b = c1.row(align=True)
        if x == "Geometry":
            f2 = 0.24
        elif x == var:
            f2 = 0.255
        else:
            f2 = 0.25
        
        
        c2 = c1b.split(factor=f2, align=True)
        c2a = c2.row(align=True)
        c2a.box().label(text="") if x != "Geometry" else c2a.row(align=True)
        
        c2b = c2.row(align=True)
        if x == var:
            f3 = 0.3175
        elif x == "Visualize":
            f3 = 0.337
        else:
            f3 = 0.33333
            
        c3 = c2b.split(factor=f3, align=True)
        c3a = c3.row(align=True)
        c3a.box().label(text="") if x != var else c3a.row(align=True)
        
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