#-------------------------------------------- Venturial ----------------------------------------------#
Module = """delete__pycache__.py"""

Description = """Use this to remove pycache. They are usually generated when Blender installs an addon. 
                 An Addon is a python module to blender. __pycache__ contains bytecode compiled by the 
                 python interpreter to make the addon run faster. This is to be removed when the addon is 
                 distributed publically. If version control (git) is used, this folder is typically 
                 listed in the ignore(.gitignore) file. Nevertheless, it is useful have a pycache 
                 deletion file which can be run as a script from inside or outside of Blender."""
#-----------------------------------------------------------------------------------------------------#

import os
import shutil

try:
    import bpy
    mypath = bpy.utils.script_paths('addons')[0] + "/venturial"
    print("Running as Blender Script.")
    
except TypeError:
    mypath = os.getcwd()
    print("Running as External Script.")
       
for i in [r for r, d, f in os.walk(mypath) if os.path.basename(r) == "__pycache__"]:
    shutil.rmtree(i)