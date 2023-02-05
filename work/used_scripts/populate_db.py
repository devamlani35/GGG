import pandas as pd
import mysql.connector
import sys
import boto3
import os
import json

"""
Script to load image pathes from JSON and populate RDS
"""
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
token="*****"
# Load Files
with open("out.json") as f:
    dir_files = json.load(f)
with open("text_load.txt") as f:
    yeses = list(map(str.strip, f.readlines()))

try:
    #Connect to RDS MySQL
    conn =  mysql.connector.connect(host=ENDPOINT, user=USER, password=token, port=PORT, database=DBNAME)
    cur = conn.cursor()

    counter = 0
    id = 0
    # For file, label
    for key,vals in dir_files.items():
        label = 0
        points = []
        if key in yeses:
             label = 1
        for file in vals:
            path = key + "/" + file
            points.append([id,path, label])
            id += 1
        #Insert id, file, label into mysql
        query = """INSERT INTO data_paths (id,path, label) VALUES (%s, %s, %s)"""
        counter += 1
        print(counter)
        cur.executemany(query, points)

    query_results = cur.fetchall()
    conn.commit()
    print(query_results)
except Exception as e:
    print("Database connection failed due to {}".format(e))
