import json
import socket


def interpret_command(cmd):
    try:
        data = json.loads(cmd)
        cmd, args = data['command'], data['args']

        # todo move command handling outside

    except ValueError:
        return


def maintain_connection(name):
    HOST, PORT = "localhost", 9999  # todo read config
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    sock.sendall("connect {0}\n".format(name))

    while True:
        received = sock.recv(1024)
        if received:
            print received
            interpret_command(received)

            if received == 'close':
                sock.close()
                break

    sock.close()


def main():
    # todo validate name, config, etc
    maintain_connection('test')

if __name__ == '__main__':
    main()
