#!/bin/bash

FILE="$1"
BUCKET="$2"
EXPIRE="$3"

aws s3 cp "$FILE" "s3://$BUCKET/"
aws s3 presign --expires-in "$EXPIRE" "s3://$BUCKET/$(basename "$FILE")"