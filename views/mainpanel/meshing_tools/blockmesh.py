from venturial.models.blockmesh.design_operators import *
from bpy.types import Panel

class blockmesh_menu:

    def layout(self, tools, context):

        cs = context.scene

        # Row 1 
        row1 = tools.row(align=True)
        split = row1.split(factor = 0.18, align=True)
        
        row1c1 = split.row(align=True)
        row1c1.alignment = 'RIGHT'
        row1c1.label(text="Blocks:")
        
        row1c2 = split.row(align = True)
        row1c2split = row1c2.split(factor = 0.50, align=True)
        
        row1c2c1 = row1c2split.row(align=True).split(factor=0.33, align=True)
        row1c2c1p1 = row1c2c1.row(align=True)
        row1c2c1p2 = row1c2c1.row(align=True)
        
        row1c2c2 = row1c2split.row(align=True).split(factor=0.3175, align=True)
        row1c2c2p1 = row1c2c2.row(align=True)
        row1c2c2p2 = row1c2c2.row(align=True)
        
        row1c2c1p1.prop(cs, "cellShape_units", text="", slider=True)
        row1c2c1p2.prop(cs, "cellShapes", text="")
        
        row1c2c2p1.popover(VNT_PT_cell_location.bl_idname, text=cs.spawn_type)
        row1c2c2p2.operator(VNT_OT_add_to_viewport.bl_idname, text="Generate Blocks")
        
        # Row 2
        row2 = tools.row(align=True)
        split = row2.split(factor = 0.185, align=True)
        
        r2c1 = split.row(align=True)
        r2c2 = split.row(align=True)
        
        r2c1spt = r2c1.split(factor=0.175, align=True)
        a = r2c1spt.split(align=True)
        b = r2c1spt.row(align=True)
                
        a.prop(cs, "transform", text="", toggle=1, icon="LOCKED" if cs.transform == False else "UNLOCKED")
        b.enabled = cs.transform
        b.box().label(text="Transform")
        b.scale_y = 0.56 
        
        r2c2.enabled = cs.transform
        r2c2.prop(cs, "transformation_methods", expand=True)
        
        # Row 3
        row3 = tools.row(align=True)
        split = row3.split(factor = 0.185, align=True)
        
        r3c1 = split.row(align=True)
        r3c2 = split.row(align=True)
        
        r3c1spt = r3c1.split(factor=0.175, align=True)
        a = r3c1spt.split(align=True)
        b = r3c1spt.row(align=True)
                
        a.prop(cs, "snapping", text="", toggle=1, icon="LOCKED" if cs.snapping == False else "UNLOCKED")
        b.enabled = cs.snapping
        b.box().label(text="Snapping")
        b.scale_y = 0.56 
        
        r3c2.enabled = cs.snapping
        r3c2.prop(cs, "snapping_methods", expand=True)
        
        # Row 4
        row5 = tools.row(align=True)
        split = row5.split(factor = 0.18)

        r5c1 = split.row()
        r5c1.alignment = 'RIGHT'
        r5c1.label(text = "Set Cells:")
        
        r5c2 = split.row(align=True)
        r5c2split = r5c2.split()
        r5c2c1 = r5c2split.row(align=True)
        r5c2c2 = r5c2split.row()
        
        r5c2c1.prop(cs, "cell_x", toggle=True)
        r5c2c1.prop(cs, "cell_y", toggle=True)
        r5c2c1.prop(cs, "cell_z", toggle=True)
        
        r5c2c2.prop(cs, "ctm", slider=True)
        
        row6 = tools.row()
        row6.scale_y = 1.3
        
        row6spt = row6.split(factor = 0.448)
      
        row6a = row6spt.column().row()
        row6b = row6spt.column(align=True).split(align=True)
        
        row6asplit = row6a.split(factor = 0.413)
        row6ac1 = row6asplit.row()
        row6ac2 = row6asplit.row()
    
        row6ac1.operator(VNT_OT_compose.bl_idname, text="Compose")
        row6ac2.operator(VNT_OT_get_blocks.bl_idname, text="Get Blocks")
        
        row6bspt = row6b.split(factor = 0.252)
        
        row6ba = row6bspt.split(align=True)
        row6ba.operator(VNT_OT_blocksdatacontrol.bl_idname, icon="ADD", text="").action = 'ADD'
        
        row6bb = row6bspt.column(align=True)
        row6bb1 = row6bb.split(align=True)
        row6bb1.label(text = "")
        row6bb1.ui_units_y = 0.2
        
        row6bb2 = row6bb.split(align=True)
        row6bb2.scale_y = 0.85
        
        row6bb2.operator(VNT_OT_blocksdatacontrol.bl_idname, icon="REMOVE", text="").action = 'REMOVE'
        row6bb2.operator(VNT_OT_showselectedblocks.bl_idname, icon="STICKY_UVS_DISABLE", text="")
        row6bb2.operator(VNT_OT_select_unselect_allblocks.bl_idname, icon="STICKY_UVS_LOC", text="")
        
        row6bb2.alert = True
        row6bb2.operator(VNT_OT_remove_blocks.bl_idname, icon="CANCEL", text="")
        row6bb2.operator(VNT_OT_remove_all_blocks.bl_idname, icon="TRASH", text="")
        row6bb2.operator(VNT_OT_clearblocks.bl_idname, icon="TRASH", text="")
        
        


class VNT_PT_cell_location(Panel):
    """A pop-up UI panel for selecting the location of cell generation"""
    bl_idname = "VNT_PT_cell_location"
    bl_label = ""
    bl_space_type =  "VIEW_3D"   
    bl_region_type = "UI"
    bl_options = {'INSTANCED'}

    def draw(self, context):
        layout = self.layout
        cs = context.scene
        
        row = layout.row(align=True)
        row.operator(VNT_OT_location_spawnner.bl_idname, text="Grid", depress=True if cs.spawn_type == "Grid" else False).options = "Grid"
        row.operator(VNT_OT_location_spawnner.bl_idname, text="3D Cursor", depress=True if cs.spawn_type == "3D Cursor" else False).options = "3D Cursor"
        row.operator(VNT_OT_location_spawnner.bl_idname, text="Center", depress=True if cs.spawn_type == "Center" else False).options = "Center"
        