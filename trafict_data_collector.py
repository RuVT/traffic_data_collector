import os
import datetime
import requests
import json
import yaml
import boto3
from urllib.parse import quote_plus

BASE_URL = 'https://maps.googleapis.com/maps/api/distancematrix'
GOOGLE_MAPS_API_KEY = os.environ['GOOGLE_MAPS_API_KEY']
TRAFFIC_DATA_SOURCE_BUCKET_NAME = os.environ['TRAFFIC_DATA_SOURCE_BUCKET_NAME']

def get_trafct_data(origin, destination, key):
    request_url = "{url}/json?origins={origin}&destinations={destination}&departure_time=now&key={key}".format(
        url=BASE_URL,
        origin=origin, 
        destination=destination, 
        key=key)
    return requests.get(request_url)

origin = "Priv. Cereme, Urbi Villas del Prado 2, Tijuana"
destination = "SRT, Tijuana"

def handler(event, context):
    client = boto3.client('s3')
    response = get_trafct_data(quote_plus(origin), quote_plus(destination), GOOGLE_MAPS_API_KEY)
    json_obj = json.loads(response.content)
    yaml_str = yaml.dump(json_obj)
    today = datetime.datetime.now()
    key = '{year}/{month}/{day}/{hh_mm_ss}_traffic_data.yaml'.format(
        year=today.year,
        month=today.month,
        day=today.day,
        hh_mm_ss=today.strftime('%H_%M_%S')
    )
    client.put_object(Body=yaml_str, Bucket=TRAFFIC_DATA_SOURCE_BUCKET_NAME, Key=key)
    body = {
        "message": "executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }
    return response
