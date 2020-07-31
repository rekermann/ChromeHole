import ntp
import socket

class vals:
    """
    Helper Class to keep track of values
    """
    def __init__(self):
        self.targets = ['192.168.1.1', '192.168.1.214']
        self.ipForward = False
        self.spoof = False
        self.macs = ['4c:ed:fb:d5:d3:34', '34:02:86:62:ef:8a']
        self.fakes = ['51.145.123.29']
        self.ntpServer = ntp.NTProxy
        self.ntpSocket = socket.socket
        self.ntpStatus = False

