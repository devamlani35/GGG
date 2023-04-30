import pickle
file = "n02018207/n02018207_11937.JPEG"
with open("labels.pkl", "rb") as f:
    labels = pickle.load(f)
ind = -1
for i in range(len(labels)):
    if labels[i][0] == file:
        ind = i
        break
labels.pop(ind)
with open("labels.pkl", "wb") as f:
    pickle.dump(labels, f)
