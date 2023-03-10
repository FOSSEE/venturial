bl_info = {"name": "Venturial",
           "description": "A GUI to alleviate the effort of constructing OpenFOAM cases.",
           "author": "Rajdeep Adak at FOSSEE, IIT Bombay",
           "contributors": "visit www.github.com/venturial/contributors", 
           "version": (0, 1, 0),
           "blender": (3, 2, 1),
           "location": "View3D > Side bar > Venturial",
           "category": "Development"}

import bpy, bmesh
import bpy.utils.previews

from bpy.utils import register_class, unregister_class

from bpy.props import (IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       BoolProperty,
                       StringProperty,
                       PointerProperty,
                       CollectionProperty,
                       EnumProperty)

from bpy.types import (Operator,
                       Panel,
                       AddonPreferences,
                       PropertyGroup,
                       UIList)
                       

from gpu_extras.batch import batch_for_shader
from bpy_extras.view3d_utils import location_3d_to_region_2d

from venturial.models.header.file_handling_operators import *
from venturial.models.header.developer_menu_operators import *
from venturial.models.header.general_operators import *
from venturial.models.header.help_menu_operators import *

from venturial.models.blockmesh.layout_operators import *
from venturial.models.blockmesh.design_operators import *
# from venturial.models.geometry_designer_operators import *
# from venturial.models.mesh_file_manager_operators import *
# from venturial.models.get_vertices_operators import *
# from venturial.models.boundary_control_operators import *
# from venturial.models.run_panel_operators import *

from venturial.views.user_mode_view import VNT_PT_usermodeview
from venturial.views.header.view import *
from venturial.views.schemas.UIList_schemas import *

from venturial.utils.custom_icon_object_generator import register_custom_icon, unregister_custom_icon

class CUSTOM_objectCollection(PropertyGroup): 
    
    vertindex : StringProperty()
    
    face_des : StringProperty()
    face_type : EnumProperty(name= "",
                             description= "Type of Face (pre-defined)",
                             items= [('None', "None", ""),
                                     ('empty', "empty", ""),
                                     ('symmetryPlane', "symmetryPlane", ""),
                                     ('patch', "patch", ""),
                                     ('wedge', "wedge", ""),
                                     ('wall', "wall", "")])
                                     
    face_clr : FloatVectorProperty(name = "Face Color",
                                   subtype = "COLOR",
                                   size = 4,
                                   min = 0.0,
                                   max = 1.0,
                                   default = (1.0,1.0,1.0,1.0))
                           
    
    b_name: StringProperty()
    setcellx: IntProperty()
    setcelly: IntProperty()
    setcellz: IntProperty()
    
    grading: StringProperty()
    
    index: IntProperty()
        
    vertptx: FloatProperty()
    vertpty: FloatProperty()
    vertptz: FloatProperty()
    
    fandl : StringProperty()
    intptx : FloatProperty()
    intpty : FloatProperty()
    intptz : FloatProperty()
       
    path : StringProperty(name="",
                          description="Path to Directory",
                          default='',
                          maxlen=1024,
                          subtype='DIR_PATH')
        
    dictname : StringProperty(name="",
                              description="Name of File:",
                              default='',
                              maxlen=1024)
        
    objname : StringProperty(name="",
                             description="Name of Geometry",
                             default='',
                             maxlen=1024) 
    
    facename : StringProperty(name="",
                              description="Name of Face",
                              default='',
                              maxlen=1024)    
    
    enabled : BoolProperty()
    
    faceindex : StringProperty()
    blkindex: StringProperty()



classes = (VNT_OT_new_mesh_file,
           VNT_OT_select_mesh_filepath, 
           VNT_OT_build_mesh,
           VNT_OT_import_mesh, 
           VNT_OT_save_mesh,
           VNT_OT_new_case,
           VNT_OT_open_case,
           VNT_OT_see_older,
           VNT_OT_delete_mesh_file_items,
           VNT_OT_dev_mode,
           VNT_OT_dev_tools,
           VNT_OT_user_general_settings,
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
           VNT_OT_blockmesh_panel_layout_options,
           fileitemproperties,
           VNT_MT_dev_menu,
           VNT_MT_file_menu,
           VNT_PT_uicategory,
           VNT_MT_about_venturial,
           VNT_MT_about_fossee,
           VNT_MT_help_menu,
           CUSTOM_objectCollection,
           VNT_UL_mesh_file_manager,
           VNT_UL_mesh_file_coroner,
           VNT_OT_add_to_viewport,
           VNT_OT_compose,
           VNT_OT_get_blocks,
           VNT_OT_remove_blocks,
           VNT_OT_remove_all_blocks,
           VNT_OT_clearblocks,
           VNT_OT_blocksdatacontrol,
           VNT_OT_showselectedblocks,
           VNT_OT_select_unselect_allblocks)


def update_prompt_meshing_tool(self, context):
        context.scene.tool_type = self.prompt_meshing_tool
        context.scene.mesh_dict_name = 'blockMeshDict' if self.prompt_meshing_tool == 'BlockMesh' else 'snappyHexMeshDict'

def update_snapping(self, context):
    bpy.context.scene.tool_settings.use_snap = context.scene.snapping
    if context.scene.snapping == True:
        bpy.context.scene.tool_settings.snap_elements = {context.scene.snapping_methods}
        
def update_snapping_method(self, context):
    bpy.context.scene.tool_settings.snap_elements = {context.scene.snapping_methods}
    
def update_cellxyz(self, context):
    
    scn = context.scene
    for i in range(0, len(scn.bcustom)):
        if scn.bcustom[i].enabled:
            scn.bcustom[i].setcellx = self.cell_x
            scn.bcustom[i].setcelly = self.cell_y
            scn.bcustom[i].setcellz = self.cell_z
            
def update_mode(self, context):
    bpy.ops.object.mode_set(mode = 'EDIT' if self.mode != 'OBJECT' else self.mode)
    if self.mode != 'OBJECT': bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type=self.mode, action='TOGGLE')
    
    
def update_face_mode(self, context):
    if self.face_sel_mode == True:
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE', action='TOGGLE')
        obj = context.edit_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        
        for f in bm.faces:
            f.select = False
        bm.select_flush_mode()   
        me.update()
        
    else:
        bpy.ops.object.mode_set(mode = 'OBJECT')
        

def update_uicategory_mode(self, context):
    
    context.scene.ui_category = self.tool_type
    

def test_enum_update(self, context):
    print(self.test_enum)


def register():  
    
    register_custom_icon("venturial_logo", "/venturial/icons/custom_icons/venturial_logo.png")
    register_custom_icon("fossee_logo", "/venturial/icons/custom_icons/fossee_logo.png")
    register_custom_icon("new_mesh_file_2", "/venturial/icons/custom_icons/new_mesh_file_2.png")
    register_custom_icon("build_mesh_2", "/venturial/icons/custom_icons/build_mesh_2.png")
    
    for cls in classes:
        register_class(cls)
    
    bpy.types.Scene.ui_category = StringProperty(default="BlockMesh")
    
    bpy.types.Scene.tool_type = EnumProperty(items = [("BlockMesh", "BlockMesh", ""),
                                                      ("SnappyHexMesh", "SnappyHexMesh", ""),
                                                      ("Simulation", "Simulation", ""),
                                                      ("Post-Processing", "Post-Processing", "")],
                                                     default = "BlockMesh",
                                                     update = update_uicategory_mode)
    
    
    bpy.types.Scene.prompt_meshing_tool = EnumProperty(default = 'BlockMesh',
                                                       items = [('BlockMesh', 'BlockMesh', ''),
                                                                ('SnappyHexMesh', 'SnappyHexMesh', '')],
                                                       update = update_prompt_meshing_tool)

    
    bpy.types.Scene.scene_blockmesh_panel_categories = EnumProperty(items = [('Recents', 'Recents', ''),
                                                                             ('Design', 'Design', ''),
                                                                             ('Edges', 'Edges', ''),
                                                                             ('Visualize', 'Visualize', ''),
                                                                             ('Run', 'Run', '')],
                                                                    default = 'Recents')
    
    bpy.types.Scene.test_enum = EnumProperty(items = [('Recents', 'Recents', ''),
                                                      ('Design', 'Design', ''),
                                                      ('Edges', 'Edges', ''),
                                                      ('Visualize', 'Visualize', ''),
                                                      ('Run', 'Run', '')],
                                                      default = {'Recents'},
                                                      options = {'ENUM_FLAG'},
                                                      update=test_enum_update)
    
    bpy.types.Scene.cellShapes = EnumProperty(items = [('summon_hexahedrons', 'Hexahedron', ''),
                                                       ('summon_wedges', 'Wedge (Experimental)', ''),
                                                       ('summon_prisms', 'Prism', ''),
                                                       ('summon_pyramid', 'Pyramid (Experimental)', ''),
                                                       ('summon_tetrahedron', 'Tetrahedron (Experimental)', ''),
                                                       ('summon_tetrahedral_wedge', 'Tetrahedral wedge (Experimental)', '')],
                                              default = 'summon_hexahedrons',
                                              description = "Cell Shape Types")
    
    bpy.types.Scene.cellShape_units = IntProperty(min=1,
                                                  max=50,
                                                  default=1)
    
    
    bpy.types.Scene.mfile_item_ptr = bpy.props.PointerProperty(type=fileitemproperties)
    bpy.types.Scene.mfile_item = CollectionProperty(type=fileitemproperties)    
    bpy.types.Scene.mfile_item_index = IntProperty()
    
    bpy.types.Scene.mesh_dict_name = StringProperty()
    bpy.types.Scene.mesh_dict_path = StringProperty()
    bpy.types.Scene.row_en = BoolProperty(default=True)
    
    bpy.types.Scene.cell_x = IntProperty(name = "X: ", 
                                         description = "Select Number of cells along X",
                                         min = 1,
                                         max = 1000,
                                         default = 1,
                                         update = update_cellxyz)
                                         
    bpy.types.Scene.cell_y = IntProperty(name = "Y: ", 
                                         description = "Select Number of cells along Y",
                                         min = 1,
                                         max = 1000,
                                         default = 1,
                                         update = update_cellxyz)
                                         
    bpy.types.Scene.cell_z = IntProperty(name = "Z: ", 
                                         description = "Select Number of cells along Z",
                                         min = 1,
                                         max = 1000,
                                         default = 1,
                                         update = update_cellxyz)
                                         
    bpy.types.Scene.ctm = FloatProperty(name = "Convert To Meters:", 
                                        description = "Set converttoMeters parameter of Blockmeshdict",
                                        min = 0.001,
                                        max = 100.0,
                                        default = 0.1)
    
    bpy.types.Scene.transform = BoolProperty(default=False)
    
    bpy.types.Scene.transformation_methods = EnumProperty(items = [('Move', 'Move (G)', 'Shortcut: G'),
                                                                   ('Rotate', 'Rotate (R)', 'Shortcut: R'),
                                                                   ('Scale', 'Scale (S)', 'Shortcut: S')],
                                                          default = 'Move')
    
    bpy.types.Scene.snapping = BoolProperty(default=False, update=update_snapping)
    
    bpy.types.Scene.snapping_methods = EnumProperty(items = [('VERTEX', 'Vertex', ''),
                                                             ('EDGE', 'Edge', ''),
                                                             ('FACE', 'Face', '')],
                                                    default = 'VERTEX',
                                                    update = update_snapping_method)
    
    bpy.types.Scene.simblk = CollectionProperty(type=CUSTOM_objectCollection)
    bpy.types.Scene.simblk_index = IntProperty()
    
        
    bpy.types.Scene.bcustom = CollectionProperty(type=CUSTOM_objectCollection)
    bpy.types.Scene.bcustom_index = IntProperty()
    
    bpy.types.Scene.vcustom = CollectionProperty(type=CUSTOM_objectCollection)
    bpy.types.Scene.vcustom_index = IntProperty()
    
    bpy.types.Scene.fcustom = CollectionProperty(type=CUSTOM_objectCollection)
    bpy.types.Scene.fcustom_index = IntProperty()
    
    
    bpy.types.Scene.cnt = IntProperty()
    
    
    bpy.types.Scene.mode = EnumProperty(items = [('OBJECT', 'Object Mode', '', 'OBJECT_DATAMODE', 1),
                                                 ('VERT', 'Vertex Mode', '', 'VERTEXSEL', 2),
                                                 ('FACE', 'Face Mode', '', 'FACESEL', 3),
                                                 ('EDGE', 'Edge Mode', '', 'EDGESEL', 4)],
                                        default = 'OBJECT',
                                        update=update_mode)
    
    bpy.types.Scene.bdclist = EnumProperty(name= "",
                                           description= "Select Boundary Condition",
                                           items= [('wedge', "wedge", ""),
                                                   ('empty', "empty", ""),
                                                   ('symmetryPlane', "symmetryPlane", ""),
                                                   ('wall', "wall", ""),
                                                   ('patch', "patch", "")])
    
    bpy.types.Scene.face_name = PointerProperty(type=CUSTOM_objectCollection)
    bpy.types.Scene.facedes = PointerProperty(type=CUSTOM_objectCollection)
    
    
    bpy.types.Scene.acustom = CollectionProperty(type=CUSTOM_objectCollection)
    bpy.types.Scene.acustom_index = IntProperty()
    
    bpy.types.Scene.pcustom = CollectionProperty(type=CUSTOM_objectCollection)
    bpy.types.Scene.pcustom_index = IntProperty()
    
    bpy.types.Scene.scustom = CollectionProperty(type=CUSTOM_objectCollection)
    bpy.types.Scene.scustom_index = IntProperty()
    
    bpy.types.Scene.bscustom = CollectionProperty(type=CUSTOM_objectCollection)
    bpy.types.Scene.bscustom_index = IntProperty()
    
    bpy.types.Scene.ipcnt = IntProperty(name = "IP: ", 
                                        description = "Select Number of Interpolation Points",
                                        min = 1,
                                        max = 30,
                                        default = 1)

    bpy.types.Scene.edgelist = EnumProperty(name= "",
                                            description= "Type of Edge (pre-defined)",
                                            items= [('arc', "arc", ""),
                                                    ('polyLine', "polyLine", ""),
                                                    ('spline', "spline", ""),
                                                    ('BSpline', "BSpline", "")])
    
    bpy.types.Scene.face_sel_mode = BoolProperty(default=False, update=update_face_mode)
    
    
def unregister():
    
    for cls in reversed(classes):
        unregister_class(cls)
    
    unregister_custom_icon("venturial_logo", "/venturial/icons/custom_icons/venturial_logo.png")
    unregister_custom_icon("fossee_logo", "/venturial/icons/custom_icons/fossee_logo.png")
    unregister_custom_icon("new_mesh_file_2", "/venturial/icons/custom_icons/new_mesh_file_2.png")
    unregister_custom_icon("build_mesh_2", "/venturial/icons/custom_icons/build_mesh_2.png")
    

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
    
    
    
    
    
    
    
    
        
    
    # del bpy.types.Scene.category 
    # del bpy.types.Scene.category_expand 
    # del bpy.types.Scene.meshing_tool_type 
    # del bpy.types.Scene.non_meshing_tool_type

    # del bpy.types.Scene.geo_design_options 
    # del bpy.types.Scene.cellShapes 
    # del bpy.types.Scene.cellShape_units 
                                         
    # del bpy.types.Scene.mfile_item_ptr 
    # del bpy.types.Scene.mfile_item 
    # del bpy.types.Scene.mfile_item_index 
    
    # del bpy.types.Scene.mesh_dict_name 
    # del bpy.types.Scene.mesh_dict_path 
    # del bpy.types.Scene.row_en
    
    # del bpy.types.Scene.cell_x                        
    # del bpy.types.Scene.cell_y 
    # del bpy.types.Scene.cell_z                        
    # del bpy.types.Scene.ctm
                       
    # del bpy.types.Scene.transform     
    # del bpy.types.Scene.transformation_methods
                                          
    # del bpy.types.Scene.snapping    
    # del bpy.types.Scene.snapping_methods 
                                                                                 
    # del bpy.types.Scene.simblk 
    # del bpy.types.Scene.simblk_index 
    
    # del bpy.types.Scene.bcustom 
    # del bpy.types.Scene.bcustom_index 
    
    # del bpy.types.Scene.mode
    
    # del bpy.types.Scene.vcustom
    # del bpy.types.Scene.vcustom_index
    
    # del bpy.types.Scene.fcustom
    # del bpy.types.Scene.fcustom_index
    
    # del bpy.types.Scene.bdclist
    # del bpy.types.Scene.face_name
    # del bpy.types.Scene.facedes
    
    # del bpy.types.Scene.acustom 
    # del bpy.types.Scene.acustom_index 
     
    # del bpy.types.Scene.pcustom 
    # del bpy.types.Scene.pcustom_index 
     
    # del bpy.types.Scene.scustom 
    # del bpy.types.Scene.scustom_index 
     
    # del bpy.types.Scene.bscustom 
    # del bpy.types.Scene.bscustom_index 
    
    # del bpy.types.Scene.ipcnt
    # del bpy.types.Scene.edgelist
    
    # del bpy.types.Scene.face_sel_mode