import bpy

custom_icons = {}

def register_custom_icon(icon, rel_path):
    img = bpy.utils.previews.new()
    img_path = bpy.utils.script_paths(subdir='addons')[1]+rel_path
    img.load(icon, img_path, 'IMAGE')
    custom_icons[icon] = img
    
def unregister_custom_icon(icon, rel_path):
    for img in custom_icons.values():
        bpy.utils.previews.remove(img)
    custom_icons.clear()    
    