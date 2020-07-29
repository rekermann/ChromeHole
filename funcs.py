import sys
import socket
import os

class forward:
    def __init__(self):
        self.ip_forward = False

    def toggleIpforward(self):
        file_path = "/proc/sys/net/ipv4/ip_forward"
        print(self.ip_forward)
        with open(file_path, "w") as f:
            if self.ip_forward:
                print(0, file=f)
                self.ip_forward = False
            else:
                print(1, file=f)
                self.ip_forward = True
        return


def validIPAddress(ip):
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False


def cls():
    os.system("clear")
    return

def getIp(name):
    tmp = []
    ips = socket.getaddrinfo(socket.gethostbyname(name), None)
    for x in ips:
        tmp.append(x[4][0])

    return tmp


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
            if i <= len(tmp):
                if validIPAddress(sys.argv[i]):
                    target = sys.argv[i]
                else:
                    print(sys.argv[i] + " is not an valid ip address")
                    print("")
                    exit()
            else:
                print("Missing value for -t")
                exit()
        elif x == "-f":
            p = i
            f = False
            while (p != len(tmp)) and tmp[p] != "-g" and (tmp[p] != "-t"):
                if validIPAddress(sys.argv[p]):
                    fake.append(sys.argv[p])
                else:
                    print(sys.argv[p] + " is not an valid ip address")
                    print("")
                p = p + 1
            if p <= len(tmp):
                if validIPAddress(sys.argv[p]):
                    fake.append(sys.argv[p])
                else:
                    print(sys.argv[p] + " is not an valid ip address")
                    print("")
            else:
                print(sys.argv[p] + " is not an valid ip address")
                print("")
        elif x == "-g":
            if i <= len(tmp):
                if validIPAddress(sys.argv[i]):
                    gw = sys.argv[i]
                else:
                    print(sys.argv[i] + " is not an valid ip address")
                    print("")
            else:
                print("Missing value for -g")
                print("")

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


