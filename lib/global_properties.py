from bpy.props import (IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       BoolProperty,
                       StringProperty,
                       PointerProperty,
                       CollectionProperty,
                       EnumProperty)
import bpy

from bpy.types import PropertyGroup

from venturial.models.blockmesh.boundary_control_operators import list_current_faces

class CUSTOM_LocProps(bpy.types.PropertyGroup):
    vert_loc: FloatVectorProperty(name='verts')

def color_change(self,context):
    return

def size_change(self,context):
    return

class VNT_global_properties_collection_edge_verts(bpy.types.PropertyGroup):
    vert_collection: CollectionProperty(
        name = "Vert Collection",
        type = CUSTOM_LocProps)
    vertex_col: CollectionProperty(
        name = "Vert Collection for changing and storing intermediate values",
        type = CUSTOM_LocProps)
    vc: CollectionProperty(
        name = "Storing intermediate values",
        type = CUSTOM_LocProps)
    color : FloatVectorProperty(
                 name = "Color Picker",
                 subtype = "COLOR",
                 size = 4,
                 min = 0.0,
                 max = 1.0,
                 default = (1.0,1.0,1.0,1.0),
                 update = color_change)
    size : IntProperty(name="size",default=1,min=1,max=5,update=size_change)
    edge_type: EnumProperty(
        name="Edge Types",
        description="Types of edges supported by OpenFOAM",
        items=[
            ("ARC", "Arc", "Arc type of edge"),
            ("PLY", "Polyline", "Polyline type of edge"),
            ("SPL", "Spline", "Spline type of edge"),
            ("BSPL", "BSpline", "BSpline type of edge"),
        ],
    ) 

class VNT_global_properties_collection(PropertyGroup): 
    
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
    
    master_face : EnumProperty("Master Face", items=list_current_faces)
    slave_face : EnumProperty("Slave Face", items=list_current_faces)
    
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

    vert_collection: CollectionProperty(
        name = "Vert Collection",
        type = CUSTOM_LocProps)
    vertex_col: CollectionProperty(
        name = "Vert Collection for changing and storing intermediate values",
        type = CUSTOM_LocProps)
    vc: CollectionProperty(
        name = "Storing intermediate values",
        type = CUSTOM_LocProps)
    color : FloatVectorProperty(
                 name = "Color Picker",
                 subtype = "COLOR",
                 size = 4,
                 min = 0.0,
                 max = 1.0,
                 default = (1.0,1.0,1.0,1.0),
                 update = color_change)
    size : IntProperty(name="size",default=1,min=1,max=5,update=size_change)

    edge_type: EnumProperty(
        name="Edge Types",
        description="Types of edges supported by OpenFOAM",
        items=[
            ("ARC", "Arc", "Arc type of edge"),
            ("PLY", "Polyline", "Polyline type of edge"),
            ("SPL", "Spline", "Spline type of edge"),
            ("BSPL", "BSpline", "BSpline type of edge"),
        ],
    ) 
    edge_verts: CollectionProperty(type=VNT_global_properties_collection_edge_verts)