from django.apps import AppConfig
from multiprocessing import Process
from threading import Thread
from django import db
import asyncio
import os

class WebServer(Thread):
    def __init__(self):
        super().__init__()
        self.daemon = True

    def run(self):
        db.connections.close_all()

        import web_socket

        asyncio.run(web_socket.start_server())

class ConnectionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'connections'

    def ready(self):
        env = os.environ.get("WEBSERVER_SET")

        if env is None:
            web = WebServer()
            web.start()

            os.environ["WEBSERVER_SET"] = 'True'