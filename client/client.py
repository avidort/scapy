import json
import socket


# noinspection PyClassHasNoInit
class CommandHandler:
    @staticmethod
    def test(args, raw):
        print("[debug] actual test @ client")
        print args
        print raw


def command_processor(cmd):
    try:
        data = json.loads(cmd)
        cmd, args, raw = data['command'], data['args'], data['raw']
        getattr(CommandHandler, cmd)(args, raw)

    except:
        return


def maintain_connection(name):
    HOST, PORT = "localhost", 9999  # todo read config
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    sock.sendall("connect {0}\n".format(name))

    while True:
        received = sock.recv(1024)
        if received:
            print "received: " + received
            command_processor(received)

            if received == 'close':
                sock.close()
                break

    sock.close()


def main():
    # todo validate name, config, etc
    maintain_connection('avidor')

if __name__ == '__main__':
    main()
