import boto3

s3 = boto3.client('s3', region_name='us-east-1')

bucket = 'ds2002-bvc5vq'
local_file = 'another_image.jpg'
key = 'another_image.jpg'

with open(local_file, 'rb') as f:
    response = s3.put_object(
        Body=f,
        Bucket=bucket,
        Key=key,
        ACL='public-read'
    )

print(response)