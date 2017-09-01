import boto3
import uuid

from config.config import Config
from utils.utils import Utils

class DynamoDB(object):

    count = 0;

    def __init__(self):
        pass

    def connect_to_dynamo(self, region, aws_acces_id, aws_secret_key):

        client = boto3.resource("dynamodb",
                                region_name=region,
                                aws_access_key_id=aws_acces_id,
                                aws_secret_access_key=aws_secret_key)
        return client

    def insert_data_in_image_data_table(self, dynamo_client, **kwargs):

        table = dynamo_client.Table(Config.image_table)

        response = table.put_item(
            Item={
                'ID': kwargs["unique_id"],
                'image_name': kwargs["image_name"],
                'image_url': kwargs["url"]}
            )
        return True

    def insert_data_in_label_table(self, dynamo_client, **kwargs):

        table = dynamo_client.Table(Config.label_table)

        for item in kwargs["label"]:
            self.count = self.count + 1
            unique_id = Utils.unique_id()
            response = table.put_item(
                Item={
                    'id': unique_id,
                    'image_id': kwargs["image_id"],
                    'name': item["Name"],
                    'confidence': item["Confidence"]}
                )
        return True

    def scan_table(self, table):
        print(table.scan(Config.table_name))

    def get_item(self, table, param):
        print(table.get_item(Key=param))