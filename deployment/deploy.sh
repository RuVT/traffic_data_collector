#!/usr/bin/env bash
KEY=$1
ENV=$2
if [ -z $KEY ] || [ -z $ENV ]
then
    echo "Usage: deploy.sh <GOOGLE_API_KEY> <stg/prd>"
    exit 1
fi

npm install
pipenv install
npm run deploy -- --GOOGLE_MAPS_API_KEY  --stage "${ENV,,}"
