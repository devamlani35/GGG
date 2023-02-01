import boto3
import numpy as np
if __name__ == "__main__":
    client = boto3.client('s3', aws_access_key_id="AKIAQ74I5ZRXHM5AEHSH", aws_secret_access_key="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")
    res = client.get_object(Bucket="arn:aws:s3-object-lambda:us-east-1:068469771374:accesspoint/s3-lambda-3c2", Key = "n01514668/n01514668_10004.JPEG")
    img_arr = np.frombuffer(res["Body"].read(), dtype=np.float32)
    img_arr = img_arr.reshape((720,1280, 3))
    print(img_arr)
