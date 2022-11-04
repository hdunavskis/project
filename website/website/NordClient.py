import os
import threading
from dotenv import load_dotenv
from nordigen import NordigenClient
from requests.models import HTTPError
from django.http import Http404

load_dotenv()
class ClientSingleton:
    __instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if not cls.__instance:
                cls.__instance = super().__new__(cls)
                cls.client = cls._get_client()
        return cls.__instance


    @staticmethod
    def _get_client():
        client = NordigenClient(
            secret_id=os.getenv('SECRET_ID'),
            secret_key=os.getenv('SECRET_KEY')
        )
        try:
            client.generate_token()
        except HTTPError as http_response:
            #log error here
            raise Http404('Login failed! Check credentials!') from http_response
        return client
