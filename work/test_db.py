import pandas as pd
import mysql.connector
import sys
import boto3
import os
import json
ENDPOINT = "gnome-1.cwqqmyn32oy5.us-east-1.rds.amazonaws.com"
PORT="3306"
USER="dev"
REGION="us-east-1a"
DBNAME="train"
os.environ['LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN'] = '1'
#Num_files = 167585
#gets the credentials from .aws/credentials
session = boto3.Session(profile_name='default')
client = session.client('rds')
token="gnome123"
conn =  mysql.connector.connect(host=ENDPOINT, user=USER, password=token, port=PORT, database=DBNAME)
df = pd.read_sql_table("data_paths", conn)
print(df.shape)
