import boto3

client = boto3.client('s3')
res = client.get_object(Bucket="arn:aws:s3-object-lambda:us-east-1:068469771374:accesspoint/s3-lambda-3c2", Key = "n01514668/n01514668_10004.JPEG")
print(res)
