import os 
import torch
from torch.utils.data import Dataset
import pickle
import numpy as np
import cv2
class ImDataset(Dataset):
    def __init__(self):
        with open("labels.pkl", "rb") as f:
            self.labels = pickle.load(f)
    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        img_path = self.labels[idx][0]
        img = cv2.imread(img_path)
        img = cv2.normalize(img, None, 0, 1.0, cv2.NORM_MINMAX, dtype=cv2.CV_32F)
        img = np.flip(img,axis=2)
        new_img = img.copy()
        img = torch.Tensor(new_img)
        img = torch.permute(img, (2,0,1))
        label =int(self.labels[idx][1])
        return img, label
if __name__ == "__main__":
    db = ImDataset()
