import numpy as np
import torch
from sklearn.model_selection import train_test_split
import os
import mysql.connector
import boto3
from PIL import Image

client = boto3.client('s3')

class ImDataset():

    REGION = "us-east-1a"

    os.environ['LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN'] = '1'
    def __init__(self,mode="part1", db_table="data_paths", db_host="gnome-1.cwqqmyn32oy5.us-east-1.rds.amazonaws.com", bucket_arn="arn:aws:s3-object-lambda:us-east-1:068469771374:accesspoint/s3-lambda-3c2"):
        num_files = 167585
        self.batch_size = 10
        self.file_indices = np.arange(0,num_files,1)
        self.train_indices, self.val_indices = train_test_split(self.file_indices, train_size=0.9, test_size=0.1)
        self.n_batches = len(self.train_indices)
        self.table = db_table
        self.mode = mode
        self.db_host = db_host
        self.arn = bucket_arn

    def reshuffle(self):
        self.train_indices, self.val_indices = train_test_split(self.file_indices, train_size = 0.9, test_size = 0.1)

    def __getitem__(self, idx):
        start = idx*self.batch_size
        return self.query_db(self.train_indices[start:start+10])

    def query_db(self,idxs):
        conn = mysql.connector.connect(host=self.db_host, user="dev", password="gnome123", port="3306", database="train")
        cur = conn.cursor()
        query_results = []
        for idx in idxs:
            cur.execute("SELECT * FROM {} WHERE id={};".format(self.table,idx))
            query_results.append(cur.fetchall()[0])
        X_paths = list(map(lambda x: x[1], query_results))
        y_labels = torch.Tensor(list(map(lambda x: x[-1], query_results)))
        X = list()
        for val in X_paths:
            print(val)
            res = client.get_object(Bucket=self.arn, Key = val)
            img_arr = np.frombuffer(res["Body"].read(), dtype=np.float32)
            img_arr = img_arr.reshape((720,1280, 3))
            t_img = img_arr.copy()
            X.append(t_img)
        X = torch.Tensor(X)
        return X, y_labels

if __name__ == "__main__":
    ds= ImDataset()
    print(ds[0])
