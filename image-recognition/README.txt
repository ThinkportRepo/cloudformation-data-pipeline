Image Recognition CloudFormation Stack

This repository contains all files required to build an image recognition module via AWS CloudFormation.
It accesses images from an S3 bucket and copies them to a new S3 bucket if they contain a given object.
Requires an AWS Account with access permission to CloudFormation, S3, Lambda, IAM Roles and CloudWatch.


Setup

1. You need AWS S3 buckets that contain your raw data and your lambda code.
Create your own via S3 directly, use existing ones or build them via CloudFormation using the provided .yml file.
For the latter:
AWS Services (in your internet browser)
--> CloudFormation
--> Create Stack
--> With new resources
--> Template is ready
--> Upload a teamplate file
--> Choose "data-transform_buckets.yml" from the repository. Then, enter a stack name, the requested parameters
and any tags you might want to give the stack (ex: name).
If constructed this way, the names of the buckets will be "[appName]-[environment]-[your AWS Account ID]--rawdata"
and "[appName]-[environment]-[your AWS Account ID]--code" (using the parameters you entered).

2. Place "image-recognition_lambda.py.zip" (important: .zip version) in the code bucket you just created.
Do not rename this file.

3. Build the image recognition stack itself:
AWS Services
--> CloudFormation
--> Create Stack
--> With new resources
--> Template is ready
--> Upload a teamplate file
--> Choose "image-recognition.yml" from the repository. IMPORTANT: In the "Parameters" section, you have to set
"codeBucketName" as the name of the bucket that contains your code, and likewise "sourceBucketName" for your
raw data bucket. The latter CANNOT BE CHANGED later (in the same stack - you can of course build a new one).
"imageRecognitionObject" is the object you will search for in images (ex: Car, Dog, Flower) and can later be changed.
Also, enter a stack name and any tags you might want to give the stack (ex: name).

4. To delete a stack, first empty all S3 buckets that it contains. Deleting a stack will also delete
all associated resources unless specified otherwise.


Usage

Upload an image file to your raw data bucket. If it contains the object specified in step 3 ("imageRecognitionObject"),
it will be copied into the result bucket ("[appName]-[environment]-[your AWS Account ID]--result").
You can change the object to recognize at any time:
AWS Services
--> CloudFormation
--> Choose the stack
--> Update
--> Use current Template
--> Enter a different "imageRecognitionObject"