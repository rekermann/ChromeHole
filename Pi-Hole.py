#!/usr/bin/env python3
import funcs
import menu
import vals
import os


def main():
    funcs.setup()
    v = vals.vals()
    funcs.toggleIpforward(v)
    bash = ("ip addr add 51.145.123.29/0 dev dummy label dummy:0")
    os.system(bash)
    try:
        while True:
            menu.menu(v)
            pass
    except KeyboardInterrupt:
        funcs.interrupt(v)


if __name__ == '__main__':
    if "nt" in os.name:
        print(menu.bcolors.FAIL + "Can only run on a unix system" + menu.bcolors.ENDC)
        exit()
    elif os.getuid() != 0:
        print(menu.bcolors.FAIL + "Run this application as root" + menu.bcolors.ENDC)
        exit()
    main()

