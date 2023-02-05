# Garden Gnome Guardian, Real-time pest detection trained on ImageNet
## infrastructure:
#### Model training hosted on Amazon EC2 server
#### Image files stored in AWS S3 Bucket
#### Customized Lambda function triggered on get-object operation to preprocess image data
#### S3 image paths and corresponding labels stored in an AWS MySql rds
