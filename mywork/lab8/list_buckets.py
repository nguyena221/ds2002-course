import boto3

# create client
s3 = boto3.client('s3', region_name='us-east-1')

# make request
response = s3.list_buckets()

# print all bucket names
for r in response['Buckets']:
    print(r['Name'])