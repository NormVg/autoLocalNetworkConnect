from zeroconf import Zeroconf, ServiceBrowser
import socket
import requests

class FlaskServiceListener:
    def __init__(self):
        self.flask_service = None

    def add_service(self, zeroconf, service_type, name):
        info = zeroconf.get_service_info(service_type, name)
        if info:
            self.flask_service = info
            server_ip = socket.inet_ntoa(info.addresses[0])
            server_port = info.port
            print(f"Discovered Flask server at {server_ip}:{server_port}")
            resp = requests.get(f"http://{server_ip}:{server_port}/yes")
            print(resp.text)
            print(f"Metadata: {info.properties}")

    def remove_service(self, zeroconf, service_type, name):
        print(f"Service removed: {name}")

zeroconf = Zeroconf()
listener = FlaskServiceListener()
browser = ServiceBrowser(zeroconf, "_http._tcp.local.", listener)

try:
    
    input("Press Enter to stop discovery...\n")
finally:
    zeroconf.close()
