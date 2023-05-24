import json
import logging
import os
from abc import ABCMeta, abstractmethod
import time
from json import JSONDecodeError

import boto3
from sqs_launcher import sqs_logger

QUEUE_URL = os.environ.get("QUEUE_URL")


class SqsListener(object):
    __metaclass__ = ABCMeta

    def __init__(self, queue, **kwargs):
        boto3_session = boto3.Session()

        self._queue_name = queue
        self._poll_interval = kwargs.get("interval", 5)
        self._queue_visibility_timeout = kwargs.get('visibility_timeout', '600')
        self._queue_url = QUEUE_URL
        self._message_attribute_names = kwargs.get('message_attribute_names', [])
        self._attribute_names = kwargs.get('attribute_names', [])
        self._wait_time = kwargs.get('wait_time', 20)
        self._max_number_of_messages = kwargs.get('max_number_of_messages', 1)

        # must come last
        if boto3_session:
            self._session = boto3_session
        else:
            self._session = boto3.session.Session()

        self._region_name = self._session.region_name
        self._client = boto3.client("sqs")

    def _start_listening(self):
        while True:
            messages = self._client.receive_message(
                QueueUrl=self._queue_url,
                MessageAttributeNames=self._message_attribute_names,
                AttributeNames=self._attribute_names,
                WaitTimeSeconds=self._wait_time,
                MaxNumberOfMessages=self._max_number_of_messages
            )

            if 'Messages' in messages:

                sqs_logger.debug(messages)
                sqs_logger.info("{} messages received".format(len(messages['Messages'])))
                for message in messages['Messages']:
                    receipt_handle = message['ReceiptHandle']
                    message_body = message['Body']
                    message_attributes = None
                    attributes = None

                    try:
                        message_dict = json.loads(message_body)
                    except JSONDecodeError:
                        self._client.delete_message(
                            QueueUrl=self._queue_url,
                            ReceiptHandle=receipt_handle
                        )
                        continue

                    self.handle_message(message_dict, message_attributes, attributes)
                    self._client.delete_message(
                        QueueUrl=self._queue_url,
                        ReceiptHandle=receipt_handle
                    )

            else:
                time.sleep(self._poll_interval)
                self._poll_interval += 60

    def listen(self):
        sqs_logger.info("Listening to queue " + self._queue_name)
        self._start_listening()

    @abstractmethod
    def handle_message(self, body, attributes, messages_attributes):
        """
        Implement this method to do something with the SQS message contents
        :param body: dict
        :param attributes: dict
        :param messages_attributes: dict
        :return:
        """
        return
