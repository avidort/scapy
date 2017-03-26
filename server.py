import SocketServer
import thread
queue = ''


class CommandHandler:
    def test(self, args):
        print("actual test")
        print args


class ConnectionHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        global queue

        self.data = self.request.recv(1024).strip()
        print "incoming connection from {}".format(self.client_address[0])

        # todo flow: validate -> reject and close connection if bad -> listen for orders

        while True:
            if queue:
                self.request.sendall(queue)
                if queue == 'close':
                    break
                queue = ''


def main():
    global queue
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
