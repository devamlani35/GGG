import boto3
import numpy as np
from PIL import Image
if __name__ == "__main__":
    client = boto3.client('s3')
    res = client.get_object(Bucket="arn:aws:s3-object-lambda:us-east-1:068469771374:accesspoint/s3-lambda-3c2", Key = "n01514668/n01514668_10004.JPEG")
    img_arr = np.frombuffer(res["Body"].read(), dtype=np.float32)
    img_arr = img_arr.reshape((720,1280, 3))
    new_arr = img_arr*255
    new_arr = new_arr.astype(np.int8)
    print(new_arr)
    img = Image.fromarray(new_arr, "RGB")
    img.show()
