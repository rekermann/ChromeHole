import menu
import funcs

def main():
    t = funcs.forward()
    menu.startup(t)
    menu.menu()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        menu.interrupt()


if __name__ == '__main__':
    main()
