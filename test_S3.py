# import boto3
# import boto3.s3
# import sys
# from boto3.s3.key import Key
import os

S3_BUCKET = os.environ.get('S3_BUCKET_NAME')
AWS_ACCESS_KEY_ID=os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY=os.environ.get('AWS_SECRET_ACCESS_KEY')



import boto3


# Create an S3 client
s3 = boto3.client('s3')

filename = "/Users/amirulislam/Desktop/images_quick_post/potsandpans.jpeg"
S3_BUCKET = os.environ.get('S3_BUCKET_NAME')

# Uploads the given file using a managed uploader, which will split up large
# files automatically and upload parts in parallel.
s3.upload_file(filename, S3_BUCKET, "images/filename")
 