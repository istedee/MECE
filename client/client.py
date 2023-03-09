import consumer
import client_ui


def main():
    client_ui.main()

if '__main__' == __name__:
    try:
        main()
    except KeyboardInterrupt as e:
        pass
    except:
        raise
