import boto3


class S3(object):
    def __init__(self):
        pass

    def connect_to_s3(self, aws_acces_id, aws_secret_key):
        s3 = boto3.resource('s3', aws_access_key_id=aws_acces_id, aws_secret_access_key=aws_secret_key)
        return s3

    def get_bucket(self, s3_client, bucket_name):
        return s3_client.Bucket(name=bucket_name)

    def get_images_from_bucket(self, bucket_object):
        image_list = []
        for obj in bucket_object.objects.all():
            image_list.append(obj.key)
        return image_list
