import json
import boto3
import os
from urllib.parse import unquote_plus
from PIL import Image
from io import BytesIO


s3_client = boto3.client('s3')


def lambda_handler(event, context):
    # read environment variables
    result_bucket = os.environ['resultBucketNameVar']
    side = os.environ['imageMaxSizeVar']
    print('resizing to a max side length of ' + side)
    side = int(side)
    size = (side, side)
    for record in event['Records']:
        # find source file (hopefully an image)
        source_bucket = record['s3']['bucket']['name']
        source_key = unquote_plus(record['s3']['object']['key'])
        print('sourceBucket: ', source_bucket)
        print('source_key: ', source_key)
        response = {}
        # downsize ----------------
        resized_key = 'resized_' + source_key
        small_image = downsize_image(source_bucket, source_key, size)
        # -------------------------
        if small_image != False:
            # if resizing worked, save resized image
            s3_client.put_object(
                Body = small_image,
                Bucket = result_bucket,
                Key = resized_key
            )
            print('resized!')
            response = {'Image': 'resized'}
        else:
            # if not an image, return error
            print('something went wrong. not an image file?')
            response = {'Image:': 'failed'}
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }


def downsize_image(bucket, key, size):
    try:
        # load image
        file_byte_string = s3_client.get_object(Bucket=bucket, Key=key)['Body'].read()
        image = Image.open(BytesIO(file_byte_string))
        # actualy downsizing
        image.thumbnail(size, Image.ANTIALIAS)
        # create a temporary file to save new image to (and jump to start)
        temp_file = BytesIO()
        image.save(temp_file, format=image.format)
        temp_file.seek(0)
    except Exception as e:
        # if it didnt work, set to False
        print(e)
        temp_file = False
    return temp_file
