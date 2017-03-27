import SocketServer
import thread

import client_model as cm

clients = {}


class ClientManager():
    def add_client(self, name, ipaddr):
        clients[ipaddr] = cm.ClientModel(name, ipaddr)

    def msg_all_clients(self, message):
        for client in clients:
            clients[client].push_message(message)


class CommandHandler():
    def test(self, args, raw):
        print("actual test")
        print args
        print raw

    def msg(self, args, raw):
        print "sending: " + args[0]
        ClientManager().msg_all_clients(args[0])


class ConnectionHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        global clients

        self.data = self.request.recv(1024).strip()
        ip = self.client_address[0]
        print "Incoming connection from {}".format(ip)

        ClientManager().add_client('my client', ip)

        # todo flow: validate -> reject and close connection if bad -> listen for orders

        while True:
            for message in clients[ip].get_messages():
                if message:
                    clients[ip].pop_message(message)
                    print message
                    self.request.sendall(message)
                    if message == 'close':
                        break


def main():
    HOST, PORT = "localhost", 9999  # todo read config
    server = SocketServer.TCPServer((HOST, PORT), ConnectionHandler)
    thread.start_new_thread(server.serve_forever, ())
    while True:
        cmd = raw_input()

        if not cmd:
            continue

        if cmd[0] == ' ':
            cmd = cmd[1:]

        if cmd.count(' '):
            raw = cmd[cmd.find(' ') + 1:]
            args = raw.split(' ')
            cmd = cmd[:cmd.find(' ')]
        else:
            raw = args = None

        try:
            getattr(CommandHandler(), cmd)(args, raw)
            # eval('CommandHandler().{0}({1}, "{2}")'.format(cmd, args, raw))
        except AttributeError:
            print "Unknown command: {0}".format(cmd)

if __name__ == "__main__":
    main()
