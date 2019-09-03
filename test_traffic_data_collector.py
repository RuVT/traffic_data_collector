import os
import yaml
import boto3
from moto import mock_dynamodb2, mock_s3
import unittest
from traffic_data_collector import get_table_items, \
    save_data_to_s3, \
    get_trafct_data


class TestTrafficDataCollector(unittest.TestCase):
    TABLE_NAME = 'my_table'
    BUCKET_NAME = 'my_bucket'
    BUCKET_KEY = 'test/file.yaml'
    DATA = 'some data'

    # def setUp(self):
    #     pass
    #
    # @mock_dynamodb2
    # def test_get_table_items(self):
    #     """
    #     Unit test for the get_table_items function using moto
    #     lib for mocking.
    #     """
    #     dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    #     table = dynamodb.create_table(
    #         TableName=self.TABLE_NAME,
    #         KeySchema=[{
    #             'AttributeName': 'uuid',
    #             'KeyType': 'HASH'
    #         }],
    #         AttributeDefinitions=[{
    #             'AttributeName': 'uuid',
    #             'AttributeType': 'S'
    #         }],
    #         ProvisionedThroughput={
    #             'ReadCapacityUnits': 1,
    #             'WriteCapacityUnits': 1
    #         })
    #     table.put_item(Item={
    #         'uuid': 'one',
    #         'origin': 'NY',
    #         'destination': 'LA'
    #     })
    #     items = get_table_items(self.TABLE_NAME)
    #     self.assertIsNotNone(items)
    #     self.assertTrue(type(items) == list)
    #
    # @mock_s3
    # def test_save_data_to_s3(self):
    #     """
    #     Unit testing for the save_data_s3 using the moto
    #     lib for mocking.
    #     """
    #     s3 = boto3.resource('s3', region_name='us-east-1')
    #     s3.create_bucket(Bucket=self.BUCKET_NAME)
    #     save_data_to_s3(self.BUCKET_NAME, self.BUCKET_KEY, self.DATA)
    #     obj = s3.Object(self.BUCKET_NAME, self.BUCKET_KEY)
    #     data_str = obj.get()['Body'].read().decode('utf-8')
    #     self.assertEqual(data_str, self.DATA)
    def test_get_trafct_data(self):
        """
        Integration testing using the real google maps api
        """
        GOOGLE_MAPS_API_KEY = os.environ['GOOGLE_MAPS_API_KEY']
        response = get_trafct_data('Tijuana, BC', 'Ensenada, BC', GOOGLE_MAPS_API_KEY)
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

