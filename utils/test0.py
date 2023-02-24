

# import json

# js = json.dumps(tutorial1)

# open('/home/rajdeepadak/.config/blender/3.2/scripts/addons/venturial/utils/sample.json', 'w')
# fp.write(js)
# fp.close()

# import json
# data = [1,2,3,4,5]
# y =json.dumps(data)

# # print(y)
# import json

# li = [2, 5]
# test = open('test.json', 'w')
# try:
#     json.dump(li, test)
# finally:
#     test.close()

# import json
  

# f = open('/home/rajdeepadak/.config/blender/3.2/scripts/addons/venturial/utils/sample.json')
  
# # returns JSON object as 
# # a dictionary
# data = json.load(f)
  
# # Iterating through the json
# # list
# print(data)
  
# Closing file
#f.close()



tutorial1 = {
             "line1": {"type": "ml_text", # multi-line text
                       "value": "Sample text: A random paragraph is present here."},
             "line2": {"type": "img", # filepath to the image
                       "value": "/home/usr/bin/addon/images/img1.png"},
             "line3": {"type": "ml_text",
                       "value": "Some random text"},
             "line4": {"type": "img", # filepath to the image
                       "value": "/home/usr/bin/addon/images/img2.png"}
            }


import json
with open('/home/rajdeepadak/.config/blender/3.2/scripts/addons/venturial/utils/test.json', 'w', encoding='utf-8') as f:
    json.dump(tutorial1, f, ensure_ascii=False, indent=4)