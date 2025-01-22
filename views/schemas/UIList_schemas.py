import bpy
from bpy.types import (UIList, PropertyGroup)
from bpy.props import StringProperty, BoolProperty, IntProperty, EnumProperty
#from venturial.models.header.file_handling_operators import VNT_OT_deactivate_mesh_file_item
class VNT_UL_mesh_file_manager(UIList):
    """Callable class for mesh file manager"""
    
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        """Method to define schema of a file manager item"""
        cs = context.scene
        row = layout.box().row()
        row.scale_y = 0.68
    
        r2spt = row.split(factor=0.167, align=True)
        a = r2spt.row(align=True)
        b = r2spt.row(align=True)
        
        a.alignment = "CENTER"
        a.label(text=item.ITEM_project)
        
        bspt = b.split(factor=0.298, align=True)
        b1 = bspt.row(align=True)
        b2 = bspt.row(align=True)
        
        b1.alignment = "CENTER"
        b1.prop(item, "ITEM_name", text="", emboss=False)
        
        b2spt = b2.split(factor=0.85)
        c1 = b2spt.row(align=True)
        c2 = b2spt.row(align=True)
        
        c1spt = c1.split(factor = 0.357)
        d1 = c1spt.row(align=True)
        d2 = c1spt.row(align=True)
        
        d1.alignment = "CENTER"
        d1.prop(item, "ITEM_type", text="", emboss=False)
        
        d2.alignment = "EXPAND"
        d2.prop(item, "ITEM_location", text="", emboss=True)

        c2.alignment = "RIGHT"
        c2.alert=True
        c2.operator("vnt.deactivate_mesh_file_item", text="", icon="PANEL_CLOSE").dump_file_id = item.ITEM_identifier
        
class VNT_UL_mesh_file_coroner(UIList):
    """Callable class for mesh file coroner"""
    
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        """Method to define schema of a file manager item"""
        cs = context.scene
        row = layout.box().row()
        row.scale_y = 0.68
 
        row.prop(item, "ITEM_select", text="")
        row.prop(item, "ITEM_project", text="", emboss=False)
        row.prop(item, "ITEM_name", text="", emboss=False)
        row.label(text = item.ITEM_location)

class fileitemproperties(PropertyGroup):
    """Property attributes of a file item managed by mesh file manager"""
    ITEM_select : BoolProperty()
    ITEM_index : IntProperty()
    ITEM_type : StringProperty()
    ITEM_project : StringProperty()
    ITEM_name : StringProperty()
    ITEM_location : StringProperty(subtype="DIR_PATH")
    ITEM_history : StringProperty()
    ITEM_identifier : StringProperty()
   
        
class tutorialitemproperties(PropertyGroup):
    """Attributes of a tutorial item displayed by the tutorial system menu"""
    TUT_select : BoolProperty()
    TUT_index : IntProperty()
    TUT_type : EnumProperty(items = [('BM', 'Blockmesh', '', "EVENT_B", 0),
                                     ('SHM', 'Snappyhexmesh', '', "EVENT_S", 1),
                                     ('SOLVER', 'Solver', '', "RNA", 2),
                                     ('USAGE', 'Usage', '', "USER", 3),
                                     ('MISC', 'Miscellaneous', '', "QUESTION", 4)],
                            default = 'BM')
    TUT_name : StringProperty()
    TUT_location : StringProperty(subtype="DIR_PATH")
    TUT_progress : IntProperty(default=0,
                               min = 0,
                               max = 100)
    TUT_bookmark : BoolProperty()
    
    
class recent_item_properties(PropertyGroup):
    """Property attributes of a recent item."""
    REC_select : BoolProperty()
    REC_index : IntProperty()
    REC_type : StringProperty()
    REC_name : StringProperty()
    REC_location : StringProperty(subtype="DIR_PATH")
    REC_history : StringProperty()
  
    
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

class CUSTOM_UL_face_merge(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index): 
        box = layout.box()
        col = box.column()
        row = col.split()
        row.prop(item, "master_face", text="Master Face", emboss=True)
        row = row.split()
        row.prop(item, "slave_face", text="Slave Face", emboss=True)
        # row.prop(item, "enabled", text="", index=index)
   
    def invoke(self, context, event):
        pass

'''
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
'''

class CUSTOM_UL_edges_Main(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        row = layout.row()
        row.label(text=f"Edge {index}")
        row.prop(item, "edge_type" , text="")
    
    def invoke(self, context, event):
        pass

class CUSTOM_UL_edges_Sub(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        sr = f"{context.scene.ecustom[context.scene.ecustom_index].name}0{index+1}"
        ob = bpy.data.objects[sr]
        layout.prop(ob, 'location')

    def invoke(self, context, event):
        pass