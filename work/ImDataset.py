import numpy as np
import torch
from sklearn.model_selection import train_test_split
import os
import mysql.connector
import boto3

client = boto3.client('s3')

class ImDataset():

    REGION = "us-east-1a"

    os.environ['LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN'] = '1'
    def __init__(self,mode, db_table, db_host, bucket_arn):
        num_files = 167585
        self.batch_size = 10
        self.file_indices = np.arange(0,num_files,1)
        self.train_indices, self.val_indices = train_test_split(self.file_indices, train_size=0.9, test_size=0.1)
        self.n_batches = len(self.train_indices)

    def reshuffle(self):
        self.train_indices, self.val_indices = train_test_split(self.file_indices, train_size = 0.9, test_size = 0.1)

    def __getitem__(self, idx):
        start = idx*self.batch_size
        return self.query_db(self.train_indices[start:start+10])

    def query_db(self,idxs):
        conn = mysql.connector.connect(host="gnome-1.cwqqmyn32oy5.us-east-1.rds.amazonaws.com", user="dev", password="gnome123", port="3306", database="train")
        cur = conn.cursor()
        for idx in range(idxs):
            cur.execute("SELECT * FROM data_paths WHERE id={};".format(idx))
        query_results = cur.fetchall()
        X_paths = list(map(lambda x: x[1], query_results))
        y_labels = torch.Tensor(list(map(lambda x: x[-1], query_results)))
        X = torch.Tensor()
        for val in X_paths:
            res =
            temp_x = torch.Tensor(res["data"])
            X.add(temp_x)
        return X, y_labels


