import json
import cv2
import numpy as np
img = "../backup_images/n02101556/n02101556_5512.JPEG"
img = cv2.imread(img)

img = cv2.resize(img, (720, 1280))
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img = np.flip(img,axis=2)
img = img.tolist()

with open("temp.json", "w") as f:
    json.dump(img, f)
