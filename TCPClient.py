import asyncore
import socket
import time

class TCPClient(asyncore.dispatcher):
    host = "192.168.10.12"
    port = 2000
    mesg = "Hello World\n"

    def __init__(self):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((self.host, self.port))

    def handle_connect(self):
        pass

    def handle_close(self):
        self.close()

    def handle_read(self):
        self.recv(4096)

    def writable(self):
        return True

    def handle_write(self):
        self.send(self.mesg)
        self.close()
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((self.host, self.port))

