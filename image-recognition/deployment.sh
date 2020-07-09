# deployment sh for image recognition stack

# ------- parameters -------
# PLEASE CHANGE ACCORDINGLY

# find your accNumber via "aws sts get-caller-identity", the "account" number

accNumber_param="562760952310"
region_param="eu-central-1"

appName_param="image-recognition"
environment_param="test"
stackName_param="imageRecognitionStack"
codeBucketName_param="0000000code-bucket"
sourceBucketName_param="0000000data-bucket"

# can be any object
imageRecognitionObject_param="Cat"
# can be with or without
imageRecognitionMode_param="with"
# can be 55-100
imageRecognitionConfidence_param=55

# only change if you also change the corresponding files
templateName_param="image-recognition.yml"
codeKey_param="image-recognition_lambda.py"
codeRuntime_param="python3.7"


# --------------------------------------------
# ------- automatic part starting here -------
# --------------------------------------------


# ------- set region -------

aws configure set region "$region_param"
aws configure set default.region "$region_param"

# ------- create/update lambda zip and place in bucket -------

rm "${codeKey_param}.zip"
zip "${codeKey_param}.zip" "$codeKey_param"

aws s3api put-object \
    --bucket "$codeBucketName_param" \
    --key "${codeKey_param}.zip" \
    --body "${codeKey_param}.zip"

# ------- deploy cloudformation stack -------

aws cloudformation deploy \
    --template-file "$templateName_param" \
    --stack-name "$stackName_param" \
    --tags name="$stackName_param" \
    --capabilities CAPABILITY_NAMED_IAM \
    --parameter-overrides \
        appName="$appName_param" \
        codeBucketName="$codeBucketName_param" \
        codeKey="${codeKey_param}.zip" \
        codeRuntime="$codeRuntime_param" \
        environment="$environment_param" \
        imageRecognitionConfidence="$imageRecognitionConfidence_param" \
        imageRecognitionMode="$imageRecognitionMode_param" \
        imageRecognitionObject="$imageRecognitionObject_param" \
        sourceBucketName="$sourceBucketName_param"

# ------- configure notification trigger -------

# build the lambda arn to use in json
lambdaArn="arn:aws:lambda:${region_param}:${accNumber_param}:function:${appName_param}-${environment_param}--function"

# note: this will delete existing notification cnfigurations
aws s3api put-bucket-notification-configuration \
    --bucket "$sourceBucketName_param" \
    --notification-configuration '{
            "LambdaFunctionConfigurations": [
                {
                    "LambdaFunctionArn": "'"$lambdaArn"'",
                    "Events": ["s3:ObjectCreated:*"]
                }
            ]
        }'

# ------- update lambda code -------

aws lambda update-function-code \
    --function-name "${appName_param}-${environment_param}--function" \
    --s3-bucket "$codeBucketName_param" \
    --s3-key "${codeKey_param}.zip"


