#from venturial.views.schemas.UIList_schemas import VNT_UL_mesh_file_manager
from venturial.models.header.file_handling_operators import *
from venturial.models.blockmesh.design_operators import *
from venturial.utils.custom_icon_object_generator import *
from bpy.types import Panel

class blockmesh_layout_controller:
    """Controller class for defining and designating layout callbacks"""
    def __init__(self, type):
        self.type = type
        self.callback = {"Recents": "VNT_ST_recents",
                         "Design": "VNT_ST_design",
                         "Visualize": "VNT_ST_visualize"}
        
    def output(self, layout, context):
        getattr(self, self.callback[self.type])(layout, context)
        
    def VNT_ST_recents(self, layout, context):
        cs = context.scene
        layout = layout.box().box()
        
        row1 = layout.row()
        row1.ui_units_y = 0.9
        
        row1spt = row1.split()
        row1a = row1spt.column().row()
        row1b = row1spt.column(align=True).split(align=True).column(align=True)

        row1a.scale_y = 1.3
        
        row1a.operator(VNT_OT_new_mesh_file.bl_idname, text="New Mesh")
        row1a.operator(VNT_OT_build_mesh.bl_idname, text="Build Mesh")
        
        row1bc1 = row1b.row()
        row1bc1.label(text="")
        row1bc1.ui_units_y = 0.3
     
        row1bc2 = row1b.split(align=True)
        
        row1bc2.operator(VNT_OT_import_mesh.bl_idname, text="", icon="FILEBROWSER")
        row1bc2.operator(VNT_OT_save_mesh.bl_idname, text="", icon="IMPORT")
        row1bc2.operator(VNT_OT_see_older.bl_idname, text="", icon="TIME")
        row1bc2.alert = True
        row1bc2.operator(VNT_OT_delete_mesh_file_items.bl_idname, text="", icon="TRASH")
        row1bc2.alert = True
        
        row2 = layout.row(align=False)
        row2.scale_y = 1.4
        row2.template_list("VNT_UL_mesh_file_manager", "", cs, "mfile_item", cs, "mfile_item_index", rows= 2)
        
    def VNT_ST_design(self, layout, context):
        cs = context.scene
        layout = layout.box().box()
        
        row1 = layout.row()
        split = row1.split(factor = 0.185)
        
        row1c1 = split.row()
        row1c1.alignment = 'CENTER'
        row1c1.label(text="Cells:")
        
        row1c2 = split.row(align = True)
        row1c2split = row1c2.split(factor = 0.50)
        
        row1c2c1 = row1c2split.row(align=True).split(factor=0.33, align=True)
        row1c2c1p1 = row1c2c1.row(align=True)
        row1c2c1p2 = row1c2c1.row(align=True)
        
        row1c2c2 = row1c2split.row(align=True).split(factor=0.3175, align=True)
        row1c2c2p1 = row1c2c2.row(align=True)
        row1c2c2p2 = row1c2c2.row(align=True)
        
        row1c2c1p1.prop(cs, "cellShape_units", text="", slider=True)
        row1c2c1p2.prop(cs, "cellShapes", text="")
        
        row1c2c2p1.popover(VNT_PT_cell_location.bl_idname, text=cs.spawn_type)
        row1c2c2p2.operator(VNT_OT_add_to_viewport.bl_idname, text="Create Cells")
        
        row2 = layout.row()
        split = row2.split(factor = 0.185)
        
        r2c1 = split.row()
        r2c2 = split.row()
        
        r2c1.alignment = 'CENTER'
        r2c1.prop(cs, "transform", text=" Transform")
        
        r2c2.enabled = cs.transform
        r2c2.prop(cs, "transformation_methods", expand=True)
        
        row3 = layout.row()
        split = row3.split(factor = 0.185)
        
        r4c1 = split.row()
        r4c2 = split.row()
        
        r4c1.alignment = 'CENTER'
        r4c1.prop(cs, "snapping", text=" Snapping  ")
        
        r4c2.enabled = cs.snapping
        r4c2.prop(cs, "snapping_methods", expand=True)
        
        row5 = layout.row(align=True)
        split = row5.split(factor = 0.185)

        r5c1 = split.row()
        r5c1.alignment = 'CENTER'
        r5c1.label(text = "Set Cells:")
        
        r5c2 = split.row(align=True)
        r5c2split = r5c2.split()
        r5c2c1 = r5c2split.row(align=True)
        r5c2c2 = r5c2split.row()
        
        r5c2c1.prop(cs, "cell_x", toggle=True)
        r5c2c1.prop(cs, "cell_y", toggle=True)
        r5c2c1.prop(cs, "cell_z", toggle=True)
        
        r5c2c2.prop(cs, "ctm", slider=True)
        
        row6 = layout.row()
        row6.scale_y = 1.3
        
        row6spt = row6.split(factor = 0.46)
      
        row6a = row6spt.column().row()
        row6b = row6spt.column(align=True).split(align=True)
        
        row6asplit = row6a.split(factor = 0.413)
        row6ac1 = row6asplit.row()
        row6ac2 = row6asplit.row()
    
        row6ac1.operator(VNT_OT_compose.bl_idname, text="Compose")
        row6ac2.operator(VNT_OT_get_blocks.bl_idname, text="Get Blocks")
        
        row6bspt = row6b.split(factor = 0.24)
        
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
        
    def VNT_ST_visualize(self, layout, context):
        cs = context.scene
        layout = layout.box()
        
        row1 = layout.row().box()
        
        title = row1.row()
        title.label(text= "Geometry")
        
        r1spt = row1.split(factor = 0.4)
        
        r1c1 = r1spt.row()
        r1c1.prop(cs, "statistics", toggle=True, text="Statistics") #statistics
        r1c1.popover(VNT_PT_statistics_settings.bl_idname, text="", icon="DOWNARROW_HLT") #statistics settings
        
        r1c2 = r1spt.row(align=True)
        r1c2.prop(cs, "geo_params", expand=True)
        r1c2.prop(cs, "outline_color", text="")
        
        row2 = row1.row()
        
        r2spt = row2.split(factor = 0.4)
        
        r2c1 = r2spt.row()
    
        r2c2 = r2spt.row()
        r2c2.prop(cs, "shading", expand=True) #object mode/wire frame mode
        r2c2.prop(cs, "wire_opacity", slider=True) #wireframe mode opacity
        
        row3 = row1.row()
        
        r3spt = row3.split(factor = 0.4)
        
        r3c1 = r3spt.row()
    
        r3c2 = r3spt.row()
        
        r3c2.prop(cs, "bfc", toggle=True, text="Backface Culling") #backface culling
        r3c2.prop(cs, "xray", toggle=True, text="X-ray") #xray
        r3c2.prop(cs, "xray_opacity", slider=True) #xray opacity control
        

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
        