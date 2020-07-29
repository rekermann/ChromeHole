from scapy.all import *


def sniffer(target):
    sniff(filter="host " + target, prn=change_send)


def change_send(pkt):
    sendp(pkt)
    return
