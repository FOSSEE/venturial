#------------------------------------------- Blender-Python-Package-Manager --------------------------------------------#
Module = """blender_package_handler_script.py"""

Description = """Run this as a Script from Blender. Running this file outside of Blender is currently 
                 restricted as that capability is yet to be implemented."""
   
Future_Requirements = """1. Present User with a usage documentation(rules for entering name of package 
                            and method) when the script is run.
                         2. User can enter package name and method(that dictates what to do with the 
                            package).
                         3. Method if valid is executed after step 2.
                         4. Checks for method validity and package name validity are to be implemented 
                            as well.
                         5. This file may also be used to develop a GUI-based package manager addon for
                            Blender and this can be bundled with the OpenFOAM-GUI SDK. 
                         6. Error Handling and exception raises are yet to be implemented."""
#----------------------------------------------------------------------------------------------------------------------#-

import subprocess
import sys
from pathlib import Path


class blender_package_handler:
    
    def __init__(self, py_exec=None, lib=None):
        self.py_exec = str(sys.executable)
        
    def blender_ensure_pip(self):
        """ensure if pip is present in blender"""
        subprocess.call([self.py_exec, "-m", "ensurepip", "--user" ])
        print("Completed")
        
    def blender_list_packages(self):
        """ensure if pip is present in blender"""
        subprocess.call([self.py_exec, "-m", "pip", "list" ])
        
    def blender_upgrade_pip(self):
        """upgrade Blender-python pip"""
        subprocess.call([self.py_exec, "-m", "pip", "install", "--upgrade", "pip" ])
        print("Completed")
        
    def blender_install_package(self, package_name):
        """install a package into Blender's python library with pip"""
        subprocess.call([self.py_exec, "-m", "pip", "install", package_name])
        
    def blender_uninstall_package(self, package_name):
        """uninstall a package from Blender's python library with pip"""
        subprocess.call([self.py_exec, "-m", "pip", "uninstall", package_name])
    

try:
    import bpy
    ml = [(func, getattr(blender_package_handler(), func).__doc__) for func in dir(blender_package_handler) if callable(getattr(blender_package_handler, func)) and not func.startswith("__")]

    for i in ml:
        print(i)

    method_name = str(input("Enter name of method: "))

    if method_name in ['blender_install_package', 'blender_uninstall_package']:
        package_name = str(input("Enter name of valid package: "))
        getattr(blender_package_handler(), method_name)(package_name)
        
    else:
        getattr(blender_package_handler(), method_name)()

except ImportError:
    print("Run this Script within Blender.")

