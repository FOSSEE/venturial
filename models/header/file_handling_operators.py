from bpy.types import Operator
from bpy_extras.io_utils import ExportHelper
from bpy.props import IntProperty, BoolProperty, StringProperty, EnumProperty
import bpy, os, re, time
from datetime import datetime
from pathlib import Path
from venturial.utils.mesh_dictionary_controller import mesh_dictionary_controller
from venturial.utils.custom_icon_object_generator import *
#from venturial.views.schemas.UIList_schemas import VNT_UL_mesh_file_manager, VNT_UL_mesh_file_coroner
from venturial.utils.custom_icon_object_generator import *

class new_case_prompt:
    """Prompt for creating new mesh file"""
    
    def get_unique_file_identifier(self, fp):
        now = str(datetime.now())
        char = [":", ".", " ", "-"]

        for i in char:
            now = now.replace(i, "")
        identifier = str(os.path.basename(fp) + now[-12:])
      
        return identifier 
        

    def draw(self, layout, context, check=None):
        """Method to draw the new mesh file prompt layout"""
        cs = context.scene
        layout.enabled = cs.row_en
        
        row0 = layout.row()
        row0.label(text="")
        row0.scale_y = 0.1
        row0.ui_units_y = 0.05

        row1 = layout.row()
        row1spt = row1.split(factor = 0.3)
        r1c1 = row1spt.row()
        r1c2 = row1spt.row()
        
        r1c1.label(text="Case Directory")
        
        r1c2spt = r1c2.split(factor = 0.8)
        
        a = r1c2spt.row()
        b = r1c2spt.split()
        
        a.box().label(text=cs.mesh_dict_path)
        a.scale_y = 0.58
        b.operator(VNT_OT_select_mesh_filepath.bl_idname, text="", icon_value=custom_icons["file-browser-2"]["file-browser-2"].icon_id)
        
        row2 = layout.row()
        row2spt = row2.split(factor = 0.3)
        r2c1 = row2spt.row()
        r2c2 = row2spt.row()
        
        r2c1.label(text="Case Name")
        r2c2.box().label(text=os.path.basename(cs.mesh_dict_path))
        r2c2.scale_y = 0.56

        row3 = layout.row()
        row3spt = row3.split(factor = 0.3)
        
        r3c1 = row3spt.row()
        r3c2 = row3spt.row() 
        
        r3c1.label(text="Meshing Tool")
        r3c2.prop(cs, "prompt_meshing_tool", expand=True)
        
        row4 = layout.row()
        row4spt = row4.split(factor = 0.252)
        
        r4c1 = row4spt.row()
        r4c2 = row4spt.row() 
        
        r4c2spt = r4c2.split(factor=0.05)
        
        ra = r4c2spt.row()
        rb = r4c2spt.row()
        
        r4c1.label(text="Mesh Dictionaries")
    
        ra.prop(cs, "edit_dict_name", icon="LOCKED" if cs.edit_dict_name == True else "UNLOCKED", text="")
        
        rb.scale_y = 0.57 if cs.edit_dict_name == True else 1.0
        rb.box().label(text=cs.bm_dict_name) if cs.edit_dict_name == True else rb.prop(cs, "bm_dict_name", text="")
        rb.box().label(text=cs.shm_dict_name) if cs.edit_dict_name == True else rb.prop(cs, "shm_dict_name", text="")
        
        if cs.objects:
            row5 = layout.row()
            row5.alignment = 'CENTER'
            row5.label(text="Clicking OK will remove all objects from scene. Make sure it is saved.", icon="ERROR")

    def execute(self, optr, context):
        """method to create a new mesh file item into mesh file manager. This will also generate
        an empty mesh dictionary at the chosen file location."""
        
        cs = context.scene

        if os.path.isdir(cs.mesh_dict_path):
            
            for obj in cs.objects:
                obj.select_set(True)
            bpy.ops.object.delete()
            
            x = list(cs.prompt_meshing_tool)  
                
            for i in x:
                item = cs.mfile_item.add()
                item.ITEM_index = len(cs.mfile_item) - 1
                item.ITEM_type = i
                item.ITEM_name = cs.bm_dict_name if i == "BlockMesh" else cs.shm_dict_name
                item.ITEM_location = cs.mesh_dict_path
                item.ITEM_project = os.path.basename(cs.mesh_dict_path)
                item.ITEM_identifier = self.get_unique_file_identifier(cs.mesh_dict_path)

            cs.mfile_item_index = len(cs.mfile_item)-1
                
            getattr(mesh_dictionary_controller(), "dict_initiate")(optr, context)

        else:
            optr.report({'INFO'}, 'Select a directory.')

class VNT_OT_new_case(Operator):
    """Create a new mesh file"""

    bl_label = "New"
    bl_idname = "vnt.new_case"
    bl_description = "Create a new case"

    def draw(self, context):
        layout = self.layout
        getattr(new_case_prompt(), "draw")(layout, context)
     
    def execute(self, context):

        getattr(new_case_prompt(), "execute")(self, context)
        return {'FINISHED'}

    def invoke(self, context, event):
        cs = context.scene
        cs.row_en = True
        #cs.prompt_meshing_tool = cs.tool_type
        #cs.mesh_dict_name = "blockMeshDict" if cs.tool_type == "BlockMesh" else "snappyHexMeshDict"
        if cs.pref_pointer.default_path_checkbox:
            cs.mesh_dict_path = cs.pref_pointer.default_mesh_dict_path
  
        return context.window_manager.invoke_props_dialog(self, width=600)


class VNT_OT_select_mesh_filepath(Operator, ExportHelper):
    """Opens a file browser to set the location path of mesh file.
    This operator is drawn after pressing the New Mesh button.
    Accessible graphically only after VNT_OT_new_mesh_file is executed."""

    bl_label = "New"
    bl_description = "Opens a file browser to set the location path of mesh file"
    bl_idname = "vnt.select_mesh_filepath"
    filename_ext = ""

    center_x: IntProperty()
    center_y: IntProperty()
    check: BoolProperty(default=False)
    is_dir: BoolProperty(default=False) #used to check if selected path is a directory

    def error_msg(self, layout):
        row = layout.row()
        row.alignment = 'CENTER'
        row.label(text="Selected path is not a directory", icon = "ERROR")

    def draw(self, context):
        layout = self.layout
        getattr(new_case_prompt(), "draw")(layout, context) if self.is_dir == True else self.error_msg(layout)

    def execute(self, context):
        context.scene.row_en = True
        if self.check == True:

            if os.path.isdir(str(Path(self.properties.filepath))):
                self.is_dir = True
                context.scene.mesh_dict_path = str(Path(self.properties.filepath))

            else:
                self.is_dir = False
                context.scene.mesh_dict_path = ""
                self.report({'INFO'}, 'Select a directory.')

            bpy.context.window.cursor_warp(self.center_x, self.center_y)
            self.check = False
            return context.window_manager.invoke_props_dialog(self, width=500)

        else:
            getattr(new_case_prompt(), "execute")(self, context)
            return {'FINISHED'}

    def invoke(self, context, event):
        self.center_x = event.mouse_x
        self.center_y = event.mouse_y

        context.scene.row_en = False
        context.window_manager.fileselect_add(self)
        self.check = True
    
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


class VNT_OT_open_case(Operator):
    """Open an OpenFOAM case"""
    bl_label = "Open an OpenFOAM Case"
    bl_idname = "vnt.open_case"
    bl_description = "Open an OpenFoam Case"

    def execute(self, context):
        return {'FINISHED'}


# This method should be encapsulated within a class, preferably the same class to which 
# its update variable belongs to. This could be a potential cause of bug in the future. 
def select_all_mfile_items(self, context):
    cs = context.scene
    cs.mfile_item

    for i in cs.mfile_item:
        i.ITEM_select = self.select_all
        
class VNT_OT_delete_mesh_file_items(Operator):
    """Permanently delete selected mesh file items. A confirmation prompt will appear."""

    bl_label = "Delete mesh files"
    bl_idname = "vnt.delete_mesh_files"
    bl_description = "Permanently delete selected mesh file items. A confirmation prompt will appear."

    select_all :  BoolProperty(default=False,
                               update=select_all_mfile_items)

    @classmethod
    def poll(cls, context):
        return bool(context.scene.mfile_item)

    def draw(self, context):
        layout = self.layout
        row = layout.row()

        row.prop(self, "select_all", text="Select all")
        cs = context.scene
        row = layout.row()
        row.scale_y = 1.4
        
        row.template_list("VNT_UL_mesh_file_coroner", "", cs,
                          "mfile_item", cs, "mfile_item_index", rows=2)
        
    def delete_selected(self, sel, context):
        cs = context.scene
        
        for i in sel:
            l = len(cs.mfile_item)
            for j in range(0, l):
                if cs.mfile_item[j].ITEM_identifier == i:
                    cs.mfile_item_index = j
                    cs.mfile_item.remove(j)
                    break
            cs.mfile_item_index = 0
        
    def execute(self, context):
        cs = context.scene
        if self.select_all == True:
            cs.mfile_item.clear()
            self.report({'INFO'}, "All mesh files removed")

        else:
            selfiles = []
            curr_id = cs.mfile_item[cs.mfile_item_index].ITEM_identifier
            
            for i in range(0, len(cs.mfile_item)):
                if cs.mfile_item[i].ITEM_select == True:
                    selfiles.append(cs.mfile_item[i].ITEM_identifier)
                    
            if cs.mfile_item[cs.mfile_item_index].ITEM_identifier in selfiles:
                self.delete_selected(selfiles, context)

            else:
                self.delete_selected(selfiles, context)
                
                for i in range(0, len(cs.mfile_item)):
                    if cs.mfile_item[i].ITEM_identifier == curr_id:
                        cs.mfile_item_index = i
                        break
            
        return{'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=600)

class VNT_OT_deactivate_mesh_file_item(Operator):
    """Removes the mesh file from mesh file manager.
    The mesh file is not permanently deleted. It can be re-built with the build mesh option."""

    bl_label = "Deactivate mesh file item"
    bl_idname = "vnt.deactivate_mesh_file_item"
    bl_description = "Removes the mesh file from mesh file manager. The mesh file is not permanently deleted."

    dump_file_id: StringProperty()

    def execute(self, context):
        cs = context.scene
        
        if cs.mfile_item[cs.mfile_item_index].ITEM_identifier == self.dump_file_id:
            if cs.mfile_item_index == 0:
                cs.mfile_item.remove(cs.mfile_item_index)
                cs.mfile_item_index = 0
            else:    
                j = cs.mfile_item_index
                cs.mfile_item.remove(cs.mfile_item_index)
                cs.mfile_item_index = j-1
            
        else:
            j = cs.mfile_item_index
            for r in range(0, len(cs.mfile_item)):
                if cs.mfile_item[r].ITEM_identifier == self.dump_file_id:
                    break  
            
            if r < j:
                cs.mfile_item.remove(r)
                cs.mfile_item_index -= 1     
            else:
                cs.mfile_item.remove(r)
                        
            
        return{'FINISHED'}
