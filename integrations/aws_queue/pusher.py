import os

from integrations.aws_queue.aws_sns import publish_message_to_sns
import json


class Pusher:
    TOPIC_ARN = os.environ.get("SNS_TOPIC_ARN")

    @classmethod
    def push_to_sns(cls, data):
        return publish_message_to_sns(data, cls.TOPIC_ARN)

    @classmethod
    def push_country_configurations_to_sns(cls, data):
        # data["details"] = "country_configurations"
        message_id = cls.push_to_sns(data)

        response = {
            "message_id": message_id,
            "info": "The message pushed to sns successfully" if message_id else "failed to push the message"
        }
        return response
