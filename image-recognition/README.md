# Image Recognition CloudFormation Module

This repository contains all files required to build an image recognition module via AWS. It accesses images from an S3 bucket and saves all images with/without a given object to a new S3 bucket (with or without depends on the chosen mode).

Requires an AWS Account with access permission to CloudFormation, S3, Lambda, IAM Roles, CloudWatch and Amazon Rekognition.


## Setup

1. You need AWS S3 buckets that contain your source data and your lambda code. Create your own via S3 directly, use existing ones or build them via CloudFormation using the provided .yml file. For the latter, repeat for code and source:
* AWS Services (in your internet browser)
* CloudFormation
* Create Stack
* With new resources
* Template is ready
* Upload a teamplate file
* Choose "code-bucket.yml" / "source-bucket.yml" from the repository. Then, enter a stack name, the requested parameters and any tags you might want to give the stack (ex: name).
If constructed this way, the names of the buckets will be "[appName]-[environment]-[your AWS Account ID]--code" and "[appName]-[environment]-[your AWS Account ID]--source", using the parameters you entered.

2. Place "image-recognition_lambda.py.zip" (important: .zip version) from the repository in the code bucket you just created/identified.

3. Build the image recognition stack itself:
* AWS Services
* CloudFormation
* Create Stack
* With new resources
* Template is ready
* Upload a teamplate file
* Choose "image-recognition.yml" from the repository. IMPORTANT: In the "Parameters" section, you have to set "codeBucketName" as the name of the bucket that contains your code, and likewise "sourceBucketName" for your source bucket. "codeKey" is the name of your lambda function and "codeRuntime" its runtime, for which the default is correct unless you changed them. For the other parameters, follow their descriptions. They can later be changed. Also, add any tags you might want to give the stack (ex: name).

4. Set a notification trigger from your source bucket to the lambda function.
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

5. To delete a stack, first empty all S3 buckets that it contains. Deleting a stack will also delete
all associated resources unless specified otherwise.


## Alternative Setup via Bash Script -- requires a Unix system

1. Create/identitfy source and code buckets as above.

2. Open "deployment.sh" and enter your parameters in the first part as requested.
* accId_param: your Accound Number (Find it via "aws sts get-caller-identity", key "Account")
* region_param: the default region your account will be set to, where all resources will be deployed
* appName_param: your app's name
* environment_param: your app's current environment (eg. "dev")
* stackName_param: your CloudFormation Stack's name
* codeBucketName_param: s3 bucket that contains your lambda code
* sourceBucketName_param: source s3 bucket
* imageRecognitionObject_param: the object to be recognized in images
* imageRecognitionMode_param: search for images with/without imageRecognitionObject by setting as "with" or "without"
* imageRecognitionConfidence_param: the minimum confidence for the recognition algorithm, in percent (> 55)

3. Run "deployment.sh" via "bash deployment.sh".


## Usage

Upload an image file to your source bucket. If it contains (or does not contain, depending on mode) the object specified in step 3 ("imageRecognitionObject"), it will be copied into the result bucket ("[appName]-[environment]-[your AWS Account ID]--result"). You can change the object to be recognized, the recognition mode (with/without the object) and the minimum confidence at any time:
* AWS Services
* CloudFormation
* Choose the stack
* Update
* Use current Template
* Enter a different "imageRecognitionObject"/"imageRecognitionMode"/"imageRecognitionConfidence"
