import time
from threading import Thread

from app.api.v1.serializers.country import CountryConfSchema
from app.api.v1.views.countries import create_country_configuration
from integrations.aws_queue.base_sqs_listener import SqsListener


class SqsEventListener(SqsListener):
    def handle_message(self, body, attributes, messages_attributes):
        """
         The following is a dummy example to clarify how to handle
         the retried data from sqs
        """
        data = {
            "alpha_2": "RO",
            "alpha_3": "REE",
            "name": "str",
            "description_ar": "str",
            "description_en": "str",
            "is_banned": True,
            "is_active": True,
            "phone_code": "str",
            "note": "str",
        }

        create_country_configuration(request=CountryConfSchema(**data))


class EventListenerThread(Thread):
    def run(self, *args, **kwargs):
        listener = SqsEventListener('poc_development')
        listener.listen()
        time.sleep(5)


async def sqs_event_listener():
    event = EventListenerThread()
    event.start()
