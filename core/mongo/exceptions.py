from fastapi import HTTPException


class DocumentNotFound(HTTPException):
    """Can't find a document with the provided query"""

    def __init__(self, collection, value):
        self.collection = collection.name
        self.value = value
        self.status_code = 404
        self.detail = {
            "msg": self.__str__(),
        }

    def __str__(self):
        return "%s=%s doesn't exist" % (
            self.collection,
            self.value
        )
