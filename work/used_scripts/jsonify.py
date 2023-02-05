import json
import os
"""
Script to turn images directory to JSON file to populate db
"""
dirs = os.listdir("../backup_images")
dic = {}
for val in dirs:
    if val==".DS_Store":
        continue
    dic[val] = os.listdir("../backup_images/" + val)
with open("out.json", "w") as f:
    json.dump(dic, f)
