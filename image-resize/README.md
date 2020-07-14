# Image Resizing CloudFormation Module

This repository contains all files required to build an image resizing module via AWS. It accesses images from an S3 bucket, resizes them (retaining the aspect ratio) and saves the resized images to a new S3 bucket.

Requires an AWS Account with access permission to CloudFormation, S3, Lambda, IAM Roles and CloudWatch.


Setup

1. You need AWS S3 buckets that contain your source data and your lambda code. Create your own via S3 directly, use existing ones or build them via CloudFormation using the provided .yml file. For the latter, repeat for code and source:
* AWS Services (in your internet browser)
* CloudFormation
* Create Stack
* With new resources
* Template is ready
* Upload a teamplate file
* Choose "code-bucket.yml" / "source-bucket.yml" from the repository. Then, enter a stack name, the requested parameters and any tags you might want to give the stack (ex: name). If constructed this way, the names of the buckets will be "[appName]-[environment]-[your AWS Account ID]--code" and "[appName]-[environment]-[your AWS Account ID]--source", using the parameters you entered.

2. Place "image-resize_lambda.py.zip" and "Klayers-python37-Pillow.zip" (important: .zip versions) from the repository in the code bucket you just created/identified.

3. Build the image recognition stack itself:
* AWS Services
* CloudFormation
* Create Stack
* With new resources
* Template is ready
* Upload a teamplate file
* Choose "image-resize_lambda.yml" from the repository. IMPORTANT: In the "Parameters" section, you have to set "codeBucketName" as the name of the bucket that contains your code, and likewise "sourceBucketName" for your source bucket. "codeKey" is the name of your lambda function and "codeRuntime" its runtime, for which the default is correct unless you changed them. "imageMaxSize" is the maximum side length your resized images will have in pixels. For the other parameters, follow their descriptions. They can later be changed. Also, add any tags you might want to give the stack (ex: name).

4. Set a notification trigger from your source bucket to the lambda function:
* AWS Services
* S3
* Choose your source bucket
* Properties
* Events (scroll down)
* Add notification
* Give it a descriptive name
* Choose "All object create events"
* For "Send to", choose "Lambda Function"
* Choose your lambda function
* Save

5. To delete a stack, first empty all S3 buckets that it contains. Deleting a stack will also delete all associated resources unless specified otherwise.


Usage

Upload an image file to your source bucket. It will be resized to the maximum side length given in step 3 ("imageMaxSize"), retaining the aspect ratio of the image. The resized image is saved to the result bucket ("[appName]-[environment]-[your AWS Account ID]--result").
You can change the maximum side length at any time:
* AWS Services
* CloudFormation
* Choose the stack
* Update
* Use current template
* Enter a different "imageMaxSize"
