from bpy.types import Operator
from bpy_extras.io_utils import ExportHelper
from bpy.props import IntProperty, BoolProperty, StringProperty, EnumProperty
import bpy, os
from pathlib import Path
from venturial.utils.mesh_dictionary_controller import mesh_dictionary_controller
from venturial.utils.custom_icon_object_generator import *
#from venturial.views.schemas.UIList_schemas import VNT_UL_mesh_file_manager, VNT_UL_mesh_file_coroner

class new_mesh_file_prompt:
    """Prompt for creating new mesh file"""
    
    def draw(self, layout, context):
        """Method to draw the new mesh file prompt layout"""
        cs = context.scene
        row0 = layout.row()
        row0.label(text="")
        row0.scale_y = 0.1
        row0.ui_units_y = 0.05
        
        row = layout.row()
        row.enabled = cs.row_en
        row.label(text="Meshing Tool")
        row.prop(cs, "prompt_meshing_tool", text="")
        
        row = layout.row()
        row.enabled = cs.row_en
        row.label(text="Mesh file name")
        row.prop(cs, "mesh_dict_name", text="")
        
        row = layout.row()
        row.enabled = cs.row_en
        row.operator(VNT_OT_select_mesh_filepath.bl_idname, text="Select mesh file path")
        row.prop(cs, "mesh_dict_path", text="")        
        
        row = layout.row()
        row.alignment = 'CENTER'
        row.label(text="Clicking OK will remove all objects from scene", icon="ERROR")
        
    def execute(self, optr, context):
        """method to create a new mesh file item into mesh file manager. This will also generate
        an empty mesh dictionary at the chosen file location."""
        for obj in context.scene.objects:
            obj.select_set(True)
        bpy.ops.object.delete()
        
        if os.path.isdir(context.scene.mesh_dict_path):
            item = context.scene.mfile_item.add()
            item.ITEM_index = len(context.scene.mfile_item) - 1
            item.ITEM_type = context.scene.tool_type
            item.ITEM_name = context.scene.mesh_dict_name
            item.ITEM_location = context.scene.mesh_dict_path
            
            context.scene.mfile_item_index = len(context.scene.mfile_item)-1
            getattr(mesh_dictionary_controller(), "dict_initiate")(optr, context)
            
        else:
            optr.report({'INFO'}, 'Select a directory.')
            
        return {'FINISHED'}

class VNT_OT_new_mesh_file(Operator):
    """Create a new mesh file"""
    
    bl_label = "New Mesh" 
    bl_idname = "vnt.new_mesh_file"
    bl_description = "Create a new mesh file" 
    
    def draw(self, context):
        layout = self.layout
        getattr(new_mesh_file_prompt(), "draw")(layout, context)

    def execute(self, context):
        
        getattr(new_mesh_file_prompt(), "execute")(self, context)
    
    def invoke(self, context, event):
        cs = context.scene
        cs.row_en = True
        cs.prompt_meshing_tool = cs.tool_type
        cs.mesh_dict_name = "blockMeshDict" if cs.tool_type == "BlockMesh" else "snappyHexMeshDict"
        return context.window_manager.invoke_props_dialog(self, width=500)
    

class VNT_OT_select_mesh_filepath(Operator, ExportHelper):
    """Opens a file browser to set the location path of mesh file.
    This operator is drawn after pressing the New Mesh button.
    Accessible graphically only after VNT_OT_new_mesh_file is executed."""
    
    bl_label = "New Mesh"
    bl_description = "Opens a file browser to set the location path of mesh file"
    bl_idname = "vnt.select_mesh_filepath"
    filename_ext = ""
    
    center_x : IntProperty()
    center_y : IntProperty()
    check : BoolProperty(default=False)
    
    def draw(self, context):
        layout = self.layout
        getattr(new_mesh_file_prompt(), "draw")(layout, context)
        
    def execute(self, context):
        context.scene.row_en = True
        if self.check == True:
            
            if os.path.isdir(str(Path(self.properties.filepath))):
                context.scene.mesh_dict_path = str(Path(self.properties.filepath))
            
            else:
                context.scene.mesh_dict_path = ""
                self.report({'INFO'}, 'Select a directory.')
                
            bpy.context.window.cursor_warp(self.center_x, self.center_y)
            self.check = False
            return context.window_manager.invoke_props_dialog(self, width=500)   
        
        else:
            getattr(new_mesh_file_prompt(), "execute")(self, context)
            return {'FINISHED'}
        
    def invoke(self, context, event):
        self.center_x = event.mouse_x
        self.center_y = event.mouse_y
                
        context.scene.row_en = False
        context.window_manager.fileselect_add(self)
        self.check = True
        #context.scene.row_en = True
        return {'RUNNING_MODAL'}


class VNT_OT_build_mesh(Operator):
    """Build mesh from blockmeshdict file"""
    
    bl_label = "Build Mesh" 
    bl_idname = "vnt.build_mesh"
    bl_description = "Build mesh from blockmeshdict file" 

    def execute(self, context):
        return {'FINISHED'}

class VNT_OT_import_mesh(Operator):
    """Import mesh from blockmeshdict file"""
    
    bl_label = "Import Mesh" 
    bl_idname = "vnt.import_mesh"
    bl_description = "Import mesh from blockmeshdict file" 

    def execute(self, context):
        return {'FINISHED'}

    
class VNT_OT_save_mesh(Operator):
    """Save mesh to file"""
    
    bl_label = "Save Mesh" 
    bl_idname = "vnt.save_mesh"
    bl_description = "Save mesh to file" 

    def execute(self, context):
        return {'FINISHED'}
    
    
class VNT_OT_new_case(Operator):
    """Create a new OpenFOAM case"""
    bl_label = "Create a new OpenFOAM case"
    bl_idname = "vnt.new_case"
    bl_description = "Create a new OpenFoam Case" 

    def execute(self, context):
        return {'FINISHED'}
    
class VNT_OT_open_case(Operator):
    """Open an OpenFOAM case"""
    bl_label = "Open an OpenFOAM Case"
    bl_idname = "vnt.open_case"
    bl_description = "Open an OpenFoam Case" 

    def execute(self, context):
        return {'FINISHED'}  
    

class VNT_OT_see_older(Operator):
    """See history of all previously worked mesh files"""
    
    bl_label = "See Older" 
    bl_idname = "vnt.see_older"
    bl_description = "See older history of previously worked mesh files" 

    def execute(self, context):
        return {'FINISHED'}
    

class VNT_OT_delete_mesh_file_items(Operator):
    """Remove all mesh file items from mesh file manager. A prompt will appear with the 
    options to select what to remove."""
    
    bl_label = "Remove mesh files" 
    bl_idname = "vnt.remove_mesh_files"
    bl_description = "Build mesh from blockmeshdict file" 
    
    select_all : BoolProperty(default=False)
    
    @classmethod
    def poll(cls, context):
        return bool(context.scene.mfile_item)
    
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        
        row.prop(self, "select_all", text = "Select all")
        cs = context.scene
        row = layout.row()
        row.scale_y = 1.4
        row.template_list("VNT_UL_mesh_file_coroner", "", cs, "mfile_item", cs, "mfile_item_index", rows= 2)

    def execute(self, context):
        cs = context.scene
        if self.select_all == True:
            cs.mfile_item.clear()
            self.report({'INFO'}, "All mesh files removed")
            
        else:
            selfiles = []
            for i in range(0, len(cs.mfile_item)):
                if cs.mfile_item[i].ITEM_select == True:
                    selfiles.append(cs.mfile_item[i].ITEM_index)
            
            for i in selfiles:
                l = len(cs.mfile_item)
                
                for j in range(0, l):
                    if cs.mfile_item[j].ITEM_index == i: 
                        
                        cs.mfile_item_index = j
                        cs.mfile_item.remove(j)
                        break 
                cs.mfile_item_index = 0
            
        return{'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=400)   