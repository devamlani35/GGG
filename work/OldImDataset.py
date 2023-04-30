import numpy as np
import torch
from sklearn.model_selection import train_test_split
import os
import mysql.connector
import boto3
from PIL import Image
import time
client = boto3.client('s3')

# Custom Dataset class, does not inherit from torch Dataset because files are not stored on hard drive
class ImDataset():
    REGION = "us-east-1a"
    os.environ['LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN'] = '1'

    # Initialization function, sets instance variables
    def __init__(self,num_files = 167585, mode="part1", db_table="data_paths", db_host="gnome-1.cwqqmyn32oy5.us-east-1.rds.amazonaws.com", bucket_arn="arn:aws:s3-object-lambda:us-east-1:068469771374:accesspoint/s3-lambda-3c2"):
        self.batch_size = 10
        self.file_indices = np.arange(0,num_files,1)
        self.train_indices, self.val_indices = train_test_split(self.file_indices, train_size=0.9, test_size=0.1)
        self.table = db_table
        self.mode = mode
        self.db_host = db_host
        self.arn = bucket_arn

    # Reshuffles batches between epochs
    def reshuffle(self):
        self.train_indices, self.val_indices = train_test_split(self.file_indices, train_size = 0.9, test_size = 0.1)

    # Implementation of __getitem__, calls helper method query_db
    def __getitem__(self, idx):
        start = idx*self.batch_size
        return self.query_db(self.train_indices[start:start+self.batch_size])

    # Returns the number of batches
    def __len__(self):
        length = len(self.train_indices)//self.batch_size+1
        if len(self.train_indices)%self.batch_size:
            length -= 1
        return length

    # Returns the size of the validation set
    def get_len_val(self):
        return len(self.val_indices)

    # Method to get images from s3 buckets
    def query_db(self,idxs):
        #Connects to rds
        start_time = time.time()
        conn = mysql.connector.connect(host=self.db_host, user="dev", password="gnome123", port="3306", database="train")
        cur = conn.cursor()
        query_results = []
        # Queries the file paths and corresponding labels
        for idx in idxs:
            cur.execute("SELECT * FROM {} WHERE id={};".format(self.table,idx))
            query_results.append(cur.fetchall()[0])
        print(time.time()-start_time)
        x_paths = list(map(lambda x: x[1], query_results))
        y_labels = torch.Tensor(list(map(lambda x: x[-1], query_results)))
        x = list()
        # Calls GETOBJECT on s3 API for each file in x_paths, uses lambda endpoint to get preprocessed images
        for val in x_paths:
            try:
                res = client.get_object(Bucket=self.arn, Key = val)

                # Changes bytes to numpy array and reshapes
                img_arr = np.frombuffer(res["Body"].read(), dtype=np.float32)
                img_arr = img_arr.reshape((720,1280, 3))
                t_img = img_arr.copy()
                x.append(t_img)
            except:
                return None, None
        x = np.array(x)
        x = torch.Tensor(x)
        x = torch.permute(x, (0,3,1,2))
        return x, y_labels

    # Gets a validation data point
    def get_valid(self, idx):
        return self.query_db(self.val_indices[idx])[0]


if __name__ == "__main__":
    ds= ImDataset()
    print(ds[0])
