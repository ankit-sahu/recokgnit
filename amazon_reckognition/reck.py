try:
    import boto3
except ImportError as e:
    print("Did not find boto3 module, installing it")
    import subprocess
    subprocess.call(["pip3", "install", "boto3"])
    import boto3
    print("Installation complete.")

from config.config import Config
from lib.dynamodb import DynamoDB
from lib.s3 import S3
from lib.rekognition import Rekognition
from utils.utils import Utils


if __name__ == '__main__':

    s3 = S3()
    s3_client = s3.connect_to_s3(aws_acces_id=Config.ACCESS_ID, aws_secret_key=Config.ACCESS_KEY)
    bucket_obj = s3.get_bucket(s3_client, Config.bucket_name)
    list_of_images = s3.get_images_from_bucket(bucket_obj)

    rekog = Rekognition()
    rekog_client = rekog.connect_to_rekognition(
        region=Config.REGION,
        aws_acces_id=Config.ACCESS_ID,
        aws_secret_key=Config.ACCESS_KEY
    )
    response = rekog.parse_images_and_detect_labels(rekog_client, Config.bucket_name, list_of_images)
    print(response)

    dynamo = DynamoDB()
    ddb_client = dynamo.connect_to_dynamo(
        region=Config.REGION,
        aws_acces_id=Config.ACCESS_ID,
        aws_secret_key=Config.ACCESS_KEY)

    for item in response:
        image_name, labels, response_metadata = Utils.json_processor(item)
        unique_id_for_image_data_table = Utils.unique_id()
        url = Utils.url_generator(image_name)
        image_data_resp = dynamo.insert_data_in_image_data_table(ddb_client, image_name=image_name,
                                                                 unique_id=unique_id_for_image_data_table,
                                                                 url=url)

        label_with_rounded_confidence = Utils.get_rounded_confidence(labels)
        label_resp = dynamo.insert_data_in_label_table(ddb_client,
                                                       image_id=unique_id_for_image_data_table,
                                                       label=label_with_rounded_confidence)

    # table = ddb_client.Table(Config.table_name)
    # dynamo.scan_table(table)
    # dynamo.get_item(table,{"ID": "d772c4d0-5af7-11e7-a362-4c32759ec6fb"})


