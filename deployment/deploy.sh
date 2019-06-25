#!/usr/bin/env bash
KEY=$1
if [ -z $KEY ]
then
    echo "Usage: deploy '<GOOGLE_API_KEY>'"
    exit 1
fi
echo "serverless deploy -- --GOOGLE_MAPS_API_KEY $KEY"