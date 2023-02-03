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
cur = conn.cursor()
cur.execute("SELECT * FROM data_paths WHERE id=3;")
query_results = cur.fetchall()
<<<<<<< HEAD:work/test_db.py
print(query_results)
=======
print(query_results)
>>>>>>> 08316499b573eba334c6e2e31edf262b7a686458:work/used_scripts/test_db.py
