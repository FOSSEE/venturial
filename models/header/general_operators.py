from bpy.types import Operator
from bpy.props import EnumProperty, IntProperty, BoolProperty, StringProperty
import bpy, json, functools, os
from bpy_extras.io_utils import ExportHelper
from venturial.utils.custom_icon_object_generator import *
from pathlib import Path

class settings_panel_properties:
    """Prompt for creating new mesh file"""

    # Using invoke_props_dialog now, but may require to modify with a better dialog box control feature.
    def draw(self, layout, context):
        """Method to draw the new mesh file prompt layout"""
        cs = context.scene
        ptr = cs.pref_pointer
        layout.enabled = cs.row_en
        
        # Create space under title
        row0 = layout.row()
        row0.label(text="")
        row0.scale_y = 0.1
        row0.ui_units_y = 0.05
        
        # First Row
        row1 = layout.row()
        r1spt = row1.split(factor = 0.3)
        
        a = r1spt.row()
        b = r1spt.row(align=True)
        b.enabled = ptr.default_path_checkbox
        
        a.prop(ptr, "default_path_checkbox", text = "")
        a.label(text = "Default mesh file path")
        
        bspt = b.split(factor = 0.8, align=True)
        b1 = bspt.row()
        b2 = bspt.split()
        
        b1.prop(ptr, "default_mesh_dict_path", text = "")
        b2.operator(VNT_OT_select_default_mesh_filepath.bl_idname, text = "", icon_value=custom_icons["file-browser-2"]["file-browser-2"].icon_id)

        # Second Row
        row2 = layout.row()
        r2spt = row2.split(factor = 0.3)
        
        a = r2spt.row()
        b = r2spt.row(align=True)
        b.enabled = ptr.default_tut_path_checkbox
        
        a.prop(ptr, "default_tut_path_checkbox", text = "")
        a.label(text = "Default tutorials directory")
        
        bspt = b.split(factor = 0.8, align=True)
        b1 = bspt.row()
        b2 = bspt.split()
        
        b1.prop(ptr, "default_tutorials_dir", text = "")
        b2.operator(VNT_OT_select_default_tut_filepath.bl_idname, text = "", icon_value=custom_icons["file-browser-2"]["file-browser-2"].icon_id)

        
        # Third Row
        row3 = layout.row()
        r3spt = row3.split(factor = 0.3)
        
        a = r3spt.row()
        b = r3spt.row(align=True)
        b.enabled = ptr.default_tut_path_checkbox
        
        a.prop(ptr, "default_user_data_path_checkbox", text = "")
        a.label(text = "Default user data path")
        
        bspt = b.split(factor = 0.8, align=True)
        b1 = bspt.row()
        b2 = bspt.split()
        
        b1.prop(ptr, "default_user_data_path", text = "")
        b2.operator(VNT_OT_select_default_user_data_filepath.bl_idname, text = "", icon_value=custom_icons["file-browser-2"]["file-browser-2"].icon_id)
        
        # penultimate Row
        rowu = layout.row()
        rowu.operator(VNT_OT_save_preferences.bl_idname, text = "Save Preferences")
        rowu.operator(VNT_OT_reset_preferences.bl_idname, text = "Reset Preferences")
        rowu.operator(VNT_OT_import_preferences.bl_idname, text = "Import Preferences")
        
        # last Row
        rowl = layout.row()
        rowl.alignment = "CENTER"
        rowl.label(text="Clicking OK will apply the preferences.", icon="ERROR")
     
class VNT_OT_save_preferences(Operator):
    """Save user preferences"""
    bl_label = "Save user preferences"
    bl_idname = "vnt.save_preferences"
    bl_description = "Open user general settings window"
    
    pref_loc : StringProperty(default=bpy.utils.script_paths(subdir='addons')[1]+"/venturial/preferences/user_custom_settings.json")
    
    def __init__(self, cs=None, pref_data=None):
        """Initialise a dictionary to store the user preferences for dumping 
        into user_settings.json file."""
        self.cs = bpy.context.scene
        self.pref_data = {key: getattr(self.cs.pref_pointer, key) for key in self.cs.pref_pointer.__annotations__.keys()}
    
    def toggle(self):
        self.cs.row_en = True
    
    def __del__(self):
        """Wait for 0.1 seconds for save preferences dialog box to close and then toggle row_en
        to allow interaction with settings dialog box."""
        bpy.app.timers.register(functools.partial(self.toggle), first_interval=0.1)
        
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        rowspt = row.split(factor=0.3)
        
        r1 = rowspt.row()
        r2 = rowspt.row()
        
        r1.label(text="Preferences will be saved in: ")
        r2.prop(self, "pref_loc", text="")
        
    def execute(self, context):
        """Save user preferences into user_settings.json file."""
        cs = context.scene
        cs.row_en = True # Enable interaction with settings dialog box
        
        with open(self.pref_loc, "w") as out:
            json.dump(self.pref_data, out, indent=2)
        
        return {"FINISHED"}
    
    def invoke(self, context, event):
        """invoke a dialog box (draw) to set user settings location"""
        cs = context.scene
        cs.row_en = False # Disable interaction with settings dialog box.
        
        return context.window_manager.invoke_props_dialog(self, width=500)
    
class VNT_OT_reset_preferences(Operator):
    """Reset preferences to system default"""
    bl_label = "Reset Preferences"
    bl_idname = "vnt.reset_preferences"
    bl_description = "Reset preferences to system default"
    
    default_pref_loc : StringProperty(default=bpy.utils.script_paths(subdir='addons')[1]+"/venturial/preferences/system_default_settings.json")
    
    def __init__(self, cs=None, default_prefs=None):
        """Initialise a dictionary to store default preferences data read from default_pref_loc"""
        self.cs = bpy.context.scene
        with open(self.default_pref_loc, 'r') as inp : self.default_prefs = json.load(inp)
        
    def toggle(self):
        self.cs.row_en = True
        
    def __del__(self):
        """Wait for 0.1 seconds for reset preferences dialog box to close and then toggle row_en
        to allow interaction with settings dialog box."""
        bpy.app.timers.register(functools.partial(self.toggle), first_interval=0.1)
        
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        
        row.alignment = "CENTER"
        row.label(text="Confirm Reset ?")
        
    def execute(self, context):
        cs = context.scene
        for i, j in self.default_prefs.items():
            setattr(cs.pref_pointer, i, j)
        
        return {"FINISHED"}
    
    def invoke(self, context, event):
        """invoke a dialog box (draw) to confirm the reset"""
        cs = context.scene
        cs.row_en=False
        return context.window_manager.invoke_props_dialog(self, width = 200)
    
class VNT_OT_import_preferences(Operator, ExportHelper):
    """Opens a file browser to import_preferences from alternate json file."""
    bl_label = "Import Preferences"
    bl_idname = "vnt.import_preferences"
    bl_description = "Import preferences from another source"
    
    check_extension = False
    
    center_x: IntProperty()
    center_y: IntProperty()
    check: BoolProperty(default=False)

    def __init__(self, imported_prefs=None):
        self.imported_prefs = {}
    
    def draw(self, context):
        layout = self.layout
        getattr(settings_panel_properties(), "draw")(layout, context)

    def execute(self, context):
        context.scene.row_en = True
        if self.check == True:

            if Path(self.properties.filepath).suffix == '.json':
                print("loading preferences from alternate json")
                
                with open(str(Path(self.properties.filepath)), 'r') as inp : self.imported_prefs = json.load(inp)
                
                for i, j in self.imported_prefs.items(): setattr(context.scene.pref_pointer, i, j)
                
            else:
                self.report({'INFO'}, 'Select a json file.')

            bpy.context.window.cursor_warp(self.center_x, self.center_y)
            self.check = False
            return context.window_manager.invoke_props_dialog(self, width=500)
        
        else:
            # getattr(new_mesh_file_prompt(), "execute")(self, context)
            return {'FINISHED'}
        

    def invoke(self, context, event):
        self.center_x = event.mouse_x
        self.center_y = event.mouse_y

        context.scene.row_en = False
        context.window_manager.fileselect_add(self)
        self.check = True
        return {'RUNNING_MODAL'}
     
        
class VNT_OT_user_general_settings(Operator):
    """User general settings"""
    bl_label = "User Settings"
    bl_idname = "vnt.user_general_settings"
    bl_description = "Open user general settings window"
    
    def draw(self, context):
        layout = self.layout
        getattr(settings_panel_properties(), "draw")(layout, context)
       
    def execute(self, context):   
        """This method will save all changes made to user settings""" 
        
        return {'FINISHED'}
        #return context.window_manager.invoke_props_dialog(self, width=600)
        
    def invoke(self, context, event=None):
        """invoke the settings dialog box"""
        context.scene.row_en = True
        return context.window_manager.invoke_props_dialog(self, width=600)


class VNT_OT_select_default_mesh_filepath(Operator, ExportHelper):
    """Opens a file browser to set the location of default path of mesh file.
    This operator is similar to VNT_OT_select_mesh_filepath drawn but sets only the default path
    Accessible graphically only after VNT_OT_user_general_settings is executed."""

    bl_label = "Set Default"
    bl_description = "Opens a file browser to set the location of default path of mesh file"
    bl_idname = "vnt.select_default_mesh_filepath"
    filename_ext = ""

    center_x: IntProperty()
    center_y: IntProperty()
    check: BoolProperty(default=False)

    def draw(self, context):
        layout = self.layout
        getattr(settings_panel_properties(), "draw")(layout, context)

    def execute(self, context):
        context.scene.row_en = True
        if self.check == True:

            if os.path.isdir(str(Path(self.properties.filepath))):   
                setattr(self, "bl_label", "User Settings")                             
                context.scene.pref_pointer.default_mesh_dict_path = str(Path(self.properties.filepath))

            else:
                self.report({'INFO'}, 'Select a directory.')

            bpy.context.window.cursor_warp(self.center_x, self.center_y)
            self.check = False
            #return context.window_manager.invoke_props_dialog(self, width=500)
            bpy.ops.vnt.user_general_settings('INVOKE_DEFAULT')
            return {'FINISHED'}
        
        else:
            return {'FINISHED'}
        

    def invoke(self, context, event):
        self.center_x = event.mouse_x
        self.center_y = event.mouse_y

        context.scene.row_en = False
        context.window_manager.fileselect_add(self)
        self.check = True
        return {'RUNNING_MODAL'}
    
class VNT_OT_select_default_tut_filepath(Operator, ExportHelper):
    """Opens a file browser to set the location of default path for tutorials directory.
    This operator is similar to VNT_OT_select_mesh_filepath drawn but sets only the default path
    Accessible graphically only after VNT_OT_user_general_settings is executed."""

    bl_label = "Set Default"
    bl_description = "Opens a file browser to set the location of default path for tutorials directory"
    bl_idname = "vnt.select_default_tut_filepath"
    filename_ext = ""

    center_x: IntProperty()
    center_y: IntProperty()
    check: BoolProperty(default=False)

    def draw(self, context):
        layout = self.layout
        getattr(settings_panel_properties(), "draw")(layout, context)

    def execute(self, context):
        context.scene.row_en = True
        if self.check == True:

            if os.path.isdir(str(Path(self.properties.filepath))):
                context.scene.pref_pointer.default_tutorials_dir = str(Path(self.properties.filepath))

            else:
                #context.scene.default_mesh_dict_path = ""
                self.report({'INFO'}, 'Select a directory.')

            bpy.context.window.cursor_warp(self.center_x, self.center_y)
            self.check = False
            #return context.window_manager.invoke_props_dialog(self, width=500)
            bpy.ops.vnt.user_general_settings('INVOKE_DEFAULT')
            return {'FINISHED'}
        
        else:
            return {'FINISHED'}
        

    def invoke(self, context, event):
        self.center_x = event.mouse_x
        self.center_y = event.mouse_y

        context.scene.row_en = False
        context.window_manager.fileselect_add(self)
        self.check = True
        return {'RUNNING_MODAL'}


class VNT_OT_select_default_user_data_filepath(Operator, ExportHelper):
    """Opens a file browser to set the location of default path for user data directory.
    This operator is similar to VNT_OT_select_mesh_filepath drawn but sets only the default path
    Accessible graphically only after VNT_OT_user_general_settings is executed."""

    bl_label = "Set Default"
    bl_description = "Opens a file browser to set the location of default path for user data directory"
    bl_idname = "vnt.select_default_user_data_filepath"
    filename_ext = ""

    center_x: IntProperty()
    center_y: IntProperty()
    check: BoolProperty(default=False)

    def draw(self, context):
        layout = self.layout
        getattr(settings_panel_properties(), "draw")(layout, context)

    def execute(self, context):
        context.scene.row_en = True
        if self.check == True:

            if os.path.isdir(str(Path(self.properties.filepath))):
                context.scene.pref_pointer.default_user_data_path = str(Path(self.properties.filepath))

            else:
                #context.scene.default_mesh_dict_path = ""
                self.report({'INFO'}, 'Select a directory.')

            bpy.context.window.cursor_warp(self.center_x, self.center_y)
            self.check = False
            #return context.window_manager.invoke_props_dialog(self, width=500)
            bpy.ops.vnt.user_general_settings('INVOKE_DEFAULT')
            return {'FINISHED'}
        
        else:
            return {'FINISHED'}
        

    def invoke(self, context, event):
        self.center_x = event.mouse_x
        self.center_y = event.mouse_y

        context.scene.row_en = False
        context.window_manager.fileselect_add(self)
        self.check = True
        return {'RUNNING_MODAL'}



class VNT_OT_venturial_maintools(Operator):
    """Click to Open Venturial's post-processing page"""
    bl_label = "Open Venturial post-processing page" 
    bl_idname = "vnt.venturial_maintools"
    bl_description = " "

    maintools : EnumProperty(items = [("BlockMesh", "BlockMesh", "Based on OpenFOAM's blockmesh utility. Venturial's BlockMesh page displays options for defining the physical domain of fluid interactions."),
                                      ("SnappyHexMesh", "SnappyHexMesh", "Based on OpenFOAM's snappyhexmesh utility. Venturial's SnappyHexMesh page displays options for defining the physical domain of fluid interactions."),
                                      ("Solution Modeling", "Solution Modeling", "Venturial Simulation control page displays options for defining fluid and environmental characteristics."),
                                      ("Post-Processing", "Post-Processing", "Venturial Post-processing page displays options for processing simulation output data.")],
                             default = "BlockMesh")
    
    x : IntProperty()
    y : IntProperty()
    
    def execute(self, context):   
        if self.maintools in ["BlockMesh", "SnappyHexMesh"]:  
            context.scene.meshing_tool = self.maintools
        else:
            context.scene.solution_tools = self.maintools
        
        #print(self.maintools)
        
        bpy.context.window.cursor_warp(0, 0)
        bpy.context.window.cursor_warp(self.x, self.y)
        
        return {'FINISHED'}
        
    def invoke(self, context, event):
        self.x = event.mouse_x
        self.y = event.mouse_y
        
        return self.execute(context)
    
    
class VNT_OT_venturial_homepage(Operator):
    """Click to visit Venturial's Homepage"""
    bl_label = "Open Venturial Homepage" 
    bl_idname = "vnt.venturial_homepage"
    bl_description = "Open default browser to navigate to Venturial's Homepage"

    def execute(self, context):     
        return {'FINISHED'}

  
class VNT_OT_fossee_homepage(Operator):
    """Click to visit FOSSEE's Homepage"""
    bl_label = "Open FOSSEE Homepage" 
    bl_idname = "vnt.fossee_homepage"
    bl_description = "Open default browser to navigate to FOSSEE's Homepage"

    def execute(self, context):     
        return {'FINISHED'}


class VNT_OT_close_venturial(Operator):
    """Close Venturial"""
    bl_label = "Exit" 
    bl_idname = "vnt.close_venturial"
    bl_description = "Click to Venturial. A confirmation prompt will appear before disabling the addon."
    
    def draw(self, context):
        scn = context.scene
        
        layout = self.layout
        row = layout.row()
        row.alignment = "CENTER"
        row.label(text="       Click OK to confirm Exit.")
        row = layout.row()
        row.alignment = "CENTER"
        row.label(text="       To re-enable Venturial:")
        row = layout.row()
        row.alignment = "CENTER"
        row.label(text="Go to Edit-> Preferences->Add-ons -> Search 'Venturial' -> Tick Checkbox.")
        
    def execute(self, context):   
        bpy.ops.preferences.addon_disable(module="venturial")  
        return {'FINISHED'}
        
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=410)
    
  


    
    
