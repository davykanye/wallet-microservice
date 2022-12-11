import os
import requests
import json
from django.conf import settings


class Base:
    """Base Class used across defined.

    Args:
        key (str): .

    Methods:
    __init__(self, name: str):
            self.name = name

    """

    def __init__(self):
        self._PAYSTACK_AUTHORIZATION_KEY = settings.PAYSTACK_AUTHORIZATION_KEY
        self._CONTENT_TYPE = "application/json"
        self._BASE_END_POINT = "https://api.paystack.co"
        # not to self: raise-specific-error
        if not self._PAYSTACK_AUTHORIZATION_KEY:
            raise Exception(
                "Missing Authorization key argument or env variable")

    def _url(self, path):
        return f'{self._BASE_END_POINT}/{path}'

    def _headers(self):
        return {"Content-Type": self._CONTENT_TYPE,
                "Authorization": f"Bearer {self._PAYSTACK_AUTHORIZATION_KEY}", }

    def _parse_json(self, response_obj):
        """
        This function takes in every json response sent back by the
        server and trys to get out the important return variables
        Returns a python tuple of status code, status(bool), message, data
        """
        parsed_response = response_obj.json()

        status = parsed_response.get('status', None)
        message = parsed_response.get('message', None)
        data = parsed_response.get('data', None)
        return response_obj.status_code, status, message, data

    def _request(self, url, method, data=None):
        """
        Generic function to handle all API url calls
        Returns a python tuple of status code, status(bool), message, data
        """
        method_map = {
            'GET': requests.get,
            'POST': requests.post,
            'PUT': requests.put,
            'DELETE': requests.delete
        }

        url = self._url(url)

        payload = json.dumps(data) if data else data
        request = method_map.get(method)

        if not request:
            raise Exception("Request method not recognised or implemented")

        response = request(url, headers=self._headers(),
                           data=payload, verify=True)
        if response.status_code == 404:
            return response.status_code, False, "The object request cannot be found", None

        if response.status_code in [200, 201]:
            return self._parse_json(response)
        body = response.json()
        return response.status_code, body.get('status'), body.get('message'), body.get('errors')
