from bpy.props import (IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       BoolProperty,
                       StringProperty,
                       PointerProperty,
                       CollectionProperty,
                       EnumProperty)

from bpy.types import PropertyGroup
from venturial.utils.default_properties import default_properties

class VNT_user_preferences_collection(PropertyGroup):
    
    default_path_checkbox : BoolProperty(description="Enable to set default new mesh file location.",
                                         default = getattr(default_properties(), "load_user_preferences")("default_path_checkbox"))
    
    default_mesh_dict_path : StringProperty(description="Default new mesh file location.",
                                            default = getattr(default_properties(), "load_user_preferences")("default_mesh_dict_path"))

    default_tut_path_checkbox : BoolProperty(description="Enable to set default tutorials directory",
                                             default = getattr(default_properties(), "load_user_preferences")("default_tut_path_checkbox"))
    
    default_tutorials_dir : StringProperty(description="Location of Tutorial files",
                                           default = getattr(default_properties(), "load_user_preferences")("default_tutorials_dir"))
    
    default_user_data_path_checkbox: BoolProperty(description="Enable to set default user data directory",
                                                  default = getattr(default_properties(), "load_user_preferences")("default_user_data_path_checkbox"))
     
    default_user_data_path: StringProperty(description="Location of User data files",
                                           default = getattr(default_properties(), "load_user_preferences")("default_user_data_path"))