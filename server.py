import SocketServer
import thread

queue = ''
clients = []


def add_client(name, ipaddr):
    clients.append({'name': name, 'ipaddr': ipaddr, 'queue': []})
    return len(clients) - 1


def msg_all_clients(message):
    for client in clients:
        client['queue'].append(message)


class CommandHandler():
    def test(self, args):
        print("actual test")
        print args

    def msg(self, args):
        print "sending: " + args[0]
        msg_all_clients(args[0])


class ConnectionHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        global queue, clients

        self.data = self.request.recv(1024).strip()
        print "incoming connection from {}".format(self.client_address[0])

        client = add_client('my client', self.client_address[0])

        # todo flow: validate -> reject and close connection if bad -> listen for orders

        while True:
            for task in clients[client]['queue']:
                if task:
                    print task
                    self.request.sendall(task)
                    if task == 'close':
                        break
                    clients[client]['queue'].remove(task)


def main():
    HOST, PORT = "localhost", 9999  # todo read config
    server = SocketServer.TCPServer((HOST, PORT), ConnectionHandler)
    thread.start_new_thread(server.serve_forever, ())
    while True:
        cmd = raw_input()
        args = cmd.split(' ')
        if len(args) > 1:
            cmd = args[0]
            del args[0]
        else:
            args = []

        try:
            eval('CommandHandler().{0}({1})'.format(cmd, args))
        except AttributeError:
            print "Unknown command: {0}".format(cmd)

if __name__ == "__main__":
    main()
