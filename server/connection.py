import thread
import SocketServer

client = clients = None


def init(client_factory, host, port):
    global client, clients
    client = client_factory
    clients = client_factory.client_registry
    server = SocketServer.TCPServer((host, port), ConnectionHandler)
    thread.start_new_thread(server.serve_forever, ())


class ConnectionHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        ip, data = self.client_address[0], self.request.recv(1024).strip()
        client_name = data[data.find(' ') + 1:]
        print 'Incoming connection from {0}: {1}'.format(ip, data)

        client.add(ip, client_name)

        # todo validate connection against config when there's one

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
