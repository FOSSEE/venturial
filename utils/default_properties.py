import addon_utils, json, bpy
from pathlib import Path

class default_properties:
    def __init__(self):
        self.default_prefs_path = ""
        self.default_prefs_keys = ['default_path_checkbox',
                                   'default_mesh_dict_path', 
                                   'default_tut_path_checkbox',
                                   'default_tutorials_dir',
                                   'default_user_data_path_checkbox',
                                   'default_user_data_path']
        self.default_prefs_values = [False, 
                                     bpy.utils.script_paths(subdir='addons')[1]+"/venturial/user_data/",
                                     False,
                                     bpy.utils.script_paths(subdir='addons')[1]+"/venturial/tutorials/",
                                     False,
                                     bpy.utils.script_paths(subdir='addons')[1]+"/venturial/user_data/"]
        self.default_prefs_dict = {}
        
        
    def read_prefs_data(self, file: str):
        with open(self.default_prefs_path+file, 'r') as inp: 
            self.default_prefs_dict = json.load(inp)
            
    def write_prefs_data(self, file: str):
        with open(self.default_prefs_path+file, "w") as out:
            self.default_prefs_dict = {k:v for k, v in zip(self.default_prefs_keys, self.default_prefs_values)}
            json.dump(self.default_prefs_dict, out, indent=2)
        
    def load_user_preferences(self, key):
        """Preferences are loaded from user_custom_settings.json if the file is present in venturial/preferences, 
        else preferences are loaded from system_default_settings.json"""

        #locate path where venturial is installed.
        for addon in addon_utils.modules():
            if addon.bl_info['name'] == "Venturial":
                self.default_prefs_path = str(Path(addon.__file__).parent.absolute())+"/preferences"
                break
        
        if "user_custom_settings.json" in [x.name for x in Path(self.default_prefs_path).glob('**/*') if x.is_file]:
            print("Loading from custom preferences.")
            self.read_prefs_data("/user_custom_settings.json")
            
        else:
            if "system_default_settings.json" in [x.name for x in Path(self.default_prefs_path).glob('**/*') if x.is_file]:
                print("No custom preferences found. Loading default system preferences.")
                self.read_prefs_data("/system_default_settings.json")
                
            else:
                print("No default preferences or custom preferences found.\n Creating default system preferences.")
                self.write_prefs_data("/system_default_settings.json")
                self.read_prefs_data("/system_default_settings.json")
                
        return self.default_prefs_dict[key]