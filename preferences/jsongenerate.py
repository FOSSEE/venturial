import json 

path = "/home/rajdeepadak/.config/blender/3.2/scripts/addons/venturial/preferences/sample_json.json"

dict_ = {"Parent 0": 
            {"Child 0": "john",
             "Child 1": "ava",
             "Child 2": "peter",
             "Child 3": "kyle",
             "Child 4": "joseph"}, 
        "Parent 1": 
            {"Child 0": "john",
             "Child 1": "ava",
             "Child 2": "peter",
             "Child 3": "kyle",
             "Child 4": "joseph"},
        "Parent 2": 
            {"Child 0": "john",
             "Child 1": "ava",
             "Child 2": "peter",
             "Child 3": "kyle",
             "Child 4": "joseph"}}

print(dict_)
with open(path, "w") as out:
    json.dump(dict_, out, indent=2)