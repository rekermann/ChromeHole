import ntp
import socket

class vals:
    """
    Helper Class to keep track of values
    """
    def __init__(self):
        self.targets = []
        self.ipForward = False
        self.spoof = False
        self.macs = []
        self.fakes = []
        self.ntpServer = ntp.NTProxy
        self.ntpSocket = socket.socket
        self.ntpStatus = False

