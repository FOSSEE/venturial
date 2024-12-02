import json 

rec_no = 7
path = "/home/rajdeepadak/.config/blender/3.2/scripts/addons/venturial/user_data/recent" + str(rec_no) + ".json"
rec_name = "blockMeshDict"

dict_ = {"name" : rec_name,
         "index": 1,
         "type" : "blockmeshdict",
         "timestamp" : "date/time during save",  
         "mesh_json" : "some_location",
         "blend_file" : "some_other_location"
        }

with open(path, "w") as out:
    json.dump(dict_, out, indent=2)