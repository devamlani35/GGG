import mysql.connector
import sys
import boto3
import os

ENDPOINT = "gnome-1.cwqqmyn32oy5.us-east-1.rds.amazonaws.com"
PORT="3306"
USER="dev"
REGION="us-east-1a"
DBNAME="train"
os.environ['LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN'] = '1'

#gets the credentials from .aws/credentials
session = boto3.Session(profile_name='default')
client = session.client('rds')
token="gnome123"
try:
    conn =  mysql.connector.connect(host=ENDPOINT, user=USER, password=token, port=PORT, database=DBNAME, ssl_ca='SSLCERTIFICATE')
    cur = conn.cursor()
    cur.execute("""SELECT now()""")
    query_results = cur.fetchall()
    print(query_results)
except Exception as e:
    print("Database connection failed due to {}".format(e))
