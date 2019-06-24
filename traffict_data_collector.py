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
ORIGIN_DESTINATION_TABLE_NAME = os.environ['ORIGIN_DESTINATION_TABLE_NAME']


def get_trafct_data(origin, destination, key):
    """
    The function that makes the request to google api
        origin: a string in url format indicating the starting point 
        destination: a string in url format indicating the end point
        key: the google api key
    """
    request_url = "{url}/json?origins={origin}&destinations={destination}&departure_time=now&key={key}".format(
        url=BASE_URL,
        origin=origin, 
        destination=destination, 
        key=key)
    return requests.get(request_url)

def handler(event, context):
    """
    This function is the entry point of the lambda.
    It reads the items from a table and based in the origin and destination 
    gets the traffic data and saves it in a s3 bucket.
    """
    s3 = boto3.client('s3')
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(ORIGIN_DESTINATION_TABLE_NAME)

    scan = table.scan()
    for item in scan['Items']:
        id = item['uuid']
        origin = item['origin']
        destination = item['destination']
        response = get_trafct_data(quote_plus(origin), quote_plus(destination), GOOGLE_MAPS_API_KEY)
        json_obj = json.loads(response.content)
        yaml_str = yaml.dump(json_obj)
        today = datetime.datetime.now()
        key = '{id}/{date}_traffic_data.yaml'.format(
            id=id,
            date=today.strftime("%Y_%m_%d_%H_%M")
        )
        s3.put_object(Body=yaml_str, Bucket=TRAFFIC_DATA_SOURCE_BUCKET_NAME, Key=key)


    body = {
        "message": "executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }
    return response
