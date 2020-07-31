import time
import funcs


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def menuBanner(v):
    funcs.cls()

    print(f"""
    {bcolors.OKGREEN}
          _/_/_/  _/_/_/        _/    _/            _/           
           _/    _/    _/      _/    _/    _/_/    _/    _/_/    
          _/    _/_/_/        _/_/_/_/  _/    _/  _/  _/_/_/_/   
         _/    _/            _/    _/  _/    _/  _/  _/          
      _/_/_/  _/            _/    _/    _/_/    _/    _/_/_/
    {bcolors.BOLD}
      |IP Forward = {v.ipForward}|  |Targets = {v.targets}|
      |Spoofing = {v.spoof}|  |Fake Ips = {v.fakes}|
      |NTP server = {v.ntpStatus}| |Sniff = {v.sniff}|
      --------------------------------------------------------
    {bcolors.ENDC}
    """)

    return


def mainMenu(v):
    menuBanner(v)
    print("      --------------------------------------------------------")
    print("      |1 - Edit Targets          |2 - Edit Fake Ips          |")
    print("      |3 - Toggle Spoof          |4 - Toggle Sniff           |")
    print("      |5 - Toggle NTP Server     |6 - Toggle IP Forward      |")
    print("      --------------------------------------------------------")
    try:
        i = int(input("      Enter Choice: "))
    except ValueError:
        print("      " + bcolors.WARNING + "Only input integers" + bcolors.ENDC)
        time.sleep(1)
        return

    if 0 < i <= 8:
        menuSwitch(v, i)


def menuSwitch(v, i):
    if i == 1:
        menuBanner(v)
        print("      --------------------------------------------------------")
        print("      |1 - Add targets           |2 - Delete Target          |")
        print("      --------------------------------------------------------")
        try:
            i = int(input("      Enter Choice: "))
        except ValueError:
            print("      " + bcolors.WARNING + "Only input integers" + bcolors.ENDC)
            time.sleep(1)
        except KeyboardInterrupt:
            return

            return
        if i == 1:
            funcs.addTargets(v)
        elif i == 2:
            funcs.removeTargets(v)
        else:
            print("      " + bcolors.WARNING + str(i) + " is not a selection" + bcolors.ENDC)
            time.sleep(1)
            return

        return
    if i == 2:
        menuBanner(v)
        print("      --------------------------------------------------------")
        print("      |1 - Add Fake IP          |2 - Delete Fake IP          |")
        print("      --------------------------------------------------------")
        try:
            i = int(input("      Enter Choice: "))
        except ValueError:
            print("      " + bcolors.WARNING + "Only input integers" + bcolors.ENDC)
            time.sleep(1)
        except KeyboardInterrupt:
            return

        if i == 1:
            funcs.addFakes(v)
        elif i == 2:
            funcs.removeFake(v)
        else:
            print("      " + bcolors.WARNING + str(i) + " is not a selection" + bcolors.ENDC)
            time.sleep(1)
            return

        return
    if i == 3:
        if v.spoof:
            funcs.restoreSpoof(v)
        else:
            funcs.startSpoof(v)
        return
    if i == 4:
        funcs.toggleSniff(v)
        return
    if i == 5:
        funcs.ntpToggle(v)
        return

    if i == 6:
        funcs.toggleIpforward(v)
        return

    if i == 7:
        return

    if i == 8:
        return

    return
