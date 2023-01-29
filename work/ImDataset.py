import numpy as np
from sklearn.model_selection import train_test_split
import os
import mysql.connector
import boto3

class ImDataset():
    ENDPOINT = "gnome-1.cwqqmyn32oy5.us-east-1.rds.amazonaws.com"
    PORT = "3306"
    USER = "dev"
    REGION = "us-east-1a"
    DBNAME = "train"
    os.environ['LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN'] = '1'
    def __init__(self):
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
        

