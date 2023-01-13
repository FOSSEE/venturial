from bpy.types import (UIList, PropertyGroup)
from bpy.props import StringProperty, BoolProperty, IntProperty

class SP_UL_mesh_file_manager(UIList):
    """Callable class for mesh file manager"""
    
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        """Method to define schema of a file manager item"""
        cs = context.scene
        row = layout.box().row()
        row.scale_y = 0.68
        
        row.label(text="", icon = "EVENT_B" if item.ITEM_type == "BlockMesh" else "EVENT_S")
        row.prop(item, "ITEM_name", text="", emboss=False)
        row.prop(item, "ITEM_location", text="", emboss=True)
        #row.prop(cs.mfile_item_ptr, "ITEM_history")

class SP_UL_mesh_file_coroner(UIList):
    """Callable class for mesh file coroner"""
    
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        """Method to define schema of a file manager item"""
        cs = context.scene
        row = layout.box().row()
        row.scale_y = 0.68
 
        row.prop(item, "ITEM_select", text="")
        row.label(text="", icon = "EVENT_B" if item.ITEM_type == "BlockMesh" else "EVENT_S")
        row.prop(item, "ITEM_name", text="", emboss=False)
        row.prop(item, "ITEM_location", text="", emboss=True)

class fileitemproperties(PropertyGroup):
    """Property attributes of a file item managed by mesh file manager"""
    ITEM_select : BoolProperty()
    ITEM_index : IntProperty()
    ITEM_type : StringProperty()
    ITEM_name : StringProperty()
    ITEM_location : StringProperty(subtype="DIR_PATH")
    ITEM_history : StringProperty()
   
    
class CUSTOM_UL_verts(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        row = layout.row() 
        #row.scale_y = 0.68
        split = row.split(factor=0.2)
        
        r1 = split.column()
        r2 = split.column()
        
        r1.prop(item, "enabled", text="", index=index)
        
        
        r2split = r2.split(factor = 0.3)
        r2c1 = r2split.column()
        r2c2 = r2split.column()
        
        r2c1.prop(item, "vertindex", text="", emboss=False, translate=False)
        r2c2.prop(item, "name", text="", emboss=False, translate=False)
        
    def invoke(self, context, event):
        pass
    
    
# UIList for Blocks
class CUSTOM_UL_blocks(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        box = layout.box()
        col = box.column()
        
        row = col.split(factor=0.12)
        row.scale_y = 0.68
        row.prop(item, "b_name", text="", emboss=False, translate=False)
        
        row = row.split(factor=0.33)
        row.prop(item, "name", text="", emboss=False, translate=False)
        
        row = row.split(factor=0.45)
        row.prop(item, "grading", text="", emboss=False, translate=False, expand = False)
        
        row = row.split(factor=0.255, align=True)
        row.prop(item, "setcellx", text="", emboss=True, translate=False)
        row = row.split(factor=0.34, align=True)
        row.prop(item, "setcelly", text="", emboss=True, translate=False)
        row = row.split(factor=0.63, align=True)
        row.prop(item, "setcellz", text="", emboss=True, translate=False)

        row.prop(item, "enabled", text="", index=index)
        
    def invoke(self, context, event):
        pass
    
    
class CUSTOM_UL_faces(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index): 
        box = layout.box()
        col = box.column()
        row = col.split(factor=0.2)
        row.prop(item, "face_des", text="", emboss=True)
        row = row.split(factor=0.4)
        row.prop(item, "face_type", text="", emboss=True)
        row = row.split(factor = 0.05)
        row.separator()
        row = row.split(factor = 0.39)
        row.prop(item, "face_clr", text="", emboss=True)
        
        row = row.split(factor = 0.77)
        row.prop(item, "name", text="", emboss=False)
        row.prop(item, "enabled", text="", index=index)
   
    def invoke(self, context, event):
        pass
    
class CUSTOM_UL_edges(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        split = layout.row()
        split.prop(item, "fandl", text="", emboss=False, translate=False)
        split.prop(item, "intptx", text="", emboss=True, translate=False)
        split.prop(item, "intpty", text="", emboss=True, translate=False)
        split.prop(item, "intptz", text="", emboss=True, translate=False)
        split.prop(item, "enabled", text="", index=index)
        
    def invoke(self, context, event):
        pass