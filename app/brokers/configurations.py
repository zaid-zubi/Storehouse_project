from fastapi import HTTPException, status
import requests


def get_countries():
    url = "http://127.0.0.1:8001/countries/"
    response = requests.get(url)
    return response.json()


class CountryBroker:
    def __init__(self):
        self.host = "http://127.0.0.1:8001/countries/"

    # GET: // Countries
    def get_countries(self):
        response = requests.get(self.host)
        print(response.json())
        if response.status_code >= 200 and response.status_code <= 300:
            return response.json()
        else:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Service not available",
            )

    # GET: // Country
    def get_country_by_id(self, id: int):
        self.host = self.host + f"{id}/"
        response = requests.get(self.host)
        print(response.json())
        if response.status_code >= 200 and response.status_code <= 300:
            return response.json()
        else:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Service not available",
            )
