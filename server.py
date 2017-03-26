import SocketServer
import thread
import sys


queue = ''

clients = []


def add_client(conn, name):
    clients.append({'conn': conn, 'name': name, 'queue': []})


def msg_all_clients(message):
    for client in clients:
        print client.queue.append(message)
        globals()[client['conn']].request.sendall(message)


class CommandHandler():
    def test(self, args):
        print("actual test")
        print args

    def msg(self, args):
        print "sending: " + args
        msg_all_clients(args)


class ConnectionHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        global queue, clients

        self.data = self.request.recv(1024).strip()
        print "incoming connection from {}".format(self.client_address[0])

        add_client(self, self.client_address[0])
        print clients



        # todo flow: validate -> reject and close connection if bad -> listen for orders

        # while True:
        #     if queue:
        #         self.request.sendall(queue)
        #         if queue == 'close':
        #             break
        #         queue = ''


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
            eval('CommandHandler().{0}("{1}")'.format(cmd, args))
        except AttributeError:
            print "Unknown command: {0}".format(cmd)

if __name__ == "__main__":
    main()
