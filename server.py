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
    def test(self, args, raw):
        print("actual test")
        print args
        print raw

    def msg(self, args, raw):
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
