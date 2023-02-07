# Garden Gnome Guardian, Real-time pest detection trained on ImageNet
## Goal:
##### To use deep learning techniques to identify and locate garden pests (ex. Squirrels) in image frames in real time. 
## Cloud Infrastructure:
##### Model training hosted on Amazon EC2 server
##### Image files stored in AWS S3 Bucket
##### Customized Lambda function triggered on get-object operation to preprocess image data
##### S3 image paths and corresponding labels stored in an AWS MySql RDS
## ImDataset
##### Customized Dataset/Dataloader used to query training/validation data through use of AWS S3 API
##### TODO: Add asynchronous calls to accelerate model training
## Real-time detection using pyTorch
### Two models: one Convolutional Neural Network and one Regional Convolutional Neural Network
##### First model used for computational ease, determines whether a pest is detected
##### This model is loosely based on AlexNet
##### TODO: Implement and optimize second model to locate the pest within a camera frame
## Expansions/modifications:
##### Hyperparameters can be adjusted and finetuned for different object detection tasks
##### Model can be adjusted for multi-class classification






MIT License

Copyright (c) 2023 Dev Amlani

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
