from model import CNN
import torch
import cv2
import numpy as np
if __name__ == "__main__":
    model = CNN()
    model.load_state_dict(torch.load("model.pt29", map_location=torch.device('cpu')))
    model.eval()
    img = cv2.imread("dog.jpeg")
    img = cv2.normalize(img, None, 0, 1.0, cv2.NORM_MINMAX, dtype=cv2.CV_32F)
    img = np.flip(img,axis=2)
    new_img = img.copy()
    img = torch.Tensor(new_img)
    img = torch.permute(img, (2,0,1))
    y = model(img)
    print(y)
