from scapy.all import *


def sniffer(target):
    sniff(filter="host " + target, prn=change_send)


def change_send(pkt):
    txt = io.StringIO()
    sys.stdout = txt
    sendp(pkt)
    sys.stdout = sys.__stdout__
    return
