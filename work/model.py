import torch
import torch.nn as nn
import numpy as np
import pandas as pd
import torch.nn.functional as F
import time
from torch.nn.functional import softmax
from torch.nn import MaxPool2d
from torch.nn import Conv2d
from torch import flatten
from torch.nn import Dropout
from torch.nn import Linear
import torch.optim as optim
import ImDataset
from torch.utils.data import DataLoader, random_split
relu = F.relu
device = torch.device("cuda:0")

class CNN (nn.Module):

    def __init__ (self):
        super().__init__()
        #Note: when training, all shapes begin with batch_size
        # Reshape to (48,80,80)
        self.c1 = Conv2d(3,48,21,1, padding=0)
        # Reshape to (48,40,40)
        self.p1 = MaxPool2d(5,2,padding=2)
        
        # Reshape to (192,14,14)
        self.c2 = Conv2d(48, 192,7,3, padding=3)
        # Reshape to (192,14,14)
        self.p2 = MaxPool2d(3,1,padding=0 )
        # Reshape to (384,14,14)
        self.c3 = Conv2d(192, 384,7,1,padding="same")
        self.c4 = Conv2d(384,384, 7,1,padding="same")
        # Reshape to (256,14,14)
        self.c5 = Conv2d(384, 256, 5,1,padding="same")
        # Reshape from (256,14,14) to (256,5,5)
        self.p3 = MaxPool2d(3, 2)

        self.d1 = Dropout(p=0.2)
        # Flatten here, then begin fully-connected layers
        self.l1 = Linear(6400, 1200)
        self.d2 = Dropout(p=0.2)
        self.l2 = Linear(1200, 120)
        self.l3 = Linear(120, 10)
        self.l4 = Linear(10,2)
         
    def forward(self, x):
        x = self.c1(x)
        x = self.p1(relu(x))
        x = relu(self.c2(x))
        x = self.p2(x)
        x = relu(self.c3(x))
        x = relu(self.c4(x))
        x = relu(self.c5(x))
        x = self.p3(x)
        x = self.d1(x)
        
        x = flatten(x,1)
        x = relu(self.l1(x))
        x = self.d2(x)
        x = relu(self.l2(x))
        x = relu(self.l3(x))
        x = softmax(self.l4(x), dim=1)
        return x

def is_increasing(losses):
    for i in range(1, len(losses)):
        if losses[i]<losses[i-1]:
            return False
    return True

if __name__ == "__main__":
    saved = False
    ds = ImDataset.ImDataset()
    model = CNN().to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(), lr=0.0001, momentum=0.9)
    epochs = 30
    train_size = int(len(ds)*0.9)+1
    test_size = int(len(ds)*0.1)
    train_data, val_data = random_split(ds, [train_size, test_size])
    train_loader = DataLoader(train_data, batch_size = 64, shuffle=True)
    val_loader = DataLoader(val_data, batch_size=64, shuffle =True)

    val_losses = []
    print("Training")
    for epoch in range(epochs):
        batch_c = 0
        running_loss = 0.0
        model.train()
        for X_train, y_train in train_loader:
            optimizer.zero_grad()
            y_train = y_train.float()
            X_train = X_train.to(device)
            y_train = y_train.to(device)
            y_pred = model(X_train)
            y_pred = torch.amax(y_pred, axis=1)
            y_pred = y_pred.float()
            loss = criterion(y_pred, y_train)
            loss.backward()
            optimizer.step()
            running_loss += float(loss.item())
            batch_c += 1
        valid_loss = 0.0
        model.eval()
        for X_val, y_val in val_loader:
            y_val = y_val.float()
            X_val = X_val.to(device)
            y_val = y_val.to(device)
            y_pred_val = model(X_val)
            y_pred_val = torch.amax(y_pred_val, axis=1)
            y_pred_val=y_pred_val.float()
            loss = criterion(y_pred_val, y_val)
            valid_loss += float(loss)
            val_losses.append(valid_loss)
        print("epoch:{}, loss:{}, valid_loss:{}".format(epoch, running_loss, valid_loss))
        with open("losses.txt", "a") as f:
            f.write("epoch:{}, loss:{}, valid_loss:{}".format(epoch, running_loss, valid_loss))
            
        torch.save(model.state_dict(), "model.pt"+str(epoch))

