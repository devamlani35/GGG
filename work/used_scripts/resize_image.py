import os
from PIL import Image
counter=0
os.chdir("../backup_images")
#Loop through each file in images directory
for directory in os.listdir():
    if directory == ".DS_Store":
        continue
    for file in  os.listdir(directory):
        im = Image.open(directory+"/"+file)
        # Resize image to needed size
        if im.size == (1280,720):
            continue
        im = im.resize((1280,720))
        # Remove old file and resave file
        os.remove(directory+"/"+file)
        im.save(directory+"/"+file)
    counter += 1
    print(counter)
    print(directory)
print("done")

