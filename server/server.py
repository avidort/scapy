import thread
import SocketServer
import cmd_proc
import client_factory as client
clients = client.client_registry


# noinspection PyClassHasNoInit
class CommandHandler:
    @staticmethod
    def test(args, raw):
        print("[debug] actual test")
        print args
        print raw

    @staticmethod
    def msg(args, raw):
        print "[debug] sending: " + raw
        client.message_all(raw)


class ConnectionHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        ip, data = self.client_address[0], self.request.recv(1024).strip()
        client_name = data[data.find(' ') + 1:]
        print 'Incoming connection from {0}: {1}'.format(ip, data)

        client.add(ip, client_name)

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
    thread.start_new_thread(server.serve_forever, ())
    cmd_proc.command_processor(CommandHandler)

if __name__ == '__main__':
    main()
