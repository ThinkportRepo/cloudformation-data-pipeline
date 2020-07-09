import json
import boto3
import os
from urllib.parse import unquote_plus


s3_client = boto3.client('s3')
rekognition_client = boto3.client('rekognition')


def lambda_handler(event, context):
    # read environment variables
    result_bucket = os.environ['resultBucketNameVar']
    rec_object = os.environ['recognitionObject']
    rec_confidence = int(os.environ['recognitionConfidence']) # cloudformation only allows numbers between 55 and 100
    rec_mode = os.environ['recognitionMode'] # cloudformation only allows "with" or "without"
    print('searching for images ' + rec_mode + ' ' + rec_object + ' with at least ' + str(rec_confidence) + ' % confidence')
    for record in event['Records']:
        # find source file (hopefully an image)
        source_bucket = record['s3']['bucket']['name']
        source_key = unquote_plus(record['s3']['object']['key'])
        print('sourceBucket: ' + source_bucket + ', source_key: ' + source_key)
        response = {}
        # transform ---------------
        object_found = recognize_object(source_bucket, source_key, rec_object, rec_confidence)
        # -------------------------
        if object_found == 'error':
            # if not an image, return error
            print('not an image?')
            response = {'Object': 'not an image'}
        else:
            if (object_found and rec_mode == 'with'):
                # if mode is "with" and an object is found, copy the image to result bucket
                result_key = rec_object + '-containing_' + source_key
                s3_client.copy({'Bucket': source_bucket, 'Key': source_key}, result_bucket, result_key)
                print('found ' + rec_object + ', therefore copied!')
                response = {'Object': 'successfully found'}
            elif (not object_found) and rec_mode == 'without':
                # if mode is "without" and no object is found, copy the image to result bucket
                result_key = rec_object + '-free_' + source_key
                s3_client.copy({'Bucket': source_bucket, 'Key': source_key}, result_bucket, result_key)
                print('found no ' + rec_object + ', therefore copied!')
                response = {'Object': 'successfully not found'}
            else:
                # else, don't copy
                print('not an image ' + rec_mode + ' ' + rec_object + ', so not copied')
                response = {'Object': 'not what we wanted'}
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }


def recognize_object(bucket, key, object, confidence):
    object_found = False
    try:
        # run Amazon Rekognition with minimum confidence
        rekognition_answer = rekognition_client.detect_labels(
            Image = {'S3Object': {'Bucket': bucket, 'Name': key}},
            MinConfidence = confidence
        )
        for label in rekognition_answer['Labels']:
            # check all labels for our object
            print(label['Name'] + ' with ' + str(round(label['Confidence'])) + ' % confidence')
            if label['Name'].lower() == object.lower() and label['Confidence'] >= confidence:
                object_found = True
                print('found ' + object + "!!")
                # break # if you don't want to read all recognized objects
    except Exception as e:
        # if it didnt work, set to error
        print(e)
        object_found = 'error'
    return object_found