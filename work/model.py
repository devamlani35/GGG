import torch
import torch.nn as nn
import numpy as np
import pandas as pd
import torch.nn.functional as F
from torch.nn.functional import softmax
from torch.nn import MaxPool2d
from torch.nn import Conv2d
from torch import flatten
from torch.nn import Dropout
from torch.nn import Linear
import torch.optim as optim
import ImDataset
relu = F.relu


class CNN (nn.Module):

    def __init__ (self):
        super().__init__()
        # Reshape from (720,1280,3) to (233,420,48)
        self.c1 = Conv2d(3,48,21,3)
        # Reshape from (233,420,48) to (76,138,48)
        self.p1 = MaxPool2d(5,3)
        # Reshape from (76,138,48) to (23,44,192)
        self.c2 = Conv2d(48, 192,7,3)
        # Reshape from (23,44,192) to (13,17,192)
        self.p2 = MaxPool2d(11, (1,2))
        # Retains Shape
        self.c3 = Conv2d(192, 384,7,1,padding="same")
        self.c4 = Conv2d(384,384, 7,1,padding="same")
        self.c5 = Conv2d(384, 256, 5,1,padding="same")
        # Reshape from (13,17,192) to (5,7,192)
        self.p3 = MaxPool2d(3, 2)

        self.d1 = Dropout(p=0.2)
        # Flatten here, then begin fully-connected layers
        self.l1 = Linear(6720, 1200)
        self.d2 = Dropout(p=0.2)
        self.l2 = Linear(1200, 120)
        self.l3 = Linear(120, 10)
        self.l4 = Linear(10,2)
        
    def forward(self, x):
        x = self.p1(relu(self.c1(x)))
        x = self.p2(relu(self.c2(x)))
        x = relu(self.c3(x))
        x = relu(self.c4(x))
        x = relu(self.c5(x))
        x = self.p3(x)
        x = self.d1(x)
        x = flatten(x)
        x = relu(self.l1(x))
        x = self.d2(x)
        x = relu(self.l2(x))
        x = relu(self.l3(x))
        x = softmax(self.l4(x))
        return x

def is_increasing(losses):
    for i in range(1, len(losses)):
        if losses[i]<losses[i-1]:
            return False
    return True

if __name__ == "__main__":
    saved = False
    ds = ImDataset.ImDataset()
    model = CNN()
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
            X_train, y_train = ds[batch_c]
            print("got_scans")
            optimizer.zero_grad()

            y_pred = model(X_train)
            loss = criterion(y_train, y_pred)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
            print("batch_done")
            if not batch_c%1000:
                print("epoch = {}, batch = {}, loss = {}".format(epoch, batch_c, running_loss))
        valid_loss = 0.0
        model.eval()
        for bc in range(ds.get_len_val()):
            X_test, y_test = ds.get_valid_batch(bc)
            y_pred_val = model(X_test)
            loss = criterion(y_test, y_pred_val)
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
