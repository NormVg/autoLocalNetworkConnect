from flask import Flask
from zeroconf import Zeroconf, ServiceInfo
import socket

app = Flask(__name__)

# Get the correct local network IP
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))  # Google's DNS to determine the active network interface
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

# Register Zeroconf service
def register_service():
    zeroconf = Zeroconf()
    server_ip = get_local_ip()  # Fetch correct local IP
    service_info = ServiceInfo(
        "_http._tcp.local.",  # Service type
        "FlaskServer._http._tcp.local.",  # Service name
        addresses=[socket.inet_aton(server_ip)],  # Convert IP to bytes
        port=5000,  # Flask server port
        properties={"info": "My Flask server!"},  # Optional metadata
    )
    zeroconf.register_service(service_info)
    print(f"Service registered: {server_ip}:5000")
    return zeroconf, service_info

@app.route("/")
def hello_world():
    return "Hello, Zeroconf with Flask!"

@app.route("/yes")
def yes():
    return " haa bhai jinda ha"

if __name__ == "__main__":
    zeroconf, service_info = register_service()
    try:
        app.run(host="0.0.0.0", port=5000)  # Bind to all network interfaces
    finally:
        zeroconf.unregister_service(service_info)
        zeroconf.close()
