from bpy.props import (IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       BoolProperty,
                       StringProperty,
                       PointerProperty,
                       CollectionProperty,
                       EnumProperty)

from bpy.types import PropertyGroup

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

