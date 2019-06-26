import os
import datetime
import requests
import json
import yaml
import boto3
from urllib.parse import quote_plus

def get_trafct_data(origin, destination, key):
    """
    The function that makes the request to google api
        origin: a string in url format indicating the starting point 
        destination: a string in url format indicating the end point
        key: the google api key
    """
    url = 'https://maps.googleapis.com/maps/api/distancematrix'
    request_url = "{url}/json?origins={origin}&destinations={destination}&departure_time=now&key={key}".format(
        url=url,
        origin=quote_plus(origin), 
        destination=quote_plus(destination), 
        key=key)
    return requests.get(request_url)

def get_table_items(table_name):
    """
    Read all the items from a dynamodb.
        table_name: the name of the table
    """
    dynamodb = boto3.resource('dynamodb', 'us-east-1')
    table = dynamodb.Table(table_name)
    table_scan = table.scan()
    return table_scan['Items']

def save_data_to_s3(bucket_name, key, data_str):
    """
    Creates a new item in a s3 bucket base in a text string.
        bucket_name: the name of the bucket
        key: the path to save the file
        data_str: the string to save
    """
    s3 = boto3.client('s3')
    s3.put_object(Body=data_str, Bucket=bucket_name, Key=key)

def handler(event, context):
    """
    This function is the entry point of the lambda.
    It reads the items from a table and based in the origin and destination 
    gets the traffic data and saves it in a s3 bucket.
    """
    GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY', '')
    TRAFFIC_DATA_SOURCE_BUCKET_NAME = os.environ.get('TRAFFIC_DATA_SOURCE_BUCKET_NAME', '')
    ORIGIN_DESTINATION_TABLE_NAME = os.environ.get('ORIGIN_DESTINATION_TABLE_NAME', '')

    items = get_table_items(ORIGIN_DESTINATION_TABLE_NAME)
    for item in items:
        id = data['uuid']
        origin = item['origin']
        destination = item['destination']
        response = get_trafct_data(origin, destination, GOOGLE_MAPS_API_KEY)
        json_obj = json.loads(response.content)
        yaml_str = yaml.dump(json_obj)
        today = datetime.datetime.now()
        key = '{id}/{date}_traffic_data.yaml'.format(
            id=id,
            date=today.strftime("%Y_%m_%d_%H_%M")
        )
        save_data_to_s3(TRAFFIC_DATA_SOURCE_BUCKET_NAME, key, yaml_str)

    body = {
        "message": "executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }
    return response
