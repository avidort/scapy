import thread
import SocketServer
import client_factory as client
clients = client.client_registry


# noinspection PyClassHasNoInit
class CommandHandler:
    @staticmethod
    def test(args, raw):
        print("actual test")
        print args
        print raw

    @staticmethod
    def msg(args, raw):
        print "sending: " + raw
        client.message_all(raw)


class ConnectionHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        ip, data = self.client_address[0], self.request.recv(1024).strip()
        print 'Incoming connection from {0}: {1}'.format(ip, data)

        client.add(ip, 'my client')

        # todo flow: validate -> reject and close connection if bad -> listen for orders

        connection = 'active'
        while connection == 'active':
            for message in clients[ip].get_messages():
                if message:
                    try:
                        self.request.sendall(message)
                        clients[ip].pop_message(message)
                        if message == 'close':
                            connection = 'closed'
                    except SocketServer.socket.error:
                        connection = 'timeout'

        client.remove(ip)
        print 'Connection closed from {0} ({1})'.format(ip, connection)


def main():
    HOST, PORT = "localhost", 9999  # todo read config
    server = SocketServer.TCPServer((HOST, PORT), ConnectionHandler)
    server.timeout = 5
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
            print 'Unknown command: {0}'.format(cmd)

if __name__ == '__main__':
    main()
