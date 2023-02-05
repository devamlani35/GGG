# Garden Gnome Guardian, Real-time pest detection trained on ImageNet
## Cloud Infrastructure:
#### Model training hosted on Amazon EC2 server
#### Image files stored in AWS S3 Bucket
#### Customized Lambda function triggered on get-object operation to preprocess image data
#### S3 image paths and corresponding labels stored in an AWS MySql RDS
## ImDataset
#### Customized Dataset/Dataloader used to query training/validation data through use of AWS S3 API
#### TODO: Add asynchronous calls to accelerate model training
## Real-time detection using pyTorch
### Two models: one Convolutional Neural Network and one Regional Convolutional Neural Network
#### First model used for computational ease, determines whether a pest is detected
#### This model is loosely based on AlexNet
#### TODO: Implement and optimize second model to locate the pest within a camera frame
