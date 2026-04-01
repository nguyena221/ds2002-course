#!/bin/bash

AMI=ami-07ff62358b87c7116
INSTANCE_TYPE=t2.nano
INSTANCE_NAME=ds2002-bvc5vq
KEY_NAME=key-ec2-bvc5vq
SECURITY_GROUP_ID=sg-0be6679b34372f15a
SUBNET_ID=subnet-085a38474f2e3b60c

aws ec2 run-instances \
  --image-id "$AMI" \
  --instance-type "$INSTANCE_TYPE" \
  --key-name "$KEY_NAME" \
  --security-group-ids "$SECURITY_GROUP_ID" \
  --subnet-id "$SUBNET_ID" \
  --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=$INSTANCE_NAME}]"
