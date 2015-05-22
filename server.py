__author__ = 'Harry'

import asyncore
import asynchat
import socket
import json
import urllib.request
import traceback

clients = {}
room = []

class MessageHandler(asynchat.async_chat):
    def __init__(self, sock, addr):
        asynchat.async_chat.__init__(self, sock=sock, map=clients)
        self.set_terminator(b'\0')
        self._username = ""
        self._received_data = ""

    def handle_close(self):
        pass

    def collect_incoming_data(self, data):
        self._received_data += data.decode('UTF-8')

    def found_terminator(self):
        self._received_data = self._received_data.strip('\0')
        split_string = self._received_data.split(' ', 1)
        key = split_string[0]
        print(self._received_data)
        if key == "SET_USERNAME":
            self._username = split_string[1]
        elif key == "MESSAGE":
            for client in room:
                if client != self:
                    client.push(bytes(self._received_data + "\0", 'UTF-8'))
        elif key == "CHAT_START":
            for client in room:
                client.push(bytes("CHAT_START\0", 'UTF-8'))
        elif key == "COMMAND":
            for client in room:
                if client != self:
                    client.push(bytes(self._received_data + "\0", 'UTF-8'))
        self._received_data = ""

    # def handle_error(self):
    #     '''Handle any uncaptured error in the core. Overrides asyncore's handle_error
    #     This prevents the server from disconnecting when it use to send something twice
    #     and then disconnect.'''
    #     trace = traceback.format_exc()
    #     try:
    #         print(trace)
    #     except Exception as e:
    #         print('Uncaptured error!' + e)



class Server(asyncore.dispatcher):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self, map=clients)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)
        print("Server started.")
        print("IP address is {}.".format(host))
        print("Port is {}.".format(port))
        print("Waiting for connections...")

    def handle_accepted(self, sock, addr):
        print("Incoming conection from {}".format(repr(addr)))
        handler = MessageHandler(sock, addr)
        if len(room) >= 2:
            handler.push(bytes("ROOM_FULL", 'UTF-8'))
        else:
            room.append(handler)


def main():
    # server = Server("localhost", 8000)
    # External IP address
    # my_ip = json.loads(urllib.request.urlopen('https://api.ipify.org/?format=json').read().decode('UTF-8'))['ip']
    # Internal IP address
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    my_ip = s.getsockname()[0]
    s.close()
    server = Server(my_ip, 8888)
    asyncore.loop(timeout=1, map=clients)



if __name__ == '__main__':
    main()