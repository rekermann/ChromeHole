import time
import funcs
import ntp


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def menu(v):
    funcs.cls()

    print(f"""
    {bcolors.OKGREEN}
          _/_/_/  _/_/_/        _/    _/            _/           
           _/    _/    _/      _/    _/    _/_/    _/    _/_/    
          _/    _/_/_/        _/_/_/_/  _/    _/  _/  _/_/_/_/   
         _/    _/            _/    _/  _/    _/  _/  _/          
      _/_/_/  _/            _/    _/    _/_/    _/    _/_/_/
    
      |IP Forward = {v.ipForward}|  |Targets = {v.targets}|
      |Spoofing = {v.spoof}|  |Fake Ips = {v.fakes}|
      |NTP server = {v.ntpStatus}|
      --------------------------------------------------------
    {bcolors.ENDC}
    """)
    print("      --------------------------------------------------------")
    print("      |1 - Add targets           |2 - Delete Target          |")
    print("      |3 - Add Fake IP           |4 - Remove Fake IP         |")
    print("      |5 - Toggle Spoof          |6 - WIP STRIP              |")
    print("      |7 - Toggle NTP Server     |8 - Toggle IP Forward      |")
    print("      --------------------------------------------------------")
    try:
        i = int(input("      Enter Choice: "))
    except ValueError:
        print("      " + bcolors.WARNING + "Only input integers" + bcolors.ENDC)
        time.sleep(1)
        return

    if 0 < i <= 8:
        menuSwitch(v, i)

    return


def menuSwitch(v, i):
    if i == 1:
        funcs.addTarget(v)
        return
    if i == 2:
        funcs.removeTargets(v)
        return
    if i == 3:
        funcs.addFake(v)
        return
    if i == 4:
        funcs.removeFake(v)
        return
    if i == 5:
        if v.spoof:
            funcs.restore(v)
        else:
            funcs.startSpoof(v)
        return

    if i == 6:
        # WIP
        return

    if i == 7:
        funcs.ntpToggle(v)
        return

    if i == 8:
        funcs.toggleIpforward(v)
        return

    return
