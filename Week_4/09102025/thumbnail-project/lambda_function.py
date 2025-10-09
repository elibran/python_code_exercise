import boto3
import os
from urllib.parse import unquote_plus
from PIL import Image
import uuid

s3_client = boto3.client('s3')

def resize_image(image_path, resized_path):
    with Image.open(image_path) as image:
        image.thumbnail((128, 128))
        image.save(resized_path)

def lambda_handler(event, context):
    for record in event['Records']:
        source_bucket = record['s3']['bucket']['name']
        key = unquote_plus(record['s3']['object']['key'])
        dest_bucket = os.environ['DEST_BUCKET']
        download_path = f'/tmp/{uuid.uuid4()}{key}'
        upload_path = f'/tmp/resized-{key}'
        s3_client.download_file(source_bucket, key, download_path)
        resize_image(download_path, upload_path)
        dest_key = f'resized-{os.path.basename(key)}'
        s3_client.upload_file(upload_path, dest_bucket, dest_key)
    return {'statusCode': 200, 'body': 'Success!'}