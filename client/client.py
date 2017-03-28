import socket
# import sys

HOST, PORT = "localhost", 9999
# data = " ".join(sys.argv[1:])

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to server and send data
sock.connect((HOST, PORT))
sock.sendall("connect\n")

while True:
    # Receive data from the server and shut down
    received = sock.recv(1024)
    if received:
        print received

        if received == 'close':
            sock.close()
            break

sock.close()

# print "Sent:     {}".format(data)