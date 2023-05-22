import json 

tut_no = 4
path = "/home/rajdeepadak/.config/blender/3.2/scripts/addons/venturial/tutorials/tut" + str(tut_no) + ".json"
tut_name = "Tackle Complex Geometries with the Snappyhexmesh GUI"

dict_ = {"name" : tut_name,
         "index": 4,
         "type" : "sanppyhexmesh",
         "timestamp" : "date/time during save",  
         "content" : {
                      "Text 0": {"Child 0": "john",
                                 "Child 1": "ava",
                                 "Child 2": "peter",
                                 "Child 3": "kyle",
                                 "Child 4": "joseph"}, 
                      "Text 1": {"Child 0": "john",
                                 "Child 1": "ava",
                                 "Child 2": "peter",
                                 "Child 3": "kyle",
                                 "Child 4": "joseph"},
                      "Text 2": {"Child 0": "john",
                                 "Child 1": "ava",
                                 "Child 2": "peter",
                                 "Child 3": "kyle",
                                 "Child 4": "joseph"}
                      }
        }

with open(path, "w") as out:
    json.dump(dict_, out, indent=2)