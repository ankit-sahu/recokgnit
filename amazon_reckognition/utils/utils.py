from lib.rekognition import Rekognition
from config.config import Config

import uuid


class Utils(object):

    def __init__(self):
        pass

    @classmethod
    def json_processor(cls, json_data):

        image_name = list(json_data)[0]
        labels = list(json_data.values())[0]["Labels"]
        response_metadata = list(json_data.values())[0]["ResponseMetadata"]
        return image_name, labels, response_metadata

    # we need to round the confidence values coz amazon dynamo DB throws the error as:
    # TypeError: Float types are not supported. Use Decimal types instead.
    # Two sol : convert the float to a string and pass it to a Decimal() method or round up the confidence.

    @classmethod
    def get_rounded_confidence(cls, labels):

        label_with_rounded_confidence = []
        for label in labels:
            new_label = {}
            new_label["Name"] = label["Name"]
            new_label["Confidence"] = round(label["Confidence"])
            label_with_rounded_confidence.append(new_label)
        return label_with_rounded_confidence

    @classmethod
    def unique_id(cls):
        return str(uuid.uuid1())

    @classmethod
    def url_generator(cls, image_name):
        url = '{}/{}/{}'.format(Config.host_name, Config.bucket_name, image_name)
        return url



