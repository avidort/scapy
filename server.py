import SocketServer
import thread
import time

queue = ''


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


if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    server = SocketServer.TCPServer((HOST, PORT), ConnectionHandler)
    thread.start_new_thread(server.serve_forever, ())

    while True:
        queue = raw_input()
        print queue
