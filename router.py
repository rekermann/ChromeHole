""" from scapy.sendrecv import sendp import uuid
WIP cLhgKpZ5 https://socifi-doc.atlassian.net/wiki/spaces/SC/pages/94371841/DNS+Fix+to+keep+Android+Splash+Page+and+the+Captive+Portal+Notification+active

def build_arp_response(target1, target2):

    ether_index = 0
    arp_index = 1

    mac =':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff)
        for ele in range(0,8*6,8)][::-1])

    arp = Ether() / ARP()
    arp[ether_index].src = mac
    arp[arp_index].hwsrc = mac
    arp[arp_index].psrc = target1
    arp[arp_index].hwdst = get_mac(target2)
    arp[arp_index].pdst = target2

    return arp

"""

"""arppkt = spoofer.build_arp_response(target1, target2)

while True:
    sendp(arppkt, verbose=False)
    time.sleep(0.1)"""