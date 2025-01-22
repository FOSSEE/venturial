bl_info = {
    "name": "Venturial",
    "description": "A GUI to alleviate the effort of constructing OpenFOAM cases.",
    "author": "Rajdeep Adak at FOSSEE, IIT Bombay",
    "contributors": "visit www.github.com/venturial/contributors",
    "version": (0, 1, 0),
    "blender": (3, 2, 1),
    "location": "View3D > Side bar > Venturial",
    "category": "Development",
}

import bpy, bmesh, os
import bpy.utils.previews

from bpy.utils import register_class, unregister_class

from bpy.props import (
    IntProperty,
    FloatProperty,
    FloatVectorProperty,
    BoolProperty,
    StringProperty,
    PointerProperty,
    CollectionProperty,
    EnumProperty,
)

from bpy.types import Operator, Panel, AddonPreferences, PropertyGroup, UIList


from gpu_extras.batch import batch_for_shader
from bpy_extras.view3d_utils import location_3d_to_region_2d

from venturial.startup.get_tutorials_list import add_tutorials_to_scene
from venturial.startup.get_recents_list import add_recents_to_scene

from venturial.models.header.file_handling_operators import *
from venturial.models.header.developer_menu_operators import *
from venturial.models.header.general_operators import *
from venturial.models.header.help_menu_operators import *

from venturial.models.mainpanel_sublayout_operators import *
from venturial.models.blockmesh.design_operators import *
from venturial.models.visualizer_operators import (
    VNT_OT_vertex_data_control,
    VNT_OT_edge_data_control,
    VNT_OT_boundary_data_control,
)
# from venturial.models.blockmesh.edge_operators import *
from venturial.models.tutorials_menu_operators import *

# from venturial.models.geometry_designer_operators import *
# from venturial.models.mesh_file_manager_operators import *
from venturial.models.blockmesh.get_vertices_operators import *
from venturial.models.blockmesh.boundary_control_operators import *
from venturial.models.run_panel_operators import *

from venturial.views.schemas.UIList_schemas import *
from venturial.views.user_mode_view import VNT_PT_usermodeview
from venturial.views.header.view import *
from venturial.views.mainpanel.meshing_tools.blockmesh import VNT_PT_cell_location
from venturial.views.mainpanel.view import (
    VNT_OT_active_project_indicator,
    VNT_OT_list_category,
)
from venturial.views.mainpanel.tutorials import VNT_PT_filter_tutorials
from venturial.views.mainpanel.recents import VNT_PT_filter_recents
from venturial.views.mainpanel.visualizer import VNT_PT_statistics_settings

from venturial.utils.custom_icon_object_generator import (
    register_custom_icon,
    unregister_custom_icon,
)

from venturial.lib.update_methods import *
from venturial.lib.preferences_properties import VNT_user_preferences_collection
from venturial.lib.global_properties import VNT_global_properties_collection, VNT_global_properties_collection_edge_verts, CUSTOM_LocProps

from venturial.models.edges_panel_operators import *

classes = (
    VNT_user_preferences_collection,
    VNT_OT_save_preferences,
    VNT_OT_reset_preferences,
    VNT_OT_import_preferences,
    VNT_OT_new_case,
    VNT_OT_select_mesh_filepath,
    VNT_OT_build_mesh,
    VNT_OT_import_mesh,
    VNT_OT_open_case,
    VNT_OT_delete_mesh_file_items,
    VNT_OT_deactivate_mesh_file_item,
    VNT_OT_dev_mode,
    VNT_OT_dev_tools,
    VNT_OT_user_general_settings,
    VNT_OT_select_default_mesh_filepath,
    VNT_OT_select_default_tut_filepath,
    VNT_OT_select_default_user_data_filepath,
    VNT_OT_list_category,
    VNT_OT_venturial_maintools,
    VNT_OT_venturial_homepage,
    VNT_OT_fossee_homepage,
    VNT_OT_close_venturial,
    VNT_OT_user_guide,
    VNT_OT_developer_guide,
    VNT_OT_feature_request,
    VNT_OT_report_bugs,
    VNT_OT_developer_support,
    VNT_OT_user_community,
    VNT_OT_developer_community,
    VNT_OT_release_notes,
    VNT_PT_usermodeview,
    VNT_OT_mainpanel_layout,
    fileitemproperties,
    recent_item_properties,
    tutorialitemproperties,
    VNT_MT_dev_menu,
    VNT_MT_file_menu,
    VNT_PT_uicategory,
    VNT_MT_about_venturial,
    VNT_MT_about_fossee,
    VNT_MT_help_menu,
    CUSTOM_LocProps,
    VNT_global_properties_collection_edge_verts,
    VNT_global_properties_collection,
    VNT_UL_mesh_file_manager,
    VNT_UL_mesh_file_coroner,
    CUSTOM_UL_verts,
    CUSTOM_UL_blocks,
    CUSTOM_UL_faces,
    CUSTOM_UL_edges_Main,
    CUSTOM_UL_edges_Sub,
    VNT_OT_faceactions,
    VNT_OT_set_face_name,
    VNT_OT_set_type_face,
    VNT_PT_cell_location,
    VNT_OT_selectfaces,
    VNT_OT_clearfaces,
    VNT_OT_fill_dict_file,
    VNT_OT_cleardictfileonly,
    VNT_OT_New_Boundary,
    VNT_OT_vertactions,
    VNT_OT_add_update_verts,
    VNT_OT_select_unselect_allverts,
    VNT_OT_clearverts,
    VNT_PT_statistics_settings,
    VNT_OT_location_spawnner,
    VNT_OT_add_to_viewport,
    VNT_OT_compose,
    VNT_OT_get_blocks,
    VNT_OT_remove_blocks,
    VNT_OT_remove_all_blocks,
    VNT_OT_clearblocks,
    VNT_OT_blocksdatacontrol,
    VNT_OT_showselectedblocks,
    VNT_OT_select_unselect_allblocks,
    VNT_OT_vertex_data_control,
    VNT_OT_edge_data_control,
    VNT_OT_boundary_data_control,
    # VNT_OT_generate_edge,
    # VNT_OT_edit_edge,
    # VNT_OT_destroy_edge,
    VNT_OT_more_tutorials_viewer,
    VNT_OT_tutorial_viewer,
    VNT_PT_filter_tutorials,
    VNT_PT_filter_recents,
    VNT_OT_active_project_indicator,
    OBJECT_OT_add_single_vertex,
    VNT_OT_new_edge,
    VNT_OT_new_vert,
    VNT_OT_remove_edge,
    VNT_OT_remove_vert,
)


def register():

    register_custom_icon(
        "venturial_logo", "/venturial/icons/custom_icons/venturial_logo.png"
    )
    register_custom_icon("fossee_logo", "/venturial/icons/custom_icons/fossee_logo.png")
    register_custom_icon(
        "new_mesh_file_2", "/venturial/icons/custom_icons/new_mesh_file_2.png"
    )
    register_custom_icon(
        "build_mesh_2", "/venturial/icons/custom_icons/build_mesh_2.png"
    )
    register_custom_icon(
        "warning_sign_1", "/venturial/icons/custom_icons/warning_sign_1.png"
    )
    register_custom_icon(
        "file-browser-2", "/venturial/icons/custom_icons/file-browser-2.png"
    )

    for cls in classes:
        register_class(cls)

    bpy.types.Scene.search_tuts = StringProperty(default="Search Tutorials")
    bpy.types.Scene.search_recents = StringProperty(default="Search Recents")
    bpy.types.Scene.edit_dict_name = BoolProperty(default=True)

    bpy.types.Scene.current_tool_text = StringProperty(default="BlockMesh")
    bpy.types.Scene.meshing_tool = EnumProperty(
        items=[("BlockMesh", "BlockMesh", ""), ("SnappyHexMesh", "SnappyHexMesh", "")],
        default="BlockMesh",
        update=update_current_tool_text_1,
    )

    bpy.types.Scene.solution_tools = EnumProperty(
        items=[
            ("Solution Modeling", "Solution Modeling", ""),
            ("Post-Processing", "Post-Processing", ""),
        ],
        update=update_current_tool_text_2,
    )

    bpy.types.Scene.spawn_type = EnumProperty(
        items=[
            ("Grid", "Grid", ""),
            ("3D Cursor", "3D Cursor", ""),
            ("Center", "Center", ""),
        ],
        default="Grid",
    )

    bpy.types.Scene.prompt_meshing_tool = EnumProperty(
        default={"BlockMesh"},
        items=[("BlockMesh", "BlockMesh", ""), ("SnappyHexMesh", "SnappyHexMesh", "")],
        options={"ENUM_FLAG"},
        update=update_mesh_dict_names,
    )

    bpy.types.Scene.mainpanel_categories = EnumProperty(
        items=[
            ("Explore", "Explore", ""),
            ("Geometry", "Geometry", ""),
            ("Edges", "Edges", ""),
            #  ('Step Controls', 'Steps Controls', ''),
            ("Boundary", "Boundary", ""),
            ("Visualize", "Visualize", ""),
            ("Run", "Run", ""),
        ],
        default="Explore",
    )

    bpy.types.Scene.cellShapes = EnumProperty(
        items=[
            ("Hexahedron", "Hexahedron", ""),
            ("Wedge (Experimental)", "Wedge (Experimental)", ""),
            ("Prism", "Prism", ""),
            ("Pyramid (Experimental)", "Pyramid (Experimental)", ""),
            ("Tetrahedron (Experimental)", "Tetrahedron (Experimental)", ""),
            (
                "Tetrahedral wedge (Experimental)",
                "Tetrahedral wedge (Experimental)",
                "",
            ),
        ],
        default="Hexahedron",
        description="Cell Shape Types",
    )

    bpy.types.Scene.cellShape_units = IntProperty(min=1, max=50, default=1)

    bpy.types.Scene.bm_dict_name = StringProperty(default="blockMeshDict")
    bpy.types.Scene.shm_dict_name = StringProperty()

    bpy.types.Scene.pref_pointer = bpy.props.PointerProperty(
        type=VNT_user_preferences_collection
    )

    bpy.types.Scene.mfile_item_ptr = bpy.props.PointerProperty(type=fileitemproperties)
    bpy.types.Scene.mfile_item = CollectionProperty(type=fileitemproperties)
    bpy.types.Scene.mfile_item_index = IntProperty(update=update_uicategory_mode)

    bpy.types.Scene.tut_item_ptr = bpy.props.PointerProperty(
        type=tutorialitemproperties
    )
    bpy.types.Scene.tut_item = CollectionProperty(type=tutorialitemproperties)
    bpy.types.Scene.tut_item_index = IntProperty()

    bpy.types.Scene.rec_item_ptr = bpy.props.PointerProperty(
        type=recent_item_properties
    )
    bpy.types.Scene.rec_item = CollectionProperty(type=recent_item_properties)
    bpy.types.Scene.rec_item_index = IntProperty()

    bpy.types.Scene.mesh_dict_path = StringProperty()
    bpy.types.Scene.row_en = BoolProperty(default=True)

    bpy.types.Scene.cell_x = IntProperty(
        name="X: ",
        description="Select Number of cells along X",
        min=1,
        max=1000,
        default=1,
        update=update_cellxyz,
    )

    bpy.types.Scene.cell_y = IntProperty(
        name="Y: ",
        description="Select Number of cells along Y",
        min=1,
        max=1000,
        default=1,
        update=update_cellxyz,
    )

    bpy.types.Scene.cell_z = IntProperty(
        name="Z: ",
        description="Select Number of cells along Z",
        min=1,
        max=1000,
        default=1,
        update=update_cellxyz,
    )

    bpy.types.Scene.ctm = FloatProperty(
        name="Convert To Meters:",
        description="Set converttoMeters parameter of Blockmeshdict",
        min=0.001,
        max=100.0,
        default=0.1,
    )

    bpy.types.Scene.transform = BoolProperty(default=False)

    bpy.types.Scene.transformation_methods = EnumProperty(
        items=[
            ("Move", "Move (G)", "Shortcut: G"),
            ("Rotate", "Rotate (R)", "Shortcut: R"),
            ("Scale", "Scale (S)", "Shortcut: S"),
        ],
        default="Move",
    )

    bpy.types.Scene.snapping = BoolProperty(default=False, update=update_snapping)

    bpy.types.Scene.snapping_methods = EnumProperty(
        items=[("VERTEX", "Vertex", ""), ("EDGE", "Edge", ""), ("FACE", "Face", "")],
        default="VERTEX",
        update=update_snapping_method,
    )

    bpy.types.Scene.simblk = CollectionProperty(type=VNT_global_properties_collection)
    bpy.types.Scene.simblk_index = IntProperty()

    bpy.types.Scene.bcustom = CollectionProperty(type=VNT_global_properties_collection)
    bpy.types.Scene.bcustom_index = IntProperty()

    bpy.types.Scene.vcustom = CollectionProperty(type=VNT_global_properties_collection)
    bpy.types.Scene.vcustom_index = IntProperty()

    bpy.types.Scene.fcustom = CollectionProperty(type=VNT_global_properties_collection)
    bpy.types.Scene.fcustom_index = IntProperty()

    bpy.types.Scene.ecustom = CollectionProperty(type=VNT_global_properties_collection_edge_verts)
    bpy.types.Scene.ecustom_index = IntProperty()

    bpy.types.Scene.vert_index = IntProperty(name="Vertex Index", default=0)

    bpy.types.Scene.edge_control_methods = EnumProperty(
        items=[("IP", "Interpolation Points", ""), ("AA", "Axis angle", "")],
        default="IP",
    )

    bpy.types.Scene.curve_type = EnumProperty(
        items=[
            ("ARC", "Arc", "Arc type of edge"),
            ("PLY", "Polyline", "Polyline type of edge"),
            ("SPL", "Spline", "Spline type of edge"),
            ("BSPL", "BSpline", "BSpline type of edge"),
        ],
        default="ARC",
    )

    bpy.types.Scene.cnt = IntProperty()

    bpy.types.Scene.mode = EnumProperty(
        items=[
            ("OBJECT", "Object Mode", "", "OBJECT_DATAMODE", 1),
            ("VERT", "Vertex Mode", "", "VERTEXSEL", 2),
            ("FACE", "Face Mode", "", "FACESEL", 3),
            ("EDGE", "Edge Mode", "", "EDGESEL", 4),
        ],
        default="OBJECT",
        update=update_mode,
    )

    bpy.types.Scene.bdclist = EnumProperty(
        name="",
        description="Select Boundary Condition",
        items=[
            ("wedge", "wedge", ""),
            ("empty", "empty", ""),
            ("symmetryPlane", "symmetryPlane", ""),
            ("wall", "wall", ""),
            ("patch", "patch", ""),
        ],
    )

    bpy.types.Scene.face_name = PointerProperty(type=VNT_global_properties_collection)
    bpy.types.Scene.facedes = PointerProperty(type=VNT_global_properties_collection)

    bpy.types.Scene.acustom = CollectionProperty(type=VNT_global_properties_collection)
    bpy.types.Scene.acustom_index = IntProperty()

    bpy.types.Scene.pcustom = CollectionProperty(type=VNT_global_properties_collection)
    bpy.types.Scene.pcustom_index = IntProperty()

    bpy.types.Scene.scustom = CollectionProperty(type=VNT_global_properties_collection)
    bpy.types.Scene.scustom_index = IntProperty()

    bpy.types.Scene.bscustom = CollectionProperty(type=VNT_global_properties_collection)
    bpy.types.Scene.bscustom_index = IntProperty()

    bpy.types.Scene.ipcnt = IntProperty(
        name="IP: ",
        description="Select Number of Interpolation Points",
        min=1,
        max=30,
        default=1,
    )

    bpy.types.Scene.face_sel_mode = BoolProperty(default=False, update=update_face_mode)

    bpy.types.Scene.statistics = BoolProperty(default=False)

    bpy.types.Scene.bfc = BoolProperty(default=False, description="Backface Culling")

    bpy.types.Scene.xray = BoolProperty(default=False, description="X ray mode")

    bpy.types.Scene.xray_opacity = FloatProperty(
        name="X-ray opacity", description="X-ray opacity", min=0.0, max=1.0, default=0.5
    )

    bpy.types.Scene.geo_params = EnumProperty(
        description="Geometry parameters",
        items=[
            ("Center", "Center", ""),
            ("Orientation", "Orientation", ""),
            ("Outline", "Outline", ""),
        ],
        default={"Center", "Orientation", "Outline"},
        options={"ENUM_FLAG"},
    )

    bpy.types.Scene.outline_color = FloatVectorProperty(
        name="Outline Color",
        subtype="COLOR",
        size=4,
        min=0.0,
        max=1.0,
        default=(0.0, 0.5, 0.0, 1.0),
    )

    bpy.types.Scene.shading = EnumProperty(
        description="Geometry Shading",
        items=[("Solid", "Solid", ""), ("Wire", "Wire", "")],
    )

    bpy.types.Scene.wire_opacity = FloatProperty(
        name="Wire opacity", description="Wire opacity", min=0.0, max=1.0, default=0.5
    )

    bpy.types.Scene.enable_vert_vis = BoolProperty(name="")
    bpy.types.Scene.enable_edge_vis = BoolProperty(name="")
    bpy.types.Scene.enable_bound_vis = BoolProperty(name="")

    bpy.types.Scene.vert_order = BoolProperty(name="")

    bpy.types.Scene.vert_props = EnumProperty(
        description="Vertex visualization properties",
        items=[("Indices", "Indices", ""), ("Coordinates", "Coordinates", "")],
        default={"Indices"},
        options={"ENUM_FLAG"},
    )

    bpy.types.Scene.vert_source = EnumProperty(
        description="Vertex visualization properties",
        items=[("Geometry", "Geometry", ""), ("blockmeshdict", "blockmeshdict", "")],
        default="Geometry",
    )

    bpy.types.Scene.vert_text_size = IntProperty(
        name="Text Size:",
        description="Select Size of Vertex Info Text being Displayed",
        min=6,
        max=100,
        default=40,
    )

    bpy.types.Scene.vert_text_color = FloatVectorProperty(
        name="Text Color",
        subtype="COLOR",
        size=4,
        min=0.0,
        max=1.0,
        default=(0.0, 0.0, 1.0, 1.0),
    )

    bpy.types.Scene.active_projects = EnumProperty(
        description="horizontally placed dynamic list of active projects in the project manager.",
        items=get_active_projects,
    )

    bpy.app.handlers.load_factory_startup_post.append(add_tutorials_to_scene)
    bpy.app.handlers.load_factory_startup_post.append(add_recents_to_scene)


def unregister():

    for cls in reversed(classes):
        unregister_class(cls)

    unregister_custom_icon(
        "venturial_logo", "/venturial/icons/custom_icons/venturial_logo.png"
    )
    unregister_custom_icon(
        "fossee_logo", "/venturial/icons/custom_icons/fossee_logo.png"
    )
    unregister_custom_icon(
        "new_mesh_file_2", "/venturial/icons/custom_icons/new_mesh_file_2.png"
    )
    unregister_custom_icon(
        "build_mesh_2", "/venturial/icons/custom_icons/build_mesh_2.png"
    )
    unregister_custom_icon(
        "warning_sign_1", "/venturial/icons/custom_icons/warning_sign_1.png"
    )
    unregister_custom_icon(
        "file-browser-2", "/venturial/icons/custom_icons/file-browser-2.png"
    )

    del bpy.types.Scene.ui_category
    del bpy.types.Scene.tool_type
    del bpy.types.Scene.prompt_meshing_tool
    del bpy.types.Scene.scene_blockmesh_panel_categories
    del bpy.types.Scene.test_enum
    del bpy.types.Scene.cellShapes
    del bpy.types.Scene.cellShape_units
    del bpy.types.Scene.mfile_item_ptr
    del bpy.types.Scene.mfile_item
    del bpy.types.Scene.mfile_item_index
    del bpy.types.Scene.mesh_dict_name
    del bpy.types.Scene.mesh_dict_path
    del bpy.types.Scene.row_en
    del bpy.types.Scene.cell_x
    del bpy.types.Scene.cell_y
    del bpy.types.Scene.cell_z
    del bpy.types.Scene.ctm
    del bpy.types.Scene.transform
    del bpy.types.Scene.transformation_methods
    del bpy.types.Scene.snapping
    del bpy.types.Scene.snapping_methods
    del bpy.types.Scene.simblk
    del bpy.types.Scene.simblk_index
    del bpy.types.Scene.bcustom
    del bpy.types.Scene.bcustom_index
    del bpy.types.Scene.vcustom
    del bpy.types.Scene.vcustom_index
    del bpy.types.Scene.fcustom
    del bpy.types.Scene.fcustom_index
    del bpy.types.Scene.ecustom
    del bpy.types.Scene.ecustom_index
    del bpy.types.Scene.vert_index
    del bpy.types.Scene.cnt
    del bpy.types.Scene.mode
    del bpy.types.Scene.bdclist
    del bpy.types.Scene.face_name
    del bpy.types.Scene.facedes
    del bpy.types.Scene.acustom
    del bpy.types.Scene.acustom_index
    del bpy.types.Scene.pcustom
    del bpy.types.Scene.pcustom_index
    del bpy.types.Scene.scustom
    del bpy.types.Scene.scustom_index
    del bpy.types.Scene.bscustom
    del bpy.types.Scene.bscustom_index
    del bpy.types.Scene.ipcnt
    del bpy.types.Scene.edgelist
    del bpy.types.Scene.face_sel_mode
