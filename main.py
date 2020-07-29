import funcs
import menu
import vals
import os


def main():
    funcs.setup()
    v = vals.vals()
    try:
        while True:
            menu.menu(v)
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

