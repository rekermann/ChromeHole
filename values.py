import ntp
import socket
import json


class Values:
    """
    Helper Class to keep track of values
    """
    def __init__(self):
        with open("values.json") as f:
            data = json.load(f)

        self.targets = data.get("targets")
        self.ipForward = False
        self.spoof = False
        self.macs = []
        self.fakes = data.get("fakes")
        self.ntpServer = ntp.NTProxy
        self.ntpSocket = socket.socket
        self.ntpStatus = False
        self.sniff = False

