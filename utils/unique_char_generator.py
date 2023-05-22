from datetime import datetime
import re

x = "/home/rajdeepadak/.config/blender/3.2/scripts/addons/venturial/utils/unique"
print(x.basename)

now = str(datetime.now())
char = [":", ".", " ", "-"]

for i in char:
    now = now.replace(i, "")
    
print(now[-12:])