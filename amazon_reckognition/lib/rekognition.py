import boto3


class Rekognition(object):

    def __init__(self):
        pass

    def connect_to_rekognition(self, region, aws_acces_id, aws_secret_key):

        client = boto3.client("rekognition",
                              region_name=region,
                              aws_access_key_id=aws_acces_id,
                              aws_secret_access_key=aws_secret_key
                              )
        return client

    def parse_images_and_detect_labels(self,rekognition_client,
                                       bucket_name,
                                       image_list,
                                       max_labels=10,
                                       min_confidence=60
                                       ):

        s3_bucket = bucket_name

        attr_list = []
        for image_name in image_list:
            json_dictionary = {}
            response = rekognition_client.detect_labels(
                Image={
                    'S3Object': {
                        'Bucket': s3_bucket,
                        'Name': image_name,
                    },
                },
                MaxLabels=max_labels,
                MinConfidence=min_confidence,
            )
            json_dictionary[image_name] = response
            attr_list.append(json_dictionary)
        return attr_list