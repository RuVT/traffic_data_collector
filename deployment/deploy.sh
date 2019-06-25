#!/usr/bin/env bash
KEY=$1
BUILD_NUMBER=$2
if [ -z $KEY ] || [ -z $BUILD_NUMBER ]
then
    echo "Usage: deploy.sh <GOOGLE_API_KEY> <BUILD_NUMBER>"
    exit 1
fi
pip3 install pipenv --user
pushd $BUILD_NUMBER
serverless deploy --GOOGLE_MAPS_API_KEY  --alias $BUILD_NUMBER
popd
