from venturial.models.header.file_handling_operators import *
from venturial.models.blockmesh.design_operators import *
# from venturial.models.blockmesh.edge_operators import *
from venturial.models.blockmesh.boundary_control_operators import *
from venturial.models.run_panel_operators import *
from venturial.utils.custom_icon_object_generator import *
from venturial.views.mainpanel.visualizer import visualizer_menu
from venturial.views.mainpanel.tutorials import tutorial_menu
from venturial.views.mainpanel.recents import recents_menu
from venturial.views.mainpanel.meshing_tools.blockmesh import blockmesh_menu
from venturial.views.mainpanel.meshing_tools.snappyhexmesh import snappyhexmesh_menu
from venturial.models.edges_panel_operators import *

import blf

import time, bpy

class layout_controller:
    """Controller class for defining and designating layout callbacks"""
    def __init__(self, type):
        self.type = type
        self.callback = {"Explore": "VNT_ST_explorer",
                         "Geometry": "VNT_ST_geometry",
                         "Visualize": "VNT_ST_visualize",
                         "Edges": "VNT_ST_edges",
                         "Step Controls": "VNT_ST_step_controls",
                         "Run": "VNT_ST_run",
                         "Boundary": "VNT_ST_boundary"}
        
    def output(self, layout, context):
        layout = layout.box()
        layout.separator(factor=0.05)
        
        getattr(self, self.callback[self.type])(layout, context)
        
    def VNT_ST_explorer(self, layout, context):
        cs = context.scene
        box1 = layout.box()
           
        row1 = box1.row()
        row1.scale_y = 1.3
        
        row1.operator(VNT_OT_new_case.bl_idname, text="New", icon="NEWFOLDER")
        row1.operator(VNT_OT_open_case.bl_idname, text="Open Case", icon="FOLDER_REDIRECT")
        row1.operator(VNT_OT_build_mesh.bl_idname, text="Build Mesh", icon="MOD_LINEART")
        row1.operator(VNT_OT_import_mesh.bl_idname, text="Import Mesh", icon="IMPORT")
        row1.alert = True
        row1.operator(VNT_OT_delete_mesh_file_items.bl_idname, text="Delete", icon="TRASH")
        row1.alert = False
        
        row2 = box1.row(align=True)
        row2.scale_y =  0.75
        row2.ui_units_y = 0.87
        
        r2spt = row2.split(factor=0.193,align=True)
        a = r2spt.row(align=True)
        b = r2spt.row(align=True)
        
        bspt = b.split(factor=0.243, align=True)
        b1 = bspt.row(align=True)
        b2 = bspt.row(align=True)
        
        b2spt = b2.split(factor = 0.325, align=True)
        c1 = b2spt.row(align=True)
        c2= b2spt.row(align=True)
        
        a.box().operator(VNT_OT_list_category.bl_idname, text="Case", depress=False, emboss=False)
        b1.box().operator(VNT_OT_list_category.bl_idname, text="Mesh Dictionary", depress=False, emboss=False)
        c1.box().operator(VNT_OT_list_category.bl_idname, text="Meshing Tool", depress=False, emboss=False)
        c2.box().label(text="Mesh file Path")
   
        row3 = box1.row(align=False)
        row3.scale_y = 1.4
        row3.template_list("VNT_UL_mesh_file_manager", "", cs, "mfile_item", cs, "mfile_item_index", rows=2)
       
        row4 = layout.row(align=False)
        row4spt = row4.split(factor=0.4)
        row4l = row4spt.column() 
        row4r = row4spt.column()
        
        getattr(recents_menu(), "layout")(row4l, context)
        getattr(tutorial_menu(), "layout")(row4r, context)
        
    def VNT_ST_geometry(self, layout, context):
        cs = context.scene
        tools = layout.box()

        if cs.current_tool_text == "BlockMesh":
            getattr(blockmesh_menu(), "layout")(tools, context)

        else:
            getattr(snappyhexmesh_menu(), "layout")(tools, context)


        # THis feature is to be implemented later down the line
        # projects = layout.box()
        # r7 = projects.row() 

        # This shabby piece of code is similar to the draw method of top navigation bar, but relatively better.
        # This creates a horizontal tabs list of active projects (cases) dynamically. 
        # for i in range(0, len(cs.mfile_item)):
        #     x = r7.column(align=True).row(align=True)
            
        #     x.operator("VNT_OT_active_project_indicator", 
        #                text=cs.mfile_item[i].ITEM_name, 
        #                emboss = True if cs.mfile_item[i].ITEM_identifier == cs.mfile_item[cs.mfile_item_index].ITEM_identifier else False).active_file_id = cs.mfile_item[i].ITEM_identifier
            
        #     x.operator("vnt.deactivate_mesh_file_item",
        #                text="",
        #                emboss = True if cs.mfile_item[i].ITEM_identifier == cs.mfile_item[cs.mfile_item_index].ITEM_identifier else False,
        #                icon="PANEL_CLOSE").dump_file_id = cs.mfile_item[i].ITEM_identifier
            
        #     x.scale_y = 1.7 if cs.mfile_item[i].ITEM_identifier == cs.mfile_item[cs.mfile_item_index].ITEM_identifier else 1.9
        #     x.scale_x = 0.9730 + len(cs.mfile_item)*(0.009 if len(cs.mfile_item) == 3 else 0.01) if cs.mfile_item[i].ITEM_identifier == cs.mfile_item[cs.mfile_item_index].ITEM_identifier else 1.0
    
        # r7.ui_units_y = 0.00001
            
        # r8 = projects.row(align=True)
        # for i in range(0, len(cs.mfile_item)):
        #     y = r8.column(align=True)
        #     if cs.mfile_item[i].ITEM_identifier == cs.mfile_item[cs.mfile_item_index].ITEM_identifier:
        #         y.label(text="") # Active tab in the view
        #     else:
        #         y.scale_y = 0.8
        #         y.box().label(text="") # Passive tabs in the view
        
        # r10 = projects.row()
        # r10.scale_y = 1.4
        # r10.template_list("CUSTOM_UL_blocks", "", cs, "bcustom", cs, "bcustom_index", rows=2)
                   
    def VNT_ST_visualize(self, layout, context):
        outline = layout.box()
        
        getattr(visualizer_menu(), "geometry_visualizer")(outline, context)
        
        r1 = outline.row()
        r1spt = r1.split(factor=0.5)
        
        vert_outline = r1spt.row()
        block_outline =  r1spt.row()
        
        getattr(visualizer_menu(), "vertex_visualizer")(vert_outline, context)
        getattr(visualizer_menu(), "block_visualizer")(block_outline, context)
        
        r2 = outline.row()
        r2spt = r2.split(factor=0.5)
        
        edge_outline = r2spt.row()
        boundary_outline =  r2spt.row()
        
        getattr(visualizer_menu(), "edge_visualizer")(edge_outline, context)
        getattr(visualizer_menu(), "boundary_visualizer")(boundary_outline, context)
      
    def VNT_ST_edges_old(self, layout, context):
        cs = context.scene
        layout = layout.box()
        
        row0 = layout.row()
        row0spt = row0.split(factor = 0.4)
        
        r0c1 = row0spt.row(align=True)
        r0c2 = row0spt.row(align=True)
        
        r0c1spt = r0c1.split(align=True)
        a = r0c1spt.row(align=True)
        b = r0c1spt.row(align=True)
        
        a.box().label(text="Curve Type")
        a.scale_y = 0.56 
        b.prop(cs, "curve_type", text="")
        
        r0c2spt = r0c2.split(factor = 0.34, align=True)
        p = r0c2spt.row(align=True)
        q = r0c2spt.row(align=True)
        
        p.box().label(text="Control Method")
        p.scale_y = 0.56
        q.prop(cs, "edge_control_methods", expand=True)
        
        row1 = layout.row()
        row1spt = row1.split(factor = 0.4)
        
        r1c1 = row1spt.row(align=True)
        r1c2 = row1spt.row(align=True)
        
        r1c1spt = r1c1.split(align=True)
        a = r1c1spt.row(align=True)
        b = r1c1spt.row()
        
        a.operator(VNT_OT_generate_edge.bl_idname, text = "Generate Edge")
        b.operator(VNT_OT_edit_edge.bl_idname, text = "Edit Edge")
        b.alert = True
        b.operator(VNT_OT_destroy_edge.bl_idname, icon="TRASH")
        b.alert = False

    def VNT_ST_edges(self, layout, context):
        '''
        Code for the edge tab in the addon tab
        '''

        vert_ = None

        def draw_loc(context):
            """
            Draws the location of the selected vertex
            """
            cs = context.scene
            if vert_ != None:
                print("removed")
                bpy.types.SpaceView3D.draw_handler_remove(vert_, 'WINDOW')
            
            if len(cs.ecustom) and vert_ == None:
                idx = cs.ecustom_index
                idx_v = len(cs.ecustom[idx].vert_collection)

                if idx_v >= 1:
                    a = bpy.data.objects[f"{cs.ecustom[idx].name}0{(idx_v//2)+1}"].location
    
        # def draw_vertex_properties(context, idx, a):
        #     text_pos = view3d.location_3d_to_region_2d(context.region, context.space_data.region_3d, a)
        #     blf.position(0, text_pos[0], text_pos[1], 0)
        #     blf.size(0, 50, 50)
        #     blf.color(0,255,255,255,125)
        #     blf.draw(0, f"Spline{idx}")

        cs = context.scene
        ec = cs.ecustom
        min_rows = 3
        row = layout.row()

        split = layout.split(factor=0.2)
        split.template_list("CUSTOM_UL_edges_Main","", cs, "ecustom", cs, "ecustom_index", rows=min_rows)
        
        if len(ec) > 0 and cs.ecustom_index != -1:
            user = ec[cs.ecustom_index]
            split.template_list(
                listtype_name = "CUSTOM_UL_edges_Sub",
                list_id = "",
                dataptr = user,
                propname = "vert_collection",
                active_dataptr = cs,
                active_propname = "ecustom_index",
                rows = min_rows
            )
        
        row1 = layout.row()
        draw_p(self, context)
        row1.operator('vnt.new_edge')
        row1.prop(cs, "curve_type")
        row1.operator('vnt.remove_edge')
        row2 = layout.row()
        row2.operator('vnt.new_vert')
        row2.operator('vnt.remove_vert')
        row3 = layout.row(align=True)
        row3.label(text="Vertex Coordinates")
        row3.prop(cs, "vertx")
        row3.prop(cs, "verty")
        row3.prop(cs, "vertz")

        if len(ec):
            layout.prop(ec[cs.ecustom_index], "color")
            layout.prop(ec[cs.ecustom_index], "size")
            draw_loc(context)
    
    def VNT_ST_boundary(self, layout, context):
        cs = context.scene
        layout=layout.box()
        data = cs.face_name

        # r0 = layout.row()
        # r0.label(text="Boundary Controls")

        r0 = layout.row()
        r0.prop(cs, "face_sel_mode", toggle=True)
        
        r1 = layout.row()
        r1.operator(VNT_OT_New_Boundary.bl_idname, text="New Boundary")

        # r1 = layout.row()
        
        # r1.label(text="Boundary Name:")
        # r1.prop(data, "facename")
        
        # r2 = layout.row()
        # r2.operator(VNT_OT_set_face_name.bl_idname, text="Set Boundary Name")
        
        # r3 = layout.row()
        # r3.label(text="Boundary Condition")
        # r3.prop(cs, "bdclist")
        
        # r4 = layout.row()
        # r4.operator(VNT_OT_set_type_face.bl_idname, text="Set Boundary Condition")
        
        # r4 = layout.row()
        # r4.scale_y = 1.4
        # r4.active_default = True
        # r4.operator(VNT_OT_faceactions.bl_idname, text="Add Boundary").action = "ADD"
        # r4.active_default = False
        
        # new line
        r2 = layout.row().grid_flow(row_major=True, columns=4, even_columns=False, align = True)
        
        r2.operator(VNT_OT_selectfaces.bl_idname, text="", icon="STICKY_UVS_LOC").select_all = True
        r2.operator(VNT_OT_selectfaces.bl_idname, text="", icon="STICKY_UVS_DISABLE").select_all = False
        r2.operator(VNT_OT_faceactions.bl_idname, text="", icon="REMOVE").action = "REMOVE"
        r2.alert = True
        r2.operator(VNT_OT_clearfaces.bl_idname, text="", icon="TRASH")
        r2.alert = True

        r3 = layout.row()
        r3.scale_y = 1.4
        r3.template_list("CUSTOM_UL_faces", "", cs, "fcustom", cs, "fcustom_index", rows=2)

    def VNT_ST_step_controls(self, layout, context):
        cs = context.scene
        layout = layout.box()
        
        row0 = layout.row()
        row0spt = row0.split(factor = 0.4)
        
        r0c1 = row0spt.row(align=True)
        r0c2 = row0spt.row(align=True)
        
        r0c1spt = r0c1.split(align=True)
        a = r0c1spt.row(align=True)
        b = r0c1spt.row(align=True)
        
        a.box().label(text="Snappy Hex Mesh Step Controls")

    def VNT_ST_run(self, layout, context):
        cs = context.scene
        layout = layout.box()
        
        row0 = layout.row()
        row0spt = row0.split(factor = 0.4)
        
        r0c1 = row0spt.row(align=True)
        r0c2 = row0spt.row(align=True)
        
        r0c1spt = r0c1.split(align=True)
        a = r0c1spt.row(align=True)
        b = r0c1spt.row(align=True)
        
        a.box().label(text="Run Utilities")

        sec1 = layout.row(align=True)
        sec1.scale_y = 1.4
        sec1.ui_units_y = 2.0
        sec1.prop(cs, "geo_design_options", expand=True)
        
        row = layout.row()
        row.active_default = True
        row.operator(VNT_OT_fill_dict_file.bl_idname, icon="FILE_TICK", text="Generate Blockmesh Dictionary")
        
        row.active_default = False
        row.alert = True
        row.operator(VNT_OT_cleardictfileonly.bl_idname, icon="TRASH", text="Clear Blockmesh Dictionary")
        row.ui_units_y = 1.7


class VNT_OT_active_project_indicator(Operator):
    """This Operator defines the instance of an active projec in the project manager.
    It is used to create horizontal tabs."""

    bl_label = ""
    bl_description = ""
    bl_idname = "vnt.active_project_indicator"
    filename_ext = ""

    active_file_id: StringProperty()
    
    def delay_funct(self):
        print("delaying")
    
    def execute(self, context):
        cs = context.scene
        
        for i in range(0, len(cs.mfile_item)):
            if cs.mfile_item[i].ITEM_identifier == self.active_file_id:
                index = i
                break
        
        cs.mfile_item_index = index
        
        return {'FINISHED'}
       
class VNT_OT_list_category(Operator):
    """This Operator is simply used for center aligned text category for UI List. 
    It plays no execution purpose."""

    bl_label = ""
    bl_description = ""
    bl_idname = "vnt.list_category"
  
    def execute(self, content):
        return {'FINISHED'}