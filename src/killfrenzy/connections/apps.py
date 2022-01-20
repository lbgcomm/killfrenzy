from django.apps import AppConfig
from threading import Thread
from django import db
import asyncio
import os
import web_socket

class ConnectionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'connections'

    def ready(self):
        env = os.environ.get("WEBSERVER_SET")

        if env is None:
            web_socket.socket_c.start()

            os.environ["WEBSERVER_SET"] = 'True'