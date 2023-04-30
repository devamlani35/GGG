import pickle
import os
    
with open("safe.pkl", "rb") as f: 
    old = pickle.load(f)
tot = []
directory = "/home/ubuntu/s3_files"

for folder in os.listdir(directory):
    temp = directory + "/" + folder
    for file in os.listdir(temp):
        path = temp + "/" + file
        tot.append([path, old[folder + "/" + file]])
with open("new.pkl", "wb") as f:
    pickle.dump(tot, f)
