import boto3
import numpy as np
from PIL import Image
if __name__ == "__main__":
    # Script to test preprocessing done by AWS Lambda by undoing steps and reshowing image
    client = boto3.client('s3')
    # Load object through Lambda access point
    res = client.get_object(Bucket="arn:aws:s3-object-lambda:us-east-1:068469771374:accesspoint/s3-lambda-3c2", Key = "n01514668/n01514668_10004.JPEG")
    # Convert from bytes into image
    img_arr = np.frombuffer(res["Body"].read(), dtype=np.float32)
    img_arr = img_arr.reshape((720,1280, 3))
    new_arr = img_arr*255
    new_arr = new_arr.astype(np.int8)
    img = Image.fromarray(new_arr, "RGB")
    # Show image
    img.show()
