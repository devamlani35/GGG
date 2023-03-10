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
relu = F.relu
device = torch.device("cuda:0")

class CNN (nn.Module):

    def __init__ (self):
        super().__init__()
        #Note: when training, all shapes begin with batch_size
        # Reshape to (48,234,420)
        self.c1 = Conv2d(3,48,21,3, padding=0)
        # Reshape to (48,77,139)
        self.p1 = MaxPool2d(5,3)
        # Reshape to (192,24,45)
        self.c2 = Conv2d(48, 192,7,3)
        # Reshape to (192,14,18)
        self.p2 = MaxPool2d(11, (1,2))
        # Reshape to (384,14,18)
        self.c3 = Conv2d(192, 384,7,1,padding="same")
        self.c4 = Conv2d(384,384, 7,1,padding="same")
        # Reshape to (256,14,18)
        self.c5 = Conv2d(384, 256, 5,1,padding="same")
        # Reshape from (256,14,18) to (256,6,8)
        self.p3 = MaxPool2d(3, 2)

        self.d1 = Dropout(p=0.2)
        # Flatten here, then begin fully-connected layers
        self.l1 = Linear(12288, 1200)
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
    optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)
    epochs = 50
    val_losses = []
    print("Training")
    for epoch in range(epochs):
        running_loss = 0.0
        ds.reshuffle()
        model.train()
        for batch_c in range(len(ds)):
            print(batch_c)
            X_train, y_train = ds[batch_c]
            print("got_scans")
            optimizer.zero_grad()
            if X_train==None:
                continue
            X_train = X_train.to(device)
            y_train = y_train.to(device)
            start_time = time.time()
            y_pred = model(X_train)
            y_pred = torch.amax(y_pred, axis=1)
            loss = criterion(y_pred, y_train)
            loss.backward()
            optimizer.step()
            print(time.time()-start_time)
            running_loss += loss.item()
            if not batch_c%1000:
                print("epoch = {}, batch = {}, loss = {}".format(epoch, batch_c, running_loss))
        valid_loss = 0.0
        model.eval()
        for bc in range(ds.get_len_val()):
            X_test, y_test = ds.get_valid_batch(bc)
            if (X_test, y_test) == (None, None):
                continue
            y_pred_val = model(X_test)
            y_pred_val = torch.amax(y_pred_val, axis=1)
            loss = criterion(y_pred_val, y_test)
            valid_loss += loss
        if valid_loss < val_losses[-1]:
            print("saving model")
            with open("model.pt", "w") as f:
                torch.save(model,f)
            saved=True
        val_losses.append(valid_loss)
        if len(val_losses) > 10 and is_increasing(val_losses[-5:]):
            if saved:
                print("Ending training, not saving")
                break
            else:
                with open("model.pt", "w") as f:
                    torch.save(model, f)
                    print("Ending training, saving")
                    break

    print("Model training terminated, final loss: {}, final epochs: {}".format(val_losses[-1], epoch))

