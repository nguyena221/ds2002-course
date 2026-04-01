#!/bin/bash

AMI=ami-REPLACE_ME
INSTANCE_TYPE=t2.nano
INSTANCE_NAME=ds2002-bvc5vq
KEY_NAME=key-ec2-bvc5vq
SECURITY_GROUP_ID=sg-REPLACE_ME
SUBNET_ID=subnet-REPLACE_ME

aws ec2 run-instances \
  --image-id "$AMI" \
  --instance-type "$INSTANCE_TYPE" \
  --key-name "$KEY_NAME" \
  --security-group-ids "$SECURITY_GROUP_ID" \
  --subnet-id "$SUBNET_ID" \
  --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=$INSTANCE_NAME}]"
