import socket
import json
import numpy as np

class UDPSender:
    def __init__(self, ip='127.0.0.1', port=9999):
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_sample(self, ip_val: np.ndarray, is_val: np.ndarray):
        payload = {
            'ip': ip_val.tolist(),
            'is': is_val.tolist()
        }
        self.sock.sendto(json.dumps(payload).encode('utf-8'), (self.ip, self.port))

    def send_stop(self):
        payload = {'stop': True}
        self.sock.sendto(json.dumps(payload).encode('utf-8'), (self.ip, self.port))
