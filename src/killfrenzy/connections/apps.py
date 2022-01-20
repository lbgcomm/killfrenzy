from django.apps import AppConfig
import os

import web_socket

class ConnectionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'connections'

    def ready(self):
        env = os.environ.get("WEBSERVER_SET")

        if env is not None:
            print("RUNNING FROM READY")
            web_socket.socket_c.start()
        else:
            os.environ["WEBSERVER_SET"] = 'True'